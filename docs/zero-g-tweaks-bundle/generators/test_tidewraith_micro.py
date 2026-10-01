"""Read-only regression checks for the isolated strict-32px companion exports."""
import hashlib
import json
import unittest

from PIL import Image
from build_tidewraith_micro import FACTOR, OUT, PALETTES, SPEC, UV


@unittest.skipUnless((OUT/'tidewraith_micro.geo.json').exists(),
                     'Rejected micro study is not part of the approved-pair release')
class MicroTests(unittest.TestCase):
    def setUp(self):
        self.geo = json.loads((OUT/'tidewraith_micro.geo.json').read_text())['minecraft:geometry'][0]
        self.scaled = json.loads((OUT/'tidewraith_micro_scaled.geo.json').read_text())['minecraft:geometry'][0]
        self.bones = {b['name']: b for b in self.geo['bones']}

    def test_pivots_parents_and_no_cycles(self):
        for name, (parent, pivot, _, _) in SPEC.items():
            self.assertEqual(self.bones[name]['pivot'], pivot)
            self.assertEqual(self.bones[name].get('parent'), parent)
        for name in self.bones:
            seen = set()
            while name:
                self.assertNotIn(name, seen)
                seen.add(name)
                name = self.bones[name].get('parent')

    def test_uv_rectangles_and_texture_budget(self):
        self.assertEqual((self.geo['description']['texture_width'], self.geo['description']['texture_height']), (32, 32))
        for bone in self.bones.values():
            for cube in bone['cubes']:
                for face in cube['uv'].values():
                    for origin, extent in zip(face['uv'], face['uv_size']):
                        self.assertGreaterEqual(min(origin, origin+extent), 0)
                        self.assertLessEqual(max(origin, origin+extent), 32)
                        self.assertNotEqual(extent, 0)
        for png in OUT.glob('*.png'):
            with Image.open(png) as image:
                self.assertEqual(image.size, (32, 32))

    def test_scaled_geometry_and_rest_rotations(self):
        for source, scaled in zip(self.geo['bones'], self.scaled['bones']):
            self.assertEqual(source['name'], scaled['name'])
            self.assertEqual(source.get('rotation'), scaled.get('rotation'))
            for a, b in zip(source['pivot'], scaled['pivot']):
                self.assertAlmostEqual(a*FACTOR, b)
            for a, b in zip(source['cubes'], scaled['cubes']):
                self.assertEqual(a['uv'], b['uv'])
                for field in ('origin', 'size'):
                    for v, w in zip(a[field], b[field]):
                        self.assertAlmostEqual(v*FACTOR, w)

    def test_eye_clips_and_animation_scaling(self):
        eyes = {name for name in self.bones if name.startswith('eye_')}
        self.assertEqual(len(eyes), 8)
        anim = json.loads((OUT/'tidewraith_micro.animation.json').read_text())['animations']
        scaled = json.loads((OUT/'tidewraith_micro_scaled.animation.json').read_text())['animations']
        blink = next(c for name, c in anim.items() if name.endswith('.blink'))
        self.assertEqual(set(blink['bones']), eyes)
        for clip, entry in anim.items():
            self.assertTrue(set(entry['bones']) <= set(self.bones))
            for name, channels in entry['bones'].items():
                for channel, frames in channels.items():
                    for time, values in frames.items():
                        target = scaled[clip]['bones'][name][channel][time]
                        for v, w in zip(values, target):
                            self.assertAlmostEqual(v*(FACTOR if channel == 'position' else 1), w)

    def test_emissive_corner_and_shared_pattern_variants(self):
        layout = None
        for style, colours in PALETTES.items():
            key = 'tidewraith_micro'+('' if style == 'standard' else '_'+style)
            base = Image.open(OUT/f'{key}.png').convert('RGBA')
            glow = Image.open(OUT/f'{key}_glowmask.png').convert('RGBA')
            indices = {tuple(bytes.fromhex(c[1:])): i for i, c in enumerate(colours)}
            current = [indices[base.getpixel((x, y))[:3]] if base.getpixel((x, y))[3] else None
                       for y in range(32) for x in range(32)]
            if layout is not None:
                self.assertEqual(layout, current)
            layout = current
            for y in range(32):
                for x in range(32):
                    pixel = glow.getpixel((x, y))
                    if pixel[3]:
                        self.assertTrue(24 <= x < 32 and 24 <= y < 32)
                        self.assertEqual(pixel, base.getpixel((x, y)))

    def test_shared_mirrored_wings_lobes_tentacles(self):
        for left, right in (('wing_left', 'wing_right'), ('lobe_left', 'lobe_right'),
                            ('tentacle_1', 'tentacle_2'), ('tentacle_3', 'tentacle_4')):
            for a, b in zip(self.bones[left]['cubes'], self.bones[right]['cubes']):
                self.assertEqual(set(a['uv']), set(b['uv']))
                for face in ('north', 'south', 'up', 'down'):
                    if face not in a['uv']:
                        continue
                    first, second = a['uv'][face], b['uv'][face]
                    self.assertEqual(first['uv'][0]+first['uv_size'][0], second['uv'][0])
                    self.assertEqual(first['uv_size'][0], -second['uv_size'][0])

    def test_manifest_hashes(self):
        manifest = json.loads((OUT/'manifest.json').read_text())
        for name, digest in manifest['files'].items():
            self.assertEqual(hashlib.sha256((OUT/name).read_bytes()).hexdigest(), digest, name)


if __name__ == '__main__':
    unittest.main()
