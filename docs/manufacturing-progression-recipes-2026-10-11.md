# Manufacturing recipes across the existing progression

The owner clarified material progression, then continued after the proposed starting costs. This batch enables **two ingots → one compressed plate** and **four ingots → one cog**, using only the 21 already registered dimension-metal families. There are 42 shaped recipes and 21 recipe-book unlocks, granted on obtaining each metal's ingot. No vanilla/Nullifite parts or gem cogs are added.

This is initial manual crafting at a crafting table; a plate can also fit the player crafting grid. A compressor machine, machine FE costs and broader machine recipe balance remain future work. Neither part has a reusable ingot remainder or a reverse conversion recipe.

## Selected casing stages

| Progression step | Casing | Dust | Required previous core |
| --- | --- | --- | --- |
| 6 | Cyrrium | Pulsar Dust | Iron block |
| 9 | Tectium | Tremor Dust | Cyrrium casing |
| 12 | Wraithsteel | Spectral Dust | Tectium casing |
| 15 | Astrium | Fusion Dust | Wraithsteel casing |

All four use this pattern, producing **two casings**:

```text
Plate   Cog       Plate
Dust    Core      Dust
empty   StarGlass empty
```

Each batch uses two plates, one matching cog, two matching dusts, one listed core and one Star Glass. Parts represent eight matching metal ingots per batch, versus four direct ingots previously. Dust count changes from four to two. The existing core progression and two-casing output remain unchanged; these are starting balance values, not final progression approval.

Purple (`star_glass`), blue (`star_glass_blue`) and teal (`star_glass_teal`) are interchangeable via `zerog_tweaks:manufacturing/star_glass`. Plain vanilla glass does not qualify. Empty lower corners reserve design room only; extra items in them currently invalidate the recipe rather than being consumed unexpectedly.

## Sixteen-step numbering

Steps mean the existing tool-profile level minus four: Nullifite 1, Ferrox 2, Moonsteel 3, Olympium 4, Cobaltium 5, Cyrrium 6, Cerulite 7, Ruskite 8, Tectium 9, Skarnite 10, Salvium 11, Wraithsteel 12, Eidolite 13, Photium 14, Astrium 15 and Solvanite 16. Precious branches share their existing levels. This update adds no new mining tiers or sixteen-tier machines.

Star Glass is used only at selected steps above step 1. The earlier baseline remains unchanged. Armour/smithing, tools, gates, machine processing jobs and stored inventories are untouched. Machines that already require these casings inherit the new casing costs; their own recipe patterns are unchanged. Additional recipe families can be updated later without turning every ingredient into a cog/plate requirement.

Original sprites: [component artwork](manufacturing-components-2026-10-11.md). The initial pending-fabrication note there is historical and superseded by this follow-up. Editable recipe source/data: [Design](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Design/docs/manufacturing-components).

## Verification and delivery

All two required isolated gameplay tests passed in 2.302 seconds (`20261011_053601_runWorkflowTests.log`): all 42 loaded part recipes, exact assembled quantities, no reusable metal remainder, too-few ingots, wrong metal substitutions, twelve valid casing/colour combinations, plain glass rejection, missing cog/core and extra items in the empty slots. This tests the actual loaded recipe matching/assembly API, not a full player's crafting-menu click or recipe-book UI approval. The test server stopped normally.

Clean normal build passed in 42 seconds (`20261011_053801_clean.log`). Three source/JAR contracts passed, including byte-identical recipes and unlock data, whitelist, palette/model bindings, predecessor chain and absence of test classes. Asset audit checked 8,021 models, 1,529 blockstates, 4,005 PNGs and 130 animation metadata with zero errors.

Installed the same `1.0.12-dev` build with Minecraft closed. Prior JAR is recoverable at `ZeroG/zerog-mod-backups/20261011-053930-UTC`; hub, saves and dependencies are unchanged. SHA256: `443b7a9c09ea8a67943c397ce2a16476c39987b44c2656b4c94e7bc238ce2ba6`. [Asset report](reports/manufacturing-recipes-assets-20261011.json) · [Install receipt](reports/manufacturing-recipes-install-20261011.json).
