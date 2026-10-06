# Mining, refinery, transport and jelly repairs

Minecraft Java 1.21.1 / NeoForge. The version remains **1.0.12-dev**.
This is a focused repair batch, not completion of the entire shared-systems queue.
Existing saves, dimensions, registry IDs and the inspection hub are preserved.

## What changed

### Mining progression

All 39 ore registrations in `BlockInit`, plus Cerulite Cluster, now require the
correct tool for drops. Existing material-tier tags still determine which pickaxe
is valid. Planet mineral registrations already had this property. Soil, farmland,
wood and plants were not indiscriminately assigned pickaxe requirements.

The regression uses a survival player: bare hands and a wooden pick fail Cerulite
harvest eligibility, while its appropriate custom pick succeeds. Another check
covers every registered ZeroG block carrying a `needs_*_tool` tag.

### Ore Refinery

The old free five-input table is replaced by the registered `refining` recipe type
and shared powered processing terminal. Its block, item and block-entity IDs stay
unchanged. There are **79 recipes**: 39 authored ore routes, 38 raw-material/storage
block routes, and native/optional-addon Stardust boost routes.

Ores follow the authored outputs: metal ores generally produce raw materials;
raw materials refine into ingots. Gems/dusts retain their corresponding outputs.
Raw storage blocks represent nine units, not one: Raw Nullifite Block gives
**18 ingots**, or **27** with a casing upgrade, at nine times the raw-unit energy.

Physical slots remain input 0, catalyst 1, output 2. Three independently bounded
upgrade slots follow them. A casing uses each recipe's authored upgraded count;
Cryo Core and efficiency dust retain the shared processing rules. Output space
is reserved using the upgraded count **before** energy is spent.

Top/left/right feed reagents, rear feeds catalysts, and front/bottom expose output.
Energy is a real FE capability. Upgrades are inserted in the terminal, not through
incidental automation slots. Configurable processing-machine sides remain pending.

Old three-slot saves expand safely to six slots. Old unpaid progress is reset;
modern paid progress, stored energy, inventories and upgrades survive reload.
The legacy menu ID remains registered, but normal interaction opens the shared
powered menu. Unrelated catalysts are not consumed.

### Transport

Loaded connected networks no longer silently fail at 257 nodes. Traversal visits
accepted nodes once and never loads remote chunks. One leader still owns the
network transfer budget; the change does not multiply throughput per segment.

Routing changes from any connected terminal propagate to the connected loaded
nodes. “Nearest” keeps port priority first, then compares breadth-first pipe-path
distance from the actual buffered source. It does not use the leader's position
or straight-line distance. Round-robin/random choices remain available.

A disabled face no longer marks an otherwise reachable node as visited too early:
an alternate path still includes that node in the shared rate and safety checks.

Hazardous fluids must be supported by **every connected pipe**. Simulation and
real insertion reject an unsafe mixed-tier network. Buffered fluid also cannot
be delivered through that unsafe network. Fluid buffers are retained, not deleted.
This is conservative whole-network protection, not selective safe-branch routing.

### Royal and Cosmic Jelly

Both have independent source/flowing IDs, liquid blocks, collectable buckets,
client texture registration, translucent rendering and coloured underwater fog.
The Liquids creative category discovers their buckets automatically.

With the orbital addon installed, four jelly items plus an empty bucket make
1,000 mB; the reverse returns four items and the bucket crafting remainder.
This preserves the existing **250 mB per genetics job** and existing success
chances. No new synthesis balance or required dependency was invented.

Right-clicking a genetics terminal with a fluid container now attempts a real
server-side tank transfer. Other ordinary held items open the modern terminal;
wrenches and sneak block-placement keep their own actions.

The fluids reuse approved original gold/midnight honey artwork. Dedicated jelly
artwork and standalone survival obtainability remain pending, not falsely presented
as newly approved art. Buckets remain available for creative inspection without
the optional addon.

## Verification

The original bugs were reproduced before their fixes: bare-hand eligibility,
257-node loss of budget, ignored nonleader routing, wrong nearest chest, unpaid
refinery production, absent jelly source, hazardous mixed-tier fill, missing bucket
interaction, missing cluster tool flag, and alternate-path traversal.

**73 required isolated server tests passed with Productive Bees and the orbital
addon installed**, including the repaired workflow, source bucket placement/pickup,
actual bucket-to-splicer interaction, bounded upgrades, output reservation and
paid-job save/reload. Transcript: `20261006_152111_runWorkflowTests.log`.

**11 blocker tests also passed without the optional bee addons**. These overlap
the larger suite and are not 11 additional distinct tests. Transcript:
`20261006_152337_runWorkflowTests.log`. The final production build, asset audit and installation
receipt are recorded with this delivery. Server tests do not approve GUI layout,
shader rendering, worn armour or actual player travel in the graphical client.

## Next work, in order

1. Survival recipes for bee machines, frames, consumables and standalone jelly.
2. Committed energy pulses, proper fluid waves, and defined gas IDs/units/networks.
3. Validated side configuration for remaining machines.
4. Larger authored alveary shells, detailed formation-error display, honey-production
   tank routing, and hive discovery by newly spawned/bred bees.
5. Concord Codex advancement research gates. This is the approved mechanism;
   per-trait unlock mapping/caps still need an explicit specification. Undefined
   lifespan, climate, territory and module rules are not invented PB APIs.
6. Recipe discovery guide or optional JEI/EMI; guardian/template progression,
   missing structures/mobs, later chapters and broad planetary ecology checks.

Existing historical documentation and images remain intact. Code belongs on
`1.21.x`, generators/design notes on `Design`, and guides/JARs/checksums on `Docs`.
