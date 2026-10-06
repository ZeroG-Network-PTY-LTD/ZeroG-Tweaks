# Supplied machine workshop — 7 October 2026

Minecraft Java 1.21.1 / NeoForge; version stays **1.0.12-dev**.

## Open the new copy, not the original

In the ZeroG CurseForge instance, select **ZeroG Supplied Workshop 1.0.12 — Seed 0**.
Its folder is `ZeroG_Planet_Showcase_1_0_12_Supplied_Workshop_Seed0`.
Follow the **WEST: WORKSHOP** sign near the hub. The first station is at
**−100, 64, −20**. If your preserved player was last in another dimension,
return through its hub gate, or use
`/execute in minecraft:overworld run tp @s -88 65 -5`.

The existing ServicePorts save is unchanged. This is a copy of that save, not a
replacement seed or regenerated dimensions. Player data, the 34 planetary
destinations, 68 gate records, original apiary exhibits and ten Vault rooms remain.
Only the western workshop block region and its once-only marker are added; distant
GameTest regions are not imported. The new copy starts in daylight for solar testing.

## Station layout and supplies

All machine fronts face south. Four separated chests to the right hold test supplies.
These are **admin inspection stocks**, not new survival crafting recipes. Load the
machine manually so you can inspect its input filters, controls and products.
Do not put spare casing/cryo/dust upgrades into ordinary reagent slots.

| Machine | Position (X, Y, Z) | Operating supplies / requirement |
| --- | --- | --- |
| Ore Refinery | −100, 64, −20 | Loaded refining-recipe ingredients, catalysts and spare upgrades |
| Alloy Forge | −76, 64, −20 | Loaded alloy ingredients and catalysts, with spare upgrades |
| Crystal Growth Chamber | −52, 64, −20 | Real recipe seeds/feed, including reusable seeds |
| Salvage Station | −28, 64, −20 | Actual salvage inputs, not generic coal |
| Combustion Generator | −100, 64, −46 | Coal and oak logs |
| Solar Array | −76, 64, −46 | Daylight and unobstructed sky; no invented fuel |
| Fusion Reactor | −52, 64, −46 | Fusion Dust |
| Geno Station | −28, 64, −46 | Filled Productive Bees iron-bee cage, vials and honey bottles |
| Genetic Splicer | −100, 64, −72 | Analysed cage, component-bearing trait serum, jelly items/buckets |
| Centrifuge | −76, 64, −72 | Ingredients accepted by the installed addon contract |
| Starmetal Smelter | −52, 64, −72 | Ingredients accepted by its actual input-slot contract |
| Silk Weaver | −28, 64, −72 | Valid thread inputs; ignored pattern slots are not advertised as inputs |
| Frame Infusion Altar | −100, 64, −98 | Valid frame/reagent inputs from the installed addon filter |
| Alveary service supplies | −76, 64, −98 | Bees, frames, starlight/honey/jelly buckets, ports and six-tier lines/cells/tanks |

The four core processing kits are generated from **loaded recipe ingredients**,
including count requirements and catalysts. They are not a separate hardcoded recipe
table. Addon supplies are filtered against the installed machine API. Genetics cages
carry verified Productive Bees attributes; they are not empty cages or fictional alleles.
Use the Geno Station controls to analyse/sample, and the Splicer controls to request
a job. Its supplied productivity serum is a valid example, not a promise that applying
the same allele already held by a bee will improve it.

Processing/genetics stations have charged Astrium cells connected by real conduits.
Generator stations instead lead to **empty input-configured cells**, so output storage
is available. The existing northern alveary shells retain their charged external cells.
Load bees and frames into the tier's supported slots; advanced biology/research rules
still have the limitations listed in the live TODO ledger.

For another explicit test hub, an operator can run `/zerog hub workshop`. It rejects
ordinary survival worlds and occupied plots. It is **not automatically run when old
hubs open**. Its persisted marker prevents rebuilding/refilling used supplies or
overwriting player changes. Workshop chunks are kept loaded only in this test hub.

## Verification and limits

Five required isolated checks passed in `20261006_171606_runPlanetHubTests.log`:

- Refinery accepts supplied ore, processes through its registered block ticker and
  real cell/conduit capabilities; a repeated workshop command preserves edited stock.
- Forge, crystal growth and salvage complete examples using supplied recipe materials
  and their registered machine/cable/cell tickers, without injecting machine FE.
- Genetics supplies contain real filled cages and valid serum/catalyst components.
- Alveary service stocks contain accepted bees/frames and a Starlight bucket.
- Existing shell/room exhibits and smoker checks pass. Older hub display order is
  validated by each placed controller's actual tier, not today's guide-list position.

The first red checkpoint found the absent supplied workshop. Further checks found
the missing alveary service kit before it was added. Registered tickers are explicitly
stepped in the machine-operation checks; this is not a claim that unattended distant
world ticking, client GUI appearance, shaders or every addon recipe were play-tested.
The player's in-game inspection remains the next approval boundary.

Clean production build passed. Asset audit: **7,937 models, 1,522 blockstates,
3,893 PNGs, 96 animation metadata files, zero errors**. Test classes/fixtures do not
ship. The installed JAR hash is
`cc3bc6aedee20d36f52557c20e0ae9508a29752c0ed6ff2357e85498df384610`.
The previous JAR is backed up under `zerog-mod-backups/20261006-172119-UTC`.
See the [installation receipt](supplied-workshop-install-2026-10-07.json) and
[original-save preservation receipt](supplied-workshop-export-2026-10-07.json).

## Next: recipe balance, hardest to easiest

**No survival costs changed in this delivery.** First inspect these stations, then
work backward from the hardest late-story equipment, high-tier alvearies/storage and
gate upgrades toward the early Moon/Mars and Overworld equipment. For each recipe,
agree the ingredient IDs/counts, unlock milestone, catalyst/remainder behavior and
whether its resources are obtainable before that point in the Concord storyline.
Do not implement placeholder costs while exact costs remain pending.

Gas identities/units, energy pulses/fluid waves, remaining machine-side controls,
advanced alveary rules, recipe discovery and wider progression/ecology audits remain
tracked separately in [the live TODO ledger](storage-and-machinery-todo.json).
