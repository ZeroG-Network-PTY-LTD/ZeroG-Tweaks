# Sol machine and transport field guide

Minecraft Java 1.21.1 · NeoForge · same-version `1.0.12-dev` candidate.
This describes implemented controls, not every proposed research mechanic.

## Genetics: preserve the specimen, change one verified trait

Use a supported Productive Bees cage in the Geno Station. Analyze it before
sampling or splicing. Select productivity, endurance, temper, behavior or weather
tolerance—the five traits verified against the installed API. Research and jobs
are server-side; an animated terminal alone never grants a result.

| Job | Powered time | Energy | Other requirements |
| --- | --- | --- | --- |
| Analysis | 100 ticks | 20 FE/t | Supported specimen and clear output |
| Sampling | 300 ticks | 20 FE/t | Analysis complete; matching consumable inputs |
| Splicing | 400 ticks | 60 FE/t | Analyzed specimen, serum and jelly catalyst |

Royal jelly gives 75% success; cosmic jelly gives 100%. A failed splice returns
the unchanged specimen. Analysis/sampling also have slower hand-cranked modes.
Saved jobs reject changed inputs and full outputs. Eleven take-only recovery
slots retain older inventories; do not mistake them for new operating slots.
The Geno Station's registered honey support tank holds 4,000 mB.

## Alveary: formation first, then production

The tiered controller uses a separate saved frame inventory. Tiers 1–7 unlock
3, 4, 6, 8, 12, 18 and 27 slots respectively; locked cells are intentionally
unavailable. Existing specimens and legacy outputs are not discarded during
inventory migration. Formation, power and output room are checked before work.

Productive Bees products use its actual server recipes, including quantities,
chances and item components. Unsupported bee/recipe combinations show a status
instead of inventing a product. Honey bottles can be transferred to the real
honey tank, leaving glass bottles. Higher-tier FE and catalyst storage are real;
unsupported lifespan or temperature-allele fields remain marked unavailable.

Controller buttons: `?` shows verified genome data, `E` ejects, `S` compacts,
`>` pages outputs/recovery, and `Shift+V` confirms void-excess mode. Plain `V`
disables voiding. Check the status and tooltips before enabling destructive
overflow handling. Climate bars show the current biome, not invented genes.

## Transport: source → loaded network → destination

Six tiers of conduits, pipes, tubes and cells carry FE, fluids and items. Ports
and lines have input/output rules, redstone modes, routing and filters. Networks
never force-load distant chunks. Oversized graphs fail closed instead of running
partial overlapping leaders. Low-tier fluid restrictions are enforced server-side.

Use an empty hand to open controls. Side buttons cycle face rules; Shift-click
changes side priority. The Flux Wrench cycles the clicked face; Shift-use packs
the node with its saved contents, without a second loose-content drop. A matching
higher-tier block upgrades a node in place and transfers its saved state.

Use dye to color a line, or a water bottle to clean its color. Filter cards open
their editor when used in the air. Nine item templates or three filled-bucket
templates are references, not consumed inventory. Whitelist/blacklist, tag and
component modes are saved on the card; apply it to the network node afterwards.

Null Frequency Cards pair two unused, loaded Null Links. Their shared storage
has one canonical owner: contents are not copied to both blocks. Remote transfers
and menu operations pay their verified FE fees. Unloaded/unlinked or changed
owners stop access. Remote dropping/throwing actions are intentionally denied so
items cannot bypass the shared-storage transaction rules.

## Acceptance still required

The [native artwork gallery](images/full-art-rollout-v4/README.md) is made from
actual PNGs, not client captures. Please review menu readability, shift-click,
Moonsteel in both hands and item frames, worn armor fit, and shaders/particles in
the CurseForge client. Moving cargo inside pipes needs a later client renderer.
Third-party claim/team adapters and additional biological/module rules remain
listed in the [workflow ledger](sol-build-workflow-2026-10-05.md).
