# Gallery entrance repair —14October2026

Native template path regression failed in all three showcase structures: later
tower skirt geometry overwrote basement stair headroom. Previous placement tests
proved chests/spawners existed, not that players could reach their rooms.

Generator now reapplies the authored staircase and four-block clearance after
all tower detailing. Sources-v3/exports-v3 are the new local native candidates;
loot quantities, spawner metadata and structure extents are unchanged.

Both tests pass: a static full-cube/two-block-clearance traversal reaches both
loot rooms and central gallery from the surface, and all templates retain two
chests and one hostile spawner. This approximation is not real Minecraft
pathfinding, player walking, natural placement or visual approval.

Installed JAR4212a8bf and previously exported test world still contain v2.
Do not silently rewrite player saves. A future combined delivery needs a newly
verified showcase export or explicit bounded replacement approval.
Natural biome binding, site reliability, cone vent artwork and lunar draft
approval remain separate outstanding tasks.

## Native isolated check

The dedicated zerog_gallery_clearance test passes in Minecraft1.21.1/NeoForge.
All three templates are placed in isolated Cerulon/Skarn/Eidolon fixtures. Native
collision shapes show support below all ten stair steps, three clear cells above
each of five lanes, clear chest approaches, six generated loot inventories and
three hostile spawner block entities. This is server collision/loot evidence,
not actual player walking, natural hostile populations or visual approval.
Only one required test is intentionally selected; no full hub pregen task runs.
The disposable server saved and stopped normally. Client/saves/JAR unchanged.

Later14October delivery: corrected v3 templates are now in installed JAR4fcff84a.
The previously exported world still contains already-placed v2 geometry; existing
terrain was not replaced. New template placement uses v3. Natural spawning and
client walking/appearance review remain pending.
