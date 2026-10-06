# Cardinal inspection hub — 7 October

Minecraft Java 1.21.1 / NeoForge. Seed **0**. This is a new world, not a destructive rewrite of the old hubs.

Installed save: **ZeroG_Planet_Showcase_1_0_12_Cardinal_Hub_Seed0** (world-list name: **ZeroG Cardinal Hub 1.0.12 - Seed 0**).

| Direction | Inspection district |
| --- | --- |
| North / −Z | All 34 outgoing gates, arranged in six columns. Each destination has a protected return gate: 68 gate records total. |
| South / +Z | Twelve forming 5×5×5 apiary/alveary examples, covering all seven tiers, external genetics/cryo references, signs and 360-degree access. |
| West / −X | Thirteen supplied machine stations; actual loaded recipe materials, bee cages, catalysts and fuel in adjacent chests; charged power connections. Six tiers of separated power/item/fluid transfer lanes and filled tank bucket examples. |
| East / +X | Ten existing Concord Vault room schematics with labels. Spawners are disabled and trap dispensers empty: these are inspection structures, not implemented boss arenas. |

Spawn is at **0, 65, 0**, with daylight for inspecting Solar Array generation. Gates use explicit unlimited admin test power; they do not bypass structural validation or change survival gate costs.

## Machine and transport use

Load the provided materials manually. The **Inputs** button opens a left-side catalogue of accepted materials, with icons and alphabetical names inside tag-derived categories. Production stays in each machine's real output slots. This catalogue is not a full recipe input/output guide.

The western transfer lanes run left OUTPUT → seven pipe/conduit segments → right INPUT. Power, items and fluid are spaced four blocks apart; unused faces are disabled to prevent unintended connections. All six tiers have finite real supplies, not fake visual fills or automatic restocking. Tank examples hold actual Liquid Starlight for bucket collection. Southern shell ports remain movable around the bottom perimeter provided they face outward; controllers stay on the second wall row and the central flight space stays clear.

## Silk Weaver / Starmetal screen repair

The screenshots exposed a profile-loader boundary bug: the lower input slot ended at Y=78 but the loader allowed only Y=75, causing silent fallback to the old addon screen. The accepted boundary is now Y=80, before the Y=81 processing indicator. All 37 profile layouts pass the static bounds/non-overlap audit. Silk Weaver unused slots remain recovery-only; Starmetal's unused alloy slot remains recovery-only too. No recipe or inventory data is discarded to fix the presentation.

## Delivery safeguards

All **13 required hub gameplay tests passed** in `20261006_185803_runPlanetHubTests.log`: 34 destinations, 68 gate records, 60 nearby inspection villages, real machine production, shell formation, conserved transfer lanes, all 20 fluid buckets and workshop edit preservation. The first run's only failure was the historical 18-fluid test count; Royal/Cosmic Jelly now require 20 sources and eight non-honey buckets. The updated test still checks each bucket's actual placement, pickup and creative category.

The normal clean build passed; no isolated test classes ship. Asset audit: 7,937 models, 1,522 blockstates, 3,893 PNGs and 96 animation metadata files, zero binding errors. [Installed archived JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-cardinal-hub-guifix-20261007.jar), SHA256 `00e9ca12585863da551b7b9684e1aa6492d8c15957144cc976bfd3e1e3d06ba0`.

Old worlds are in `ZeroG/hub-archives-20261007`; old installed JAR is in `ZeroG/zerog-mod-backups/20261006-190221-UTC`. GeckoLib, Productive Bees and the Orbital Bees addon are unchanged.

Runtime commit: `6290d4cd` on `1.21.x` (hub builders, machine profile loader/presentation, tests and export/archive tools). Documentation, README, TODO ledger, archived JAR and checksums belong to `Docs`. No design artwork changed; `Design` remains unchanged.

Export follows isolated gameplay verification and excludes distant GameTest regions and fake-player data. Four specifically approved old hub worlds are moved outside `saves` to a recoverable archive only after the new world is exported and validated. Existing ZIP backups are retained. The same-version JAR replaces the installed build with an old-JAR backup; unrelated mods are unchanged.

Client GUI/rendering, real-player travel with Productive Bees and full planetary ecology still require player review. Successful isolated tests are not visual approval. Advanced biology, seven-wide shells, full recipe discovery and exact survival costs remain on the main TODO ledger.
