# Industrial pressing — 12 October 2026

These canonical JSON copies match the installed code-branch machine and tooling
models. Runtime data/compiler is `1.21.x/tools/generate_compressor_data.py`.
They are editable model sources, not `.bbmodel` files or GPU screenshots.

Industrial Compressor has a single-block chassis referencing existing Alloy
Forge textures. Plate Press and Cog Press are original small cube assemblies
referencing existing Tectium texture. Dedicated machine/press pixel art remains
pending; these are not the owner's newly approved metal cog/plate art rollout.

Functionality:2 ingots ->1 plate with reusable Plate Press;2 plates ->1 cog
with reusable Cog Press.42 actual recipes cover21 existing planetary metals.
Front is interaction-only; other faces have independent item and FE controls.
No fluid input exists for this dry process. Survival crafting costs remain
deferred. Native recipe/upgrade GUI and actual conduit/tube checks passed;
client visual approval is separate.

Keep model/source copies synchronized when changing artwork. The approved
concept requires each metal's own ingot palette, centred silhouettes and C
magitech shading; never regenerate shared planet-group colours as final art.
