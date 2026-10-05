# ZeroG Tweaks — Minecraft 1.21.x development

## Current same-version extension: storage and correctness first

Original wood joinery, 27/54-slot chests/barrels, six fluid tanks (5,000–5,000,000 mB),
independent generator modules and sunless crop repairs are tracked in the
[machinery workflow](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/storage-and-machinery-workflow.md).
The new player direction restores vanilla Netherite-style worn armour proportions,
cohesive orbital honeycombs, purpose-correct machine screens and explicit Alveary
power/item/fluid service substitutions. No Mekanism code/art or new dependency is bundled.
[Original editable art](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Design/docs/storage-joinery-v1) ·
[Tracked outstanding work](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/storage-and-machinery-todo.json).
Existing historical guides remain below; current corrections supersede older renderer claims.

NeoForge **1.21.1**, Java **21**, GeckoLib **4.9.3**. This is an unfinished
development build, not a shipped release or proof of modpack compatibility.

Current candidate: **1.0.12-dev**. The current implementation and evidence are
listed in the [Sol workflow ledger](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/sol-build-workflow-2026-10-05.md)
and [machine/transport controls](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/sol-machines-and-transport-runtime.md).
See the [native artwork gallery](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/images/full-art-rollout-v4/README.md)
and [editable sprite/generator sources](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Design/docs/full-art-rollout-v4).

Historical additions retained in the candidate include Cerulon terrain/mob work,
four amethyst-style budding crystal families, animated light-12 Star Glass,
six planet Star Sands and updated crystal/ingot/raw-metal artwork.
See the [illustrated update and installation guide](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/crystal-material-update-1.21.1.md).
The [dimension ecology guide](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/dimension-ecology-1.21.1.md)
covers 34 soil/farming/grass/sand families, five additional dimensional fluids
and pools, glowing vegetation/bugs, gas vents and daily impact remnants.
**Daily impacts excavate terrain by default. Back up saves; disable
`dailyImpacts` in `config/zerog_tweaks-common.toml` if unwanted.**

- [Full illustrated documentation and descriptions](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/README.md)
- [Armour, Bees, materials, mobs, eggs and drops gallery](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/current-collection-guide-1.21.1.md)
- [Blockbench design collection](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Design/docs/asset-collection-1.21.1)
- [Multiblock controls and limits](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/multiblock-reference-guide.md)
- [Build and test evidence](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/verification-1.21.1.md)
- [Development jar and SHA-256](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Docs/docs/jars)

Implemented: 80 functional armour pieces, 100 tools, eight partial full-set
bonuses, approved regular/boss Tidewraith pair, deposit/fence repairs, and a
G-key guide for eight apiary structures: layers from Y=0, rotatable views,
coordinates and quantities. Genetics/cryo are separate external modules.

New vanilla-rig creatures: twelve half-size bee families with animated wing
textures, hives, combs, bottled/bucket honey and planet nests; six cosmic Blaze
types with three persistent palettes each, emissive rods/eyes and matching rod
drops. See the [bee/Blaze guide](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Docs/docs/planet-bees-and-blazes-1.21.1.md).
Isolated server checks: 52 passed, including all planet soils and existing saplings. Client visuals and modpack compatibility
remain unverified; these are not claims of final visual approval.

Remaining limits: client visual approval, unsupported bee lifespan/tolerance and
module rules, full PB flower/territory parity, moving transport cargo renderer,
third-party claim/team adapters, some creature abilities and separate shorn-Yak
artwork. Real genetics, 27-frame progression and six-tier transport are now
implemented; the linked current ledger supersedes older milestone descriptions.

Build: `./gradlew build` (Windows: `gradlew.bat build`). Optional server tests:
`gradlew.bat runZeroGTests -PzeroGTests -PtidewraithTests`. Optional client review:
`gradlew.bat runAssetReview -PclientReview`. These launch isolated Java development
instances, not the user's CurseForge modpack. Test sources are excluded from
normal jars. Do not launch game tests without current user direction.

The coordinated workflow also provides `runWorkflowTests -PworkflowTests`,
`runGeneticsTests -PgeneticsTests` and `runPlanetHubTests -PplanetHubTests`.
Use the normal build without any test properties for a distributable JAR.

Branch ownership: code/build/runtime resources on `1.21.x`; art and generators
on `Design`; documentation/images/jars on `Docs`; shipped code only on `Released`.
Never merge Design/Docs histories into code or vice versa. Never commit directly
to Released, force-push, or delete branches/tags.
