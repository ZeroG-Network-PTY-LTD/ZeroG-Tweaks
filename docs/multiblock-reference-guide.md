# In-game apiary reference guide — Minecraft 1.21.1 development

Press **G** while in a world to open the ZeroG multiblock guide. The binding can
be changed in Controls → ZeroG Tweaks. When a compatible `aeroapiary` controller
is installed, Shift + right-click also opens the reference; this does not replace
its processing menu. The unrelated Tweaks teleporter gate does not open apiary
plans.

## Controls

- Structure arrows select the eight saved assemblies.
- Y− / Y+ select layers, starting at **Y=0**. Click the Y label to restore the
  highest layer.
- **From Y=0** shows the build up to the selected layer; **One layer** reveals
  only that horizontal slice, including internal frame housings and empty space.
- Drag the diagram for 360° rotation and tilt. Turn 90 gives quarter-turn views;
  Reset restores the front-oriented camera. Scroll over the diagram to zoom.
- Click a visible block to see its part type and exact local X/Y/Z coordinate.
  A yellow highlight identifies the selection. The parts list gives full-build
  quantities; scroll over the list to reveal additional entries.

Colour distinguishes controllers, input hatches, output/honey ports, power,
fluids, frame housings, glass and tier-specific parts. Cubes are a labelled
schematic, **not imported block textures or a world ghost overlay**. Coordinates
come directly from the authored Blockbench assemblies; decorative/emissive
overlay cubes are not counted as extra blocks. No arbitrary casing-to-port
substitutions are invented: the shown part is the authored reference for that
cell, not a completed formation validator's acceptance result.

## Genetics and cryo

The human selected **separate external modules**. They must not replace shell
blocks, hatches or internal frame housings in this guide. These are recorded as
external to all eight assemblies. Connection protocols, exact docking rules,
power/fluid/recipe handling and functional gene/cryo processing remain pending;
the guide does not falsely show existing validated sockets.

## Source and scope

Eight layouts / 944 distinct block cells are generated from
`docs/asset-collection-1.21.1/bees/blockbench_by_use/multiblocks/` with
`generators/generate_multiblock_guides.py` on `Design`, supplying `--code-root`
with a separate `1.21.x` checkout. The JSON records each original model's
SHA-256. Art and the immutable design catalogue are not changed.

This adds an in-game reference screen, not machine processing, construction
automation, world placement, a block-entity menu, or server-side formation.
Most apiary block registrations are still pending in the current Tweaks runtime.
No existing world blocks are placed or replaced by opening this guide.

Local server tests cover all eight rosters, unique coordinates, Y=0 origin,
exactly one controller each, the 944-cell total and separation of external
modules. Client review exercises rotation/layer rendering; it is not human
visual or pixel approval.

All 12 required server tests passed (`20261001_163525_runZeroGTests.log`). The
client review passed 32 quarter-turn/layer poses across all eight layouts
(`20261001_163759_runAssetReview.log`, 23:39 Asia/Bangkok on 2026-10-01).
This guide is now part of the `1.21.x` development publication, with designs on
`Design` and documentation on `Docs`. It is not installed into CurseForge.
