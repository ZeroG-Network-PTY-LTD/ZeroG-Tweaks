"""Original gameplay data for ZeroG joinery/storage. Never imports reference JARs."""
import argparse
import json
from pathlib import Path

WOODS = ["shardwood", "charwood", "hoarwood", "gildwood"]
TIERS = ["copper", "nullifite", "cyrrium", "tectium", "wraithsteel", "astrium"]

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

def append_tag(resources, namespace, kind, name, values):
    path = resources / f"data/{namespace}/tags/{kind}/{name}.json"
    doc = json.loads(path.read_text()) if path.exists() else {"replace": False, "values": []}
    doc["values"] = list(dict.fromkeys(doc["values"] + values))
    write(path, doc)

def recipe(resources, name, pattern, key, count=1):
    write(resources / f"data/zerog_tweaks/recipe/storage/{name}.json", {
        "type": "minecraft:crafting_shaped", "category": "misc", "pattern": pattern,
        "key": {k: {"item": v} for k, v in key.items()}, "result": {"id": f"zerog_tweaks:{name}", "count": count}})

def generate(resources):
    names = {"item.zerog_tweaks.storage_expansion_module": "Storage Expansion Module",
             "item.zerog_tweaks.generator_flux_module": "Generator Flux Module",
             "itemGroup.zerog_tweaks.storage_and_transport": "ZeroG: Storage & Transport",
             "container.zerog_tweaks.fluid_tank": "Fluid Tank",
             "gui.zerog_tweaks.generator_fuel": "Fuel",
             "gui.zerog_tweaks.generator_modules": "Flux modules: %s / 3",
             "gui.zerog_tweaks.generator_output": "Output: %s FE/t",
             "message.zerog_tweaks.generator_module_installed": "Flux module %s / 3 installed - %s FE buffer",
             "message.zerog_tweaks.generator_module_limit": "Generator already has three flux modules",
             "gui.zerog_tweaks.refinery.input": "Ore",
             "gui.zerog_tweaks.refinery.catalyst": "Boost",
             "gui.zerog_tweaks.refinery.output": "Out",
             "gui.zerog_tweaks.refinery.cycle": "Cycle: %s%%",
             "gui.zerog_tweaks.refinery.input_hint": "Accepts Raw Cyrrium, Cyrrium Ore, Aresite Ore, Raw Nullifite Block, or Aresite for the optional stardust boost.",
             "gui.zerog_tweaks.refinery.output_hint": "Processed output. This slot only allows extraction.",
             "block.zerog_tweaks.ore_refinery.catalyst_hint": "Optional aeroapiary Stardust: consumes one only when boosting Aresite into five Aresite. Other recipes need no catalyst.",
             "message.zerog_tweaks.storage_already_expanded": "Close this container first, or it is already expanded."}
    ids = []
    for wood in WOODS:
        for suffix, label in [("chest", "Chest"), ("barrel", "Barrel"), ("panel_door", "Panel Door"), ("lattice_trapdoor", "Lattice Trapdoor")]:
            name = wood + "_" + suffix
            ids.append("zerog_tweaks:" + name)
            names["block.zerog_tweaks." + name] = wood.capitalize() + " " + label
            entry = {"type": "minecraft:item", "name": "zerog_tweaks:" + name}
            if suffix == "panel_door":
                entry["conditions"] = [{"condition": "minecraft:block_state_property", "block": "zerog_tweaks:" + name, "properties": {"half": "lower"}}]
            write(resources / f"data/zerog_tweaks/loot_table/blocks/{name}.json", {"type": "minecraft:block", "pools": [{"rolls": 1, "conditions": [{"condition": "minecraft:survives_explosion"}], "entries": [entry]}]})
        planks = "zerog_tweaks:" + wood + "_planks"
        recipe(resources, wood + "_chest", ["PPP", "P P", "PPP"], {"P": planks})
        recipe(resources, wood + "_barrel", ["PSP", "P P", "PSP"], {"P": planks, "S": "zerog_tweaks:" + wood + "_slab"})
        recipe(resources, wood + "_panel_door", ["PP", "PP", "PP"], {"P": planks}, 3)
        recipe(resources, wood + "_lattice_trapdoor", ["PPP", "PPP"], {"P": planks}, 2)
    recipe(resources, "storage_expansion_module", ["ICI", "CHC", "ICI"], {"I": "zerog_tweaks:moonsteel_ingot", "C": "minecraft:copper_ingot", "H": "minecraft:chest"})
    recipe(resources, "generator_flux_module", ["CRC", "RIR", "CRC"], {"C": "minecraft:copper_ingot", "R": "minecraft:redstone", "I": "zerog_tweaks:moonsteel_ingot"})
    for i, tier in enumerate(TIERS):
        tank = tier + "_fluid_tank"
        names["block.zerog_tweaks." + tank] = tier.capitalize() + " Fluid Tank (T" + str(i+1) + ")"
        write(resources / f"data/zerog_tweaks/loot_table/blocks/{tank}.json", {"type": "minecraft:block", "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": "zerog_tweaks:" + tank}]}]})
    append_tag(resources, "minecraft", "block", "mineable/axe", ids)
    append_tag(resources, "minecraft", "block", "wooden_doors", ["zerog_tweaks:"+w+"_panel_door" for w in WOODS])
    append_tag(resources, "minecraft", "item", "wooden_doors", ["zerog_tweaks:"+w+"_panel_door" for w in WOODS])
    for kind in ("block", "item"):
        append_tag(resources, "minecraft", kind, "wooden_trapdoors", ["zerog_tweaks:"+w+"_lattice_trapdoor" for w in WOODS])
        append_tag(resources, "c", kind, "chests/wooden", ["zerog_tweaks:"+w+"_chest" for w in WOODS])
        append_tag(resources, "c", kind, "barrels/wooden", ["zerog_tweaks:"+w+"_barrel" for w in WOODS])
    append_tag(resources, "minecraft", "block", "mineable/pickaxe", ["zerog_tweaks:"+t+"_fluid_tank" for t in TIERS])
    lang_path = resources / "assets/zerog_tweaks/lang/en_us.json"
    lang = json.loads(lang_path.read_text())
    lang.update(names)
    write(lang_path, lang)
    return {"wood_blocks": 16, "tank_tiers": 6, "upgrade_items": 2}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resources", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(generate(args.resources)))
