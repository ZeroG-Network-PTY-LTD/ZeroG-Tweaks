# Machine interfaces and powered legacy processing — 7 October

Minecraft Java 1.21.1 / NeoForge, same-version **1.0.12-dev** hotfix.

## What changed

- Centrifuge and Starmetal Smelter now expose real energy capabilities to ZeroG conduits. Existing recipes and output quantities are preserved.
- Configurable server defaults: `centrifugeFEPerWorkTick = 20`, `starmetalSmelterFEPerWorkTick = 80`. Their persistent buffer holds 40,000 FE. Work pauses without sufficient power; blocked outputs and idle machines spend no processing energy. Existing 200-step jobs include a charged completion tick.
- Combustion's fuel catalogue opens left of the complete machine/player-inventory panel. It lists the backend's accepted fuels, actual burn ticks, item images and alphabetical names within tag-derived categories; dust remains excluded.
- Processing, legacy workshop and genetics screens gain accepted-input catalogues using their real recipe predicates or slot filters. These are **not** a complete input/output recipe browser. Encoded bees and serums still require valid saved genetics, not merely a generic catalogue item.
- Silk Weaver and Starmetal screens identify unused slots as extraction/recovery only. Their purpose, cycle and energy labels no longer share the same text region.
- Solar/Fusion headers and capacity text are bounded; Solar has no misleading fuel slot. Tank/transport labels are bounded too.
- Genetics retains all slots but uses a 240-pixel-high layout with one recovery row and non-overlapping player inventory. Full state remains available through header tooltips.

## Verification and limits

All **83 required isolated NeoForge gameplay tests passed**, including real conduit charging, no-power pauses, blocked-output conservation, actual smelter output, centrifuge energy/progress reload, and genetics slot bounds/non-overlap. Build and asset checks are recorded separately with the installed JAR checksum. These checks do not establish client rendering or shader approval.

This changes a menu-state network payload: update both client and server to this same build. Registry IDs and version remain unchanged. No player saves or planetary terrain are modified.

## Still pending

Installed candidate: [archived JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-machine-gui-power-20261007.jar), SHA256 `dfb44fc2d7619abbdbad3bc3a1d11bb3c0129862f6ba330db132a76ab849a1aa`. Clean production build passed; asset audit checked 7,937 models, 1,522 blockstates, 3,893 PNGs and 96 animation metadata files with zero errors. The previous installed JAR is backed up under `ZeroG/zerog-mod-backups/20261006-183242-UTC`; other mods are unchanged. Runtime commit: `00cd70c9` on `1.21.x`.

Generator/genetics/legacy per-face controls; bounded upgrade contracts; directional power pulses and liquid waves; specified gases and units; advanced alveary biology/Codex unlocks and seven-wide layouts; full recipe discovery; story and ecology audits; dedicated jelly/port artwork and diagnostics. Survival crafting remains last and awaits exact approved costs. Check the GUI in-game at your chosen GUI scale before visual approval.

Remote Code, Design and Docs were checked: no newer weapon/armour commits were found at the start of this batch. Existing approved armour and tools are retained. No design textures were modified, so no artificial Design commit is needed.
