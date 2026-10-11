"""Relay source/water contracts; ordinary ocean generation requires separate evidence."""
import json,unittest
from pathlib import Path
from audit_structure_routes import read_template
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'src/main/resources/data/zerog_tweaks'
SOURCE=ROOT.parent/'zerog-design-integrated/docs/wasteland-ruins/generated/data/zerog_tweaks'

class Relay(unittest.TestCase):
    def test_no_zero_depth_or_empty_builder_bounds(self):
        code=(ROOT/'src/main/java/net/zerog/tweaks/worldgen/SubmergedJigsawStructure.java').read_text()
        self.assertRegex(code,r'addPieces\(context, startPool, Optional.empty\(\), 1,')
        guard=code.index('if (pieces.isEmpty()) return Optional.empty();')
        self.assertLess(guard,code.index('pieces.getBoundingBox()'))
        self.assertIn('Heightmap.Types.OCEAN_FLOOR_WG',code)
        self.assertIn('FluidTags.WATER',code)
    def test_flooded_original_layout_and_source_bindings(self):
        allowed={'minecraft:water','minecraft:chest','minecraft:iron_bars','zerog_tweaks:abyssal_stone',
            'zerog_tweaks:abyssal_stone_bricks','zerog_tweaks:corroded_hull','zerog_tweaks:hull_plating',
            'zerog_tweaks:chiseled_hull','zerog_tweaks:pulsar_lamp'}
        for variant in (0,1):
            p=Path(f'structure/sunken_relay/small_{variant}.nbt')
            self.assertEqual((DATA/p).read_bytes(),(SOURCE/p).read_bytes())
            t=read_template(DATA/p);self.assertEqual(t['size'],[19,12,19])
            self.assertTrue({s['Name'] for s in t['palette']} <= allowed)
            blocks={tuple(b['pos']):t['palette'][b['state']] for b in t['blocks']}
            for x in (8,9,10):
                for z in range(2,14):
                    for y in (2,3,4):self.assertEqual(blocks[x,y,z]['Name'],'minecraft:water')
            self.assertEqual(blocks[9,3,14]['Name'],'minecraft:water')
            chests=[b for b in t['blocks'] if b.get('nbt',{}).get('LootTable')]
            self.assertEqual(len(chests),1);self.assertEqual(chests[0]['nbt']['LootTable'],'zerog_tweaks:chests/sunken_relay')
            self.assertEqual(blocks[9,2,14]['Properties']['waterlogged'],'true')
            self.assertTrue(all(s.get('Properties',{}).get('waterlogged')=='true' for s in t['palette'] if s['Name']=='minecraft:iron_bars'))
    def test_existing_ocean_biomes_and_bounded_placement(self):
        files=['tags/worldgen/biome/has_structure/sunken_relay.json','worldgen/structure/sunken_relay.json',
            'worldgen/structure_set/sunken_relay.json','worldgen/template_pool/sunken_relay/start.json']
        for f in files:self.assertEqual((DATA/f).read_bytes(),(SOURCE/f).read_bytes())
        biome_ids={b['biome'] for b in json.loads((DATA/'dimension/g2_p1.json').read_text())['generator']['biome_source']['biomes']}
        self.assertEqual(set(json.loads((DATA/files[0]).read_text())['values']),biome_ids)
        for b in biome_ids:self.assertTrue((DATA/'worldgen/biome'/f"{b.split(':')[1]}.json").exists())
        structure=json.loads((DATA/files[1]).read_text());self.assertEqual(structure['type'],'zerog_tweaks:submerged_jigsaw')
        self.assertEqual(structure['max_height_difference'],6)
        placement=json.loads((DATA/files[2]).read_text())['placement']
        self.assertEqual((placement['spacing'],placement['separation']),(40,20))
if __name__=='__main__':unittest.main()
