# Frozen Outpost

Added two small Concord cold-weather shelter layouts using existing Hoarwood, permafrost brick, salvaged hull plating, snow and spectral lights. One rear roof is damaged; the other is intact. No new textures or story logs are introduced.

The outpost is 17×9×17 blocks with a continuous central floor, clear entrance, sheltered interior and a north-facing reward chest. Rewards use the existing Frozen Outpost table unchanged, including its guaranteed Cryo Core. No boss reward, Vault key, Wisp or new story item is invented.

Natural placement is restricted to Hoarwood Taiga and Phantom Ice Sheets. It uses the existing dry-ground structure logic, rejects unsuitable terrain, has six-block height tolerance, 32-block nearby search and 40/20-chunk random-spread spacing/separation. This does not guarantee one ruin every 40 chunks. No hub demonstration or player-save regeneration is part of this update.

For an authorized creative inspection: `/execute in zerog_tweaks:eidolon run locate structure zerog_tweaks:frozen_outpost`. Existing chunks do not regenerate themselves; newly generated suitable chunks can contain it.

## Lore and remaining work

The repository explicitly permits building Frozen Outpost as a Concord ruin but has no approved story text. Logs, quest writing and dialogue remain pending. Dedicated Sunken Relay, Buried Observatory, Sunken Lab and Impact Site structures are still missing; existing Observatory mine loot is not a dedicated building.

Editable source: [Design generator and layout notes](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/blob/Design/docs/wasteland-ruins/frozen-outpost.md). Eight-rotation gameplay checks use actual containers and loot, not just a model or loot-file existence check. Natural-world rarity, broad seeds and client appearance are separate from that focused regression.

## Test receipt

The focused isolated server run passed its one required regression covering all eight variant/rotation combinations in 2.913 seconds; Gradle/server completed normally in 1 minute 30 seconds. Transcript: `20261011_052754_runWorkflowTests.log`. Optional Productive Bees, ProductiveLib and orbital addon were present. No player saves were used. A first-run missing `server.properties` message was followed by normal setup and completion, not a failed test.

Clean normal build passed in 42 seconds (`20261011_052931_clean.log`), without GameTest classes. Both manufacturing-component checks still pass against the final JAR. Asset audit: 8,021 models, 1,529 blockstates, 4,005 PNGs, 130 animation metadata, zero errors. Both outpost templates are byte-identical in runtime source, Design and JAR. Structure route audit now finds nine configured structures and no missing references; four planned ruin chest routes remain unbound.

Installed with Minecraft closed; previous JAR is recoverable under `ZeroG/zerog-mod-backups/20261011-053053-UTC`. Version remains `1.0.12-dev`. SHA256: `1e76b059f28c2e6dc8e425ebcf2c6f8c4d7cddcadf3ef0524a196ca08efc9d3e`. No saves, hub or dependencies changed. [Asset report](reports/frozen-outpost-assets-20261011.json) · [Route report](reports/frozen-outpost-routes-20261011.json) · [Install receipt](reports/frozen-outpost-install-20261011.json).
