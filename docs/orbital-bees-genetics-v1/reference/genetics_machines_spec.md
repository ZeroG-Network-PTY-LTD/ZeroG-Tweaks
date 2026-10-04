# Orbital-Bees genetics: Genetic Splicer and Geno Station (redesign)

Mod: ZeroG Orbital-Bees (`aeroapiary`), Productive Bees add-on. Block ids stay `aeroapiary:genetic_splicer` and `aeroapiary:geno_station`.

## What exists today (found in the repo)

- Shipped in `zerog-binnie-expansion-1.21.1-1.0.0.jar` (on `Docs`); design sources in `Design` `docs/asset-collection-1.21.1/bees/` and `docs/art-rollout-v3/`.
- Old models: Splicer = 12-cube grey cabinet with a 3-rung helix hidden inside; Geno Station = 15-cube console with a cyan screen. Textures are flat swatches.
- **Old behaviour is placeholder** (from `ZeroGMachines`):
  - Genetic Splicer: slots accept queen (0), drone (1), frame (2), but `tick` runs `processTwo(0, 1, 3, frameInfusionRecipe)`.
  - Geno Station: slot 0 accepts combs only, and `tick` runs `processTwo(0, 0, 1, stardustSmelterRecipe)`.
  - Neither touches genes. The redesign below gives both a real job.

## The genetics loop

1. **Geno Station (read and sample):** put in a bee and a blank Serum Vial; it analyses the bee and draws one chosen trait into the vial, giving a **Trait Serum** that names the trait and value (e.g. "Speed: Fast").
2. **Genetic Splicer (write):** put in a queen or princess and a Trait Serum; it writes that trait into both chromosomes of the bee.

This is the Gendustry sampler/imprinter idea (Binnie isolator/inoculator in the old packs), kept to two blocks.

## Geno Station

| Slot | Index | Accepts | Notes |
| --- | --- | --- | --- |
| Specimen | 0 | any Productive Bees bee item (queen, princess, drone) | Returned to slot 3 after analysis, unless sampling consumes it |
| Blank vial | 1 | `serum_vial` | One per sample |
| Reagent | 2 | `honey_drop` (or honey bottle) | 1 per analysis, 1 per sample |
| Specimen out | 3 | output | Analysed bee (genome now readable in tooltips) |
| Serum out | 4 | output | `trait_serum` with a `aeroapiary:trait` data component {gene, value} |

- Mode buttons: **Analyse** (reagent only; reveals the genome) or **Sample** (choose a gene from the list on the screen; consumes the vial and reagent).
- Sampling a **drone** never kills it; sampling a princess or queen has a 25% chance to lower its fertility by 1 (needs care).
- Power: 20 FE/t; Analyse 100 ticks, Sample 300 ticks. Works without power at quarter speed (old packs let you hand-crank; here it is just slow).
- Screen (the glowing monitor on the model) shows the genome bars; in the GUI it is the gene list.

## Genetic Splicer

| Slot | Index | Accepts | Notes |
| --- | --- | --- | --- |
| Bee | 0 | queen or princess | The target |
| Serum | 1 | `trait_serum` | Consumed; empty `serum_vial` returns to slot 3 |
| Catalyst | 2 | `royal_jelly` (normal), `cosmic_jelly` (double chance) | Consumed per attempt |
| Bee out | 3 | output | Spliced bee |
| Vial out | 4 | output | Empty vial |

- Success 75% with royal jelly, 100% with cosmic jelly. A failed attempt keeps the bee and wastes the serum.
- Power: 60 FE/t, 400 ticks. Royal jelly feed also comes in by pipe through the back conduit (fluid, 250 mB per attempt) when the pack has the Transport fluid pipes.
- Rules: one trait per serum; species cannot be spliced (keeps mutations meaningful); traits above the bee's tier cap need the Quantum Queen Chamber research (optional).

## Code fix

- Replace the two placeholder `tick` branches in `ZeroGMachines` with `GenoStationLogic.tick` and `GeneticSplicerLogic.tick`; give each its own slot rules in `mayPlaceIn` (tables above) and its own layout in `MachineSlotLayouts`.
- Add the data component `aeroapiary:trait` (codec: gene id + value) and make `trait_serum` show it in its name and tooltip.
- Read and write genes through the Productive Bees bee-data API (the gene keys it already uses), so serums stay compatible with its breeding.
- Splicer: a `GeoBlockRenderer` draws `genetic_splicer_helix.geo.json` (idle spin when powered, fast spin and bob while working). The baked block model has no rungs, so the helix is never drawn twice.

## Files

| File | Use |
| --- | --- |
| `models/block/other/genetic_splicer.json`, `geno_station.json` | New baked models (translucent render type; glowing parts use `neoforge_data` light 15) |
| `textures/block/machines/genetic_splicer.png`, `geno_station.png` | 128 x 128 atlases, 2 px per model pixel |
| `textures/block/machines/*_glowmask.png` | For shaders/emissive layers; the models already glow without them |
| `blockstates/genetic_splicer.json`, `geno_station.json` | Now with `facing` (north, east, south, west); the block needs `HORIZONTAL_FACING`, which `ZeroGMachineBlock` already has |
| `geo/machines/genetic_splicer_helix.geo.json`, `animations/genetic_splicer_helix.animation.json`, `textures/block/machines/genetic_splicer_helix.png` | Animated helix |
| `models/item/*.json` | Parent the block model |

