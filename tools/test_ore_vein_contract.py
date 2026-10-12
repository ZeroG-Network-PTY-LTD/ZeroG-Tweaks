"""Source policy checks, not measured natural connected-deposit sizes."""
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'src/main/resources/data/zerog_tweaks/worldgen/configured_feature'
def size(name):return json.loads((ROOT/('ore_'+name+'.json')).read_text())['config']['size']
class OreVeins(unittest.TestCase):
 def test_original_lore_common_to_rare_sizes(self):
  for common,standard,precious,lore,rare in [('cobaltium','cyrrium','aurelion','starlite','cerulite'),('ruskite','tectium','pyrium','rift_opal','skarnite'),('salvium','wraithsteel','palladine','remnant_shard','eidolite'),('photium','astrium','radiantine','nova_pearl','solvanite')]:
   values=[size(n) for n in (common,standard,precious,lore,rare)]
   self.assertTrue(all(a>b for a,b in zip(values,values[1:])),(common,values))
 def test_extra_planet_metals_have_larger_veins_than_rare_gems(self):
  for metal,gem in [('lunarium','eclipse_opal'),('aresium','redshift_garnet'),('azurium','tidal_sapphire'),('basaltine','ember_spinel'),('rime_nickel','wraith_quartz'),('helion','corona_topaz')]:self.assertGreater(size(metal),size(gem),(metal,gem))
 def test_sol_ore_profile_and_story_nullifite_remain_small(self):
  self.assertGreater(size('ferrox'),size('olympium'));self.assertGreater(size('olympium'),size('aresite'))
  self.assertLessEqual(size('nullifite'),2);self.assertGreater(size('moonsteel'),size('nullifite'))
if __name__=='__main__':unittest.main()
