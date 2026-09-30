"""Read-only project-specific import checks; not native rendering certification."""
import base64
import hashlib
import io
import json
import re
import unittest
import zipfile
from PIL import Image
from export_approved_tidewraiths import ROOT, SOURCE, OUT, ASSETS, SOURCES, export_geo, export_animations, verify_sources


class ApprovedPairTests(unittest.TestCase):
    def test_closed_source_rosters_and_backup(self):
        verify_sources()
        receipt=json.loads((OUT/'backup-receipt.json').read_text())
        archive=OUT/receipt['archive']
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(),receipt['sha256'])
        with zipfile.ZipFile(archive) as z:
            expected={p.relative_to(SOURCE).as_posix():p for folder in ('abyssal-face-repair','tidewraith-concept')
                      for p in (SOURCE/folder).rglob('*') if p.is_file()}
            self.assertEqual(set(z.namelist()),set(expected))
            for name,path in expected.items():self.assertEqual(z.read(name),path.read_bytes())

    def test_bedrock_coordinate_uv_and_part_roundtrip(self):
        for key,path in SOURCES.items():
            m=json.loads(path.read_text());geo=export_geo(m,key)['minecraft:geometry'][0]
            cubes=[c for b in geo['bones'] for c in b['cubes']]
            self.assertEqual(len(cubes),len(m['elements']))
            # The traversal changes order; compare unordered full signatures,
            # preserving every dimension, pivot, planar face and mirrored UV.
            original=[]
            def signature(lo,hi,faces):
                def number(v): return float(v) if v else 0.0
                return json.dumps([[number(v) for v in lo],[number(v) for v in hi],
                    {f:[number(v) for v in rect] for f,rect in faces.items()}],sort_keys=True)
            for e in m['elements']:
                faces={f:d['uv'] for f,d in e['faces'].items() if d.get('texture') is not None}
                original.append(signature(e['from'],e['to'],faces))
            recovered=[]
            for c in cubes:
                ox,oy,oz=c['origin'];sx,sy,sz=c['size']
                lo=[-(ox+sx),oy,oz];hi=[-ox,oy+sy,oz+sz]
                # Float arithmetic order may differ by < 1e-12.
                lo=[round(v,10) for v in lo];hi=[round(v,10) for v in hi]
                faces={}
                for f,d in c['uv'].items():
                    u,v=d['uv'];w,h=d['uv_size']
                    rect=[u+w,v+h,u,v] if f in ('up','down') else [u,v,u+w,v+h]
                    faces[f]=[round(a,10) for a in rect]
                recovered.append(signature(lo,hi,faces))
            normalized=[]
            for e in m['elements']:
                normalized.append(signature([round(v,10) for v in e['from']],
                    [round(v,10) for v in e['to']],
                    {f:[round(v,10) for v in d['uv']] for f,d in e['faces'].items()
                     if d.get('texture') is not None}))
            self.assertCountEqual(normalized,recovered)
            self.assertEqual(geo['description']['texture_width'],m['resolution']['width'])

    def test_animation_bone_names_clips_and_coordinate_signs(self):
        for key,path in SOURCES.items():
            m=json.loads(path.read_text());export=export_animations(m,key)['animations']
            bones={b['name'] for b in export_geo(m,key)['minecraft:geometry'][0]['bones']}
            self.assertEqual(len(export),len(m['animations']))
            for clip in m['animations']:
                name='animation.zerog_tweaks.'+key+'.'+clip['name'].rsplit('.',1)[1]
                out=export[name]
                self.assertEqual(out['animation_length'],clip['length'])
                self.assertLessEqual(set(out['bones']),bones)
                for animator in clip['animators'].values():
                    for frame in animator['keyframes']:
                        values=out['bones'][animator['name']][frame['channel']][str(frame['time'])]
                        source=[frame['data_points'][0][a] for a in ('x','y','z')]
                        if frame['channel'] in ('position','rotation'):source[0]*=-1
                        if frame['channel']=='rotation':source[1]*=-1
                        self.assertEqual(source,values)
            self.assertEqual(export['animation.zerog_tweaks.'+key+'.fly']['animation_length'],2.417)
            blink=export['animation.zerog_tweaks.'+key+'.blink']
            self.assertEqual(len(blink['bones']),8 if key.endswith('_boss') else 2)

    def test_masks_and_textures_have_no_bogus_transparent_colour(self):
        paths=[SOURCES['tidewraith']]+[SOURCE/'tidewraith-concept'/('tidewraith_concept'+s+'.bbmodel')
                                     for s in ('','_abyssal','_pearl','_storm')]
        for path in paths:
            m=json.loads(path.read_text())
            base=Image.open(io.BytesIO(base64.b64decode(m['textures'][0]['source'].split(',',1)[1]))).convert('RGBA')
            glow=Image.open(path.with_name(path.stem+'_glowmask.png')).convert('RGBA')
            self.assertEqual(base.size,glow.size)
            self.assertIsNotNone(glow.getbbox())
            import numpy as np
            pixels=np.array(glow)
            self.assertTrue((pixels[pixels[:,:,3]==0]==0).all(), 'RGBA-zero required for unselected glow')

    def test_review_links_resolve(self):
        html=(OUT/'review.html').read_text()
        for target in re.findall(r'(?:href|src)="([^"]+)"',html):
            self.assertTrue((OUT/target).exists(),target)

    def test_optional_runtime_receipt_matches_source(self):
        path=OUT/'catalogue.json'
        if not path.exists():self.skipTest('Runtime admission pending; no resource writes yet')
        catalog=json.loads(path.read_text())
        for name,sha in catalog['runtime_files'].items():
            self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),sha)
        for mob in catalog['mobs']:
            key=mob['id'].split(':')[1];model=json.loads(SOURCES[key].read_text())
            self.assertEqual(json.loads((ASSETS/'geo'/f'{key}.geo.json').read_text()),export_geo(model,key))
            self.assertEqual(mob['boss'],key=='tidewraith_boss')
            self.assertEqual(mob['authored_scale_multiplier'],1)


if __name__=='__main__':unittest.main()
