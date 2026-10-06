"""Translate authored refining data; add registered raw-smelting and Stardust routes.

Run with the 1.21.x worktree path. This only writes the dedicated refining folder;
it never changes IDs, deletes files or touches artwork.
"""
import json
import sys
from pathlib import Path

code = Path(sys.argv[1]).resolve()
source = Path(__file__).resolve().parents[1] / "zero-g-tweaks-bundle/pending-data/recipe/refining"
dest = code / "src/main/resources/data/zerog_tweaks/recipe/refining"
dest.mkdir(parents=True, exist_ok=True)

def write(name, ingredient, result, upgraded, energy=4000, time=200, catalyst=None, conditions=None):
    data = {"type": "zerog_tweaks:refining", "inputs": [{"ingredient": ingredient}],
            "outputs": [{"stack": result}], "energy": energy, "time": time,
            "upgraded_result_count": upgraded}
    if catalyst:
        data["catalyst"] = {"ingredient": catalyst, "consumed": True}
    if conditions:
        data["neoforge:conditions"] = conditions
    (dest / (name + ".json")).write_text(json.dumps(data, indent=2) + "\n")

for path in sorted(source.glob("*.json")):
    old = json.loads(path.read_text())
    write(path.stem, old["ingredient"], old["result"], old["upgraded_result_count"], old["energy"], old["time"])

# Use the existing smelting recipes as the registry source of truth. Refining raw
# metal yields ingots; refining ores follows the authored raw/gem/dust output.
raw = {}
for path in sorted((code / "src/main/resources/data/zerog_tweaks/recipe").glob("*.json")):
    data = json.loads(path.read_text())
    if data.get("type") != "minecraft:smelting":
        continue
    ingredient = data.get("ingredient", {})
    item = ingredient.get("item", "") if isinstance(ingredient, dict) else ""
    result = data.get("result", {})
    if item.startswith("zerog_tweaks:raw_") and not item.endswith("_block") and isinstance(result, dict):
        raw[item] = result["id"]
registered_items = (code / "src/main/java/net/zerog/tweaks/registry/ItemInit.java").read_text()
for item, ingot in sorted(raw.items()):
    name = item.split(":")[1]
    write(name, {"item": item}, {"id": ingot, "count": 2}, 3)
    block = name + "_block"
    # Only use raw blocks already registered by the project.
    if ('"' + block + '"') in registered_items:
        write(block, {"item": "zerog_tweaks:" + block}, {"id": ingot, "count": 18}, 27, 36000)

write("aresite_stardust", {"item": "zerog_tweaks:aresite"},
      {"id": "zerog_tweaks:aresite", "count": 5}, 5,
      catalyst={"item": "zerog_tweaks:stardust"})
write("aresite_aero_stardust", {"item": "zerog_tweaks:aresite"},
      {"id": "zerog_tweaks:aresite", "count": 5}, 5,
      catalyst={"item": "aeroapiary:stardust"},
      conditions=[{"type": "neoforge:mod_loaded", "modid": "aeroapiary"}])
print("Generated", len(list(dest.glob("*.json"))), "refining recipes")
