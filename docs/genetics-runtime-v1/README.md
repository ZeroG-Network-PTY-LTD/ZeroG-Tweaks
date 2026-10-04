# Genetics runtime v1 — implementation contract

The approved single-block Splicer and Geno Station from `docs/single-block-machines-v1/` remain unchanged. This work adds behaviour, not a return to the retired helix assembly.

## Verified installed API, not Forestry assumptions

Inspected Productive Bees `1.21.1-13.14.0` and Orbital Bees `1.0.0`. Productive Bees uses filled `BeeCage` items, five trait values and its serialised `productivebees:attributes_handler` attachment. It does not expose the queen/princess/drone chromosome or fertility system assumed in the older draft. Do not invent those properties or a lifespan value for this API.

Supported traits: productivity, endurance, temper, behavior, weather tolerance. `GeneValue.byName`, `getSerializedName` and the enum family validate every value against the installed API. The species/type cannot be spliced. Filled cages without all five recognised saved traits are rejected rather than randomly initialising missing traits.

## Operational slots and preservation

Both machines keep their existing sixteen-slot inventory. Slots 0–2 are specimen, vial/serum, reagent/catalyst. Slots 3–4 are specimen and serum/vial outputs. Slots 5–15 are take-only recovery slots for old inventories and honey-bottle returns. No old stacks are deleted or moved silently; remove old incompatible contents manually.

Analysis marks a returned cage as analysed and displays its real traits in tooltips. Sampling copies one selected trait into the existing `aeroapiary:trait_serum` item, under validated `zerog_tweaks:trait` custom data. It returns the specimen unchanged apart from the analysis marker. Splicing updates only the chosen PB attachment field on a copy, preserving species, identity, other attachments and item components. No fabricated second chromosome or sampling fertility penalty.

## Timing and power

- Analyse: 100 ticks at 20 FE/t; without sufficient power, 400 ticks.
- Sample: 300 ticks at 20 FE/t; without sufficient power, 1,200 ticks.
- Geno Station: 10,000 FE receiving-only buffer.
- Splice: 400 powered ticks at 60 FE/t; 40,000 FE buffer; pauses without power.
- Royal jelly: 75% success. Cosmic jelly: 100%. Failure returns the unchanged specimen and empty vial, consuming one serum and catalyst.
- Sampling uses one blank vial and one honey drop or honey bottle. Analysis consumes only the honey reagent. All honey bottle containers are returned.

Inputs are fingerprinted by their complete component data. Changing them cancels the job without consuming ingredients. Outputs must have space before progress/power use, and again before commit. Jobs never run on background worldgen threads. FE and job state use the existing block entity's persistent data.

## Interface and automation

The server menu exposes selection, Analyse, Sample, Splice and Cancel through vanilla container-button packets. The server checks the machine's identity, existence, dimension and player distance; clients cannot submit a fabricated trait value. Shift-click targets accepted inputs or the player inventory. Recovery and output slots reject insertion.

An optional integration replaces only the addon's two placeholder tick/filter branches. The addon's item capability is wrapped for these machines only: insert into accepted inputs, extract from outputs/recovery, never steal the specimen. An addon update changing the verified integration signatures must be reviewed, not silently allowed to resume placeholder smelting.

## Evidence boundary and next stages

Compilation is not runtime proof. Isolated NeoForge tests cover the actual optional integration, PB cage data, jobs, containers, FE, filters and save/load before installation. The client visual layout still needs review. No provider art jobs were used.

Still separate work: jelly fluid catalyst tank, research tier caps, complete alveary 27-frame backend, transport networks, remaining artwork audit. Do not claim these are implemented by the genetics runtime.

Code belongs on `1.21.x`, this contract on `Design`, player guide/test receipts/JARs on `Docs`. Keep versions unchanged for this development update and preserve old jars outside the active mods folder.
