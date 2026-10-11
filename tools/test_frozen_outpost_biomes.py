"""Regression: cold wasteland routes must not be silently limited to Eidolon."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'src/main/resources/data/zerog_tweaks'

class FrozenOutpostBiomes(unittest.TestCase):
    def test_cold_habitats_and_source_copy(self):
        relative = Path('tags/worldgen/biome/has_structure/frozen_outpost.json')
        path = DATA / relative
        tag = json.loads(path.read_text())
        required = {'zerog_tweaks:' + name for name in (
            'hoarwood_taiga', 'phantom_ice_sheets', 'wasteland_glaciers',
            'wasteland_ice_spike_forest', 'wasteland_frozen_canyons')}
        self.assertFalse(tag['replace'])
        self.assertEqual(set(tag['values']), required)
        self.assertEqual(len(tag['values']), len(required))
        for biome in required:
            self.assertTrue((DATA / 'worldgen/biome' / (biome.split(':')[1]+'.json')).is_file())
        source = ROOT.parent / 'zerog-design-integrated/docs/wasteland-ruins/generated/data/zerog_tweaks' / relative
        self.assertEqual(path.read_bytes(), source.read_bytes())

    def test_galaxy_two_frozen_slot_has_route_and_ocean_does_not(self):
        tag = set(json.loads((DATA / 'tags/worldgen/biome/has_structure/frozen_outpost.json').read_text())['values'])
        def biomes(slot):
            dim = json.loads((DATA / 'dimension' / (slot+'.json')).read_text())
            return {entry['biome'] for entry in dim['generator']['biome_source']['biomes']}
        for slot in ('g2_p4', 'g3_p1', 'g4_p5', 'g5_p2'):
            with self.subTest(slot=slot):
                self.assertTrue(biomes(slot))
                self.assertTrue(biomes(slot) <= tag)
        self.assertFalse(biomes('g2_p1') & tag)
        structure = json.loads((DATA / 'worldgen/structure/frozen_outpost.json').read_text())
        self.assertEqual(structure['biomes'], '#zerog_tweaks:has_structure/frozen_outpost')
        self.assertFalse(structure['always_place'])

if __name__ == '__main__':
    unittest.main()