Old textures (`genetic_splicer_hd*.png`, `other/geno_station*.png`) can stay in the jar; nothing points to them after this, and no ids change.

# GUIs

Both screens use the Alveary Controller look: vanilla window and slots, recessed panels with a honey strip, dark wells for gauges. No words are baked into textures. Backgrounds are `textures/gui/geno_station.png` and `textures/gui/genetic_splicer.png` (256 x 256); both blit sprites from `textures/gui/genetics_widgets.png`.

## Geno Station screen (196 x 226)

| # | Element | Kind | x | y | w | h | Behaviour |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `p_in` | panel | 6 | 15 | 26 | 72 | Inputs panel. |
| 2 | `specimen` | slot | 10 | 19 | 18 | 18 | Slot 0: bee to read (queen, princess or drone). Ghost: bee. |
| 3 | `vial` | slot | 10 | 42 | 18 | 18 | Slot 1: blank Serum Vial (Sample mode only). Ghost: vial. |
| 4 | `reagent` | slot | 10 | 65 | 18 | 18 | Slot 2: Honey Drop or honey bottle, 1 per job. Ghost: drop. |
| 5 | `p_genome` | panel | 36 | 15 | 124 | 88 | Genome panel. |
| 6 | `genes` | list | 39 | 19 | 112 | 80 | Gene list, 8 rows of 10 px: gene name (code text, 6 px from the left), active allele bar and inactive allele bar on the right. Click a row to select it for sampling. |
| 7 | `scroll` | scroll | 152 | 19 | 6 | 80 | Scrollbar for the gene list (about 12 genes). |
| 8 | `p_out` | panel | 164 | 15 | 26 | 88 | Outputs panel. |
| 9 | `specimen_out` | slot | 168 | 19 | 18 | 18 | Slot 3: the bee after reading (genome now known). |
| 10 | `arrow` | arrow | 172 | 41 | 10 | 12 | Small down arrow, fills as the job runs. |
| 11 | `serum_out` | slot | 168 | 56 | 18 | 18 | Slot 4: Trait Serum with the sampled gene. |
| 12 | `energy` | bar | 170 | 78 | 14 | 22 | FE buffer (10,000 FE), fills from the bottom. Tooltip shows FE and FE/t. |
| 13 | `progress` | bar | 36 | 106 | 124 | 6 | Job progress, fills left to right in honey. |
| 14 | `b_analyse` | button | 36 | 115 | 60 | 14 | Analyse mode: read the genome only (uses reagent). |
| 15 | `b_sample` | button | 100 | 115 | 60 | 14 | Sample mode: copy the selected gene into a Serum Vial. Disabled until a gene is selected. |
| 16 | `inv_label` | text | 17 | 133 | 60 | 9 | Inventory label. |
| 17 | `inv` | grid | 17 | 144 | 162 | 54 | Player inventory (menu slots 5-31). |
| 18 | `hotbar` | grid | 17 | 202 | 162 | 18 | Hotbar (menu slots 32-40). |

## Genetic Splicer screen (196 x 212)

| # | Element | Kind | x | y | w | h | Behaviour |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `p_in` | panel | 6 | 15 | 26 | 76 | Inputs panel. |
| 2 | `bee` | slot | 10 | 19 | 18 | 18 | Slot 0: queen or princess to splice. Ghost: crown. |
| 3 | `serum` | slot | 10 | 43 | 18 | 18 | Slot 1: Trait Serum. Ghost: vial. |
| 4 | `catalyst` | slot | 10 | 67 | 18 | 18 | Slot 2: Royal Jelly (75%) or Cosmic Jelly (100%). Ghost: jelly. |
| 5 | `a_in` | arrow_r | 33 | 49 | 8 | 7 | Feed arrow into the chamber (lit while working). |
| 6 | `chamber` | display | 42 | 15 | 92 | 76 | Chamber window: the helix animation (8 frames, 24 x 56) centred; serum colour tints the strands; success chance top-right in code text. |
| 7 | `jelly` | tank | 138 | 15 | 14 | 76 | Royal Jelly fluid from the back conduit, 4,000 mB. Used instead of the catalyst slot when present (250 mB per attempt). |
| 8 | `a_out` | arrow_r | 153 | 49 | 8 | 7 | Output arrow. |
| 9 | `p_out` | panel | 162 | 15 | 28 | 76 | Outputs panel. |
| 10 | `bee_out` | slot | 167 | 25 | 18 | 18 | Slot 3: spliced bee. |
| 11 | `vial_out` | slot | 167 | 55 | 18 | 18 | Slot 4: empty Serum Vial. |
| 12 | `energy` | bar | 170 | 77 | 12 | 11 | FE buffer (40,000 FE), small gauge. Tooltip shows FE and FE/t. |
| 13 | `progress` | bar | 42 | 94 | 92 | 6 | Splice progress. |
| 14 | `preview` | well | 6 | 103 | 184 | 12 | Preview line (code text): "Speed: Fast  ->  Forest Queen" or the reason it cannot start. |
| 15 | `inv_label` | text | 17 | 120 | 60 | 9 | Inventory label. |
| 16 | `inv` | grid | 17 | 130 | 162 | 54 | Player inventory (menu slots 5-31). |
| 17 | `hotbar` | grid | 17 | 188 | 162 | 18 | Hotbar (menu slots 32-40). |

