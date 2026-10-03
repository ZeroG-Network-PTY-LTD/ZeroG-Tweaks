# Dimension ecology v1 — authored resources and editable studies

Source generator: `docs/zero-g-tweaks-bundle/generators/dimension_ecology.py`.
Run with `--code-root PATH` pointing at the separate 1.21.x checkout.
357 texture PNGs, 233 editable Blockbench projects, all 34 registered dimension
IDs. No paid generation, third-party texture bytes or canonical GLB admission.
Existing Liquid Starlight artwork is preserved; the five additional fluids
have 32px still / 64px flowing, sixteen-frame interpolated strips.

Each dimension has soil, dry/wet farmland, snowy-aware grass, short/tall grass
and its own Star Sand (the six named-planet sands belong to crystals-v2).
New artwork is native 32px pixel art. Galaxy palettes follow the documented
default wasteland map; future seeded reassignments need updated palette mappings.
Soil/grass can be hoed. Farmland supports vanilla wheat, water irrigation,
drying/trampling and reversion to its own soil. Other fluids do not irrigate.

Named planets have luminous shrub/flower/decorative mushroom studies, six gas
vents and independently painted vanilla-Java-bee-rig glowbugs. Bug projects
include bodies, symmetric antennae/wings, stinger and three leg planes, plus a
wing-animation study. Runtime uses vanilla BeeModel animation and a smaller
render scale, blinking PNGs and eye/wing glow masks. This is not Productive Bees
integration or final approved bee artwork. Desktop imports/rendering remain
unverified; these are editable studies, not GPU captures.

Preview PNGs/GIFs are offline references. The soil sheet shows all families;
`dimension_fluids_reference.gif` shows the six liquids; glowing flora/vent/bug
face UV art appears in `glowing_ecology_reference.png`. A face UV tile is not
an in-world bug screenshot. `manifest.json` records runtime/design hashes.
Overwritten texture bytes are recoverable in `before/`.

Runtime counterpart on 1.21.x: small vegetation patches, existing planet trees
and vanilla oak/birch mixtures, configured natural fluid pools, gas traits and
daily impacts. The existing planetary caves/ores/biomes are preserved.
Impacts run once per active dimension/day, at night, only when suitable loaded
terrain is found; no force-loading or catch-up barrage. They excavate bounded
craters with meteorite and two mining-gated ore nodes. Containers/block entities,
unbreakable blocks, fluids and unrecognised building materials prevent placement.
Player-built natural stone/soil is not distinguishable from terrain; back up saves.
No falling sky projectile, campaign structures, alien crop/fruit varieties or
claim-protection integration is claimed. Code/installation evidence lives on Docs.
