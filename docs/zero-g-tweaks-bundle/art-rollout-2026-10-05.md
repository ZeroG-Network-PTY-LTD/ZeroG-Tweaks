# Native art rollout — first implementation batch

This is a first native 32px implementation pass inspired by the approved A/C concepts, **not an exact extraction or a completed rollout of every concept**. Concept illustrations are not used as texture atlases.

## Implemented in this batch

- Original deterministic generators preserve 32×32 texture frames and stable registry IDs.
- Material/terrain ramps shift shadows toward cool violet and highlights toward warmer tones, while retaining material palettes.
- Matte soil clusters contain no ore/gem artwork or emissive animation metadata.
- All 34 dimensional dry/wet farmland pairs remain distinct: wet RGB brightness is checked against dry, with recognizable tilled furrows.
- Grass/flora and the 50-family botany source set are regenerated with the revised shading ramps. Existing crop shapes, visible produce growth stages, tree buds, melons and recipes are preserved rather than advertised as newly invented mechanics.
- Moonsteel first/third-person hand display rotations use the user's final X-axis 180-degree correction, without changing geometry, UVs, hand position or scale. This supersedes the earlier Z reversal.

## Not implemented by this batch

This section describes the first batch only. Subsequent work is tracked in
`../../wood-dust-art-v2/README.md`, `../../art-rollout-v3/README.md` and
`../../alveary-controller-gui-v1/README.md`: native wood/leaves and dust art,
white-icon recovery, controller terminals, a wider real controller GUI and the
single-render-path fix are now implemented there. Removing the addon's required
dependencies and re-authoring all weapon/armour atlases are still not claimed.

- The approved wood/leaves concept sheet has not yet been translated into runtime atlases.
- Weapon/armor atlas artwork has not been redrawn to reproduce the magitech concept.
- No new emissive render layers, dynamic colored lights or world-light settings are added by these shading changes. Existing luminous plants retain their existing behavior.
- The controller GUI overhaul, splicer overlap repair, addon blank icons and dependency removal remain separate unfinished work.

## Evidence

Source manifests and previews are in `docs/asset-collection-1.21.1/planet-art-refresh-v1/` and `docs/planet-botany-v2/`. They identify hashes, dimensions and native source files. Generator code is the editable source; no commercial texture-pack art is copied. Static validation and a successful build are not equivalent to verified in-game appearance; CurseForge play review is still required.
