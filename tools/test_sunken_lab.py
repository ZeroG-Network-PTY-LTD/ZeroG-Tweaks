"""Lab architectural palette and provenance; natural generation checked separately."""
import json,unittest
from pathlib import Path
from audit_structure_routes import read_template
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'src/main/resources/data/zerog_tweaks'
SOURCE=ROOT.parent/'zerog-design-integrated/docs/wasteland-ruins/generated/data/zerog_tweaks'

class Lab(unittest.TestCase):
    def test_equipment_and_no_working_energy_giveaways(self):
        allowed={'minecraft:air','minecraft:chest','minecraft:brewing_stand','minecraft:cauldron',
            'minecraft:potted_brown_mushroom','minecraft:potted_red_mushroom','minecraft:lime_stained_glass',
            'minecraft:cyan_stained_glass','minecraft:iron_bars','zerog_tweaks:sludgestone',
            'zerog_tweaks:polished_sludgestone','zerog_tweaks:hull_plating','zerog_tweaks:chiseled_hull',
            'zerog_tweaks:cracked_sludgestone_bricks','zerog_tweaks:pulsar_lamp'}
        for v in (0,1):
            f=Path(f'structure/sunken_lab/small_{v}.nbt')
            self.assertEqual((DATA/f).read_bytes(),(SOURCE/f).read_bytes())
            t=read_template(DATA/f);self.assertEqual(t['size'],[29,12,25])
            names={p['Name'] for p in t['palette']};self.assertTrue(names <= allowed)
            blocks={tuple(b['pos']):t['palette'][b['state']]['Name'] for b in t['blocks']}
            self.assertEqual(sum(n=='minecraft:brewing_stand' for n in blocks.values()),2)
            self.assertEqual(sum(n=='minecraft:cauldron' for n in blocks.values()),2)
            self.assertEqual(sum(n.startswith('minecraft:potted_') for n in blocks.values()),7)
            chests=[b for b in t['blocks'] if b.get('nbt',{}).get('LootTable')]
            self.assertEqual(len(chests),1);self.assertEqual(chests[0]['nbt']['LootTable'],'zerog_tweaks:chests/sunken_lab')
            self.assertFalse(any('energy_cell' in n or 'generator' in n or 'console' in n or 'acid' in n for n in names))

    def test_toxic_biomes_and_source_json(self):
        paths=['tags/worldgen/biome/has_structure/sunken_lab.json','worldgen/structure/sunken_lab.json',
            'worldgen/structure_set/sunken_lab.json','worldgen/template_pool/sunken_lab/start.json']
        for f in paths:self.assertEqual((DATA/f).read_bytes(),(SOURCE/f).read_bytes())
        tag=json.loads((DATA/paths[0]).read_text())
        expected={b['biome'] for b in json.loads((DATA/'dimension/g2_p5.json').read_text())['generator']['biome_source']['biomes']}
        self.assertEqual(set(tag['values']),expected)
        for b in expected:self.assertTrue((DATA/'worldgen/biome'/f"{b.split(':')[1]}.json").is_file())
        self.assertFalse(json.loads((DATA/paths[1]).read_text())['always_place'])
        p=json.loads((DATA/paths[2]).read_text())['placement'];self.assertEqual((p['spacing'],p['separation']),(40,20))
if __name__=='__main__':unittest.main()
