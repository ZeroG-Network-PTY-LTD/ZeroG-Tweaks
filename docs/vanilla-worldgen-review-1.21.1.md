# Minecraft Java 1.21.1 world-generation reference review

Reviewed locally on 2026-10-04. This is an inspection report, not a claim that
all proposed planetary features have been implemented or visually verified.
No vanilla templates or textures are redistributed with this report.

## Sources inspected

- Actual vanilla resources from the NeoForm cache:
  `stripServer_8bb3d3745bd6f4ac9d34d27c8a1809cf14c56fdd_resourcesOutput.jar`.
- Mapped Minecraft/NeoForge sources:
  `build/moddev/artifacts/neoforge-21.1.252-sources.jar`.
- Current local ZeroG `1.21.x` dimension JSON and ecology feature sources.

The vanilla resource archive contains **483 village structure NBT templates**.
These are Minecraft-native block/state/entity templates, not Blockbench models
or WorldEdit `.schem` files.

## Settlements: modular layouts rather than one repeated building

Vanilla plains villages use `minecraft:jigsaw`, the
`village/plains/town_centers` start pool, size 6, a maximum distance of 80,
`WORLD_SURFACE_WG` projection and `beard_thin` terrain adaptation.
The village structure set uses random-spread spacing 34 / separation 8 chunks.
These values describe vanilla, not approved ZeroG placement settings.

The town-centre pool has four ordinary alternatives of weight 50 each and four
zombie alternatives of weight 1 each. Processors provide controlled material
variation, such as mossification. Connector name, target, pool and orientation
join streets, houses, farms and occupant templates.

Three actual NBT templates were decoded:

| Vanilla template | Bounding size (X/Y/Z) | Stored block entries |
| --- | --- | --- |
| `plains_small_farm_1` | 7 / 6 / 9 | 126 |
| `plains_small_house_1` | 7 / 7 / 7 | 343 |
| `plains_meeting_point_1` | 10 / 7 / 10 | 153 |

The farm connects to streets through a `building_entrance`. The house also
connects to a villager pool. The meeting point has street connectors and pools
for villagers, cats, an iron golem and a well bottom. These sampled templates
have no direct entity entries: occupants are not necessarily embedded in each
building template.

ZeroG implementation direction: several authored 3D layouts with compatible
connectors, optional farms/hives, weighted variants and planet-specific biome
eligibility. Domes must randomly use reinforced clear or planet-coloured glass,
**not Star Glass**. Vanilla villager faces remain unchanged; variation belongs
to clothing. This report does not implement these new layouts or clothing.

## Regionalization: climate selection is separate from terrain shape

`Climate.ParameterPoint` selects biomes using temperature, humidity,
continentalness, erosion, depth and weirdness, with an offset penalty.
The density/noise router and surface rules shape terrain and its materials;
adding a biome does not itself make a cave, mountain or lake.

`OverworldBiomeBuilder` assigns underground biomes a depth range of 0.2–0.9.
Lush caves prefer humidity 0.7–1.0; dripstone caves prefer continentalness
0.8–1.0. Deep Dark uses depth 1.1 and restricted erosion. These are noise-space
values, **not block heights**.

Current ZeroG comparison: Cerulon already has depth-aware biome assignments,
including `starlight_caverns` at 0.2–0.9 and `geode_depths` at 1.1. The other
33 dimension definitions currently use depth 0 only. They can still have caves
from terrain/carvers, but do not select distinct underground biomes through
their current multi-noise entries. Preserve Cerulon's newer regional work;
do not overwrite it with a simplified blanket generator.

## Caves: carving, water and decoration are separate systems

Both vanilla lush and dripstone biome data reference cave,
`cave_extra_underground` and canyon carvers. The cave carver checks
`minecraft:overworld_carver_replaceables`; custom planetary stone must be
eligible in the intended carver configuration for it to be carved.

Lush caves combine ceiling moss, cave vines, clay/water patches, floor
vegetation, rooted azalea, spore blossoms and glow lichen. Dripstone caves put
large dripstone in local modifications and clusters/pointed dripstone in
underground decoration. Ores occupy step 6, underground decoration step 7,
springs step 8 and vegetation step 9. Feature ordering must remain compatible
across biomes sharing a generator.

The placed cave-vine feature samples height, scans upward through air for a
sturdy downward face (maximum 12 steps), offsets one block down and applies a
biome filter. Ceiling moss uses a similar scan. These are useful patterns for
alien hanging plants: validate attachment and fluid compatibility rather than
placing them indiscriminately.

## Trees and the current coverage gap

Vanilla plains tree placement combines weighted count, horizontal spread,
surface-water-depth filtering, `OCEAN_FLOOR` height selection, a sapling survival
predicate and biome filtering. Trunk placement also handles the supporting dirt
and NeoForge's `onTreeGrow` hook.

The current ZeroG fertile-patch feature permits only a fixed surface-material
list and places trees only after a successful patch, an additional random roll
and a grass-support check at the origin. The inspected noise surface rules use
several materials absent from that list, including `frozen_regolith`,
`crater_dust`, `mare_basalt`, `ashfall` and `corona_crust`. This is a concrete
coverage mismatch to investigate, **not proof of the sole tree-generation
failure**. The current small hub-test samples contained no tree logs; broader
sampling and targeted generation tests are needed before declaring trees absent
or repaired.

## Verification boundary

This review decoded real vanilla NBT/JSON and read mapped source code. It did
not launch a client, alter saves, change gameplay code, commit, push, install a
new JAR or certify the appearance/frequency of new planetary structures.
The existing isolated hub pass proves travel routes, not complete ecology.
