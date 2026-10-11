# Selected backlog — owner review, not active gameplay

Status: **DRAFT / INACTIVE**. The owner requested proposals for costs and Codex research on 11 October. These values do not alter existing recipes, saves, trait effects or advancement requirements. Approve or amend each section independently.

## 3. Alveary research proposal

Use existing personal Codex advancements, not possession of a borrowed book or another player's machine. Initial proposals unlock research access, not automatically upgraded genes:

| Research family | Proposed existing milestone | Rationale |
| --- | --- | --- |
| Temper | `zerog_tweaks:codex/mars` | Rustborn husbandry and handling |
| Behavior | `zerog_tweaks:codex/the_moon` | Lunari observation and cycle tracking |
| Productivity | `zerog_tweaks:codex/cerulite` | Precision crystal analysis |
| Endurance | `zerog_tweaks:codex/skarn` | Survival under heat and strain |
| Weather tolerance | `zerog_tweaks:codex/eidolon` | Frozen Fleet environment research |

Do not invent native lifespan, territory or mutation alleles absent from verified Productive Bees APIs. Preserve current jobs and modifiers until approved migration rules exist. Automated jobs need an approved research owner policy; proposal: placer UUID, with explicit ownership transfer and no bypass for absent/offline owners. Admin exhibits remain separately scoped.

### Larger shells proposal

Keep existing 5×5×5 and legacy formations valid. Optional T5–T7 expansion: **7×5×7**, 5×5 clear flight chamber at layers 1 and 2, full foundation/deck/roof, matching tier parts. This requires 195 structural cells: 189 matching-tier parts plus one controller, two item ports, two fluid ports and one energy port. Ports replace bottom-perimeter cells; controller replaces a second-row wall cell. Existing frame capacities 12/18/27 stay unchanged. No automatic yield/capacity bonus. External genetics/cryo modules remain external.

Before activation: approve tier availability, exact allowed casing variants and climate/module FE/fluid rules. Test every controller orientation, perimeter port relocation, overlapping ownership, broken/replaced parts, unloaded chunks, cached-handler revocation and old-save migration.

## 4. Machine contracts proposal

Keep current verified Acceleration/Coil caps (2.5× speed, 30% job-energy saving). No multiplicative stacking with legacy upgrades. Current Compact/Void support on four native processors remains; do not advertise it on genetics or legacy machines until their contracts are implemented and tested.

Proposed later extension: Compact only on consumed ingredient inputs, never reusable catalysts, cages, serum/component-bearing samples or card sockets. Void only on newly produced ordinary item outputs, never bees, gene samples, returned containers, tanks or existing stored outputs. Preserve component identity and normal-size visible stacks. Require owner approval of excluded outputs before implementation.

Existing exact-page adapters cover native processing, supported legacy recipes, genetics and generators; accepted-item catalogues alone are not sufficient. Audit newly registered machines against their actual backend before adding pages. Empty/unsupported machines must be reported, not given fabricated recipes.

## 7. Moon wreck proposal

Small **9×3×9** impact remnant: shallow meteorite fragments, broken hull/pod shell and one salvage chest. No Broken Console, Wisp, Codex, guardian key or new story log. Star Map Fragments remain the existing Act-I lore carrier. Proposed natural static rarity: one candidate per 32×32-chunk region, terrain checks reducing placements; separate from daily comet events. No excavation near gates, containers or player structures. Exact loot pool and trigger need approval before activation. Hidden coordinates, Captain dialogue and final ending consequences remain unspecified.

## 8. Survival cost proposal — hardest to easiest

All outputs below are one item. These are **input-count proposals**, not active shaped recipes. Verify target namespace and existing recipes before adding an override; preserve all registry IDs. No filled tanks or machines with contents may be consumed.

| Target | Proposed ingredients |
| --- | --- |
| Genetic Splicer | 4 Moonsteel plates, 2 Moonsteel cogs, 1 Cerulite gem, 1 Redstone block |
| Geno Station | 4 Ferrox plates, 2 Ferrox cogs, 1 Glass block, 1 Redstone block |
| Water Separator | 4 Ferrox plates, 1 Ferrox cog, 2 Glass blocks, 1 Redstone block |
| Basic apiary controller | 4 local planks, 2 Ferrox plates, 1 Ferrox cog, 1 Honeycomb, 1 Redstone |
| Basic frame | 4 Sticks, 2 local planks, 1 String |
| Royal Jelly synthesis | 2 Honey Drops, 1 Honeycomb, 1 Sugar |
| Cosmic Jelly synthesis | 1 Royal Jelly, 1 Stardust, 1 Cerulite gem |

Tiered cards: select one existing dimensional metal per tier (proposal Ferrox/Moonsteel/Cyrrium/Tectium/Wraithsteel/Astrium). Each T1 family card: 2 plates + 1 cog + 1 Redstone + its family component. Each T2–T6: previous matching family card + 2 new-tier plates + 1 new-tier cog + 1 new-tier dust + 1 empty Star Glass block (any approved colour). Family components proposed: Acceleration=Sugar, Energy Coil=Copper Ingot, Compact=Chest. Void card proposal: 2 Wraithsteel plates + 1 Wraithsteel cog + 1 Obsidian + 1 Redstone. Exact material accessibility and tier order require lore review.

Alveary shell parts and T1–T16 machine casings need a separate complete per-ID bill of materials; this proposal does not pretend to finish them. Keep previously approved manufacturing recipes unchanged. Validate crafting counts/remainders, filled-container rejection, advancement accessibility and absence of circular dependencies before activation.
