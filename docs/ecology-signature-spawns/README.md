# Ocean signature habitat — 12 October 2026

`generate_ocean_spawns.py --output <runtime spawns_signature_ocean.json> --check`
compares the regular Tidewraith biome modifier with this canonical generator.
It targets deep trenches, kelp jungles and island chains: weight10, group3-4.
Runtime separately checks exposed water, one-in-eight default pack-start chance
and a nearby regular-mob cap4 within128blocks. Boss spawning is not enabled.
Existing nearby groups may fill to four without a new rarity roll per member.
Owner12October supersedes the previous lone-mob rule. Regular mobs gain safe
non-magma liquid breathing/hazards and loaded-neighbour pack patrol; lava/slag
remain dangerous. Existing boss breathing, size and spawning rules are unchanged.
The adjacent Water Separator blockstate source preserves four terminal facings.

## Hub-only catalogue and current guide

Owner12October: retain only tier shell blocks actually used by the hub builds.
HubExhibits.serviceShellState is the shared runtime cell plan. The creative-tab
filter admits its casing/roof/controller IDs, hides other tier BlockItems and
the legacy apiary_controller, but preserves saved IDs, ordinary machines,
combs, frames and hives. No registry deletion or existing-world mutation.

generate_hub_guide.py writes the eight live schematic references from the
current hub shape:107 blocks,18 chamber air cells and five base service ports.
legacy_multiblocks.json is historical concept geometry only, not supported
formation advice. Old rendered sheets require a future artwork refresh.

planet_mines_no_rails.processor.json is the canonical rail-tag-to-air rule.
Runtime branch pool elements and hub room displays use it; source template NBT
is retained, so an unprocessed manual template placement remains historical.
Procedural mine corridors also retire rails, without changing their seed RNG.

Galaxy tracker reconciliation: the previously pending Rime Stalker, Crater
Drifter, Ash Strider and Bog Lurker now have registered runtime implementations.
All13 structure routes resolve in the source audit; that is not evidence of
all-seed ecology or complete story/boss progression. Historical tracker counts
must not be interpreted as current live registry counts. Amethyst Stalker,
remaining bosses, seeded galaxy naming and broader surveys remain outstanding.

Bog Lurkers retain acid/poison immunity and use loaded-only local pool search.
No new artwork is claimed; dedicated swim/spit animation remains pending.
Codex source pages19/20 were updated with browser/diagnostic/habitat explanations.
