# Gas production and safe pressure specification

Author: Codex. Date: 2026-10-11. Status: Approved rules, owner confirmed in chat. Reviewer: owner; implementation verification pending.

## Context
Oxygen and hydrogen, refillable canisters and six-tier gas networks already exist. Survival production was missing. Owner approved powered water separation, hydrogen:oxygen 2:1, configurable costs, fullness-based pressure and safe stopping. This is a gameplay volume conversion, not a real-world thermodynamic simulation.

## Functional requirements
FR-1: A standalone Water Separator MUST convert vanilla water to hydrogen and oxygen atomically in a 2:1 ratio. Conservative defaults: 10 mB water to 20 mB hydrogen plus 10 mB oxygen, 100 ticks, 2,000 FE.
FR-2: Each of its three tanks MUST hold 16,000 mB. Insufficient water, power or either output capacity MUST pause without consuming water or creating gas.
FR-3: Pressure MUST be labelled as fill percentage, not physical pressure. Full outputs MUST block production without fullness-induced leakage, explosions or damage. Separately approved misconnection effects are documented below.
FR-4: Six faces MUST independently select Off/Water/Hydrogen/Oxygen fluid roles and FE Input/Off. Cached capabilities MUST honor current face settings and removed/replaced blocks.
FR-5: Acceleration and Energy Coil tier 1–6 MUST use existing 2.5x/30% caps; Compact/Void MUST be rejected because this machine has no processing item inventory.
FR-6: The GUI MUST show exact conversion, base/adjusted FE and time, tank volumes, fill percentages, progress and side controls. Fluid container exchange MUST respect the clicked face.
FR-7: Tank contents, FE, progress, face settings and cards MUST persist; breaking MUST return cards as ordinary single-stack drops. Stored FE/fluids follow existing broken-tank loss behavior, not new portable storage.

## Non-functional requirements
NFR-1: Each tick MUST use constant bounded work over three tanks/two cards; no world scans, forced chunk tickets or asynchronous world access.
NFR-2: GUI changes MUST be server validated within eight blocks of the live machine. Invalid buttons MUST be rejected.
NFR-3: Existing gas IDs, pipes, recipes, gates, weather and saves MUST remain unchanged.

## Acceptance criteria
AC-1 (FR-1/2): Given paid water and space, when a cycle completes, then exactly the configured water/FE is consumed and H2/O2 output ratio is 2:1.
AC-2 (FR-2/3): Given either full output, missing water or insufficient FE, when ticked, then contents/FE do not change.
AC-3 (FR-4/NFR-2): Given disabled/reassigned faces or removed machine, when cached handlers or invalid GUI actions are used, then forbidden transfers fail.
AC-4 (FR-5): Given tier-six cards, then effective time and FE use approved caps; wrong card families are rejected.
AC-5 (FR-6/7): Given save/reload, then exact volumes/settings/cards persist and synchronized recipe values match processing.
AC-6 (NFR-3): Existing gas transport regressions MUST continue passing; client layout/animation approval remains separate.

## Edge cases
EC-1: One output full: pause both outputs, never discard gas.
EC-2: Config/cards change: reset uncommitted progress; no already consumed ingredients exist.
EC-3: Null face: no external capability; identity checks reject stale handlers.
EC-4: Optional addons absent: separator MUST function with vanilla water and ZeroG gas registrations.

## API contracts
`fill(face, water, amount, simulate) -> accepted mB`; only Water role accepts vanilla water.
`drain(face, amount, simulate) -> H2 or O2 stack`; only assigned output role exposes that gas.
`receiveEnergy(face, FE, simulate) -> accepted FE`; only enabled FE faces.
`button(0..5) -> cycle fluid role`; `button(10..15) -> toggle FE face`; other IDs rejected.

## Data models
|Field|Type|Constraints|
|---|---|---|
|water/hydrogen/oxygen|FluidTank|16,000 mB; exact registered fluid|
|stored|int|0–200,000 FE|
|progress|int|0–effective duration|
|fluidRoles|six ints|0 Off,1 Water,2 Hydrogen,3 Oxygen|
|powerFaces|six booleans|Input/Off|
|cards|two ItemStacks|Acceleration/Energy Coil; count one|

## Out of scope
Exact survival machine/card crafting costs remain deferred. No gas breathing, fuels, chemical reactions or physical pressure units. The owner subsequently approved bounded misconnection leaks and brief hydrogen exposure: see [superseding gas-effect rules](gas-misbuild-effects-2026-10-11.md). Initial block reuses existing approved industrial textures explicitly; bespoke separator art stays on the artwork TODO. Remaining machine backlog follows this verified gas batch and is not declared complete by it.
