# Approved Tidewraith pair · Minecraft 1.21.1

User decisions (2026-10-01): the repaired **two-eye face is the regular mob**;
the other **voxel-built oval manta-mouth model is the boss**. The boss keeps
its current authored size, not six times player height. Both must be spawnable.

| Runtime ID | Approved editable source | Role and dimensions |
| --- | --- | --- |
| `zerog_tweaks:tidewraith` | [two-eye Abyssal face](../shattered-skies/abyssal-face-repair/tidewraith_abyssal_concept_face.bbmodel) | Regular; 265 parts; 4096×4096 atlas; authored 68-unit / 4.25-block wingspan |
| `zerog_tweaks:tidewraith_boss` | [voxel manta-mouth](../shattered-skies/tidewraith-concept/tidewraith_concept.bbmodel) | Boss; 4,090 parts; 32×32 atlas; authored 80-unit / 5-block wingspan |

[HTML gallery](review.html) · [model-stack backup](approved-models-backup.zip)
· [backup hash receipt](backup-receipt.json). Source snapshots and their closed
hash manifests are preserved byte-for-byte. `_scaled` models in the historical
backup are companion studies, **not** the boss runtime model. The paired
non-boss head join and corrected mouth motion are retained; no geometry is
substituted by an old model or auto-scaled. Software reviews are not game captures.

## Runtime draft — not enabled by this data-only commit

The source described below is archived in [runtime-draft](runtime-draft/README.md),
with the integration patch and opt-in server tests. It is not installed in this
commit's `src/`, and this commit does not add working spawn eggs to the shipped
jar. It compiled locally and passed three server tests; client art remains
unverified and runtime import is pending the named approval.

- Two real entity registrations in `EntityInit`, attributes, client renderers
  and vanilla `DeferredSpawnEggItem` eggs. Both eggs appear in **ZeroG: Spawn
  Eggs**, plus the existing main tab.
- `Tidewraith` uses no-gravity flight, bounded wandering, visible-player chase
  and basic contact attacks. A server-driven blink controls the authored eyes;
  successful attacks trigger the authored mouth opening. Gentle authored wing,
  wing-tip and tail/tendril keyframes loop through GeckoLib.
- Boss is persistent, has a tracking-player boss bar, and preserves a clamped
  `Variant` value in saved data: 0 Standard, 1 Abyssal, 2 Pearl, 3 Storm.
- Renderers use the supplied atlases and alpha-aware emissive glow masks at
  **scale 1.0**. Glow is emissive surface rendering, not dynamic world lighting
  or a implemented particle aura. The regular model's mask is face-only.
- Initial test balance: regular 30 HP / 4 damage; boss 180 HP / 8 damage.
  These are provisional test defaults, not approved final campaign balance.
  No natural spawning, new drop tables, arenas, Void Pull, Splinter Volley,
  telegraph AoE, or game progression rewards are added by this pass.

## Test in an isolated world

Requires **Minecraft 1.21.1, NeoForge 21.1.252, Java 21 and GeckoLib 4.9.3**.
These commands apply **after** the runtime draft is integrated and its approved
assets imported. They do not work against the unchanged release jar from this
data-only commit. Do not replace your installed release until client verification
is recorded.

```mcfunction
/summon zerog_tweaks:tidewraith ~ ~3 ~
/summon zerog_tweaks:tidewraith_boss ~ ~3 ~
/summon zerog_tweaks:tidewraith_boss ~ ~3 ~ {Variant:1}
/summon zerog_tweaks:tidewraith_boss ~ ~3 ~ {Variant:2}
/summon zerog_tweaks:tidewraith_boss ~ ~3 ~ {Variant:3}
/give @s zerog_tweaks:tidewraith_spawn_egg
/give @s zerog_tweaks:tidewraith_boss_spawn_egg
```

Confirm front-facing eyes, thin dark teeth on the regular face, closed head
join, eight blinking boss eyes, attached boss mouth teeth during attack, soft
wing motion, all four boss palettes, boss-bar health updates, and save/reload.
Test at night and in a bright area to check emissive selection and transparency.

## Reproduce and verify

```sh
python3 docs/zero-g-tweaks-bundle/generators/export_approved_tidewraiths.py --backup-only
# Runtime export requires the named project-specific import exception/approval.
python3 docs/zero-g-tweaks-bundle/generators/export_approved_tidewraiths.py
cd docs/zero-g-tweaks-bundle/generators
python3 -m unittest test_tidewraith_abyssal_face test_tidewraith_concept test_approved_tidewraiths
```

The runtime exporter follows [Blockbench's Bedrock codec](https://github.com/JannisX11/blockbench/blob/master/js/formats/bedrock/bedrock.js)
and its animation coordinate signs, rather than assuming authoring-space cube
coordinates are already engine exports. JSON/PNG files are generated from the
approved `.bbmodel` snapshots. No paid provider calls.

```sh
python3 docs/zero-g-tweaks-bundle/generators/build_tidewraith_test_structure.py
./gradlew runTidewraithTests -PtidewraithTests
./gradlew build
./gradlew runClient
```

The source and scene for GameTests are in the runtime-draft archive. Once
integrated, they are opt-in and excluded from normal jars.
Server tests do **not** prove client rendering, emissive output or visual
fidelity. Runtime controllers follow the [GeckoLib 4 entity guidance](https://github.com/bernie-g/geckolib/wiki/Geckolib-Entities-(Geckolib4)).

## Admission and evidence

The `game-dev` packaging route supports GLB, not this project's Bedrock
geometry/Blockbench files. This update uses project-specific hash/geometry/
texture/animation checks if explicitly accepted; it is **not canonical
game-dev package certification**. User-supplied reference art's licence is not
independently verified; no new rights are asserted. See `verification.json` for
actual results and any outstanding gate. Do not substitute a hash check for
native import, GPU rendering, playtesting or artistic approval.
