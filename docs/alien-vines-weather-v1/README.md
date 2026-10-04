# Alien vines and visual atmosphere — 1.0.9 candidate

Original deterministic 32×32 transparent pixel art for 24 climbing vine blocks,
plus six edible fruit icons. `generate_assets.py` uses Minecraft 1.21.1's native
vine multipart layout and plane dimensions, with original un-tinted artwork.
No third-party resource-pack artwork is copied. Rows: Moon, Mars, Cerulon, Skarn,
Eidolon, Solvane. Columns: ordinary ivy, glowing ivy, visual-only venom ivy,
ripe fruit ivy. Native attachment, support updates, random growth and climbing
come from `VineBlock`; fruit ripening/harvesting is added without poison damage.

![Original vine palette](vine-palette-preview.png)

Regenerate with Windows Python/Pillow and `--code-root` pointing to the 1.21.x
checkout. Runtime PNG/JSON exports belong on 1.21.x; generator and source art
belong on Design. The script merges shared tags and preserves registry IDs.

The panorama edit and its exact output resolution/provenance are preserved at
`../planet-worldgen-overhaul/source/universe_v3.provenance.json`. Runtime stars
have substantially larger cores, independent slow twinkling, pastel colour
cycling and radial alpha-falloff halos. The source is still artwork, not an
in-game screenshot. GPU appearance remains for the user's play-test.

Future work, deliberately deferred: larger plant/vegetation redesigns,
strategically planned acid-rain damage/status effects, volcanic eruptions and
physical tornado simulation. Current new weather/ambient vents do no damage.
