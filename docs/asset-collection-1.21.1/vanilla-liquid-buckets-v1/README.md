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

The 1.0.7 runtime keeps these colour/family IDs and artwork intact. Creative
inventory categories are now Planetary Liquids (six buckets, existing `liquids`
tab ID) and Bee Honeys (twelve buckets, `honey_liquids` tab ID). Every family has
its own source, `flowing_` source-name counterpart, world block and `_bucket`
item. Existing palettes shared between a planet bee and a named bee do not merge
their identities. Isolated runtime tests verify all eighteen source pickup and
bucket placement paths, not just the appearance of these reference composites.

`vanilla_bucket_reference.png` is an offline preview composite referencing the
installed Minecraft art, not a captured in-game inventory. `manifest.json`
records the eighteen authored overlay hashes. Generator: vanilla_buckets.py;
run last after the other art generators to preserve this layering revision.
