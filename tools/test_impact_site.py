"""Static Impact Site provenance and biome contracts; gameplay uses GameTests."""
import json, unittest
from pathlib import Path
from audit_structure_routes import read_template

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'src/main/resources/data/zerog_tweaks'
SOURCE=ROOT.parent/'zerog-design-integrated/docs/wasteland-ruins/generated/data/zerog_tweaks'

class ImpactSite(unittest.TestCase):
    def test_templates_and_generator_bytes(self):
        allowed={'minecraft:air','minecraft:chest','zerog_tweaks:craterstone',
            'zerog_tweaks:cobbled_craterstone','zerog_tweaks:hull_plating','zerog_tweaks:meteorite_fragment'}
        for variant in range(2):
            relative=Path(f'structure/impact_site/small_{variant}.nbt')
            self.assertEqual((DATA/relative).read_bytes(),(SOURCE/relative).read_bytes())
            data=read_template(DATA/relative)
            self.assertEqual(data['size'],[21,7,21])
            self.assertTrue({p['Name'] for p in data['palette']} <= allowed)
            chests=[b for b in data['blocks'] if b.get('nbt',{}).get('LootTable')]
            self.assertEqual(len(chests),1)
            self.assertEqual(chests[0]['nbt']['LootTable'],'zerog_tweaks:chests/impact_site')

    def test_barren_eligibility_and_unchanged_placement_contract(self):
        relative=Path('tags/worldgen/biome/has_structure/impact_site.json')
        self.assertEqual((DATA/relative).read_bytes(),(SOURCE/relative).read_bytes())
        tag=json.loads((DATA/relative).read_text())
        biomes={x['biome'] for x in json.loads((DATA/'dimension/g2_moons.json').read_text())['generator']['biome_source']['biomes']}
        self.assertTrue(biomes <= set(tag['values']))
        self.assertEqual(len(tag['values']),3)
        for biome in tag['values']:
            self.assertTrue((DATA/'worldgen/biome'/f"{biome.split(':')[1]}.json").is_file())
        settings=json.loads((DATA/'worldgen/structure/impact_site.json').read_text())
        self.assertFalse(settings['always_place'])
        placement=json.loads((DATA/'worldgen/structure_set/impact_site.json').read_text())['placement']
        self.assertEqual((placement['spacing'],placement['separation']),(40,20))

if __name__=='__main__': unittest.main()
