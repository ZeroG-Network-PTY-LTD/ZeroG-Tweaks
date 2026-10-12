# Owner follow-ups — 12 October 2026

## Current narrowed scope: separator and pressing

Owner approved the cog/ingot/plate concept sheet, then requested prioritizing
Water Separator and a functional Industrial Compressor. The new artwork rollout
is still separate from this functionality build. Terrain profiles are opt-in only
and were regenerated inactive; no live save or dimension was changed.

Industrial Compressor has42 loaded pressing recipes covering21 existing metal
families. Plate Press is reusable tooling:2 ingots ->1 plate,2000FE/100ticks.
Cog Press is reusable tooling:2 plates ->1 cog,4000FE/160ticks. This preserves
the old four-ingot cog material budget. Machine Recipes shows actual counts,
tool reuse, outputs, FE/time and bounded upgrade adjustments. Full output, absent
power or wrong tooling pauses without consuming inputs. Survival crafting costs
for the machine/tooling remain deferred, not silently invented.

Compressor front refuses item/power capabilities, including cached access after
rotation. Other faces have independent item/power controls. No fluid handling is
advertised for this dry process. Separator front refuses item/fluid/power;
other faces accept configured water/gas, FE and supported upgrade cards only.

New machine chassis currently references existing Alloy Forge textures; original
press cube models reference Tectium texture. Dedicated chassis/press pixel art
remains pending. They are not falsely described as the approved cog/plate texture
rollout. Server and asset tests are not client visual approval.

Delivery verified12October: production clean build passed,25 standalone tests
and24 addon-present tests passed. Packaged audit checked8027 models,1531
blockstates,4005 PNGs and130 animation metadata files with zero errors and no
test classes shipped. The combined39-test attempt failed only because nearby
Tidewraith fixtures tripped the intentional population cap; isolated final
groups passed without weakening the gameplay limit.

Installed same-version1.0.12-dev JAR SHA256:
`29e69cec26c4aeac54cf3e0f1d5214a095b60cff629f8fd0f44662d790707cda`.
Old JAR moved recoverably to ZeroG/zerog-mod-backups/20261012-052449-UTC;
dependencies were preserved and only one Tweaks JAR remains. Existing saves,
weather pause and active heightmaps are unchanged. Publication separates code on
1.21.x, canonical guide/diagram sources on Design and this JAR/receipt on Docs.
Unfinished terrain compiler experiments and the multi-seed survey test are
excluded from this publication. No new terrain profile is activated in this JAR.

For creative testing:

```
/give @s zerog_tweaks:industrial_compressor
/give @s zerog_tweaks:plate_press
/give @s zerog_tweaks:cog_press
```

Find the compressor and separator in Functional Blocks; tooling in Ingredients.
Place compressor facing you, connect FE from a nonfront face, insert Plate Press
in the tooling/catalyst slot and2 matching ingots in Input. Check Recipes, then
use Cog Press with2 matching plates. Confirm presses remain and output appears.
Set top to reagent Input, back to tooling/catalyst and bottom to Output for a
simple automated layout. Side controls can select other nonfront faces.
Separator defaults: top Water, east H2, west O2; nonfront FE and card inputs.
Front remains interaction-only for both machines. In-game visual approval and
dedicated compressor/separator/press art remain outstanding.

Current follow-up batch: separator facing/category and regular Tidewraith
behavior are implemented, under final verification. Installed status is recorded
below after delivery; artwork and broader deprecation remain pending.

1. Water Separator: fix its locked placement orientation and put it in the
   functional machinery category. Rotation must not silently mislabel its ports.
2. Bee catalogue: audit obsolete crowned/old apiary blocks and hide confirmed
   unused entries. Preserve saved-world registry compatibility; determine actual
   runtime/recipe/addon use before deprecation.
3. Cogs and compressed plates: match each material's ore/ingot colour palette,
   using the approved magitech artwork and synchronized source generators.
4. Add copper cog/plate components if missing, for later pipes/frame progression.
   Future more complex crafting should retain room for additional components;
   exact costs are still awaiting approval.
5. Regular Tidewraith: submerged survival in non-magma/non-lava liquids,
   high flight, aggressive packs of3-4. Rework the currently installed single-mob
   spawn group/local cap2 together so packs can actually form. Keep boss rules
   separate, and verify each liquid's breathing and hazard path explicitly.

Acceptance details are recorded in `storage-and-machinery-todo.json`. No new
JAR, art approval, crafting costs or save migration is implied by this list.

## Audit findings and boundaries

- Separator lacked a facing property and had a single unrotated blockstate;
  actual placement/quarter-rotation now passes with unchanged tanks/cards/ports.
- Tidewraith water immersion reproduced real drowning before repair. Breathing
  and non-molten dimensional-fluid protection are scoped to regular Tidewraiths,
  not the boss or arbitrary fire/combat immunity. Packs use3-4 member biome
  groups and a minimum/default nearby cap4, correcting the old cap2.
- Owner clarified the supported catalogue is the actual hub shell builds.
  The shared HubExhibits cell plan now drives an allowlist: matching casings,
  roofs and controllers remain; non-hub tier BlockItems and old apiary_controller
  are hidden from parent/search tabs. Machines, frames, combs and hives remain.
  Actual addon creative contents and formation checks passed; registry IDs remain
  to prevent old-save corruption. No old placed blocks were erased.
- Manufacturing generator assigns planet-group palettes, causing different
  metals to share the wrong colours. Copper components are absent from the
  registered manufacturing list. Correct per-material source artwork and
  copper addition remain pending: the required game-asset-production CLI is
  unavailable on both this session's Linux and Windows PATH. No new provider
  or dependency was installed and no substitute art was claimed completed.

## New world-generation requests

- No railway blocks in newly generated procedural planetary mines. Preserve
  old corridor RNG, local timber supports and loot; rail decoration is retired.
- The authored Collapsed Mine room uses a rail-to-air processor on natural
  placement and new hub construction. Four rotations retain bound loot and
  remove all rail-tag blocks. Original source NBT/old sheets retain the historical
  layout; the runtime processor owns the changed placed form.
- New realistic terrain/heightmap work is next: six lore-themed Sol landforms
  and34 distinct planet graphs need actual fresh multi-seed slope/height surveys.
  Do not call independent noise registry keys realistic terrain proof.
- Common ores should have larger veins than increasingly rare ores. Existing
  fuel/common/standard/precious/dust/lore/rare/trade roles and newer material
  families need reconciliation before changing sizes/frequencies; preserve hosts,
  depth ranges, Nullifite story placement and mining tiers.
- Owner said a new save/world will be made. No current save was deleted/reset,
  and no new playable world has been exported by this repair batch.
