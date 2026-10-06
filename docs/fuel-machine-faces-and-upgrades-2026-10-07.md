# Fuel, machine faces and upgrade contracts

Minecraft 1.21.1 / NeoForge. This update retains **1.0.12-dev**, all existing inventories, recipes, fuel rates, saves and hub terrain. Server verification does not substitute for client GUI approval.

## Routing controls

The colour-coded matrix uses world directions: D/U/N/S/W/E. Input is red, Output green, Both purple and Off grey. Clicking a face sends a vanilla menu-button request; the server checks the actual machine, player world and distance. Empty diagram cells never send commands. Modes are independent for each resource family.

| Machine | Items | Energy | Fluids |
| --- | --- | --- | --- |
| Solar Array | None | Output / Off | None |
| Fusion Reactor | Fuel Input / Off; Fusion Dust only | Output / Off | None |
| Combustion Generator | Fuel Input / Off; existing wood/coal/mineral filters | Output / Off | None |
| Forge, Refinery, Growth Chamber, Salvage Station | Auto / Input / Catalyst / Output / Off | Input / Off | None |
| Geno Station, Genetic Splicer | Both / Input / Output / Off; existing specimen/reagent filters | Input / Off | Both / Fill / Drain / Off |
| Ordinary Centrifuge, Starmetal Smelter | Both / Input / Output / Off | Input / Off | None |
| Stardust Smelter, Silk Weaver, frame assemblers and infusion machines | Both / Input / Output / Off | No invented power capability | No invented tank |

Fusion preserves the old top-only fuel default. Combustion preserves fuel and energy availability on all faces. Older machine item/tank defaults remain Both; existing power receivers default to Input. Default legacy recovery remains available. Explicit Output exposes only product/recovery output slots, while Input cannot extract reserved materials. Inputs still follow the installed addon's verified `mayPlaceIn` contract, including unused take-only recovery slots.

Fuel and power panels sit beside the generator inventory. Genetics and legacy menus gain a separate right-hand face panel, without moving the original operating/player slots. Their accepted-input catalogues remain on the opposite side. Resource buttons only appear for supported capabilities. Standard menu data synchronizes the selected modes; clients cannot supply gene values, energy or tank contents.

Changing a face invalidates its cached external handlers. Disable/re-enable does not revive those handlers. Changing fuel permissions does not disable energy output. Changing tank access does not stop an already funded genetics job from consuming its own internal catalyst. Settings survive saves/reloads. No new gas family or unit is invented in this update.

The installed NeoForge hopper hook falls back to vanilla container insertion when capability insertion fails. An inert capability alone is therefore insufficient for the older addon containers. Their vanilla sided-container methods now apply the same filters and face modes, blocking this second route as well. The real-hopper regression reproduced the bypass before this guard was added.

## Upgrade compatibility

| Family | Accepted upgrades | Bounds and actual effect |
| --- | --- | --- |
| Forge, Refinery, Growth Chamber, Salvage | One Cyrrium/Tectium/Wraithsteel/Astrium casing; one Cryo Core; one Pulsar/Tremor/Spectral/Fusion Dust in the corresponding sockets | Casing tiers add 0.25x speed each and reduce job FE by 5% each. A valid Cryo Core adds 0.5x speed. Dust tiers reduce job FE by 5% each. Maximum 2.5x speed, 40% FE saving; duration rounds up and job FE never becomes zero. |
| Solar, Fusion, Combustion | Generator Flux Module | Maximum three. Each adds 25% configured generation and one base buffer increment; maximum 1.75x output and 4x capacity. Solar sky/weather restrictions and fuel conservation remain in force. |
| Genetics and older addon processing machines | No supported upgrade sockets | Specimens, trait serums, jelly, recipe flux and fuel are reagents, not upgrades. The menu explicitly identifies the absence of supported upgrades. New legacy upgrade effects require approved contracts before implementation. |
| Storage and transport | Existing family-specific contracts | This batch does not reinterpret storage-expansion modules as processing upgrades or change tier capacities/rates. |

An invalid old cooling-slot item previously granted the same speed bonus as a Cryo Core. It now grants **no bonus** and remains recoverable; migration never deletes it. Operating upgrade slots reject mismatched/stacked upgrades, and pipes cannot insert remote processor upgrades. Job configuration changes still reset paid progress rather than producing free outputs.

## Verification and remaining work

Tests exercise real menu buttons and item/energy/fluid capabilities, simulation versus execution, all six faces, input/output restrictions, stale handlers, forged/remote requests, saved masks and actual hopper transfer. Existing processing tests verify exact upgraded job time/cost, output blocking and reusable catalysts. Isolated worlds only; no client launch or save reset.

Final server evidence: **76 workflow + 4 genetics-job + 2 optional-addon-absent tests passed**. Workflow log `20261006_212342_runWorkflowTests.log`; genetics logs `20261006_212520_runGeneticsTests.log` and `20261006_212713_runGeneticsTests.log`. Earlier red checkpoints reproduced missing fuel/item/power commands, the invalid cooling bonus and the vanilla hopper bypass. A test initially addressed the wrong fluid face; its command mapping was corrected before the final passing run. These are server results, not rendered GUI screenshots.

Installation/build/asset evidence is retained in [the delivery receipt](fuel-machine-faces-delivery-2026-10-07.json); its same-version JAR archive and checksums preserve the previous deliveries.

Installed JAR SHA256: `c55d00ae75e222fec34831a11cfa9ff261f9a725300d7641ccd7b5692afe4a93`.
The predecessor is recoverably backed up under `ZeroG/zerog-mod-backups/20261006-212944-UTC/`.
The clean production JAR contains no GameTest classes. Asset audit: 7,937 models,
1,522 blockstates, 3,893 PNGs and 96 animation metadata files, zero errors. All 27
archived JAR checksums were regenerated without deleting previous releases or images.

Client approval remains required for matrix clicks, small-screen GUI scale, both inventory/catalogue sides and placed routing. Broader legacy upgrade effects are deliberately pending approved specifications. Transport waves/pulses, real gas definitions, advanced alveary research/biology, progression/ecology audit and exact survival costs remain separate TODO items.

Runtime belongs on [1.21.x](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/1.21.x); guides, test receipts and JAR/checksums belong on [Docs](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Docs). No design artwork changes or unrelated-history merges are required for this batch.
