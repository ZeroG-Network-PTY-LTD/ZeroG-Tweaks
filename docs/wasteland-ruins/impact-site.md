# Impact Site — static Concord remnants

Two original 21×7×21 shallow crater layouts use existing craterstone, cobbled craterstone, meteorite fragments and hull plating. A low circular rim surrounds scattered hull debris. A cleared north approach has a continuous craterstone floor; the single north-facing chest at (10,1,14) has clear lid space.

The unchanged `zerog_tweaks:chests/impact_site` table provides the existing Stardust reward. No console, Wisp, Codex, named wreck, dialogue, boss or new story text is added. Approved lore permits Concord ruins but leaves the Impact Site story unwritten.

These are static world-generation ruins, not the separately implemented daily spherical comet impacts. Their generator does not alter that event, its mining layers or timing.

Target all three registered barren wasteland biomes: Cratered Plains, Dust Badlands and Canyon Scars. Retain bounded dry-ground placement with six-block terrain tolerance, 32-block nearby search, `always_place=false`, random-spread spacing40/separation20 and independent salt19477406. Do not claim guaranteed density or placement on every planet.

Acceptance: both template variants in four rotations must place one physical chest with the correct loot table, free lid, accessible approach and actual Stardust reward. Runtime and retained Design data must agree. Ordinary fresh-world natural placement and client appearance are separate checks; do not substitute forced placement for natural evidence.

Regenerate with `generate_impact_site.py --resources /absolute/path/to/1.21.x/src/main/resources`. Uses the existing original NBT writer and approved textures, not external mesh generation.
