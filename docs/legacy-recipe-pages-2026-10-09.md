# Legacy machine recipe pages — 9 October 2026

This delivery extends the existing read-only recipe browser to **Silk Weaver,
Centrifuge and Starmetal Smelter**. It does not change their recipes, inventory
indices, automation, card storage or world saves.

## Using the browser

Open the machine and choose **Recipes**. The side panel contains Items, Recipes
and Upgrades tabs. Select an ingredient or product to see matching combinations;
All clears the filter. Previous/next controls step through complete recipes.
The panel is hidden when insufficient screen space is available. It does not
autofill slots or move items.

Each page describes input quantities, outputs, whether catalysts are consumed,
and base/current energy and duration. The catalogue reads the installed addon's
actual processing methods rather than guessing from its accepted-item list.

| Machine | Verified processing | Upgrade contract |
| --- | --- | --- |
| Silk Weaver | One silk thread → one woven silk; 200 work calls; no FE or pattern required. Recovery slots stay recovery-only. | No machine cards supported. |
| Centrifuge | Seven registered comb combinations; exact product counts shown individually. | One Acceleration and one Energy Coil card, tiers 1–6. |
| Starmetal Smelter | One stardust plus one consumed redstone flux → three Starmetal nuggets. Flux belongs in slot 2. | One Acceleration and one Energy Coil card, tiers 1–6. |

Centrifuge and Smelter base jobs take 201 successful work calls. The page reflects
the existing cumulative job rounding, configurable FE cost and installed cards.
Current approved caps remain 2.5× speed and 30% whole-job energy saving. Neither
machine advertises Compact or Void support. Exact survival card costs remain
deferred.

## Verification and limits

- Red-before-green: both required tests initially failed on missing recipe pages.
- Isolated addon-loaded server: both tests passed, covering all seven comb recipes
  and the Smelter recipe at no-card and tiers 1–6: **56 paid jobs**, plus Weaver.
- Actual outputs, consumption, duration, energy and non-mutating output browsing
  matched the catalogue; Weaver preserved its recovery contents.
- Transcript: `20261008_213707_runWorkflowTests.log` (UTC filename).
- Clean production build passed: `20261008_213939_clean.log`.
- Asset inspection: 7,977 models, 1,528 blockstates, 3,962 PNGs and 129 animation
  metadata files; zero binding errors.
- Client layout, scrolling and readability still require visual approval.
- Missing-addon discovery fails closed; the no-addon branch has not yet received
  a separate isolated test in this delivery.

## Remaining work

Genetics, generator, alveary and other legacy recipe adapters remain pending.
Machine-specific upgrade contracts are only advertised where already verified;
this delivery does not invent unsupported cards or new processing patterns.
Repository candidate only: no installed JAR, hub or player save was replaced.

Candidate: `docs/jars/zerog-tweaks-1.21.1-1.0.12-dev-legacy-recipes-20261009.jar`.
Its SHA-256 is recorded in `docs/jars/SHA256SUMS.txt`.
