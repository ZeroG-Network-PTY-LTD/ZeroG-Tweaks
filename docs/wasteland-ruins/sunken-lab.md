# Sunken Lab — chemistry and biological research ruin

Owner request: recognisable laboratory appeal, damaged power units, broken synthesis tubes, chemistry and biological equipment. Two original29×12×25 layouts use existing approved blocks/textures, with a damaged roof variant and explicit clear interior air. A low Sludgestone foundation blends into toxic-world terrain; placement stays on dry ground rather than flooding the room with damaging acid.

Zones: west chemistry benches with two empty vanilla brewing stands and two empty cauldrons; sample benches with potted mushrooms; east four coloured glass synthesis/containment chambers with solid bases, specimen plants and hull caps; rear west three dead cabinet shells, exposed iron-bar coils and a broken cable tray. One chamber has two missing glass sections per variant, and a bare tube remnant stands outside the aisle. Two existing Pulsar Lamps provide light.

Cabinets/tubes are decorative architecture, not free working ZeroG machines or FE storage. Brewing stands/cauldrons retain their normal vanilla interactions and contain no preloaded ingredients or fluids. No new machine IDs, recipes, logs, named specimens, bosses or story text. Biological props are vanilla potted mushrooms, not new research items.

A three-block service spine x13..15,z1..19 at y2/3 remains unobstructed, backed by continuous floor at y1. The north-facing chest(14,2,20) has free lid space and the unchanged `zerog_tweaks:chests/sunken_lab` table, including its Neutralizer reward. Do not invent the unwritten Lab story.

Target existing toxic wasteland Acid Swamps, Mud Flats and Moss Bogs. Bounded dry-ground jigsaw checks: terrain variation6, nearby search32, `always_place=false`; spacing40/separation20,salt19477408. This is a candidate grid, not guaranteed density. No world reset or weather/hazard changes.

Acceptance: both variants in four rotations must preserve chest/Neutralizer loot, service-spine floor/headroom, real empty vanilla apparatus, four tube bases/caps and a visible broken glass opening. Static source checks verify palette/biomes, runtime/Design bytes and no working power-machine giveaways. Natural ordinary-world placement and human visual review are separate gates.

Generator: `generate_sunken_lab.py`, original existing NBT writer. No external models or paid texture generation.
