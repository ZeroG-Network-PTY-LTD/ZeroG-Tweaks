# Planetary universe and original villager attire — 1.0.6

Original design sources for the separate `1.21.x` runtime update. Existing
Blockbench collections and reference art are unchanged, not replaced or deleted.

- `source/universe_v2.png`: original ImageGen panorama, native 1774×887. Prompt,
  provenance and SHA-256 are recorded alongside it. It is not a game screenshot
  or 4K image. Runtime adds rotation/twinkling; the source PNG itself is static.
- `source/villagers/`: 24 original transparent clothing overlays, four palettes
  for each of six planet themes. Native villager face/head/nose/hat UV areas are
  transparent. Vanilla geometry and facial textures are retained by runtime.
- `generate_villager_attire.py`: reproducible design generator; optional runtime
  export goes to a separate code checkout, never merges independent branches.

The four colony layouts are generated 3D world structures in runtime, not new
Blockbench character models. Settlement interiors contain beds, native job blocks,
themed crop farms, gardens and miniature-bee hives. No Star Glass dome material.
Client visual fit and the new connected-glass shader compatibility await review.

[Current illustrated field guide](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/planet-generation-1.0.6.md)
· [Preserved full Blockbench collection](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Design/docs/asset-collection-1.21.1).
