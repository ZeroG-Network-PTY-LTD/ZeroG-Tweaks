# ZeroG Structure Workshop

Local project-native compiler, version0.1.0. Requires Python3 standard library
only. This is not the missing game-dev plugin CLI, nor an image-to-3D model tool.
Use it to author deterministic Java Minecraft1.21.1 structure templates from
block-exact specifications; no external service, API key or installed mod needed.

Run from the code checkout:

```sh
python3 tools/structure_workshop.py doctor
python3 tools/structure_workshop.py validate path/to/source.json \
  --assets src/main/resources/assets/zerog_tweaks
python3 tools/structure_workshop.py build path/to/source.json \
  --assets src/main/resources/assets/zerog_tweaks --output path/to/new-export-v1
PYTHONPATH=tools python3 -m unittest tools/test_structure_workshop.py
```

Outputs: structure.nbt, original source.json, declared chest loot tables and a
receipt with dimensions/block counts and SHA256 hashes. Existing output paths
are refused. No live saves, JARs or natural-generation registries are modified.

## Source contract

Schema1 contains `size:[x,y,z]`, `palette:[{"Name":"namespace:block",
"Properties":{"key":"value"}}]`, `blocks:[{"pos":[x,y,z],"state":index}]`.
Each coordinate is local, nonnegative, unique and inside size. Dimensions1..128,
maximum300000 explicit blocks. Explicit air can clear authored interiors when a
template is intentionally placed; export itself never clears terrain.

Chest/barrel blocks may have `nbt:{"LootTable":"namespace:chests/name"}`.
Declare its actual Minecraft chest loot JSON under `loot_tables`, keyed by that
identifier, or list an existing verified table in `existing_loot_tables`.
To configure spawner blocks use `nbt:{"mob":"namespace:entity"}`.
Compiler writes native SpawnData with bounded
two-per-cycle/four-nearby defaults. Those are initial tool defaults, not encounter
balance approval. Templates must later be tested with real registered entity IDs.

Loot checks block explicit Wisp/Codex/Console, gate-key and smithing-template
strings; they are a guardrail, NOT a complete semantic lore audit. Nested loot
references and existing tables still need human/loaded-game review.

## Verified versus pending

Five tests pass: deterministic binary export and independent existing NBT-reader
decoding, coordinates/indices, story/unresolved loot, safe resource paths and
output preservation. Test fixture includes a chest/spawner; it is not shipped
world content. Native DataVersion3955 is used for1.21.1 templates.

Optional asset directory checks custom blockstate file presence; it does not
prove every property value, entity or loot function exists in the game registry.
Full room walkability, rotations, palette correctness, structures/biome binding,
hostile population and natural terrain placement need isolated Minecraft tests.
Generated concept artwork is a reference, not a finished template. The approved
water/hot/ice structures and cone vent models remain separate production tasks.

Store authoring concepts/generators on Design, compiler/tests on1.21.x, and player
documentation on Docs. Never merge unrelated branch histories.
