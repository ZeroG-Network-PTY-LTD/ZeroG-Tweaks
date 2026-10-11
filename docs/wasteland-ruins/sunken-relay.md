# Sunken Relay — flooded ocean-floor ruin

Two original19×12×19 structures use existing Abyssal Stone/bricks, corroded hull, Hull Plating, Chiseled Hull, two Pulsar Lamps and waterlogged iron-bar antenna ribs. A broad three-block swimming aisle leads through the ruined room to one waterlogged chest. Equipment benches are ruined architecture, not free working machines or controllers. Damage varies at the roof/wall and antenna. All otherwise empty template cells are explicit source water, not air.

The chest keeps `zerog_tweaks:chests/sunken_relay` unchanged, including guaranteed Abyssal Pearl. No new named specimens, Broken Console, Wisp, Codex, hidden-world coordinates or dialogue. The approved side quest mentions a still-broadcasting distress signal; signal text, interaction and quest consequences remain pending. A decorative antenna does not implement a broadcast.

Placement uses a separate `zerog_tweaks:submerged_jigsaw` structure type, leaving approved dry-ground routes untouched. Ocean-floor height projection,25 bounded sample columns, water above the entire footprint/antenna, valid ocean biome and maximum6-block seabed variation. No dry-island fallback or forced natural generation. Terrain blending supplies the stone foundation; room interiors remain flooded. Candidate spacing40/separation20,salt19477409 is not a guarantee of population density.

Biomes: Deep Trenches, Kelp Jungles, Island Chains. Eligibility is independent of galaxy slot numbering; native ocean slots can find it where these biomes occur. Existing saves need unexplored chunks; do not reset owner worlds to demonstrate placement.

Acceptance: two source contracts; eight rotated placements with waterlogging, free swimming aisle, unobstructed chest lid and real Pearl loot. Separate ordinary-server audit must find a natural ocean-floor site and inspect its saved piece/chest. Client appearance, drowning/navigation balance, broad seeds/habitats and distress-signal functionality remain separate.

Generator: `generate_sunken_relay.py`, using the existing original NBT writer. No new textures or copied external assets.
