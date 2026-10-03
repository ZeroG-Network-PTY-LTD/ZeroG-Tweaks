"""Fast regression: supplement, not replace, actual server generation checks."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src/main/resources/data/zerog_tweaks"

class PlanetGenerationContract(unittest.TestCase):
    def test_each_planet_has_its_own_noise_settings(self):
        settings = [json.loads(p.read_text())["generator"]["settings"]
                    for p in sorted((DATA / "dimension").glob("*.json"))]
        self.assertEqual(len(settings), 34)
        self.assertEqual(len(set(settings)), 34, "Repeated settings mirror slot terrain")

    def test_settlements_are_wired_to_all_planet_biomes(self):
        expected = {b["biome"] for p in (DATA / "dimension").glob("*.json")
                    for b in json.loads(p.read_text())["generator"]["biome_source"]["biomes"]}
        path = DATA / "neoforge/biome_modifier/planet_settlements.json"
        self.assertTrue(path.exists(), "No planet settlement placement exists")
        self.assertEqual(set(json.loads(path.read_text())["biomes"]), expected)

    def test_noise_rng_keys_are_distinct_not_only_density_names(self):
        for dimension in (DATA/"dimension").glob("*.json"):
            noises=DATA/"worldgen/noise/planet"/dimension.stem
            self.assertGreater(len(list(noises.rglob("*.json"))),8,dimension.stem)

    def test_complete_carver_surface_coverage(self):
        carvers=json.loads((ROOT/"src/main/resources/data/minecraft/tags/block/overworld_carver_replaceables.json").read_text())
        replacements=set(carvers["values"])
        for name in ("lunar_stone","martian_stone","cerulean_stone","skarn_rock","permafrost","solar_stone"):
            self.assertIn("zerog_tweaks:"+name,replacements)

    def test_impacts_exclude_arrival_regions(self):
        source = (ROOT / "src/main/java/net/zerog/tweaks/event/DailyPlanetImpacts.java").read_text()
        self.assertIn("ArrivalProtection.intersects", source)

    def test_rare_settlements_have_region_spacing_and_ground_height(self):
        source=(ROOT/'src/main/java/net/zerog/tweaks/worldgen/PlanetSettlementFeature.java').read_text()
        self.assertIn('Math.floorDiv(cx,50)',source)
        self.assertIn('rx*50+16+site.nextInt(18)',source)
        self.assertIn('getZ())-1',source)
        self.assertIn('Math.abs(h-y)>4',source)
        self.assertNotIn('depth<64',source)
        self.assertIn('level.setBlock(floor,nativeSurface,2)',source)

    def test_cave_variants_register_before_soil_maps_populate(self):
        source=(ROOT/'src/main/java/net/zerog/tweaks/registry/ZGPlanetCaveVariants.java').read_text()
        self.assertIn('for(String id:ZGDimensionTerrain.dimensions())',source)
        self.assertNotIn('for(String id:ZGDimensionTerrain.SOILS.keySet())',source)

if __name__ == "__main__":
    unittest.main()
