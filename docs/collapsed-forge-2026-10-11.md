# Collapsed Forge: volcanic smithy ruins

This original small ruin implements the Galaxy3 tracker's forge reward route: two17×8×19 damage variants with a Scoria foundation, Scorched Marble supports, Charwood beams/workbench, cold blast furnace, anvil and one chest. It uses existing artwork and unchanged `chests/collapsed_forge` loot. No new smith dialogue, active machine processing or Rift Tyrant encounter is added.

## Finding one

Search newly generated Ember Fields, Marble Contact Zone or Charwood Barrens on Skarn. Volcanic wasteland Ash Plains and Basalt Fields also permit placement. Lava Lakes are excluded; dry-land preflight can reject unsuitable sites. Initial spacing40/separation20 chunks is not a guaranteed distance between ruins or final rarity balance.

The central passage opens at both ends. Approach the chest from the workshop floor; its lid has clearance. Chest rewards can include Ruskite, Pyrium, Tectium and Skarnite upgrade templates and existing Heatproof Plating salvage. Templates are chance-based, not guaranteed in each chest.

With commands enabled: `/execute in zerog_tweaks:skarn run locate structure zerog_tweaks:collapsed_forge`. A successful locate alone does not prove a naturally placed accessible chest; natural discovery and client inspection are separate acceptance checks.

## Verification and boundaries

The source graph now traces seven structures with no missing references and binds the previously unbound Collapsed Forge chest. Design/runtime generated templates match byte-for-byte. Focused tests check eight rotated placements, walkable entry/chest routes, actual chest entities, loaded loot rolls, habitat membership and native Skarn generation. This is not proof of an ordinary survival-world journey, final rarity balance or a completed Galaxy3 boss/key ladder.

Existing saves, explored terrain, approved gates and the hub remain unchanged. Solar Shrine, larger encounters, Rift Tyrant/Captain/ending mechanics and undefined research/survival costs remain on the TODO list.

Both focused tests passed in `20261011_042556_runWorkflowTests.log` (3.420 seconds of test execution); the disposable server saved and stopped normally. A combined gate/Vault/Spire/wreck regression run is a separate delivery check.

All thirteen required combined tests passed in `20261011_042735_runWorkflowTests.log` (10.02 seconds of test execution). This includes the corrected live-controller reload boundary, Vault/Spire checks and both wreck/forge test pairs. The disposable server saved and stopped normally.

## Same-version delivery

Clean build passed in41 seconds (`20261011_042911_clean.log`). Asset audit checked7,979 models,1,529 blockstates,3,963 PNGs and130 animation metadata files with zero errors. Both forge templates ship; isolated test classes/fixtures do not.

Installed into the ZeroG CurseForge mods folder while its client was closed: `zerog-tweaks-1.21.1-1.0.12-dev.jar`, SHA256 `0c970535d33f739b5a232d09af1033cc0a8aa621b3c1bde06a2861cdfb819443`. Previous JAR remains recoverable in `zerog-mod-backups/20261011-043009-UTC`. Dependencies, saves, hub and disabled custom-weather setting were unchanged. Asset/installation receipts are under `docs/reports/collapsed-forge-*-20261011.json`; the separately named distribution JAR and checksum are on Docs.
