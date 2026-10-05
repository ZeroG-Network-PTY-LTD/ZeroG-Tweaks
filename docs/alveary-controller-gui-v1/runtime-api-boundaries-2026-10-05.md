# Runtime implementation and verified API boundaries — 2026-10-05

This note supersedes any claim that drawing a gauge or slot means its underlying mechanic exists. It does not change approved artwork or authorize invented bee traits.

## Implemented, awaiting final isolated-run results and player visual approval

- Real persisted frame storage: 27 physical slots, tier unlocks **3 / 4 / 6 / 8 / 12 / 18 / 27**, stack size one and frame-only filtering. Old frame contents migrate into this handler without moving or overwriting original output indices. Additional frames drop once on controller destruction.
- Server-owned menus: distance/identity validation, output paging and sorting, auto-eject, and explicit Shift-confirmed excess voiding (default off). The new menu cannot be mistaken for the legacy menu by its screen replacement hook.
- Structure validation uses the installed addon's real `updateFormation()`/`isFormed()` contract. Broken shells stop production.
- T3+ input FE storage and paid work; T3 honey tank8,000mB; T6 starlight catalyst tank4,000mB. Tanks persist and simulation does not mutate them. Honey collection converts an actual registered ZeroG honey bottle already in the product buffer into250mB and returns its glass bottle. Unsupported combs do not magically create honey.
- Physical same-tier energy ports, input/output hatches, frame loaders, honey ports and catalyst-fluid ports forward to one unique currently valid controller. Energy/catalyst are input-only; products/honey are output-only; frame loading cannot extract installed frames. Searches never load chunks. A broken shell, changed port role, unloaded owner or ambiguous shared wall fails closed, including previously cached handlers. Auto-eject uses actual output hatches and does not feed items back into structural blocks; it still empties products when production is paused/full.
- Six original orbital bee species use their existing registered comb outputs. Unknown bees produce nothing.
- Optional Productive Bees13.14.0 support uses the current server's `productivebees:advanced_beehive` recipes. Captured cage `entity` and configurable `type` identify the ingredient; item components, minimum/maximum quantity and chance are read from the actual recipe. All possible products reserve capacity together before a cycle rolls, preventing partial outputs and reroll exploitation. No entity is spawned to resolve a recipe.
- Only the five verified PB attributes are exposed: productivity, endurance, temper, behavior and weather tolerance. Actual diurnal/nocturnal and rain restrictions are enforced. Analysis/sampling/splicing retains identity and other attachments.

## Bounded runtime choices, not undocumented Forestry behavior

Frame productivity currently changes cycle speed: honeyed/starlit/starmetal add0.15; proven/impregnated add0.10; restraint/oblivion subtract0.05; other registered frames add0.05. Combined multiplier is bounded0.25–4.0. These are explicit ZeroG baseline rules, **not** verified historical effects for every frame.

Cycle length is `max(80,(900−100×tier)/(productivity×catalystBonus))`; catalystBonus1.2 applies only with25mB available, consumed once per completed cycle. T3+ work costs20×tierFE per tick. Product recipes determine products, not fake fertility or chromosome fields.

## Pending rather than fabricated

The installed PB API and addon expose no native queen lifespan counter, fertility/chromosome system, temperature/humidity allele, or gravity-tolerance allele. Lifespan and unavailable genome/tolerance bands remain labelled unavailable/sealed. They must not be populated with invented numbers or described as complete.

Approved climate-module effects, rotor tolerance adjustments, quantum coil charge, mutation/territory/lifespan frame effects, actual drone breeding and flower/territory requirements need separate authoritative rules and implementation. Existing art shows these planned capabilities; it is not proof of gameplay.

PB productivity changes actual recipe output quantities, not cycle speed. Verified directly from installed `productivebees-1.21.1-13.14.0.jar`, `AdvancedBeehiveBlockEntity.lambda$beeReleasePostAction$1`: for positive numeric productivity value `v`, a single output grows by `v`; larger counts `n` grow by `round(n × (1/(v+2) + (v+1)/2))`. Zero outputs remain empty. The cage trait is validated against the installed `GeneValue` enum domain. The same arithmetic reserves the maximum possible products before processing; output chance and components are preserved and oversized quantities split through the actual inventory handler. The mapped frame-cycle modifier is separate and explicit above. Full PB hive upgrade/flower simulation parity is not claimed.

