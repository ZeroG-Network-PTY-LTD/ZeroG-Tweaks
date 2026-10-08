# Gate plans, charging hologram and jump tariff

## 1. Metadata
2026-10-09; Codex; Approved by owner's explicit request to implement the described changes.

## 2. Context
Current controller exposes only current-tier Ghost and next-tier Preview. Players
need all six standing plans anchored to their actual controller. Existing gate
tariffs apply old intra-galaxy, passenger and lens factors; these are superseded
for gate jumps by the owner's exact doubling tariff. Existing launch artwork is
retained, not replaced with unapproved art.

## 3. Functional requirements
FR-1 MUST expose Tier1–6 plan selection in the controller and send validated,
controller-anchored plans without constructing blocks.
FR-2 MUST charge exactly100000/200000/400000/800000/1600000/3200000 FE for a
successful player gate jump by formed tier; admin gates MUST remain free.
FR-3 MUST NOT debit on cancellation, failed formation/destination or countdown.
FR-4 MUST activate the existing transition screen for dimension gate travel.
FR-5 MUST show a nearby hologram above the controller with galaxy, selected
planet, energy/jump cost and charging countdown, refreshed from server state.
FR-6 MUST add a creative-only gold animated energy cell with unlimited stored
supply and a shared300000 FE/tick extraction/output budget across all faces.
It MUST reject survival placement, expose no survival recipe or block loot, and
appear in Z-Admintools. GFE is its display label, not a new incompatible energy API.

## 4. Non-functional requirements
NFR-1 No saved hologram entities, forced chunks or background pre-generation.
NFR-2 Plans remain bounded to tiers1–6 and authorized nearby menus. Hologram cache
at most128 entries, expires within3 seconds and renders within32 blocks.
NFR-3 Existing IDs, ownership, destinations, service placement and upgrade slots stay compatible.

## 5. Acceptance criteria
AC-1 FR-1: Given an authorized controller, selecting each tier returns that tier's
plan; invalid tier requests fail and do not alter the world.
AC-2 FR-2: Given tiers1–6, jump prices equal the doubling table regardless of
passengers, galaxy discount or lens; admin tariff remains zero.
AC-3 FR-3: Given successful and failed launches, one success debits once while
cancelled/invalid attempts preserve FE.
AC-4 FR-4: Given a gate destination packet, transition selection retains existing
art even when an old client configuration chose OFF; non-gate travel stays vanilla.
AC-5 FR-5/NFR-2: Given synchronized controller data, bounded hologram state shows
the selected world and remaining countdown; stale/different-world state clears.
Actual shader/render readability requires subsequent client visual approval.
AC-6 FR-6: Given creative/survival placement and simulated/committed extraction,
only creative placement succeeds and all faces together commit at most300000
FE/tick; simulations do not consume quota and the next tick replenishes it.

## 6. Edge cases
EC-1 Unformed/standalone controller: preview anchors from existing resolver fallback.
EC-2 Controller moved to a flexible service position: resolved centre preserved.
EC-3 No packet receiver: gameplay still works without hologram. EC-4 Failed player
dimension change: no FE deduction. EC-5 Disconnect/world change: visual cache clears.

## 7. API contracts
```ts
type PlanRequest = { tier: 1|2|3|4|5|6 }; // existing validated menu button
type Hologram = { dimension:string; controller:BlockPos; tier:number;
 destination:string; countdown:number; energy:number; cost:number };
function jumpCost(tier:number):number;
```

## 8. Data models
| Data | Type | Constraints |
| --- | --- | --- |
| Plan tier | client integer |1–6; never changes actual formed tier |
| Jump tariff | derived integer |100000 shifted tier−1; admin0 |
| Hologram | transient packet/cache |server-generated,128 entries,3s TTL |
| Charge/countdown | existing controller state |no new saved world state |
| Creative cell | block entity/existing FE API |unlimited supply; per-tick quota |

## 9. Out of scope
No installation/world replacement without further request; new textures only for the approved gold cell,
survival costs, progression unlocks, weather changes or schematic autobuilding.
Recall item fees retain their existing rules. Existing stored FE is preserved.
