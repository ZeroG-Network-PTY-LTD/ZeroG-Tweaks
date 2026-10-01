"""Read-only checks for the user-selected Abyssal model's scoped face repair."""
import hashlib
import json
import unittest
from PIL import Image, ImageChops
from update_tidewraith_abyssal_face import OUT, FACE_PREFIXES, HEAD_SHIFT_Z, ATLAS_OFFSET
from review_mob_assets import check, image_from_model


class FaceRepairTests(unittest.TestCase):
    def setUp(self):
        self.source=json.loads((OUT/'source_model.bbmodel').read_text())
        self.path=OUT/'tidewraith_abyssal_concept_face.bbmodel'
        self.model=json.loads(self.path.read_text())

    def test_import_structure_and_non_facial_geometry(self):
        result=check(self.path)
        self.assertEqual(result['texture'],[4096,4096])
        self.assertEqual(len(self.model['textures']),1)
        self.assertEqual(len(self.source['elements']),len(self.model['elements']))
        for before,after in zip(self.source['elements'],self.model['elements']):
            if not before['name'].startswith(FACE_PREFIXES):self.assertEqual(before,after)

    def test_body_atlas_pixels_and_uvs_preserved(self):
        a=image_from_model(self.source);b=image_from_model(self.model)
        # Both RGB and alpha checked: RGBA getbbox alone can miss an RGB-only
        # change when the alpha difference is zero.
        for rect in ((0,0,4096,ATLAS_OFFSET),(0,ATLAS_OFFSET,ATLAS_OFFSET,4096)):
            diff=ImageChops.difference(a.crop(rect),b.crop(rect))
            self.assertIsNone(diff.convert('RGB').getbbox())
            self.assertIsNone(diff.getchannel('A').getbbox())

    def test_head_spacing_and_subtree_pivots(self):
        def nodes(m):
            result={}
            def walk(items):
                for n in items:
                    if isinstance(n,dict):result[n['name']]=n;walk(n['children'])
            walk(m['outliner']);return result
        a=nodes(self.source);b=nodes(self.model)
        for name in ('head','jaw','fin_l','fin_r','splinter'):
            self.assertEqual(a[name]['origin'][:2],b[name]['origin'][:2])
            self.assertAlmostEqual(a[name]['origin'][2]+HEAD_SHIFT_Z,b[name]['origin'][2])
        for name in a:
            if name.startswith(('body','root','wing','tail','tendril')):
                self.assertEqual(a[name]['origin'],b[name]['origin'])
        parts={e['name']:e for e in self.model['elements']}
        self.assertAlmostEqual(parts['head_05']['to'][2]-parts['body_00']['from'][2],.25)

    def test_two_mirrored_animated_eyes_and_six_teeth(self):
        eyes=[e for e in self.model['elements'] if e['name'].startswith('eyes_')]
        self.assertEqual(len(eyes),2)
        self.assertAlmostEqual(eyes[0]['from'][0],-eyes[1]['to'][0])
        self.assertEqual(eyes[0]['from'][1:],eyes[1]['from'][1:])
        for e in eyes:self.assertEqual(set(e['faces']),{'north','south'})
        blink=next(a for a in self.model['animations'] if a['name'].endswith('.blink'))
        self.assertEqual(len(blink['animators']),2)
        teeth=[e for e in self.model['elements'] if e['name'].startswith('upper_tooth_')]
        self.assertEqual(len(teeth),6)
        for e in teeth:self.assertEqual(e['from'][2],e['to'][2])

    def test_animation_scope_and_correct_mouth_direction(self):
        for a,b in zip(self.source['animations'],self.model['animations']):
            if not a['name'].endswith('.mouth_open'):self.assertEqual(a,b)
        clip=next(a for a in self.model['animations'] if a['name'].endswith('.mouth_open'))
        anim={a['name']:a for a in clip['animators'].values()}
        self.assertEqual(set(anim),{'mouth','jaw'})
        self.assertLess(min(k['data_points'][0]['x'] for k in anim['jaw']['keyframes']),0)
        self.assertTrue(all(k['channel']=='scale' for k in anim['mouth']['keyframes']))
        # At full opening the cavity ends at the jaw's upper edge. Oversized
        # mouth scaling would draw a black plane across the visible lower lip.
        import math
        parts={e['name']:e for e in self.model['elements']}
        lip=next(e for e in parts.values() if e['name'].startswith('jaw_lower_rim'))
        mouth=next(e for e in parts.values() if e['name'].startswith('mouth_'))
        pivot_y,pivot_z=18.5,-16+HEAD_SHIFT_Z
        angle=math.radians(-8)
        upper_y=pivot_y+(lip['to'][1]-pivot_y)*math.cos(angle)-(lip['from'][2]-pivot_z)*math.sin(angle)
        mouth_y=mouth['to'][1]+(mouth['from'][1]-mouth['to'][1])*1.12
        self.assertLess(abs(mouth_y-upper_y),.01)

    def test_receipts_and_source_backup(self):
        receipt=json.loads((OUT/'manifest.json').read_text())
        self.assertTrue(receipt['source_preserved'])
        self.assertEqual(hashlib.sha256((OUT/'source_model.bbmodel').read_bytes()).hexdigest(),receipt['source_sha256'])
        self.assertEqual(len(receipt['eye_visible_pixels']),2)
        self.assertTrue(all(receipt['eye_visible_pixels'].values()))
        for name,digest in receipt['files'].items():
            self.assertEqual(hashlib.sha256((OUT/name).read_bytes()).hexdigest(),digest,name)


if __name__=='__main__':unittest.main()
