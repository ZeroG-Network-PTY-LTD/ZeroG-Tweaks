# Planetary structure translation v1

Approved generated reference: concept-reference.png, built-in ImageGen concept
preview (not a game render), requested13October2026. Owner then requested close
block-built structures with loot rooms/aggressive mobs. Initial authoring generator
produces49x64x49 block-exact specifications using existing local grass/soil and
native decorative blocks. No custom textures were invented or copied from mods.

Current candidate source: sources-v3, exported by the separately implemented native
Structure Workshop compiler on1.21.x. exports-v3 has NBT, ordinary loot tables
and SHA256 receipts. v2 fixed a stair overwriting the initial spawner position;
superseded sources-v1/exports-v1 are local discarded experiments, not ship targets.
v3 restores staircase clearance after tower skirt detailing. Seven static checks
pass; isolated native collision verification is in progress. Installed showcase
still uses v2 until the next explicitly verified combined delivery.

Generation command from this folder:

```sh
python3 generate.py --output sources-v3
```

Compiler from code worktree: tools/structure_workshop.py build SOURCE --assets
src/main/resources/assets/zerog_tweaks --output NEW_EXPORT_FOLDER. No-overwrite
destinations preserve manual changes; approve each new generated revision.

Compiled templates live under data/zerog_tweaks/structure/planetary_showcase on
1.21.x. Five addon-enabled hub/structure tests pass: all three templates placed,
six chests yielded supplies and three hostile spawners/clear central passages
were observed. Installed in the separate13October test-region hub.

Remaining: direct visual comparison and refinements toward the concept; rotations,
full pathfinding/walkability, balanced mobs, natural biome/siting integration and
cone vent models. The first translation must NOT be described as image-identical,
a full natural-generation system or completed cone artwork. Lunar survey draft
is separate and remains inactive. Exact crafting/research rules remain deferred.
