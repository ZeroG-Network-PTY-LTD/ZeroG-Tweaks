# Material-matched cogs and plates

![Actual native sprites, enlarged and inventory-size](images/material-matched-components.png)

This is the actual native texture correction, not a concept-only delivery.
The old generator grouped several metals under one planet palette. It now uses
each ingot's six most-used material tones, excluding shared glow inlays. All44
sprites are distinct, native32x32, with transparent borders and cog bores.
Base textures and built-in visual-refresh overrides match byte-for-byte.
Near-related metals can still look related because their ingots do; they are
not identical copies. Astrium remains the violet metal of its actual ingot,
not the gold approximation in the earlier concept sheet.

Copper is now registered as an explicit manufacturing exception. It uses
vanilla Copper ingots and adds Copper plates/cogs; there is no duplicate custom
Copper ingot. Two compressor recipes preserve the established budget:
2 ingots ->1 plate,2000FE/100ticks;2 plates ->1 cog,4000FE/160ticks. Both presses
remain reusable. Existing21-family bench/casing recipes are unchanged; no new
machine, press or Copper bench survival costs were invented.

17 isolated gameplay checks passed, including all44 actual pressing recipes,
reusable tools, blocked outputs, FE conservation, reload, real conduit/tube
transfers and existing manufacturing/casing recipes. Production clean build
passed. Asset audit:8029 models,1531 blockstates,4007 PNGs,130 animation metadata
files,88 source/layer byte bindings and zero errors. Tests do not ship in the JAR.
Native palette, alpha, padding, bore, hash and source checks passed. Installed
client inventory/held/dropped visual approval is still separate.

Same-version1.0.12-dev JAR SHA256:
`3723714696dd128a9becf2f6561ea7b662601013bc947eef5312e657eadf18eb`.
Installation/backup receipt: `reports/material-matched-components-install.json`.
Source and generator: Design/docs/manufacturing-components/. The existing native
generator is a disclosed local fallback; no paid generation, Blender/GLB package
receipt or GPU proof is claimed. Canva is an editable review copy, never the
production texture source. Terrain, hub, weather and mining progression remain
unchanged. Dedicated machine/press artwork and wider pending work remain pending.
