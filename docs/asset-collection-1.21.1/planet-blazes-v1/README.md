# Cosmic Blazes — vanilla geometry and original HD source art

Void → Moon; Nova → Solvane; Nebula → Cerulon; Void-C → Skarn;
Pulsar → Mars; Comet → Eidolon. Each species randomly chooses one of three
persistent, network-synchronized palette tones. Working vanilla-shaped eggs,
low-weight hostile natural spawns and matching coloured rod drops are included.

Original 128×64 artwork uses vanilla BlazeModel's logical 64×32 UV map.
Six head faces and all rod faces are painted; rods/eyes use emissive masks.
The twelve rods orbit and bob using the actual vanilla animation code.
Blazes retain vanilla fireballs, fire immunity and ordinary flame particles:
Comet is visually icy, not a new frost-combat AI. Void-C is a dark event-horizon
palette, not a black-hole physics system. There is no world dynamic lighting.
Rod item sprites are coloured, not custom fullbright item renderers.

18 palette projects, 42 PNGs, original reference sheet and hash manifest.
Blockbench projects are bind-pose UV/geometry studies; vanilla orbit animation
is runtime code, not an exported Blockbench clip. No extra Comet shards or
non-vanilla geometry have been added. `planet_blazes_reference.png` is an
offline UV/rod reference, not an in-game screenshot or final visual approval.

Generator: `docs/zero-g-tweaks-bundle/generators/planet_blazes.py`.
No extracted Mojang artwork, paid generation or canonical GLB certification.
Runtime belongs to 1.21.x; jar/build/test evidence belongs to Docs.
