# Frozen Outpost — original Concord shelter

Two 17×9×17 templates, sharing a Hoarwood/permafrost floor, open three-block doorway, timber corner ribs, salvaged hull roof and two spectral lights. Variant 1 has a damaged rear roof corner; neither variant adds story text, inhabitants, a boss, a console log or rare ore-storage blocks. Snow is a normal one-layer roof dressing, not new weather.

Existing approved blocks/textures only. The source is `generate_frozen_outpost.py`, using the established Minecraft structure NBT writer. Generated runtime data is retained in `generated/data/zerog_tweaks`; editable construction coordinates are in the generator. No external 3D model, paid generation or new palette is required.

The central approach follows x=8, z=1..12 with clear y=2/3 and a continuous floor. One north-facing chest is at (8,2,13), with free lid space and the unchanged `zerog_tweaks:chests/frozen_outpost` table. Its existing guaranteed Cryo Core remains unchanged.

Natural placement targets Hoarwood Taiga and Phantom Ice Sheets only, with the established dry-ground jigsaw terrain check, six-block height tolerance and bounded 32-block nearby search. Random-spread spacing/separation is 40/20 chunks, independent salt 19477405, and `always_place=false`. This is a rare placement attempt grid—not a claim of one ruin per 40 chunks or guaranteed density.

Regenerate: `python3 docs/wasteland-ruins/generate_frozen_outpost.py --resources /absolute/path/to/1.21.x/src/main/resources`.

Approved lore allows a Concord ruin but has no written Frozen Outpost story. Keep logs, quests and dialogue pending approval. Focused tests check eight rotated placements, real chest/reward, corridor floors, headroom and lid clearance. Ordinary natural generation and client approval are separate checks.
