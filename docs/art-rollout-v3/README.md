# Approved A/C art workflow — 5 October 2026

This is a native Minecraft Java 1.21.1 PNG/JSON and Blockbench source rollout,
not a generated concept-sheet atlas or a claim of in-game visual approval.
Equipment/materials use C's cool hue-shifted shadows and selective accents;
vegetation retains A's natural volume with restrained C highlights.
Soil and farmland remain matte and mineral-free, with darker wet furrows.

## First rollout

| Work | Source and coverage |
| --- | --- |
| Orbital Bees white inventory icons | Recover 63 coloured default layers from editable bee projects; ship normal resources and the built-in pack. Two already-coloured addon layers remain unchanged. |
| Existing foods and mob drops | 84 original food/material/reward sprites from the existing catalogue, with hue-shifted shading. Existing masks and registered IDs retained. |
| Material inventory art | 86 ingot, nugget, raw-material, gem and orb sprites; visible top/side volume instead of flat bars and solid prototype cubes. |
| Controller terminals | Seven tier controller faces, APIARY controller and genetic-splicer terminal. Existing baked geometry retained; seven tier faces follow the existing blockstate rotations. |
| Cave berries and vine fruit | 34 cave-berry and six vine-fruit icons; clustered produce instead of flat repeated blobs. Existing family palettes retained. |
| Dripstone | 34 complete cave families: rock block, ten up/down shapes and the inventory stalactite. Natural irregular rock patterns and tapered silhouettes. |
| Melons and pumpkin | Nebula, Aurora and Solar melons, plus Eclipse pumpkin: side/top rind, rib and stem detail. No new registry IDs. |
| Vents | Six planetary gas vents plus flare-vent side/top and vent rock; both ordinary and ambient vent items inherit these placed-block models. |
| Torch blossoms | Ember Torchflower now has flared petals, a layered calyx and visible stamens, generated with the other botanical families. |
| Editable models | Nine controller projects, native flat item review projects and updated active melon project textures. Runtime generated-item models stay unchanged. |

The coloured screen art helps identify the interaction face. Its painted lamps
are not a claim that status, processing, emitted light or animation are wired.
The accompanying compatibility GUI is documented in
`../alveary-controller-gui-v1/README.md`: nine real menus get the compact reference
reference layout with paged outputs, server-synced progress/formation and guarded output sorting. Reserved
backend systems remain sealed. The renderer now only draws a full GeckoLib model
for ENTITYBLOCK_ANIMATED blocks, avoiding a second model on top of baked machines.
These are code/UI changes in addition to the terminal artwork, not texture-only fixes.

## Reproduce without losing the source-of-truth order

From the Design checkout, use the separate 1.21.x checkout for `--code` and the
installed Orbital Bees JAR for `--bee-jar`:

1. `docs/zero-g-tweaks-bundle/generators/inventory_texture_refresh.py`
2. `docs/planet-botany-v2/generate.py`
3. `docs/wood-dust-art-v2/generate.py`
4. `docs/art-rollout-v3/generate.py`
5. `docs/art-rollout-v3/audit.py`

Do not regenerate resources while Gradle is copying them. Build the production
JAR afterward and check its contents, not just loose files. Preserve the current
1.0.12-dev version for these visual fixes. Moonsteel's X-axis correction is not
changed by this artwork workflow.

## Priority fix: white icons

The saved client resource order was `vanilla`, the refresh pack, then
`mod_resources`. The original addon contained 63 pure-white default PNGs, while
the coloured recovery artwork existed only in the lower-priority pack.
The deterministic resource-resolution check reproduced 63 failures. Shipping
the same recovery artwork as ordinary ZeroG resources as well as pack resources
now preserves colour in that observed order. This does not edit the player's
options, replace the standalone bee addon, or remove its items/dependencies.

`validate_apiary_visible_art.py` tests the specific white-asset symptom;
`validate_art_rollout_v3.py` checks source/runtime/pack/JAR identity, terminal
bindings, controller rotations, editable sources and transparency. GPU/shader
appearance and actual machine interaction still need client review.

## Continue the audit

`item-model-audit.json` and `review-queue.html` record all scanned ZeroG item-model
bindings. The counts are model files, not registered items. A legacy resolution
or a texture outside the current audited sources is a **review flag**, not proof
that an image is broken or stylistically wrong. Review remaining gear sets,
flower/plant families, bee components and old machine panels against the approved
reference before calling the whole pack complete. Preserve all existing IDs.

Source previews are `controller-terminals-preview.png`,
`material-sprites-preview.png` and `environment-preview.png`. They are original
texture contact sheets, not game captures or evidence of dynamic glow.
