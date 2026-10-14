# Approved planetary structure revision

Owner confirmed both replacement with planet-matched ZeroG blocks and the
handover bounding dimensions on 14 October 2026. This is authorization for
a new revision, not approval of the existing Kimi geometry as concept-identical.

| Structure | Planet | Target width × length × height | Underground depth |
| --- | --- | --- | --- |
| Overgrown bio-habitat | Cerulon | 48 × 48 × 52 | 16 |
| Crimson monolith | Skarn | 48 × 48 × 56 | 20 |
| Cryogenic outpost | Eidolon | 54 × 54 × 50 | 14 |

Use ZeroG architectural, soil, grass, stone, vegetation and lighting palettes
appropriate to each planet. Vanilla material names in the supplied handover
are appearance references, not a required construction palette. Retain air
for passages and functional containers/spawners where no custom equivalent
exists; do not replace them with decorative solid blocks.

Preserve the concepts' silhouettes, curved bridges/rings, spires, chambers
and subterranean routes. Rebuild geometry rather than simply scaling every
voxel: scaling can collapse corridors, stairs and block-entity positions.
Entrances must be accessible from local terrain. Foundations must reach
ground/seabed; no detached platforms. No dimension gates in loot structures.
Provide explorable interiors, loot rooms and hostile-mob space.

## Measured source baseline (not completed revision)

All three existing Kimi templates declare 49 × 64 × 49. Their non-air counts
are 12,843 (water), 12,215 (hot) and 14,061 (ice). Serialized entries include
3,727 air cells per template and must not be described as material counts.
The handover totals 28,450 / 31,600 / 34,200 remain estimates, not measured
requirements or block quotas. Do not fill playable rooms to match those totals.

## Delivery checks still required

- Resolve and validate each replacement block ID and its state properties.
- Produce revised editable sources and actual-template exterior/cutaway images.
- Validate target bounds, accessible rooms, stairs, loot and mob areas.
- Update placement origins, entrance anchors and tests for the revised geometry.
- Run isolated native-world grounding, travel and loot checks, then build.
- Install a same-version JAR and inspected sites only after checks pass.
- Publish separate code, Design and Docs commits with verified receipts.

Current source templates and installed JAR are unchanged by this approval note.