## Transport baseline and follow-up limits

Six tiers have real FE/item/fluid buffers and capability transfer; loaded-only graphs bounded to256 nodes, minimum-tier throughput, signal/face modes, priorities, routing, exact-ID whitelist/blacklist, persistent cells and filters. Oversized connected graphs stop rather than silently creating several partial full-rate leaders; oversized fluid networks reject unverified input. Split larger installations into deliberate independent networks. Null Links share one canonical loaded owner and charge remote capability transfers; missing/unloaded/nonreciprocal partners fail closed rather than forcing chunk loads or copying buffers.

Ordinary transport UX is implemented: nine non-consuming item ghost templates and three bucket/fluid ghost templates; whitelist/blacklist and tag/component matching; template clearing; priority edits; dye colouring and water-bottle cleaning; content-preserving in-place tier upgrades with an empty old-block refund; cell input/output and port input/output/both controls. Filter cards open a held-item editor in air and persist their templates/toggles on the actual card; switching away revokes edit authority. Applying a saved card copies its rules to the targeted machine. Templates never become physical loot or transfer contents. These require the final isolated regression verdict and client visual approval.

Null Link survival-player inventory interactions charge the same2FE/item remote fee (twice that across dimensions). Component-specific net movement counts swaps correctly without charging a reorder of the shared buffer. Insufficient power rolls back shared inventory, player inventory and carried stacks together; remote storage rejects world-dropping/throw/drag/clone click types so rollback cannot duplicate dropped entities. A menu loses authority if its reciprocal shared owner changes or unloads. Creative interaction is intentionally free.

Still pending from the full transport design: visible moving-content renderers. Keep that on the tracked list until tested; working transport is not a claim that renderer work is done.

**Transport-family GUI TODO (not redesigned in this delivery):** the current shared TransportMenu exposes nine physical slots plus both ghost-template grids for every family. Energy-only and fluid-only blocks therefore show irrelevant item/filter regions and currently permit incidental physical item storage through their raw menu handler. Restrict insertable/visible slots and controls to the family's real capabilities; preserve pre-existing incidental items through labelled extraction-only recovery rather than deleting them. Keep Null Link's genuine shared item/fluid storage and paid remote transactions intact. Give the combustion generator only its real filtered fuel slot and actual FE/burn information. A successful generic transport test is not approval of this outstanding semantic/UI cleanup.

## Tests

### Service-module and slot-layout repair

The authored 5×5×5 alveary shell also accepts explicit ZeroG service-role blocks in ordinary casing positions: `energy_port` and the six energy cells; `item_port`; `fluid_port` and the six original fluid tanks. Runtime whitelist tags live under `zerog_tweaks:alveary/{energy,item,fluid}_modules`, and the Java runtime additionally checks the actual supported block classes. Foreign machines, generators, roof substitutions and blocks inside the central flight chamber are not implicitly accepted. A service port's front must face outside the shell; a formed port's sided automation exposes that front only. Standalone ports retain their ordinary behavior.

Service modules retain their real independent buffers, saved contents, filters, redstone settings and external capabilities. The unique loaded formed controller receives FE from a configured inward-output energy cell or intake energy port. Input item ports move actual bee/frame stacks into validated handlers. Output item ports move actual production into their buffer only when auto-eject is enabled. Fluid ports feed registered starlight catalyst inward and export actual honey outward. Structural fluid tanks respect their inward-face input/output controls. Transfers are bounded and conserve source/controller buffers; ambiguous controller ownership stops the bridge.

Menu product paging starts at the actual output boundary, not at migrated legacy frame index2. The original saved inventory indices remain intact; old frame positions have a separate extraction-only recovery page. Empty legacy slot1 is sealed and labelled recovery, not portrayed as working drone breeding. The screen uses the approved alveary-specific panel and reports real eject/void states; it is not a cloned generic machine inventory.

Workflow tests cover tier capacities, conservation, filtering, simulated operations, reload, disabled faces, dangerous-fluid tier rules, Null Link fees and stale cached capabilities; generator fuel/output; genetics liquid dosing; real frame migration/tier unlocks; shell formation, real PB iron-bee recipe output components and honey save/reload. Parent integration runs the isolated servers and records verdicts. In-game screen/art approval remains a separate human check.