Menu slots for both: 0-2 inputs, 3-4 outputs (take only), 5-31 player inventory, 32-40 hotbar. Item positions are the slot box + 1.

**Geno Station ContainerData:** 0 progress, 1 max, 2 energy/10, 3 energy max/10, 4 mode (0 analyse, 1 sample), 5 selected gene index (-1 none), 6 scroll offset.
Gene rows come from the specimen's genome, sent with the slot sync (the item already carries it). Buttons send `SetMode` and `SelectGene(index)`; Sample stays disabled until a gene is selected.

**Genetic Splicer ContainerData:** 0 progress, 1 max, 2 energy/10, 3 energy max/10, 4 jelly mB, 5 success chance %, 6 status (0 ready, 1 working, 2 no serum, 3 species blocked, 4 wrong bee, 5 no catalyst, 6 no power).
The chamber shows `helix_0..7` at 3 ticks per frame while working (frame 0 when idle); a status other than 0 or 1 draws `chamber_blocked` and the reason in the preview line.

## Widget atlas (`genetics_widgets.png`)

| Sprite | u | v | w | h | Use |
| --- | --- | --- | --- | --- | --- |
| `helix_0` | 0 | 0 | 24 | 56 | Helix animation frame 0 (play 8 frames, 3 ticks each; tint strands with the serum colour in code) |
| `helix_1` | 26 | 0 | 24 | 56 | Helix animation frame 1 (play 8 frames, 3 ticks each; tint strands with the serum colour in code) |
| `helix_2` | 52 | 0 | 24 | 56 | Helix animation frame 2 (play 8 frames, 3 ticks each; tint strands with the serum colour in code) |
| `helix_3` | 78 | 0 | 24 | 56 | Helix animation frame 3 (play 8 frames, 3 ticks each; tint strands with the serum colour in code) |
| `helix_4` | 104 | 0 | 24 | 56 | Helix animation frame 4 (play 8 frames, 3 ticks each; tint strands with the serum colour in code) |
| `helix_5` | 130 | 0 | 24 | 56 | Helix animation frame 5 (play 8 frames, 3 ticks each; tint strands with the serum colour in code) |
| `helix_6` | 156 | 0 | 24 | 56 | Helix animation frame 6 (play 8 frames, 3 ticks each; tint strands with the serum colour in code) |
| `helix_7` | 182 | 0 | 24 | 56 | Helix animation frame 7 (play 8 frames, 3 ticks each; tint strands with the serum colour in code) |
| `fill_jelly` | 0 | 60 | 12 | 74 | Royal Jelly fluid fill (or use the fluid texture) |
| `fill_energy` | 14 | 60 | 12 | 20 | FE fill (bottom-up) |
| `fill_progress` | 28 | 60 | 122 | 4 | Progress fill (left to right) |
| `allele_active` | 28 | 66 | 30 | 3 | Allele bar, active (tint per gene family in code) |
| `allele_inactive` | 28 | 71 | 30 | 3 | Allele bar, inactive (tint per gene family in code) |
| `row_selected` | 62 | 66 | 110 | 10 | Selected gene row highlight |
| `row_hover` | 62 | 78 | 110 | 10 | Hovered gene row |
| `scroll_thumb` | 176 | 66 | 6 | 15 | Scrollbar thumb |
| `scroll_thumb_off` | 184 | 66 | 6 | 15 | Scrollbar thumb, disabled |
| `arrow_down_on` | 194 | 66 | 5 | 6 | Down arrow, lit (draw the top N rows by progress) |
| `arrow_right_on` | 202 | 66 | 7 | 7 | Right arrow, lit |
| `button_normal` | 0 | 140 | 60 | 14 | Mode button, normal (text drawn by code) |
| `button_hover` | 0 | 156 | 60 | 14 | Mode button, hover (text drawn by code) |
| `button_active` | 0 | 172 | 60 | 14 | Mode button, active (text drawn by code) |
| `button_disabled` | 0 | 188 | 60 | 14 | Mode button, disabled (text drawn by code) |
| `icon_analyse` | 64 | 140 | 9 | 9 | Analyse icon (magnifier) |
| `icon_sample` | 76 | 140 | 5 | 7 | Sample icon (vial) |
| `chance_badge` | 90 | 140 | 26 | 9 | Success-chance badge in the chamber corner |
| `chamber_blocked` | 120 | 140 | 92 | 76 | Red hatch over the chamber when the splice cannot start |

Lang: `screen.aeroapiary.geno_station`, `screen.aeroapiary.genetic_splicer`, `.analyse`, `.sample`, `.gene.<id>`, `.status.<n>`, `.chance` ("%s%% chance").
