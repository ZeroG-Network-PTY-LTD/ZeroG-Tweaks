# Exact legacy machine recipe pages

## 1. Metadata
Author: Codex. Date: 2026-10-09. Status: Approved implementation contract,
derived from the owner's explicit request and existing verified runtime rules.
Scope: Silk Weaver, Centrifuge and Starmetal Smelter first; remaining adapters stay tracked.

## 2. Context
The native refinery/forge/growth/salvage panel already provides recipe combinations.
These three legacy machines still present accepted-item catalogues, which omit
quantities, consumed flux, outputs and card-adjusted duration/energy.

The addon exposes authoritative centrifugeProducts/starmetal methods. Silk Weaver
has an existing ZeroG override: one silk thread becomes one woven silk in 200 calls.
Recipe discovery must reflect these rules, not create new processing chains.

## 3. Functional requirements
FR-1: The UI MUST provide Items, Recipes and Upgrades tabs for these three machines.
FR-2: Pages MUST show exact consumed inputs, reusable/consumed catalyst status,
outputs and base/current FE and ticks from authoritative runtime rules.
FR-3: Clicking an input or output MUST filter all corresponding combinations;
All, previous/next and scrolling MUST remain read-only.
FR-4: Centrifuge/Smelter MUST show their existing Acceleration/Energy Coil tier1–6
support and configured effects, without advertising Compact/Void or new sockets.
Silk Weaver MUST explicitly report no supported machine cards and no FE cost.
FR-5: Missing optional addon MUST produce no fabricated recipes or exceptions.
FR-6: Existing inventory indices, processing, automation and saved data MUST remain unchanged.

## 4. Non-functional requirements
NFR-1: Enumerate registry recipe inputs once per panel creation, not each frame.
NFR-2: Hide the panel/control below 120px available width; capture all panel clicks,
including non-left buttons, to avoid slot/drop actions underneath.
NFR-3: No new network requests, chunks, persistent world state or dependencies.

## 5. Acceptance criteria
AC-1 (FR-2): Given every registered centrifuge combination, when processing with
power, then catalogue outputs/counts and whole-job energy match actual results.
AC-2 (FR-2): Given stardust/redstone, then Smelter shows consumed flux and three
nuggets; a wrong flux does not become a recipe.
AC-3 (FR-2/4): Given each card tier, then advertised ticks/FE match cumulative
LegacyCardJobs rounding and approved 2.5x/30% bounds.
AC-4 (FR-1/3/6): Given item/output selections, then all matching pages are returned
without changing inventories/progress/energy; unsupported recipes are absent.
AC-5 (FR-2/4): Given Weaver input, then 200 calls consume one thread, yield one
silk, preserve recovery slots, use no FE and expose no supported cards.
AC-6 (FR-5): Given no addon, then all legacy page lists are empty safely.
AC-7 (NFR-1/2): Static UI review confirms cached discovery and bounded panel/input
capture; actual client layout/scroll readability remains owner's visual approval.

## 6. Edge cases
EC-1: Optional addon absent or expected reflection API changed: empty discovery,
not invented output. EC-2: Empty selection returns all pages; unknown item returns none.
EC-3: Unregistered/empty products excluded. EC-4: Unsupported Compact/Void or
old recovery slots never imply new input/upgrade support. EC-5: Config/card changes
refresh adjusted metrics without rebuilding the registry list or changing paid jobs.

## 7. API contract
```ts
type Page = { id: string; inputs: CountedIngredient[]; catalyst?: CountedIngredient;
 outputs: {stack: ItemStack; chance: number}[]; baseEnergy: number; baseTicks: number;
 energy: number; ticks: number };
type CountedIngredient = { alternatives: ItemStack[]; count: number; consumed: boolean };
function basePages(machineId: string): Page[];
function adjusted(machine: BlockEntity, pages: Page[], selected: ItemStack): Page[];
```

## 8. Data model
| Field | Type | Constraint |
| --- | --- | --- |
| Base pages | immutable runtime list | actual addon outputs; panel-local cache |
| Selection/page/scroll | client state | no inventory writes |
| Energy/time adjustment | derived integers | exact existing cumulative rounding |
| Installed cards | existing saved handler | two sockets unchanged |

## 9. Out of scope
No new recipes/cost balance, survival crafting, addon rewrite, invented Silk patterns,
Compact/Void extension, new artwork, local JAR installation or hub/save changes.
Genetics/generator/alveary/other machine adapters remain subsequent documented work.
