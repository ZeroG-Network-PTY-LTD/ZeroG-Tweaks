# Verification — 2026-10-01

Current development branch: `1.21.x`; art: `Design`; documentation: `Docs`.
Minecraft 1.21.1, NeoForge 21.1.252, GeckoLib 4.9.3, Java 21.

## Latest branch-separated publication

Fresh post-rebase normal build passed on `1.21.x`: `20261001_173530_build.log`
(00:35 Asia/Bangkok, 2026-10-02). No Minecraft client was launched for this
publication. The jar contains the multiblock guide and no opt-in test classes.
Its development-candidate SHA-256 is:

    ed04d196683fbd3dc600ba0c14a6dcff19f7d4fccba30c8a31727b33093b9cb6

All 1,381 original design roster entries are hash-verified across the branches;
six archived Java drafts now belong to code/tools rather than Design/docs.
Six guide/test files match the approved local change; newer upstream runtime
code is retained. The relocated Tidewraith exporter plans against the separate
code checkout with zero semantic resource collisions, retaining nine JSON files'
existing formatting when parsed contents are identical. It still refuses changed
geometry, animations or PNGs. No runtime artwork was overwritten.
The latest upstream code contained a fern VoxelShape.move(Vec3) API mismatch;
the one-call correction passes x/y/z, preserving the same offset.
See [exact file inventory](branch-file-inventory.json) and
[branch publication record](branch-publication.md).

The latest previously completed server run passed **12** tests, including
eight-layout/944-cell guide integrity: `20261001_163525_runZeroGTests.log`.
Client review passed **32** guide rotation/layer poses plus Tidewraith asset
uploads: `20261001_163759_runAssetReview.log`. These were isolated Java/NeoForge
checks, not CurseForge modpack or human pixel approval. They were not rerun or
represented as new tests during this publication. The integrated code branch received an
additional normal build; the earlier evidence below is retained for provenance.

Jar/checksum live under Docs/docs/jars. No CurseForge installation, official
release, world changes or finished Bees/machine gameplay is claimed.

## Earlier completed checks — historical mixed snapshot

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

    python generators/export_tidewraith_models.py --code-root ../zerog-code-1.21.x

Run that command from a separate Design checkout. It verifies source hashes and compares the existing generated runtime
files. The write flag is `--import-approved`; do not use it to bypass a new licence
or art approval decision; import also requires --receipt pointing into Docs.
This project records its accepted noncanonical
Blockbench-format and unverified reference-art licence exceptions in the
[import receipt](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/runtime-tidewraith-import-receipt.json).

## Not yet verified or implemented

No claim of in-world visual approval, exhaustive animation/clipping checks,
multiplayer compatibility or final balance. The new HD armour geometry is not
mapped onto the worn Java renderer. Bees remain design-only here; natural mob
spawns, campaign boss phases/loot, multiblock formation and functional machine
GUIs/processing are unfinished. See the [runtime review](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/local-runtime-review-1.21.1.md).
