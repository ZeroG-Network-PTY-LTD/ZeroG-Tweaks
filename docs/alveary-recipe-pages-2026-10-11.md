# Alveary production pages — 11 October 2026

Same-version 1.0.12-dev continuation. The orbital apiary/alveary controller now
has an external read-only Recipes panel with Items / Recipes / Upgrades tabs.
The main slots, frame storage, output paging and existing controls are unchanged.
The panel shifts the machine to keep inventory visible; insufficient horizontal
space disables its button rather than covering player slots.

## Recipe information

- One retained supported orbital bee or Productive Bees cage is the input.
- Loaded Productive Bees recipes are resolved server-side. The client receives
  product icon components, productivity-adjusted minimum/maximum quantities and
  individual chances; it does not guess products from the cage sprite.
- Snapshots are bound to the active valid menu and controller, sent approximately
  once per second. At most 32 products are sent; extra entries are explicitly
  marked truncated. The packet is client-bound only, not a processing request.
- Current cycle ticks, FE/t and stable-configuration cycle FE are displayed.
  Tier 3+ uses 20 times the tier in FE per productive tick; tiers 1-2 use none.
- Tier 3+ adds 250 mB local Sol honey each cycle while retaining combs; elsewhere
  Moon Honey. The 8,000 mB tank cannot mix honey types.
- Tier 6+ optional 25 mB Starlight gives x1.2 cycle speed and is consumed on
  completion; its tank is 4,000 mB.
- Frame capacities are 3/4/6/8/12/18/27 for existing tiers 1-7. Frame speed effects
  and x0.25-x4 bounds are described separately from saved bee yield productivity.
- Power/item/fluid automation goes through service ports. Acceleration, Energy
  Coil, Compact and Void cards are not newly supported by these controllers.

The controller's independent eject/void controls remain distinct from upgrade
cards. Browse/drag/outside-click handling is guarded so recipe panels do not drop
or distribute cursor items. No production, formation, progression or cost rules
are changed. The runtime Codex chapter matches the Design source generator.

## Verification and delivery

All three isolated tests passed in `20261010_234311_runWorkflowTests.log`, using
the installed orbital addon and Productive Bees 13.14.0 in a disposable world:

- All seven controller tiers: authoritative recipe quantities/chances, current
  cycle/FE rules, frame timing without yield multiplication, tiered Starlight and
  honey disclosure, removed-bee refresh, no saved-job/inventory mutation.
- Actual captured iron-bee cycle: advertised FE debit, retained cage, output
  quantity bounds and 250 mB honey. Snapshot codec preserves product components
  and menu/controller binding.
- Existing complete PB/honey-port regression: simulated/real extraction,
  full/wrong-honey pauses, resumed FE/progress and tank save/reload.

The initial run passed two checks but failed the all-tier fixture because it
looked for obsolete standalone orbital bee item IDs. The fixture was corrected
to use a real captured PB specimen, then all three passed in a fresh world.
This does not certify every bee species, client packet rendering, or newly test
an actual boosted T6 cycle. Clean production build passed in 44 seconds
(`20261010_234517_clean.log`). Asset audit checked 7,979 models, 1,529 blockstates,
3,963 PNGs and 130 animation metadata files: zero errors, no test classes shipped.

Installed into the exact ZeroG CurseForge mods folder while the client was closed.
SHA256: `e0a9ec2c0247c9b961aa0fb59e32d7febc6e41b2678590429fc08730ce69bd2b`.
Previous JAR remains recoverable in `ZeroG/zerog-mod-backups/20261010-234703-UTC`.
Code commit: `0c119d0a`. The archive and checksum are retained on Docs. Other mods,
saves, hub terrain, approved gates and the custom-weather pause are unchanged.

## Player review

1. Open a controller and Recipes. Check inventory, frame slots, controls and
   long tooltips remain visible at your GUI scale.
2. Insert an orbital bee and then a captured PB bee; check products update within
   about a second, and disappear when the input is removed.
3. Add frames and compare cycle timing without multiplying the stated item yield.
4. On T3+, power the service hatch and drain the honey port; compare a cycle's
   products and 250 mB honey. On T6+, compare optional Starlight boost.
5. With a carried stack, click/drag/release on the read-only panel; no item should
   be dropped, consumed or copied into a recipe.

## Still pending

Client appearance/cursor approval; remaining machine adapter coverage audit;
advanced biology, research milestone map and seven-wide layouts; broader
progression/ecology checks; exact survival costs last. Gates, power, pipes,
wrench and transitions retain their separate owner approval. No hub/save reset.

Coverage candidates from GUI profiles are Stardust Smelter, Frame Assembler /
Frame Component Assembler, Infusion Altar / Frame Infusion Altar and the
Gravitational Centrifuge alias. Confirm real registrations and processing first:
profile entries alone do not establish live recipes or supported upgrade cards.
