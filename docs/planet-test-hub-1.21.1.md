# Planet test hub and current gameplay candidate

**Historical 1.0.5 snapshot.** For the fresh 1.0.6 showcase, independent planetary
generation, inhabited colonies and current tests, read the
[new field guide](planet-generation-1.0.6.md). The older exported save below is
preserved, not regenerated or deleted. This guide's old unfinished-status notes
are not the current colony/clothing implementation status.

Minecraft Java 1.21.1, NeoForge 21.1.252, Java 21, GeckoLib 4.9.3.
Current candidate: `zerog-tweaks-1.21.1-1.0.5-dev.jar`.

## Enter the test hub

The locally exported save is named **ZeroG Planet Test Hub — Seed 0**, folder
`saves/ZeroG_Planet_Test_Hub_Seed0`, seed **0**, spawn **62 / 65 / 0**.
It is a separate creative test world, not an existing player's save. Normal
mob spawning, random ticks, daylight and weather were restored in this copy.
The source isolated server world and existing saves were not modified.
This save is not published in the repository.

To create a fresh one, select the **ZeroG Planet Test Hub** world type/preset
and seed **0**. Simply choosing seed 0 with the normal Overworld preset will
not create the hub. Generation prepares destinations progressively; use
`/zerog hub status` to see readiness. Start in creative with commands enabled.

The hub has 34 outbound gates and 34 return gates. Stand on the centre pad and
right-click its controller. All required parts must remain present. The hub uses
explicit unlimited test-power records; this does not grant free power to normal
survival gates. The T6 service layout and operator binding/energy support are
testing infrastructure, not a complete progression/controller GUI implementation.

The isolated server run verified all 34 round trips, missing-frame rejection
and energy simulation/persistence. Its seed was read from actual world metadata
and the hub report. That result predates the later weather candidate: do not
describe it as full testing of 1.0.5 or graphical approval.

## Gameplay additions included

- Existing food definitions now bind their FoodProperties to items. Drinks use
  drinking animation; bowl/bottle containers are retained by their components.
- Furnace/smoker/campfire recipes for 17 raw→cooked pairs, hide→leather and
  flower→vanilla dye conversions. Vanilla leather equipment/dye recipes remain
  vanilla rather than inventing new armour tiers.
- Dedicated Liquids creative tab, excluding fish buckets from its fluid roster.
- 10×10×10 symmetric comet-remnant bounds: weaker shell/mantle, rare core.
  Daily impacts remain terrain-damaging and separately configurable: back up saves.
- Existing planet materials/crops, cave decorations and tree-canopy vine hooks.
- Original galaxy panorama for mod planet dimension effects, not the Overworld.
- Opt-in cosmetic weather; see [effects, controls and limits](alien-weather-1.21.1.md).

## Important unfinished work

Limited 16×16 generation samples contained ores but no tree logs. This is a
coverage warning, not proof that every planet lacks trees. Broader sampling,
fertile-ground fixes and biome-placement checks remain needed.
Cerulon already has depth-aware cave biomes; other dimensions currently do not
select distinct cave regions by depth. See [the actual vanilla-JAR review](vanilla-worldgen-review-1.21.1.md).

New alien village layouts, clothing variations and the additional reference
ruins/boss arenas have not been implemented. Many catalogued mobs and machine/
Productive Bees gameplay features remain unfinished. Food-property regression
and hub-route tests exist, but the latest added cooking/container tests and
complete modpack interactions have not been rerun for this candidate.

Normal clean build and packaged asset/reference checks passed. No client/GPU
review, new in-game screenshots, FPS guarantee or completed release is claimed.
Only one `zerog_tweaks` JAR should be installed. Earlier candidates are retained
as historical downloads and should not be installed alongside the current one.
