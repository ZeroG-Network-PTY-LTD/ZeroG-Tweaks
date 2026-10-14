# Industrial pressing — 12 October 2026

These canonical JSON copies match the installed code-branch machine and tooling
models. Runtime data/compiler is `1.21.x/tools/generate_compressor_data.py`.
They are editable model sources, not `.bbmodel` files or GPU screenshots.

Industrial Compressor has a single-block chassis referencing existing Alloy
Forge textures. Plate Press and Cog Press are original small cube assemblies
referencing existing Tectium texture. Dedicated machine/press pixel art remains
pending; these are not the owner's newly approved metal cog/plate art rollout.

Owner14October:2 ingots ->1 plate with reusable Plate Press;4 ingots ->1 cog
with reusable Cog Press.44 actual recipes cover21 planetary metals plus Copper.
Front is interaction-only; all other faces support combined Auto item routing
and independent item and FE controls. Crafting-table component routes removed.
No fluid input exists for this dry process. Survival crafting costs remain
deferred. Native recipe/upgrade GUI and actual conduit/tube checks passed;
client visual approval is separate.

Keep model/source copies synchronized when changing artwork. The approved
concept requires each metal's own ingot palette, centred silhouettes and C
magitech shading; never regenerate shared planet-group colours as final art.

14October candidate: generate_chassis.py adds an open press chamber, silver
reinforcement and recessed reusable dies. CompressorRenderer owns synchronized
ram/item animation; do not bake another piston into the block model. Existing
original metal/terminal textures are reused, not a new concept-identical atlas.
Approved-concept-2026-10-14.png is the visual target, not installed image art.
