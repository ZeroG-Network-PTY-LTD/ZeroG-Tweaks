# Planetary residents and nearby village inspections — 1.0.8

Minecraft **Java 1.21.1**, NeoForge **21.1.252**, GeckoLib **4.9.3**, Java 21.
Six existing authored planetary species are admitted to the runtime **alongside**
ordinary villagers. Vanilla villagers, trades and clothing variants are retained.

![Authored planetary species reference sheet](images/planetary-villagers-1.0.8/overview.png)

This is the original Design reference sheet, not a new in-game screenshot.

| Home theme | Species / entity ID | Authored visual identity |
| --- | --- | --- |
| Moon, 0.5g | `zerog_tweaks:lunari` | Long legs, moon boots, pressure collar, air tank, luminous selenite crest |
| Mars, 0.7g | `zerog_tweaks:rustborn` | Dust poncho, twin-filter respirator, raised goggles |
| Cerulon, 0.9g | `zerog_tweaks:glintfolk` | Headlamp hard hat, overalls, shoulder crystals, back-mounted pick |
| Skarn, 1.2g | `zerog_tweaks:ashwright` | Broad stone body, ember details, marble mask, forge apron and pauldrons |
| Eidolon, 0.8g | `zerog_tweaks:hollow_kin` | Fur hood, salvaged hull shoulder plate, hip lantern |
| Solvane, 1.3g | `zerog_tweaks:sunwarden` | Long robe, gold mantle, sun pectoral and animated corona |

Gravity values describe the source design proportions; this update does not add
species-specific physical gravity. All other planets inherit their repository's
existing six-theme mapping rather than inventing new species assignments.

## What works in the runtime

Each species subclasses the native Minecraft villager and keeps its brain,
job-site navigation, ordinary profession trades, beds and breeding. Each has its
own entity registration and vanilla-shaped, recoloured spawn egg under **ZeroG:
Spawn Eggs**. Save data preserves species and colour style; offspring keep their
planetary species. Three original colour styles and thirteen original profession
overlays plus the unassigned appearance are composited into runtime textures.

GeckoLib plays the authored idle/walk/disagreement loops; Sunwardens additionally
play the corona rotation. Head tracking follows the native entity, and babies
use half-size rendering. Emissive source masks are retained. Ashwrights are
fire-immune; Hollow Kin do not freeze. These are not new dynamic light sources.

Each generated settlement retains **six vanilla residents** and adds **two
planetary residents**, with eight beds total. Entity construction happens only
on the server thread, not on chunk-generation workers.

## Finding layouts near the test gates

Use the fresh **ZeroG Planet Showcase 1.0.8 — Seed 0** world, seed **0**, hub spawn
**62 / 65 / 0**. It has the same 34 planetary routes and 68 active test-powered
gates. Near each planetary return gate, **one or two** inspection settlements
are selected with deterministic, planet-specific random positions and layouts,
96–384 blocks horizontally from the gate and at least 80 blocks apart.

The gate has an additional **Village inspections** coordinate sign.
`/zerog hub status` lists every prepared planet and its village positions.
After travelling to a planet, `/zerog inspection 1` (or `2`, where present)
teleports an operator into that inspection village. This command is restricted
to the opt-in test hub, not a survival progression shortcut.

Dry-land sites use solid ground and bounded slope checks, native surface/soil,
planetary masonry, wood and farmland. Ocean worlds use sealed glass inspection
habitats supported on the actual seabed, not floating platforms. Their glazing
is ordinary glass, **not Star Glass**. The village layout still uses the planet's
own construction palette and crops. Inspection habitats are not natural villages.

Ordinary-world natural villages stay rare: one candidate in each **50 × 50 chunk
region**, random offsets and at least **33 chunks** between candidate centres,
with terrain rejection making successful villages less frequent. The nearby
inspection count does not change that distribution. Previously created hub saves
have no inspection opt-in flag and are **not automatically retrofitted**.

## Limits and verification

The isolated first-generation run and a second reload run each passed all four
required NeoForge tests: all 34 return routes/inspection placements, all eighteen
liquid bucket identities and collection/category checks, crop/cave behaviour,
and native planetary villager trading/style serialization/offspring/egg checks.
Both successful servers saved all dimensions and exited normally. The failed
dry-only first candidate was not installed.

Read-only inspection of the saved entity regions found **60 inspection villages**,
**360 vanilla villagers**, and **120 planetary villagers**, with **480 unique
resident UUIDs** and persisted colour styles. Species counts: Lunari 26, Rustborn
14, Glintfolk 16, Ashwright 30, Hollow Kin 18 and Sunwarden 16. Each planet has one
or two inspection sites; reload did not create extra planetary residents.

Local transcripts: `20261003_233922_-PplanetHubTests.log` (first-generation pass),
`20261003_234643_-PplanetHubTests.log` (reload pass). The clean normal production
build passed in `20261003_234837_clean.log`; test classes are absent from the JAR.
Static checks passed 7,324 model references, 1,372 blockstates, 504 admitted
villager PNGs, 698 crop/cave PNG hashes, all eighteen bucket models and 36 liquid
animation strips, 622 preserved ecology texture payloads and 311 editable UV
projects. Saved resident counts were checked again in the exported showcase.

[Download the 1.0.8 candidate JAR](jars/zerog-tweaks-1.21.1-1.0.8-dev.jar)
 · [All preserved JAR checksums](jars/SHA256SUMS.txt)

SHA256: `1408a6ee79cf16f121820a5a7c2734ca287281e15152394bf9e7add63a8393df`.
The matching JAR is installed in the user's **ZeroG CurseForge Java instance**;
the older 1.0.7 JAR was moved into a recoverable backup outside `mods`. Dependencies,
graphics settings and existing player saves were left unchanged.

Signature planetary professions and bespoke trades from the concept sheets are
not implemented yet. Native zombification/cure is not a custom planetary-zombie
pipeline. Authored decorative crests can exceed the normal villager silhouette;
collision dimensions remain 0.6 × 1.95 blocks. Visual clipping, emissive appearance,
all-world village distribution and Iris/Sodium client rendering still need player
review. No existing player save is edited by the isolated test/export workflow.

[Editable Design source models and sheets](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Design/docs/zero-g-tweaks-bundle/blockbench/villagers)
 · [Preserved 1.0.7 crops/caves/liquids guide](crops-caves-liquids-1.0.7.md)
 · [Full planetary/gate/apiary field guide](planet-generation-1.0.6.md)
