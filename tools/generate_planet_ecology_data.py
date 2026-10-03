"""Idempotent biome ecology additions; existing dimensions/registry IDs remain intact."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"src/main/resources/data/zerog_tweaks"
def put(path,data):
    target=ROOT/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(data,indent=2)+"\n")
def main():
    dimensions={p.stem:json.loads(p.read_text()) for p in (ROOT/"dimension").glob("*.json")}
    biomes=sorted({entry["biome"] for dim in dimensions.values()
                   for entry in dim["generator"]["biome_source"]["biomes"]})
    put("worldgen/configured_feature/planet_cave_ecology.json",{"type":"zerog_tweaks:planet_cave_ecology","config":{}})
    put("worldgen/placed_feature/planet_cave_ecology.json",{
        "feature":"zerog_tweaks:planet_cave_ecology","placement":[{"type":"minecraft:count","count":1},
        {"type":"minecraft:in_square"},{"type":"minecraft:heightmap","heightmap":"WORLD_SURFACE_WG"}]})
    put("neoforge/biome_modifier/all_planet_cave_ecology.json",{
        "type":"neoforge:add_features","biomes":biomes,"features":"zerog_tweaks:planet_cave_ecology","step":"vegetal_decoration"})
    # Include the ocean wastelands omitted by the previous surface-kelp list.
    kelp=ROOT/"neoforge/biome_modifier/planet_lake_glowkelp.json"
    data=json.loads(kelp.read_text());data["biomes"]=biomes
    put("neoforge/biome_modifier/planet_lake_glowkelp.json",data)
    themes={
        "moon":["wasteland_cratered_plains","wasteland_dust_badlands","wasteland_canyon_scars"],
        "mars":["wasteland_dune_seas","wasteland_mesa_canyons","wasteland_salt_flats"],
        "cerulon":["wasteland_deep_trenches","wasteland_island_chains","wasteland_kelp_jungles"],
        "skarn":["wasteland_ash_plains","wasteland_basalt_fields","wasteland_lava_lakes",
                 "wasteland_acid_swamps","wasteland_mud_flats","wasteland_moss_bogs"],
        "eidolon":["wasteland_glaciers","wasteland_frozen_canyons","wasteland_ice_spike_forest"],
        "solvane":["wasteland_prism_fields","wasteland_crystal_caverns"]}
    for theme,names in themes.items():
        put(f"neoforge/biome_modifier/slot_{theme}_bees.json",{
            "type":"neoforge:add_spawns","biomes":["zerog_tweaks:"+n for n in names],
            "spawners":[{"type":"zerog_tweaks:"+theme+"_glowbug","weight":3,"minCount":1,"maxCount":2}]})
    # Only implemented entities are admitted. Unfinished bosses are never silently substituted.
    additions={
        "mars":(["rust_plains","oxide_badlands",*themes["mars"]],["rust_beetle","dune_burrower"]),
        "eidolon":(["frozen_graveyard","phantom_ice_sheets","hoarwood_taiga",*themes["eidolon"]],["frost_yak"]),
        "ocean":(["glimmer_sea",*themes["cerulon"]],["glimmerfish"]),
        "forest":(["gildwood_oasis","wasteland_island_chains","wasteland_moss_bogs"],["mossback","azure_fowl"]),
        "moon":(["lunar_highlands","lunar_mare","shadowed_craters",*themes["moon"]],["dune_burrower"]),
        "skarn":(["ember_fields","charwood_barrens",*themes["skarn"]],["rust_beetle"])}
    for name,(homes,mobs) in additions.items():
        put(f"neoforge/biome_modifier/planet_ready_{name}_mobs.json",{
            "type":"neoforge:add_spawns","biomes":["zerog_tweaks:"+b for b in homes],
            "spawners":[{"type":"zerog_tweaks:"+m,"weight":4,"minCount":1,"maxCount":2} for m in mobs]})
    print(f"Ecology wired for {len(dimensions)} dimensions and {len(biomes)} biomes")
if __name__=="__main__":main()
