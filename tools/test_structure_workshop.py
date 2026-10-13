import copy
import gzip
import json
import tempfile
import unittest
import sys
from pathlib import Path
from structure_workshop import build, nbt_bytes, validate

sys.path.insert(0, str(Path(__file__).parent / 'dev'))
from worldscan import _read


def fixture():
    return {'schema': 1, 'size': [5, 4, 5],
            'palette': [{'Name': 'minecraft:stone'}, {'Name': 'minecraft:chest'},
                        {'Name': 'minecraft:spawner'}],
            'blocks': [{'pos': [0, 0, 0], 'state': 0},
                       {'pos': [1, 1, 1], 'state': 1, 'nbt': {'LootTable': 'zerog_tweaks:chests/survey_supplies'}},
                       {'pos': [3, 1, 3], 'state': 2, 'nbt': {'mob': 'minecraft:zombie'}}],
            'loot_tables': {'zerog_tweaks:chests/survey_supplies': {
                'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [
                    {'type': 'minecraft:item', 'name': 'minecraft:iron_ingot'}]}]}}}


class WorkshopTests(unittest.TestCase):
    def test_repeatable_structure_header_and_block_entity_fields(self):
        data = nbt_bytes(fixture())
        self.assertEqual(data, nbt_bytes(fixture()))
        raw = gzip.decompress(data)
        self.assertEqual(raw[:3], b'\x0a\0\0')
        for field in (b'DataVersion', b'palette', b'blocks', b'LootTable', b'SpawnData', b'minecraft:zombie'):
            self.assertIn(field, raw)
        root, consumed = _read(raw, 3, 10)
        self.assertEqual(consumed, len(raw))
        self.assertEqual(root['DataVersion'], 3955)
        self.assertEqual(root['size'], [5, 4, 5])
        self.assertEqual(len(root['blocks']), 3)
        spawner = next(b['nbt'] for b in root['blocks'] if 'SpawnData' in b.get('nbt', {}))
        self.assertEqual(spawner['SpawnData']['entity']['id'], 'minecraft:zombie')
        self.assertEqual(spawner['MaxNearbyEntities'], 4)

    def test_duplicates_bounds_and_state_index_rejected(self):
        for modification in ('duplicate', 'bounds', 'state'):
            spec = fixture()
            if modification == 'duplicate':
                spec['blocks'].append(copy.deepcopy(spec['blocks'][0]))
            elif modification == 'bounds':
                spec['blocks'][0]['pos'][0] = 5
            else:
                spec['blocks'][0]['state'] = 99
            with self.assertRaises(ValueError):
                validate(spec)

    def test_story_loot_and_unresolved_table_rejected(self):
        spec = fixture()
        spec['loot_tables']['zerog_tweaks:chests/survey_supplies']['pools'][0]['entries'][0]['name'] = 'zerog_tweaks:broken_console'
        with self.assertRaises(ValueError):
            validate(spec)
        spec = fixture()
        spec['loot_tables'] = {}
        with self.assertRaises(ValueError):
            validate(spec)

    def test_resource_paths_cannot_escape_export(self):
        spec = fixture()
        table = spec['loot_tables'].pop('zerog_tweaks:chests/survey_supplies')
        spec['loot_tables']['zerog_tweaks:../../outside'] = table
        with self.assertRaises(ValueError):
            validate(spec)

    def test_export_receipt_and_existing_destination_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            dest = Path(temporary) / 'draft'
            receipt = build(fixture(), dest)
            self.assertEqual(receipt['validation']['loot_containers'], 1)
            self.assertEqual(receipt['validation']['spawners'], 1)
            self.assertTrue((dest / 'structure.nbt').is_file())
            self.assertEqual(json.loads((dest / 'receipt.json').read_text()), receipt)
            original = (dest / 'structure.nbt').read_bytes()
            with self.assertRaises(ValueError):
                build(fixture(), dest)
            self.assertEqual((dest / 'structure.nbt').read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
