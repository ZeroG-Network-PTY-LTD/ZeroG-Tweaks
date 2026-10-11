# Solar Shrine: Solvane template rewards

Two original small19×9×19 open-air Sunwarden courts use existing Solar Stone, Radiant Bricks, Gildwood and Fusion Lamps. A continuous central approach leads to one chest with clear lid space. Two damaged cornice variants reuse the same approved artwork and unchanged `chests/solar_shrine` rewards.

## Habitat and discovery

Eligible habitats are Solvane's Corona Flats, Sunspot Plateaus and Gildwood Oasis. Dry-land terrain checks reject unsuitable sites; no forced placement is enabled. Initial random-spread spacing40/separation20 chunks and32-block local search are not guaranteed distances or final rarity balance. Existing explored chunks and the hub are unchanged.

With commands enabled: `/execute in zerog_tweaks:solvane run locate structure zerog_tweaks:solar_shrine`. Ordinary natural placement, survival traversal and client visual approval remain distinct from a structure lookup or isolated generation test.

## Rewards and story boundaries

The chest can hold Photium, Radiantine, Astrium and Solvanite upgrade templates. These are chance-based existing rewards, not guaranteed per chest. The shrine does not grant the Heart of Solvane or implement the Dying Star, Sun Colossus, Sunwarden hymns, dialogue or ending choice. Unwritten story text remains pending approval.

The three recently added small structures now provide source routes to all twelve previously unbound later-tier gear templates. This is not a completed boss/key ladder or proof that every natural world contains an accessible ruin.

## Verification

Runtime/Design templates match byte-for-byte. The source graph traces eight structures with zero missing references. Isolated checks cover eight rotated shrine placements, walkable approach, real chests, nine lamps, loaded reward rolls, exclusion of Heart loot, habitat membership and bounded native Solvane generation. Combined gate/Vault/Spire/wreck/forge regression and ordinary natural-world evidence are separate acceptance checks.

Next: ordinary-world verification of all three new structures, remaining Concord ruins/signature mobs and approved encounter work. Undefined bee research, final story text, hazards and exact survival costs are not invented.

All fifteen required combined tests passed in `20261011_045923_runWorkflowTests.log` (11.57 seconds of test execution,1m39s including build/startup). Both shrine checks and the thirteen previous gate/Vault/Spire/wreck/forge regressions passed. The disposable server saved and stopped normally.

## Same-version delivery

Normal clean build passed in48 seconds (`20261011_050103_clean.log`). Asset audit checked7,979 models,1,529 blockstates,3,963 PNGs and130 animation metadata files with zero errors. Shrine templates ship without optional test classes/fixtures.

Installed while the ZeroG client was closed: `zerog-tweaks-1.21.1-1.0.12-dev.jar`, SHA256 `20a718564309989977c53ad0e870cb4d7d3be0e8b6241b4776055f088a57bf54`. Previous JAR is recoverable under `zerog-mod-backups/20261011-050224-UTC`. Dependencies, saves, hub and disabled custom weather were unchanged. Distribution JAR/checksum and `solar-shrine-assets-20261011.json`/`solar-shrine-install-20261011.json` receipts are on Docs.
