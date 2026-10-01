# Verification — 2026-10-01

Development branch: `codex/full-collection-runtime-1.21.1`.
Minecraft 1.21.1, NeoForge 21.1.252, GeckoLib 4.9.3, Java 21.

## Completed checks

| Check | Result | Scope |
| --- | --- | --- |
| Hashed design collection | 1,381 files verified, zero errors | Copied-byte integrity and size limits, not artistic approval |
| Existing item registry names | 1,217 field/ID pairs retained | Static equipment source check |
| Server GameTests | All 11 required tests passed | Armour, tools, bonuses, layers, fences, Tidewraith lifecycle, palettes and actual egg use |
| Client asset review | Passed | Two baked models, required fly/blink/mouth clips, five base PNGs and five emissive uploads |
| Fence model definitions | Previous errors absent | Final client resource reload |
| Normal Gradle build | Passed | No opt-in GameTest or client-review classes in the jar |

Server transcript: `20261001_111431_runZeroGTests.log` (18:15 Asia/Bangkok).
Client transcript: `20261001_125538_runAssetReview.log` (19:56 Asia/Bangkok).
Normal build transcript: `20261001_125720_build.log`.
Full local logs are retained in the workspace's `outputs/ZeroG_Runtime_Local_Review_1_21_1/logs/` folder; they are not copied wholesale into this repository.

Normal jar SHA-256:

    c580d91c3e7883fe6dd49c61ddf1b25a90b9a4cee0b831aec986dc58699f85dc

The jar was built locally, not copied into CurseForge or published as a release.

## Reproduce

    gradlew.bat build
    gradlew.bat runZeroGTests -PzeroGTests -PtidewraithTests
    gradlew.bat runAssetReview -PclientReview

The opt-in game checks use separate development game directories. Client review
automatically stops its own client after reporting a pass/fail marker; check that
marker, not just the process exit code. Test sources are excluded from normal
builds. The Tidewraith exporter can be checked without writes:

    python tools/export_tidewraith_models.py

It verifies immutable source hashes and compares the existing generated runtime
files. The write flag is `--import-approved`; do not use it to bypass a new licence
or art approval decision. This project records its accepted noncanonical
Blockbench-format and unverified reference-art licence exceptions in the
[import receipt](runtime-tidewraith-import-receipt.json).

## Not yet verified or implemented

No claim of in-world visual approval, exhaustive animation/clipping checks,
multiplayer compatibility or final balance. The new HD armour geometry is not
mapped onto the worn Java renderer. Bees remain design-only here; natural mob
spawns, campaign boss phases/loot, multiblock formation and functional machine
GUIs/processing are unfinished. See the [runtime review](local-runtime-review-1.21.1.md).
