# Buried Observatory — Concord observation room

Two original 21×11×21 partly sand-buried rooms use existing Sunbaked Stone Bricks, cracked bricks, Ruinstone, hull plating, Crystal Glass and supported Rustsand dressing. A small glass roof lens and four low observation plinths distinguish it from a shelter. Variant1 has a damaged rear roof corner. Supported exterior sand banks do not fall into the room or block its entrance.

The three-block north doorway and continuous x10 approach lead to one chest at(10,2,15), with empty lid space. Keep the existing `zerog_tweaks:chests/buried_observatory` table unchanged, including its Star Map Fragment reward. No console, new hidden planet, coordinates, dialogue, quest state or boss is invented. Approved lore says the Observatory leads to a hidden planet, but this implementation only supplies its existing fragments; coordinate discovery remains a separate approved-contract gap.

The existing dry-ground jigsaw route targets Dune Seas, Mesa Canyons and Salt Flats, with six-block terrain tolerance, nearby search32, `always_place=false`, spacing40/separation20 and independent salt19477407. This is a rare placement grid, not guaranteed density. Preserve original mine chests that already use this loot table.

Acceptance: both variants in four rotations must have one physical chest, actual Star Map Fragment loot, clear lid, approach headroom and continuous floor. Design/runtime bytes and registered biome/block references must agree. Test natural ordinary-world generation separately; leave client appearance, all habitats/seeds and full hidden-planet progression pending.

Source: `generate_buried_observatory.py`, using the original structure NBT writer and existing approved textures. No paid generation or external model import.
