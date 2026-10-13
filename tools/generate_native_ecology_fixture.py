"""Generate a test-only native planet preset without hub construction or save mutation."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    dimensions = {
        "minecraft:overworld": {
            "type": "minecraft:overworld",
            "generator": {
                "type": "minecraft:flat",
                "settings": {
                    "biome": "minecraft:plains", "lakes": False,
                    "features": False, "structure_overrides": [],
                    "layers": [{"height": 1, "block": "minecraft:bedrock"},
                               {"height": 126, "block": "minecraft:stone"}]
                }
            }
        }
    }
    for path in sorted((ROOT / "src/main/resources/data/zerog_tweaks/dimension").glob("*.json")):
        dimensions["zerog_tweaks:" + path.stem] = json.loads(path.read_text())
    if len(dimensions) != 35:
        raise ValueError("Expected 34 real planetary dimensions plus the test Overworld")
    target = ROOT / "src/native-ecology-gametest/resources/data/minecraft/worldgen/world_preset/flat.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({"dimensions": dimensions}, indent=2) + "\n")
    print(f"Wrote 34 native planets to test-only preset: {target}")

if __name__ == "__main__":
    main()
