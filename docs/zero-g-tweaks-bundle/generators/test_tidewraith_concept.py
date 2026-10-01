"""Read-only tests for concept rebuilds, independent of visual approval."""
import hashlib
import json
import unittest
from PIL import Image
from build_tidewraith_concept import OUT, FACTOR, PALETTES, BODY_RX, BODY_RZ, BODY_CZ, FLIGHT_PERIOD, UV, OUTER_WING_AMPLITUDE, TIP_WING_AMPLITUDE
from review_mob_assets import check


class ConceptTests(unittest.TestCase):
    def setUp(self):
        self.model=json.loads((OUT/'tidewraith_concept.bbmodel').read_text())
        self.geo=json.loads((OUT/'tidewraith_concept.geo.json').read_text())['minecraft:geometry'][0]
        self.bones={b['name']:b for b in self.geo['bones']}

    def test_eight_eyes_and_five_joint_chains(self):
        self.assertEqual(len([n for n in self.bones if n.startswith('eye_')]),8)
        for number in range(1,5):
            parent='tail_base'
            for segment in range(1,6):
                name=f'tentacle_{number}'+('' if segment==1 else f'_seg{segment}')
                self.assertEqual(self.bones[name]['parent'],parent)
                parent=name
        for name in self.bones:
            seen=set()
            while name:
                self.assertNotIn(name,seen);seen.add(name)
                name=self.bones[name].get('parent')

    def test_concept_geometry_not_rejected_slab(self):
        parts=self.model['elements']
        dome=[e for e in parts if e['name'].startswith('dome_')]
        self.assertGreater(len(dome),700)
        self.assertTrue(all(all(b-a==1 for a,b in zip(e['from'],e['to'])) for e in dome))
        for prefix in ('mouth_socket','mouth_outer','mouth_teal','mouth_blue','mouth_inner','throat'):
            self.assertTrue(any(e['name'].startswith(prefix) for e in parts),prefix)
        for side in ('left','right'):
            tips=[e for e in parts if e['name'].startswith('wing_tip_'+side)]
            self.assertLess(max(e['to'][1] for e in tips),self.bones['wing_'+side]['pivot'][1]-6)
            self.assertEqual(self.bones['wing_'+side+'_tip']['parent'],'wing_'+side+'_outer')
            lobe=[e for e in parts if e['name'].startswith('lobe_'+side)]
            self.assertLess(min(e['from'][1] for e in lobe),13)

    def test_scaled_geometry_uv_and_animation_channels(self):
        scaled=json.loads((OUT/'tidewraith_concept_scaled.geo.json').read_text())['minecraft:geometry'][0]
        for a,b in zip(self.geo['bones'],scaled['bones']):
            self.assertEqual(a['name'],b['name'])
            for x,y in zip(a['pivot'],b['pivot']):self.assertAlmostEqual(x*FACTOR,y)
            for c,d in zip(a['cubes'],b['cubes']):
                self.assertEqual(c['uv'],d['uv'])
                for field in ('origin','size'):
                    for x,y in zip(c[field],d[field]):self.assertAlmostEqual(x*FACTOR,y)
        normal=json.loads((OUT/'tidewraith_concept.animation.json').read_text())['animations']
        small=json.loads((OUT/'tidewraith_concept_scaled.animation.json').read_text())['animations']
        for key,clip in normal.items():
            self.assertTrue(set(clip['bones'])<=set(self.bones))
            for name,channels in clip['bones'].items():
                for channel,frames in channels.items():
                    for t,values in frames.items():
                        for x,y in zip(values,small[key]['bones'][name][channel][t]):
                            self.assertAlmostEqual(x*(FACTOR if channel=='position' else 1),y)

    def test_texture_budget_glow_and_variant_layout(self):
        layout=None
        for style,colours in PALETTES.items():
            key='tidewraith_concept'+('' if style=='standard' else '_'+style)
            with Image.open(OUT/f'{key}.png') as src:base=src.convert('RGBA')
            with Image.open(OUT/f'{key}_glowmask.png') as src:glow=src.convert('RGBA')
            self.assertEqual(base.size,(32,32));self.assertEqual(glow.size,(32,32))
            indices={tuple(bytes.fromhex(c[1:])):i for i,c in enumerate(colours)}
            current=[]
            for y in range(32):
                for x in range(32):
                    p=base.getpixel((x,y));g=glow.getpixel((x,y))
                    current.append(indices[p[:3]] if p[3] else None)
                    if g[3]:self.assertTrue(x>=24 and y>=24);self.assertEqual(g,p)
            if layout is not None:self.assertEqual(layout,current)
            layout=current
            check(OUT/f'{key}.bbmodel');check(OUT/f'{key}_scaled.bbmodel')

    def test_manifest_and_eye_visibility_receipts(self):
        receipt=json.loads((OUT/'manifest.json').read_text())
        self.assertEqual(len(receipt['validation']),4)
        for result in receipt['validation']:
            self.assertEqual(len(result['eye_visible_pixels']),8)
            self.assertTrue(all(result['eye_visible_pixels'].values()))
        for name,digest in receipt['files'].items():
            self.assertEqual(hashlib.sha256((OUT/name).read_bytes()).hexdigest(),digest,name)

    def test_complete_body_volume_and_intentional_front_recess(self):
        import numpy as np
        occupied=np.zeros((2*BODY_RX,20,2*BODY_RZ),dtype=bool)
        for e in self.model['elements']:
            if not e['name'].startswith(('dome_','body_fill_')):continue
            a=[round(e['from'][0]+BODY_RX),round(e['from'][1]-14),round(e['from'][2]-BODY_CZ+BODY_RZ)]
            b=[round(e['to'][0]+BODY_RX),round(e['to'][1]-14),round(e['to'][2]-BODY_CZ+BODY_RZ)]
            occupied[a[0]:b[0],a[1]:b[1],a[2]:b[2]]=True
        x,y,z=np.meshgrid(np.arange(-BODY_RX,BODY_RX)+.5,np.arange(14,34)+.5,
                         np.arange(BODY_CZ-BODY_RZ,BODY_CZ+BODY_RZ)+.5,indexing='ij')
        volume=(x/BODY_RX)**2+((y-24)/10)**2+((z-BODY_CZ)/BODY_RZ)**2<=1
        cavity=(z< -10)&((x/10)**2+((y-22)/5.4)**2<1)
        self.assertTrue(np.array_equal(occupied,volume&~cavity),'missing/excess body voxel')
        self.assertGreater(BODY_RX*2,28);self.assertGreater(BODY_RZ*2,24)
        # Regression points in the previously removed cheek, each side.
        for xx in (-11,10):
            self.assertTrue(occupied[xx+BODY_RX,22-14,-6-BODY_CZ+BODY_RZ])
        self.assertFalse(occupied[BODY_RX,22-14,-12-BODY_CZ+BODY_RZ])

    def test_gentle_mirrored_flight_and_loop(self):
        clip=next(a for a in self.model['animations'] if a['name'].endswith('.fly'))
        self.assertAlmostEqual(clip['length'],FLIGHT_PERIOD)
        anim={a['name']:a for a in clip['animators'].values()}
        for left,right,limit in (('wing_left','wing_right',6),
                                 ('wing_left_outer','wing_right_outer',OUTER_WING_AMPLITUDE),
                                 ('wing_left_tip','wing_right_tip',TIP_WING_AMPLITUDE)):
            l=anim[left]['keyframes'];r=anim[right]['keyframes']
            self.assertEqual(len(l),33)
            self.assertLessEqual(max(abs(k['data_points'][0]['z']) for k in l),limit+.001)
            for a,b in zip(l,r):
                self.assertEqual(a['time'],b['time'])
                self.assertAlmostEqual(a['data_points'][0]['z'],-b['data_points'][0]['z'])
            self.assertAlmostEqual(l[0]['data_points'][0]['z'],l[-1]['data_points'][0]['z'])
        self.assertTrue(any(e['name'].startswith('wing_hinge_') for e in self.model['elements']))
        # Distal hinges lag the base flap, rather than moving as one rigid wing.
        self.assertNotEqual(anim['wing_left']['keyframes'][0]['data_points'][0]['z']/6,
                            anim['wing_left_tip']['keyframes'][0]['data_points'][0]['z']/TIP_WING_AMPLITUDE)

    def test_teeth_are_two_sided_alpha_cutout_planes(self):
        teeth=[e for e in self.model['elements'] if e['name'].startswith(('upper_tooth_','lower_tooth_'))]
        self.assertEqual(len(teeth),30)
        for e in teeth:
            self.assertEqual(e['from'][2],e['to'][2]);self.assertEqual(set(e['faces']),{'north','south'})
        with Image.open(OUT/'tidewraith_concept.png') as image:
            tile=image.crop(tuple(UV['tooth'])).convert('RGBA')
            self.assertEqual(tile.getpixel((0,1))[3],0)
            self.assertEqual(tile.getpixel((1,1))[3],255)
            self.assertEqual(tile.getpixel((2,1))[3],0)

    def test_mouth_clip_moves_rim_and_teeth_together(self):
        clip=next(a for a in self.model['animations'] if a['name'].endswith('.mouth_open'))
        self.assertEqual(clip['loop'],'once');self.assertEqual(clip['length'],1.6)
        anim=list(clip['animators'].values())
        self.assertEqual([a['name'] for a in anim],['mouth'])
        keys=anim[0]['keyframes']
        self.assertEqual(len(keys),33)
        self.assertTrue(all(k['channel']=='scale' for k in keys))
        self.assertEqual(keys[0]['data_points'],keys[-1]['data_points'])
        self.assertEqual(keys[0]['data_points'][0],{'x':1,'y':1,'z':1})
        for axis,value in {'x':1.025,'y':1.14,'z':1}.items():
            self.assertAlmostEqual(keys[16]['data_points'][0][axis],value)
        self.assertEqual(self.bones['jaw_upper']['parent'],'mouth')
        self.assertEqual(self.bones['jaw_lower']['parent'],'mouth')
        # Geometry membership receipts: animated rims share the mouth transform
        # with the tooth rows. The fixed socket stays on the head, not the jaw.
        members={};nodes={}
        def walk(items,parent=None):
            for n in items:
                if isinstance(n,str):members[n]=parent
                else:nodes[n['uuid']]=n['name'];walk(n['children'],n['uuid'])
        walk(self.model['outliner'])
        for e in self.model['elements']:
            parent=nodes[members[e['uuid']]]
            if e['name'].startswith('mouth_socket'):self.assertEqual(parent,'head')
            elif e['name'].startswith(('mouth_outer','mouth_teal','mouth_blue','mouth_inner','throat')):
                self.assertEqual(parent,'mouth')
            elif e['name'].startswith('upper_tooth'):self.assertEqual(parent,'jaw_upper')
            elif e['name'].startswith('lower_tooth'):self.assertEqual(parent,'jaw_lower')

    def test_tooth_roots_touch_the_gum_band_at_every_frame(self):
        import numpy as np
        parts=self.model['elements']
        gums=[e for e in parts if e['name'].startswith('mouth_blue')]
        teeth=[e for e in parts if e['name'].startswith(('upper_tooth','lower_tooth'))]
        pivot=np.array(self.bones['mouth']['pivot'])
        clip=next(a for a in self.model['animations'] if a['name'].endswith('.mouth_open'))
        keys=next(iter(clip['animators'].values()))['keyframes']
        for tooth in teeth:
            root=np.array([(tooth['from'][0]+tooth['to'][0])/2,
                           tooth['to'][1] if tooth['name'].startswith('upper') else tooth['from'][1],
                           tooth['from'][2]])
            supports=[g for g in gums if g['from'][0]-1e-6<=root[0]<=g['to'][0]+1e-6
                      and g['from'][1]-1e-6<=root[1]<=g['to'][1]+1e-6]
            self.assertTrue(supports, tooth['name']+' has no gum support')
            gum_point=np.array([root[0],root[1],supports[0]['from'][2]])
            for key in keys:
                scale=np.array([key['data_points'][0][a] for a in ('x','y','z')])
                tooth_world=pivot+(root-pivot)*scale
                gum_world=pivot+(gum_point-pivot)*scale
                self.assertAlmostEqual(float(np.linalg.norm(tooth_world-gum_world)),.02)


if __name__=='__main__':unittest.main()
