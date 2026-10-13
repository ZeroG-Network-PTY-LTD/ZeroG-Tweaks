# Gas storage: existing ZeroG shells

Approved scope: Oxygen and Hydrogen measured in mB. Use the six existing ZeroG
tank shells; do not introduce a separate gas-only tank registry or third-party dependency.

| Tier | Shell | Capacity (mB) |
| --- | --- | ---: |
| 1 | Copper | 5,000 |
| 2 | Nullifite | 20,000 |
| 3 | Cyrrium | 100,000 |
| 4 | Tectium | 500,000 |
| 5 | Wraithsteel | 2,000,000 |
| 6 | Astrium | 5,000,000 |

Creative catalogue: empty canister, Oxygen canister, Hydrogen canister and twelve
prefilled tanks. Full canisters contain 1,000 mB. Tanks preserve native block-entity
data and refresh their fullness gauge after placement. No fake bucket or placeable
gas-liquid block is added.

Reuse existing gas wisps and tank frame artwork. The placed tank renderer already
fills the chamber with a translucent gas wisp rather than drawing a liquid pool.
The tank screen identifies gas and shows exact amount/capacity with world-face
configuration controls. Inventory shell models are unchanged in this batch;
contents are identified by hover text. Dedicated inventory chamber artwork remains
a visual-review task, not a claimed completed redesign.

Do not treat fill percentage as real-world pressure or invent chemistry/temperature
rules. More gases require an approved specification.
