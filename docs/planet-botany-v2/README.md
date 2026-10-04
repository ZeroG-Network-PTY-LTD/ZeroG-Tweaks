# Planet botany v2 — original art / 1.0.11 candidate

Fifty additive families: 18 flowers, 12 shrubs, 12 tree fruits, six vegetable crops and two alien melons. `manifest.json` records IDs, home themes, source hashes and 32×32 resolution. All pixels are original procedural artwork; no purchased textures or reference-image pixels were reused. `blockbench/` contains fifty editable Java-block projects with embedded textures: mature-stage crossed foliage, fruit pods and gourd geometry. These are source previews, not entity animation rigs; runtime states include the earlier growth stages too.

Existing eighteen vegetable crops retain IDs and inventory produce artwork; their four growth stages now show sprouts, blossom buds, developing produce and ripe produce. All 34 planetary short/tall grass sets receive leaf veins, directional shading and continuous two-block silhouettes. Four alien gourd families use native Minecraft stem growth.

Tree fruits use three-stage cocoa-style miniature geometry on matching custom logs. Empty-hand mature picking yields two fruits and resets the pod. Fruit items are edible and plantable. New naturally generated planetary trees can carry pods; existing trees are not retroactively populated, and sapling-grown trees can be populated manually with fruit items.

Preview PNGs and `budding-growth.gif` show source artwork, not an in-game render or automatic texture animation. Runtime crops change texture as their growth state changes. Native crossed planes are used for grass, flowers, shrubs and crops. No new venom or acid damage is introduced.

Regenerate from the Design branch with `python3 docs/planet-botany-v2/generate.py --code /absolute/path/to/1.21.x-checkout`. This intentionally updates runtime art/data in that separate checkout while retaining historical Design archives. The built-in visual repair pack is updated for matching overridden textures too.

Build success is not GPU visual verification. Seven isolated server checks and eight packaged-asset audits passed for this candidate. It is published separately on 1.21.x (runtime code/data), Design (these sources) and Docs (player guide, previews, downloadable JAR and checksum). Publication does not install it or modify existing worlds.
