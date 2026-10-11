"""Original structure palette, source bindings and desert routes; not natural proof."""
import json,unittest
from pathlib import Path
from audit_structure_routes import read_template

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'src/main/resources/data/zerog_tweaks'
SOURCE=ROOT.parent/'zerog-design-integrated/docs/wasteland-ruins/generated/data/zerog_tweaks'

class Observatory(unittest.TestCase):
    def test_original_palettes_and_source_bindings(self):
        allowed={'minecraft:air','minecraft:chest','zerog_tweaks:sunbaked_stone_bricks',
            'zerog_tweaks:cracked_sunbaked_stone_bricks','zerog_tweaks:ruinstone',
            'zerog_tweaks:hull_plating','zerog_tweaks:crystal_glass','zerog_tweaks:rustsand'}
        for v in range(2):
            relative=Path(f'structure/buried_observatory/small_{v}.nbt')
            self.assertEqual((DATA/relative).read_bytes(),(SOURCE/relative).read_bytes())
            t=read_template(DATA/relative)
            self.assertEqual(t['size'],[21,11,21])
            self.assertTrue({p['Name'] for p in t['palette']} <= allowed)
            chests=[b for b in t['blocks'] if b.get('nbt',{}).get('LootTable')]
            self.assertEqual(len(chests),1)
            self.assertEqual(chests[0]['nbt']['LootTable'],'zerog_tweaks:chests/buried_observatory')
            self.assertFalse(any('console' in p['Name'] for p in t['palette']))
            states={tuple(b['pos']):t['palette'][b['state']]['Name'] for b in t['blocks']}
            for (x,y,z),name in states.items():
                if name=='zerog_tweaks:rustsand':
                    self.assertIn(states.get((x,y-1,z)),{'zerog_tweaks:sunbaked_stone_bricks','zerog_tweaks:hull_plating'})

    def test_desert_eligibility_and_placement(self):
        files=['tags/worldgen/biome/has_structure/buried_observatory.json',
            'worldgen/structure/buried_observatory.json','worldgen/structure_set/buried_observatory.json',
            'worldgen/template_pool/buried_observatory/start.json']
        for relative in files:self.assertEqual((DATA/relative).read_bytes(),(SOURCE/relative).read_bytes())
        tag=json.loads((DATA/files[0]).read_text())
        biomes={x['biome'] for x in json.loads((DATA/'dimension/g2_p2.json').read_text())['generator']['biome_source']['biomes']}
        self.assertEqual(set(tag['values']),biomes)
        for biome in biomes:self.assertTrue((DATA/'worldgen/biome'/f"{biome.split(':')[1]}.json").is_file())
        self.assertFalse(json.loads((DATA/files[1]).read_text())['always_place'])
        p=json.loads((DATA/files[2]).read_text())['placement']
        self.assertEqual((p['spacing'],p['separation']),(40,20))

if __name__=='__main__':unittest.main()
