"""Runtime worldgen compiler: namespace density/noise graphs per stable planet ID.

Vanilla RandomState salts noise by registry key. Distinct keys therefore produce
different seed-dependent terrain, rather than the same surface in new colours.
Existing surface rules, regional biomes, caves and ore registrations are retained.
"""
import argparse
import copy
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src/main/resources/data"

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")

def compile_planets(vanilla, mapped_sources):
    source = zipfile.ZipFile(vanilla)
    # Vanilla registers its noise parameters in Java, not resource-pack JSON.
    # Read the actual mapped 1.21.1 bootstrap instead of inventing missing values.
    with zipfile.ZipFile(mapped_sources) as jar:
        names_source=jar.read("net/minecraft/world/level/levelgen/Noises.java").decode()
        noise_source=jar.read("net/minecraft/data/worldgen/NoiseData.java").decode()
    names=dict(re.findall(r'(\w+)\s*=\s*createKey\("([^"]+)"\)',names_source))
    builtin={}
    for name,octave,amplitudes in re.findall(r'register\(context,\s*Noises\.(\w+),\s*(-?\d+),\s*([^;]+?)\);',noise_source):
        builtin["minecraft:"+names[name]]={"firstOctave":int(octave),"amplitudes":[float(v.strip()) for v in amplitudes.split(",")]}
    builtin["minecraft:offset"]={"firstOctave":-3,"amplitudes":[1,1,1,0]}
    for suffix,offset in (("",0),("_large",-2)):
        for name,octave,amplitudes in (("temperature",-10,[1.5,0,1,0,0,0]),
                                      ("vegetation",-8,[1,1,0,0,0,0]),
                                      ("continentalness",-9,[1,1,2,2,2,1,1,1,1]),
                                      ("erosion",-9,[1,1,0,1,1])):
            builtin["minecraft:"+name+suffix]={"firstOctave":octave+offset,"amplitudes":amplitudes}
    def read(kind, identifier):
        namespace, name = identifier.split(":", 1)
        path = DATA / namespace / "worldgen" / kind / (name + ".json")
        if path.exists():
            return json.loads(path.read_text())
        member = f"data/{namespace}/worldgen/{kind}/{name}.json"
        try:
            return json.loads(source.read(member))
        except KeyError:
            return copy.deepcopy(builtin.get(identifier)) if kind=="noise" else None

    dimensions = sorted((DATA / "zerog_tweaks/dimension").glob("*.json"))
    biomes = set()
    natural_surfaces=set()
    habitat_biomes={theme:set() for theme in ("moon","mars","cerulon","skarn","eidolon","solvane")}
    themes=(("cerulon","mars","skarn","eidolon","skarn","solvane"),
            ("eidolon","skarn","solvane","moon","cerulon","mars"),
            ("moon","cerulon","mars","skarn","eidolon","skarn"),
            ("skarn","eidolon","skarn","solvane","moon","cerulon"))
    for dim_file in dimensions:
        name = dim_file.stem
        dim = json.loads(dim_file.read_text())
        # Re-running uses the preserved input snapshot, never compounds transforms.
        snapshot = ROOT / "tools/planet_worldgen_baselines" / (name + ".json")
        if snapshot.exists():
            settings = json.loads(snapshot.read_text())
        else:
            settings = read("noise_settings", dim["generator"]["settings"])
            write(snapshot, settings)
        seen = {}
        def clone(kind, identifier):
            key = (kind, identifier)
            if key in seen:
                return seen[key]
            value = read(kind, identifier)
            if value is None:
                return identifier
            ns, path = identifier.split(":", 1)
            target = f"planet/{name}/{ns}/{path}"
            result = "zerog_tweaks:" + target
            seen[key] = result
            # Each key has a unique positional RNG salt; octave changes distinguish
            # broad dunes/ice shelves from sharp ridges without changing cave IDs.
            if kind == "noise" and any(p in path for p in ("continentalness", "erosion", "ridge")):
                if name in ("mars", "moon"):
                    value["firstOctave"] = value["firstOctave"] - 1
                elif name in ("skarn", "solvane"):
                    value["firstOctave"] = value["firstOctave"] + 1
            value = walk(value, "noise" if kind == "noise" else None)
            write(DATA / "zerog_tweaks/worldgen" / kind / (target + ".json"), value)
            return result
        def walk(value, key=None):
            if isinstance(value, list):
                return [walk(v) for v in value]
            if isinstance(value, dict):
                return {k: walk(v, k) for k, v in value.items()}
            if isinstance(value, str) and ":" in value:
                if key == "noise":
                    if read("noise",value) is None:
                        raise ValueError("Unresolved vanilla noise parameters: "+value)
                    return clone("noise", value)
                if key not in ("type", "biome", "Name", "random_name") and read("density_function", value) is not None:
                    return clone("density_function", value)
                if key == "argument" and read("noise",value) is not None:
                    return clone("noise",value)
            return value
        settings["noise_router"] = walk(copy.deepcopy(settings["noise_router"]))
        def collect_blocks(value):
            if isinstance(value,dict):
                if isinstance(value.get("Name"),str) and value["Name"].startswith("zerog_tweaks:"):
                    natural_surfaces.add(value["Name"])
                for child in value.values(): collect_blocks(child)
            elif isinstance(value,list):
                for child in value: collect_blocks(child)
        collect_blocks(settings.get("surface_rule",{}));collect_blocks(settings["default_block"])
        natural_surfaces.update("zerog_tweaks:"+name+suffix for suffix in ("_soil","_grass_block"))
        # Shape profiles, not simply colour palettes. Positive offsets raise solid
        # density; negative offsets deepen basins. Slot variation is stable per ID.
        if name == "moon":
            bias = -0.055
        elif name == "mars":
            bias = 0.018
        elif name == "eidolon":
            bias = -0.015
        elif name in ("skarn", "solvane"):
            bias = 0.035
        elif name == "cerulon":
            bias = 0.0  # Preserve its authored ocean/archipelago density profile.
        else:
            bias = ((sum((i+1)*ord(c) for i,c in enumerate(name)) % 11)-5)*0.006
        if bias:
            settings["noise_router"]["final_density"] = {
                "type": "minecraft:add", "argument1": bias,
                "argument2": settings["noise_router"]["final_density"]}
        target = "planet/" + name
        write(DATA / "zerog_tweaks/worldgen/noise_settings" / (target + ".json"), settings)
        dim["generator"]["settings"] = "zerog_tweaks:" + target
        write(dim_file, dim)
        biomes.update(b["biome"] for b in dim["generator"]["biome_source"]["biomes"])
        theme=(themes[int(name[1])-2][int(name[4])-1] if re.fullmatch(r'g[2-5]_p[1-6]',name)
               else "moon" if name.endswith("_moons") else name)
        habitat_biomes[theme].update(b["biome"] for b in dim["generator"]["biome_source"]["biomes"])
    for feature, chance, step in (("planet_settlement", 36, "surface_structures"),
                                  ("planet_mineshaft", 18, "underground_structures")):
        write(DATA / f"zerog_tweaks/worldgen/configured_feature/{feature}.json",
              {"type": "zerog_tweaks:"+feature, "config": {}})
        write(DATA / f"zerog_tweaks/worldgen/placed_feature/{feature}.json", {
            "feature": "zerog_tweaks:"+feature, "placement": [
                {"type": "minecraft:rarity_filter", "chance": chance},
                {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"}]})
        write(DATA / f"zerog_tweaks/neoforge/biome_modifier/{feature}s.json", {
            "type": "neoforge:add_features", "biomes": sorted(biomes),
            "features": "zerog_tweaks:"+feature, "step": step})
    source.close()
    write(DATA / "zerog_tweaks/tags/block/planet_natural_surfaces.json",{"replace":False,"values":sorted(natural_surfaces)})
    # Fill missing habitats only; don't duplicate existing per-biome spawn entries.
    modifiers=DATA/"zerog_tweaks/neoforge/biome_modifier"
    present={}
    for path in modifiers.glob("*.json"):
        if path.stem.startswith("expanded_habitat_"): continue
        value=json.loads(path.read_text())
        if value.get("type")!="neoforge:add_spawns" or not isinstance(value.get("biomes"),list): continue
        spawners=value.get("spawners",[])
        if isinstance(spawners,dict): spawners=[spawners]
        for spawn in spawners: present.setdefault(spawn["type"],set()).update(value["biomes"])
    species={"moon":["dune_burrower"],"mars":["rust_beetle","dune_burrower"],
             "cerulon":["mossback","azure_fowl","glimmerfish"],"skarn":["rust_beetle"],
             "eidolon":["frost_yak"],"solvane":["crystal_stag","azure_fowl"]}
    for theme,mobs in species.items():
        for mob in mobs:
            identifier="zerog_tweaks:"+mob
            missing=habitat_biomes[theme]-present.get(identifier,set())
            if missing:
                write(modifiers/f"expanded_habitat_{theme}_{mob}.json",{"type":"neoforge:add_spawns",
                      "biomes":sorted(missing),"spawners":[{"type":identifier,"weight":4,"minCount":1,"maxCount":2}]})
    print(f"Compiled independent terrain graphs for {len(dimensions)} planets; settlements/shafts in {len(biomes)} biomes")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vanilla-resources", type=Path, required=True)
    parser.add_argument("--mapped-sources", type=Path, required=True)
    args=parser.parse_args()
    compile_planets(args.vanilla_resources,args.mapped_sources)
