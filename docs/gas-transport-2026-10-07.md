# Oxygen, hydrogen and committed transport visuals

Minecraft Java 1.21.1 / NeoForge. Same development version: **1.0.12-dev**.

## Original contained gases

The owner approved oxygen and hydrogen in **mB**, with original gas artwork rather than generic placeholders. They are registered as `zerog_tweaks:oxygen` and `zerog_tweaks:hydrogen`. They are contained gases, not placeable water-like liquid blocks: no gas oceans, breathing benefits, explosions or pressure damage are invented.

The **Refillable Gas Canister** (`gas_canister`) holds up to **1,000 mB** of one gas. Partial filling/draining is supported. Contents persist in a synchronized item component; the icon changes between empty, cyan oxygen and violet hydrogen, with an exact quantity tooltip. Ordinary liquid insertion and oxygen/hydrogen mixing are rejected. Filled examples are in **Storage & Transport**, alongside the empty canister.

Existing tanks and fluid ports use standard fluid capabilities and can hold these gases. Right-click a storage tank with a canister to exchange contents; its face permissions still apply. Gases render as translucent animated chamber wisps rather than a liquid pool. Exact recipe costs and survival gas-production machinery remain pending: creative gas examples are not a completed survival production chain.

## Six gas-tube tiers

Gas tubes (`<tier>_gas_tube`) have original 32-pixel chamber textures and six-unit cross sections. They do **not** join ordinary liquid-pipe networks. Tubes support existing side controls, filters, redstone, priorities, loaded-only routing and family-matched tier upgrades.

| Tier | Shared network maximum |
| --- | ---: |
| Copper | 250 mB/t |
| Nullifite | 1,000 mB/t |
| Cyrrium | 4,000 mB/t |
| Tectium | 16,000 mB/t |
| Wraithsteel | 64,000 mB/t |
| Astrium | 256,000 mB/t |

The weakest connected segment sets the shared rate, not a separate allowance per pipe. Each tube retains the existing 16,000 mB internal buffer. Connected tubes reject mixing different gases. Disabled faces block exchange. Failed delivery must retain source contents; simulations must not mutate storage. Standard fluid ports and tanks are shared containers, not new pressure-rated equipment.

## Transport cues

Successful FE deliveries now create directional client pulses. Blocked deliveries create none. Junction cues move through the centre instead of cutting diagonally through the casing. Liquid cues use the fluid's registered flowing sprite with undulating ribbons; gas cues use dedicated eight-frame oxygen/hydrogen wisps. These are sampled, short-lived cues of committed transfers, not exact live volume simulations or extra resource ownership. Packet emission is throttled and long routes are sampled to bound network traffic.

![Original native gas artwork—not an in-game screenshot](images/gas-transport-v1/native-preview.png)

## Verification and remaining work

The first canister regression failed because oxygen was unregistered; the first network regression failed because gas tubes were unregistered. Subsequent targeted checks verify canister simulation/capacity/persistence, gas separation, mixed-tier limits, actual/blocked deliveries and tube persistence. Automatic tick routing and standard canister exchanges are included in the final regression batch. The delivery receipt records the final passing counts, production build, source/JAR asset checks and installation checksum.

The expanded suite also caught an obsolete refinery expectation: it attempted new casing insertion despite the approved card-only migration. Its updated boundary test rejects new casings but retains a pre-existing legacy-casing fixture to verify upgraded output reservation, energy payment and reload. No old casing insertion is re-enabled to satisfy a stale test. The delivery tool now retains all unfinished TODO statuses in its receipt rather than silently omitting specification/deferred states.

All **109 required regressions passed** in `20261007_012250_runWorkflowTests.log`. The clean production build passed in `20261007_012512_clean.log`. Packaged-source checks covered 48 files; the full audit checked 7,977 models, 1,528 blockstates, 3,943 PNGs and 120 animation metadata files, with zero errors. Production excludes the opt-in test classes and fixtures.

The same-version JAR was installed into the ZeroG CurseForge instance before publication, with its predecessor backed up. SHA256: `cee28b1f252406c72df4675b23a8c7adc055fa623200db135ace363fff041101`. No hub or save was modified. See [delivery receipt](gas-transport-delivery-2026-10-07.json) and [archived JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-gas-transport-20261007.jar).

Server checks and source previews do **not** approve client appearance, animated readability, shader compatibility or all modpack interactions. Client review remains pending. Recipe production/costs, broader per-machine upgrade contracts, advanced alveary research/biology and large planetary ecology audits remain on the shared TODO ledger. The existing four-key Concord Lock sequence remains intact; separate galaxy-tier key items still need their own audit, not a replacement unlock rule.

Runtime belongs to **1.21.x**, original art/models/generator to **Design**, and this guide/images/JAR/checksums to **Docs**. Saves and hub are unchanged in this batch. No Mekanism code/assets/dependency are introduced.
