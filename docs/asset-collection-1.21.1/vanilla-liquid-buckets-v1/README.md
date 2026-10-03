# Exact vanilla bucket base, liquid-only overlays

All eighteen liquid buckets use `minecraft:item/water_bucket` as generated
item layer0, with an original liquid-only overlay in layer1. This retains the
actual vanilla silhouette, handle/rim, metal body, highlights and transparent
background. The overlay covers exactly the pixels where the installed water
bucket differs from the empty bucket; unchanged metal pixels are asserted
identical after compositing. No standalone Mojang base PNG is bundled.

This supersedes the earlier independently painted bucket icons retained in
the ecology and bee studies. Runtime textures and models, not those historical
study icons, are authoritative. Includes Starlight, five new dimensional liquids
and all twelve hive-family honeys. Item sprites are not full 3D cubes.

`vanilla_bucket_reference.png` is an offline preview composite referencing the
installed Minecraft art, not a captured in-game inventory. `manifest.json`
records the eighteen authored overlay hashes. Generator: vanilla_buckets.py;
run last after the other art generators to preserve this layering revision.
