# Generator side controls — work in progress

Solar Array and Fusion Reactor now expose independently configurable power-output faces through a colour-coded world-face panel. Existing saves default to output on every face; power rates, capacity, fuel costs and upgrade limits are unchanged.

The server validates menu commands against the actual block entity and player distance. Disabled faces block both active pushing and capability extraction. Previously cached capabilities remain invalid after a disable/re-enable round trip. The face mask is persisted in block-entity data.

Verification: the new regression first failed with “Generator disable-output GUI command is missing”. After implementation, all 69 required isolated workflow tests passed. This is server verification, not visual gameplay approval.

Still pending:

- Fusion Reactor fuel-face controls and actual hopper/cable routing coverage.
- Remaining generator, genetics and legacy-machine side controls.
- Machine-specific upgrade audit, transport animation, advanced alveary research/biology and planetary ecology checks.
- Exact survival recipe costs, intentionally deferred by the user.
- Moonsteel contributor commits: 8e6cc347, ab957229, 50be60ea, eb5e52ad, 26f7b9ef and e864569a. These were not available from the verified remote heads; reconciliation is deferred at the user's request. Do not reconstruct their changes from descriptions or restore old armour shells automatically.

Installed same-version JAR: `zerog-tweaks-1.21.1-1.0.12-dev.jar`, SHA256 `9e5dbf16f0329957a21c3408dc647639af9a318062456fd369f9f1052939eec1`. The previous JAR is recoverably backed up; saves, hub terrain and dependencies are unchanged. A clean production build and a final incremental build passed; the packaged output-only legend was checked directly. The final asset audit checked 7,937 models, 1,522 blockstates, 3,893 PNGs and 96 animation metadata files with zero errors. These checks do not certify client appearance.
