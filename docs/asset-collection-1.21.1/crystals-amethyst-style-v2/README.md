# Crystals, metals and Star Glass — local review v2

This is a new authored revision, not a rewrite of the historical collection or
its hash roster. Generator: `docs/zero-g-tweaks-bundle/generators/crystals_v2.py`.
Run from Design with `--code-root` pointing at the separate 1.21.x checkout.
No provider jobs, borrowed third-party texture bytes or paid services are used.
Palettes are derived from the project's existing `generators/data.py`.

## Review images

- `crystals_v2_preview.png`: the complete texture roster.
- `ingots_raw_reference.png`: all 16 ingot/raw-metal pairs.
- `planet_sands_reference.png`: six named-planet sands, each smelting to Star Glass.
- `star_glass_reference.png` and `animated_updates.gif`: offline appearance and animation reference.
- `blockbench/`: editable texture-embedded projects. These are NOT verified desktop screenshots.

## Artwork

32x32 newly authored pixel facets for four cluster families, ten crystal/gem
material families, and sixteen metals' ingots/raw materials. These are not
nearest-upscaled copies of the original PNGs. Existing lore colours remain.
Three dimension-tinted cluster families and their buds/root blocks remain
grayscale; their in-game palette comes from ZGBlockColors. Rimeglass remains
translucent. Ingot/raw sprites use vanilla generated item rendering; the item
models provide standard GUI/held/dropped positioning, not wearable geometry.

Star Glass has a 64x64 animated pane, sixteen frames, frametime 3, interpolation,
quartz edging, nebula spirals, stars and a singularity projection. The glass
pane is alpha 38/255 (approximately 15% opacity), with brighter frame/stars.
This is a textured depth illusion, NOT real parallax, dynamic coloured lighting
or a custom shader. Blue/light-blue, purple/magenta and cyan/green dyes change
the placed pane's nebula state; quartz stays neutral. Silk Touch returns the
default purple glass item (no per-item saved colour component).

## Runtime counterpart (1.21.x development candidate)

Existing mature cluster IDs remain. All four families grow from their budding
root through small/medium/large/full stages. Vanilla random-tick probability,
six-face growth, waterlogging and support rules are followed. Stage light is
1/2/4/5; Star Glass emits 12. Budding roots drop nothing, even with Silk Touch;
buds require Silk Touch. Existing mature-cluster loot/progression is preserved.
The old brine/frost/prism ore-patch features now place solid budding roots,
avoiding unsupported cluster blocks buried in stone.

Moon, Mars, Cerulon, Skarn, Eidolon and Solvane Star Sands are falling blocks.
Each furnace recipe takes 200 ticks and produces one Star Glass. Sand blocks
are available in Natural Blocks; glass is in Building Blocks. Planet sand
terrain generation is NOT added: that needs a separate terrain-placement
design decision. No Sky Glass registry IDs are added (human correction).

## Evidence boundary

`manifest.json` binds exact runtime/design texture hashes and resolutions.
Original overwritten texture bytes are preserved in `before/` for recovery.
The GIF is an offline reference, not an in-game/client/Blockbench capture.
No canonical GLB admission or human visual approval is claimed. Compilation,
resource checks and opt-in tests are reported separately; compiling a test
does not mean it was run. No game launch or modpack install is performed by
publishing this revision. Candidate build evidence and the jar live on Docs;
this folder contains design sources, not an installed mod.
