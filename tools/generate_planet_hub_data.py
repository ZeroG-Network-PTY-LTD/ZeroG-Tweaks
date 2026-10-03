"""Selectable new-world preset and isolated seed-zero test preset (never shipped flat override)."""
import json
from pathlib import Path

PROJECT=Path(__file__).resolve().parents[1]
DATA=PROJECT/"src/main/resources/data"
def put(root,path,data):
    target=root/path;target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(data,indent=2)+"\n")
def main():
    dimensions={"minecraft:overworld":{"type":"minecraft:overworld","generator":{
        "type":"minecraft:flat","settings":{"biome":"zerog_tweaks:planet_test_hub",
        "lakes":False,"features":False,"structure_overrides":[],
        "layers":[{"height":1,"block":"minecraft:bedrock"},{"height":126,"block":"minecraft:stone"}]}}},
        "minecraft:the_nether":{"type":"minecraft:the_nether","generator":{
            "type":"minecraft:noise","settings":"minecraft:nether","biome_source":{"type":"minecraft:multi_noise","preset":"minecraft:nether"}}},
        "minecraft:the_end":{"type":"minecraft:the_end","generator":{
            "type":"minecraft:noise","settings":"minecraft:end","biome_source":{"type":"minecraft:the_end"}}}}
    for path in sorted((DATA/"zerog_tweaks/dimension").glob("*.json")):
        dimensions["zerog_tweaks:"+path.stem]=json.loads(path.read_text())
    preset={"dimensions":dimensions}
    put(DATA,"zerog_tweaks/worldgen/world_preset/planet_test_hub.json",preset)
    put(DATA,"minecraft/tags/worldgen/world_preset/normal.json",{"replace":False,"values":["zerog_tweaks:planet_test_hub"]})
    put(DATA,"zerog_tweaks/worldgen/biome/planet_test_hub.json",{
        "has_precipitation":False,"temperature":.7,"downfall":0,"effects":{
        "sky_color":7907327,"fog_color":12638463,"water_color":4159204,"water_fog_color":329011},
        "spawners":{},"spawn_costs":{},"carvers":{},"features":[[] for _ in range(11)]})
    put(PROJECT/"src/planet-hub-gametest/resources/data","minecraft/worldgen/world_preset/flat.json",preset)
    lang=PROJECT/"src/main/resources/assets/zerog_tweaks/lang/en_us.json"
    labels=json.loads(lang.read_text());labels["generator.zerog_tweaks.planet_test_hub"]="ZeroG: Planet Test Hub"
    lang.write_text(json.dumps(labels,indent=2)+"\n")
    print("Planet hub preset: 34 planets/moons, Overworld hub, Nether and End; isolated test seed 0")
if __name__=="__main__":main()
