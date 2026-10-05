# Machinery and service-port hub — 6 October 2026

## Shipped in the same-version build

Version remains 1.0.12-dev, Minecraft Java 1.21.1 / NeoForge. The installed predecessor was backed up; existing player saves and other mods were retained.

- Alloy Forge, Crystal Growth Chamber and Salvage Station have actual recipe processing, reserved jobs, power handling, outputs and sided ports. Their upgrade limits are bounded; this does not certify every legacy machine's upgrade contract.
- Solar Array and Fusion Reactor use configurable conservative defaults. Roof obstruction and fuel/power behavior have isolated regressions. Solar Plasma fuel/cooling remains unspecified, not silently invented.
- Ordinary and sneak empty-hand combustion interactions now reach the same dedicated generator menu. Fuel information stays within that container. Live machine interactions no longer compete with decorative blueprint previews; held-tool actions remain separate.
- Silk Weaver pattern processing was audited and the ignored-pattern consumption repaired.
- Alveary service formation accepts two item ports, two fluid ports and one energy port on the bottom exterior, with the controller in a second-row casing position. External connections belong to service ports, not direct controller capabilities. Loaded-only ownership and ambiguous-owner rejection preserve native buffers.
- Transport and tanks have server-validated six-face configuration in a colour-coded 3×3 panel: red input, green output, purple both, grey disabled. Blank cells are not fictional extra sides. This is not an all-machine configuration backend.
- Original 32-pixel item-tube artwork, green-core cells and nine charge gauges replace 27 textures, with editable Design sources. Transient item/fluid motion cues are implemented; client approval and dedicated pulse/conservation cases remain pending.

## Fresh inspection world

Open **ZeroG Planet Showcase — Service Ports — Seed 0**, folder `ZeroG_Planet_Showcase_1_0_12_ServicePorts_Seed0`, seed **0**. The old saves were not deleted or reset.

The gallery north of spawn contains twelve validated **5×5×5** service shells, powered output cells/cables, six supplied machine inspection stations, six-tier transport/tank samples and external genetics/cryo references. Ten safe Concord Vault room exhibits are inspection layouts, not completed new boss combat. Ingredients in supply chests require manual placement; a station is not proof of every automation configuration.

The export records 34 destinations, 68 gates and 60 nearby inspection villages. Limited machinery chunks are kept loaded in this explicit admin hub only. This is a bounded test-world export, not an assertion that entire infinite planetary dimensions are pregenerated.

**Larger seven-wide authored alveary concept shells are still unsupported.** Replacing misleading hub examples with valid five-wide shells does not implement those larger formation rules.

## Evidence and limits

The clean production build passed and excludes GameTest fixtures. Earlier isolated workflow runs passed 59 and then 61 required checks; the final hub suite passed nine. These are separate runs, not a summed unique-test count.

The final hub checks cover formation, alternate ports/controller positions, wrong roofs, smoker, liquids, residents, atmosphere, crops/caves and destination/gate records. With Productive Bees installed, mock login does not negotiate its bee-data payload: **real player dimension travel was not tested by that run**. No production validation bypass was introduced. Real-client travel, visual GUI sizing, GPU rendering and complete ecology still require playtesting.

Base ZeroG integration with Productive Bees is optional; the separately installed Orbital Bees addon has its own dependencies. No Mekanism code or textures were copied.

## Prioritised remaining workflow

1. Client acceptance: both click modes, shift-click, side buttons, port routing, terminal facing, moving items/fluids, charge gauges and actual gate travel with installed addons/Iris.
2. Add dedicated successful/blocked transfer-pulse tests, reload safety and resource conservation; complete liquid wave visuals, directional power pulses and the actual gas registry/units/network before gas animation.
3. Extend real side-configuration backends to remaining machines; audit each compatible upgrade and bounded speed/efficiency rule. Add distinct input/output hatch artwork where still missing, rather than fake state indicators.
4. Specify and implement larger authored alveary geometries and remaining climate, lifespan, territory, gravity, rotor/coil/drone rules against verified APIs. Gene/cryo modules remain external, not invented shell sockets.
5. Approve Solar Plasma/cooling and processing-fluid quantities before adding these contracts. Complete holographic diagnostics only when attached to actual state.
6. Audit all planetary ecology over broader terrain samples: matching trees, crops, vines, cave vegetation, liquids, villagers, structures, ores and suitable mobs. Small samples are not full ecological approval.
7. Complete claim/team adapters, remaining mob mechanics and boss phases, and outstanding art review. Unapproved texture changes remain pending examples/approval.
8. Reconcile the newer Sol and Galaxy 2–5 design trackers against actual runtime; preserve their story/progression requirements and update completion only with evidence.

The machine-readable [TODO ledger](storage-and-machinery-todo.json) is the current status source. [Latest Design trackers](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Design) and [editable transport source](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Design/docs/transport-machinery-v2) remain on Design, never merged into code.
