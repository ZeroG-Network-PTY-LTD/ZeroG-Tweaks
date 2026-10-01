"""Explicit repository art-direction regression checks (not artistic approval)."""
import csv,json,unittest
from pathlib import Path
from build_mob_models import ROOT
from mob_faces import PROFILES
from review_mob_assets import render,image_from_model,check

ZG=ROOT/'docs/zero-g-tweaks-bundle/blockbench/mobs'
SS=ROOT/'docs/shattered-skies/blockbench'

class AssetRegressions(unittest.TestCase):
    def test_repository_placements(self):
        rows=list(csv.DictReader((ROOT/'docs/zero-g-tweaks-bundle/sheets/mobs/data/mob_eye_styles.csv').read_text().splitlines()))
        self.assertEqual(len(rows),38)
        for r in rows:
            self.assertEqual(PROFILES[r['mob']][0],r['eye_style'],r['mob'])

    def test_all_model_eye_counts_and_blinks(self):
        variants={r['model']:r['base_rig'] for r in json.loads((SS/'manifest.json').read_text())['models']}
        for p in list(ZG.glob('*.bbmodel'))+list(SS.glob('*.bbmodel')):
            with self.subTest(model=p.stem):
                check(p)
                m=json.loads(p.read_text());base=variants.get(p.stem,p.stem)
                eyes=[e for e in m['elements'] if e['name'].startswith('eyes_')]
                self.assertEqual(len(eyes),1 if PROFILES[base][0]=='ender_eye' else 2)
                self.assertTrue(any(a['name'].endswith('.blink') for a in m['animations']))
                if len(eyes)==1:
                    self.assertAlmostEqual(eyes[0]['from'][0],-eyes[0]['to'][0],places=5)
                    tex=image_from_model(m);uv=eyes[0]['faces']['north']['uv']
                    self.assertEqual(tex.getpixel((uv[0],uv[1]))[3],0,'Eye outline must be transparent, not a rectangle')

    def test_boss_scale(self):
        for k in ('prism_sentinel','rift_tyrant','eidolon_captain','dying_star'):
            m=json.loads((ZG/(k+'.bbmodel')).read_text())
            height=max(e['to'][1] for e in m['elements'])-min(e['from'][1] for e in m['elements'])
            self.assertAlmostEqual(height/16,10.8,places=5)

    def test_depth_regression_two_visible_sun_eyes(self):
        m=json.loads((ZG/'sun_colossus.bbmodel').read_text());debug={}
        render(m,debug=debug)
        for e in m['elements']:
            if e['name'].startswith('eyes_'):self.assertGreater(debug['visible_pixels'].get(e['name'],0),0)

    def test_phantom_dimensions_and_hierarchy(self):
        m=json.loads((SS/'tidewraith.bbmodel').read_text())
        body=next(e for e in m['elements'] if e['name'].startswith('body_'))
        self.assertEqual([b-a for a,b in zip(body['from'],body['to'])],[5,3,9])
        bones={}
        def walk(nodes,parent=None):
            for n in nodes:
                if isinstance(n,dict):bones[n['name']]=parent;walk(n['children'],n['name'])
        walk(m['outliner'])
        for s in ('l','r'):self.assertEqual(bones['wing_'+s+'_outer'],'wing_'+s)
        self.assertEqual(bones['tail_tip'],'tail')
        self.assertEqual(len([e for e in m['elements'] if e['name'].startswith('manta_gill')]),8)

if __name__=='__main__':unittest.main()
