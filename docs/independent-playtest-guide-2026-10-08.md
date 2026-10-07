# ZeroG independent playtest — start to finish

For Minecraft Java1.21.1 / NeoForge, **ZeroG Tweaks1.0.12-dev** with the Prism
Spire update. This is a complete manual test plan; no previous chat is needed.
Do not use Bedrock. No commands below delete dimensions, reset worlds or force
chunks to stay loaded. Do not run mass structure-placement commands in the hub.

## 1. Before launching

1. Launch the CurseForge **ZeroG** instance at
   `C:\Users\jakem\curseforge\minecraft\Instances\ZeroG`.
2. Its installed file is `mods/zerog-tweaks-1.21.1-1.0.12-dev.jar`.
   Verified SHA256:
   `3fe1deb13ca89bd3bb2e1ed1107cfe612a2a44a537f10959ce375f393be4450f`.
   The version deliberately remains unchanged; the version label alone cannot
   distinguish this build from earlier same-version repairs.
3. Keep Productive Bees, GeckoLib, the orbital addon and GuideME installed.
   Only the Tweaks JAR was replaced; the old file is backed up outside `mods`
   under `zerog-mod-backups/20261007-183107-UTC`.
4. For first checks disable shaders/resource packs that override ZeroG artwork.
   Repeat visual checks with your usual packs afterward, recording the difference.
5. Open **ZeroG Compact Hub1.0.12 — Seed0**:
   `ZeroG_Planet_Showcase_1_0_12_Compact_Hub_Seed0`.
   Prefer Minecraft's own **Make Backup** before deliberately breaking structures.
   This update did not reset the hub, inventories or planetary terrain.
6. Enable commands in this test world if needed: Open to LAN → Allow Cheats.
   Use a separate world/copy for destructive tests, boss fights or survival progress.

## 2. Starting position and hub orientation

Return to the central hub with:

```mcfunction
/execute in minecraft:overworld run tp @s 0 65 0
/gamemode creative
```

Hub sectors: **north gates; west machines, tanks and transport; south bee
multiblocks; east ten structure/arena exhibits**. East exhibits are previews,
not evidence that their corresponding structures generate naturally.

The six compact-hub gate pad centres are:

| Tier | X | Y | Z |
| --- | ---: | ---: | ---: |
| 1 | -22 | 64 | -22 |
| 2 | 0 | 64 | -22 |
| 3 | 22 | 64 | -22 |
| 4 | -22 | 64 | -44 |
| 5 | 0 | 64 | -44 |
| 6 | 22 | 64 | -44 |

These are pad centres, not controller coordinates.

## 3. Test all six gates normally before using teleport commands

For each gate1–6:

1. Read its tier and formation state. Confirm the physical structure is complete.
2. Stand on the pad; empty-hand right-click its controller.
3. Select a destination, click **Engage**, then **Ready** before the countdown.
4. Confirm arrival is safe, with no falling into void, suffocation or broken platform.
5. Find the return controller and repeat the ready flow. Confirm it returns to the
   original hub gate, not a different gate or an old hub.
6. Record the displayed tier, destination, arrival coordinates and return result.

Hub gates are intentionally **admin/free**. They do not certify survival power,
ownership or guardian-key restrictions. Direct teleport commands also bypass
gate functionality, so do not use them as evidence that a gate works.

## 4. Direct dimension commands for inspection

First use `/gamemode spectator`. The following commands move to0/160/0;
that location is **not** a gate/structure location or guaranteed safe ground.
Spectator prevents suffocation/fall accidents. Move to clear ground before
returning to creative. Clouds, lighting and gravity are dimension-dependent.

### Six Sol worlds

```mcfunction
/execute in zerog_tweaks:moon run tp @s 0 160 0
/execute in zerog_tweaks:mars run tp @s 0 160 0
/execute in zerog_tweaks:cerulon run tp @s 0 160 0
/execute in zerog_tweaks:skarn run tp @s 0 160 0
/execute in zerog_tweaks:eidolon run tp @s 0 160 0
/execute in zerog_tweaks:solvane run tp @s 0 160 0
```

### Galaxy2 wastelands and moon

Default habitats: p1 ocean, p2 desert, p3 volcanic, p4 frozen, p5 toxic,
p6 crystal; moons barren. Do not assume every later galaxy shares this mapping.

```mcfunction
/execute in zerog_tweaks:g2_p1 run tp @s 0 160 0
/execute in zerog_tweaks:g2_p2 run tp @s 0 160 0
/execute in zerog_tweaks:g2_p3 run tp @s 0 160 0
/execute in zerog_tweaks:g2_p4 run tp @s 0 160 0
/execute in zerog_tweaks:g2_p5 run tp @s 0 160 0
/execute in zerog_tweaks:g2_p6 run tp @s 0 160 0
/execute in zerog_tweaks:g2_moons run tp @s 0 160 0
```

### Galaxies3–5

```mcfunction
/execute in zerog_tweaks:g3_p1 run tp @s 0 160 0
/execute in zerog_tweaks:g3_p2 run tp @s 0 160 0
/execute in zerog_tweaks:g3_p3 run tp @s 0 160 0
/execute in zerog_tweaks:g3_p4 run tp @s 0 160 0
/execute in zerog_tweaks:g3_p5 run tp @s 0 160 0
/execute in zerog_tweaks:g3_p6 run tp @s 0 160 0
/execute in zerog_tweaks:g3_moons run tp @s 0 160 0
/execute in zerog_tweaks:g4_p1 run tp @s 0 160 0
/execute in zerog_tweaks:g4_p2 run tp @s 0 160 0
/execute in zerog_tweaks:g4_p3 run tp @s 0 160 0
/execute in zerog_tweaks:g4_p4 run tp @s 0 160 0
/execute in zerog_tweaks:g4_p5 run tp @s 0 160 0
/execute in zerog_tweaks:g4_p6 run tp @s 0 160 0
/execute in zerog_tweaks:g4_moons run tp @s 0 160 0
/execute in zerog_tweaks:g5_p1 run tp @s 0 160 0
/execute in zerog_tweaks:g5_p2 run tp @s 0 160 0
/execute in zerog_tweaks:g5_p3 run tp @s 0 160 0
/execute in zerog_tweaks:g5_p4 run tp @s 0 160 0
/execute in zerog_tweaks:g5_p5 run tp @s 0 160 0
/execute in zerog_tweaks:g5_p6 run tp @s 0 160 0
/execute in zerog_tweaks:g5_moons run tp @s 0 160 0
```

All34 IDs above are present in the shipped dimension data. Later galaxy content
is incomplete: an accessible dimension is not proof its story/bosses are finished.

## 5. Locate the naturally configured structures

Run these from anywhere; each searches the specified dimension near0/100/0:

```mcfunction
/execute in zerog_tweaks:g2_p6 positioned 0 100 0 run locate structure zerog_tweaks:prism_spire
/execute in zerog_tweaks:cerulon positioned 0 100 0 run locate structure zerog_tweaks:concord_vault
/execute in zerog_tweaks:mars positioned 0 100 0 run locate structure zerog_tweaks:mars_crash_site
/execute in zerog_tweaks:mars positioned 0 100 0 run locate structure zerog_tweaks:mars_aresite_shrine
```

Take the returned X/Z, enter spectator and teleport in the **same dimension**:

```mcfunction
/execute in zerog_tweaks:g2_p6 run tp @s X 160 Z
```

Replace X/Z with the actual numbers. Do not type those letters literally.
Search the ground below, then move onto a clear floor before switching modes.
`/locate` is not proof that every referenced chunk has finished placing its blocks.

### Prism Spire — newest change, inspect this first

1. Explore **fresh crystal-wasteland chunks**. Old generated terrain is unchanged.
2. Confirm a15×23×15 broken Prismstone tower: foundation, three floors,
   broad entrance, damaged windows, luminous accents and fractured crown.
3. In creative, walk in through the entrance and climb the continuous ladder.
   Check all floor exits: no blocked rung, falling through a floor or invisible wall.
4. Open the top chest. Its lid must not be blocked. A Refracting Lens is guaranteed.
   Cobaltium/Cyrrium/Aurelion templates are possible rewards, not guaranteed in
   each chest. Other supplies are intentional.
5. Check foundation blending, wall materials, lighting and surrounding vegetation.
6. Record screenshots of the outside, entrance, ladder exits and opened chest.

The disposable fresh seed0 audit found a Spire at **X96/Z48 in g2_p6**, with an
actual saved chest. That is a reference observation, **not a promise that an older
save or a world with different generation settings has the same structure**.
Initial placement spacing40/separation20 chunks is subject to terrain rejection
and final balance review. One successful sample does not establish global rarity.

### Concord Vault and Prism Sentinel

1. Locate the natural Vault on Cerulon. Navigate its rooms rather than placing a
   replacement structure over the hub or issuing commands to complete the lock.
2. Find and claim the four key altars. Each awards one key and awakens three
   room guardians; revisiting an emptied altar must not award another key.
3. Check common/uncommon/rare chest loot. Uncommon loot can already yield the
   three Galaxy2 ladder templates; no single chest guarantees all of them.
4. Use the four **Concord Vault Keys** on the chamber lock. Each stage consumes
   one key, builds the next chamber section and finally creates the Concord Prism.
5. Click the Prism to start the encounter. Check that a second start does not
   duplicate the Sentinel.
6. On a disposable world/copy, test the real fight, victory rewards and save/reload
   during a fight. Record phase behaviour, duplicate bosses or lost encounter state.
   Those combat/reload checks have not yet received full gameplay approval.

Vault room keys and the later galaxy guardian gate keys are different systems.
Do not treat four altar keys as proof later-tier guardian progression is complete.
Old saved Vaults are not retrofitted. The Vault has a one-per-world concentric
placement; merely exploring new chunks does not replace an already-generated
old Vault. Use a separate fresh test world if needed, not an unapproved reset.

### Mars

Check crash-site hulls, reachable loot and ground blending. Check the dedicated
Aresite Shrine's materials and chest separately from Rustborn settlement shrines.
For villages, explore surface terrain: record ground/farm matching, doors,
planetary residents, spacing and any floating/buried buildings. A village is not
guaranteed close to each landing gate, and settlement layout is not a standard
`/locate` structure in this guide.

### Known missing structures — do not report these as new regressions

Sunken Relay, dedicated Buried Observatory, Collapsed Forge, Frozen Outpost,
Sunken Lab, Impact Site, Eidolon derelict wrecks and Solar Shrine remain pending.
Buried Observatory loot in mineshafts is **not** its dedicated structure.
Prism Sentinel Arena has a configured asset, but no separate structure-set file
was found in this audit; use the natural Vault encounter for progression testing.
Hub arena exhibits do not establish natural boss generation.

## 6. West workshop — machines and automation

Use each supplied station's labels/materials, not guessed catalyst recipes.
Take screenshots before moving anything. Supplies are intentionally not refilled.

For Alloy Forge, Refinery, Crystal Growth Chamber, Salvage Station, Silk Weaver,
Centrifuge, Starmetal Smelter, Geno Station and Genetic Splicer:

- Normal and sneak right-click: correct intended machine screen, no old duplicate
  menu. Inspect text, player slots, output slots, tooltips and outside panels at
  your usual GUI scale and one smaller scale.
- Use a supported supplied recipe. Compare quantities/catalyst with the recipe
  display where available. Some recipe/combination pages are explicitly deferred.
- Connect power to an enabled face; check stored energy, processing and output.
  A full buffer need not continue accepting power. Disable a face: transfer must
  stop; re-enable it: transfer should resume without restarting the game.
- Repeat supported item/fluid faces with actual pipes/hoppers. Disabled faces
  must not remain accessible through cached connections.
- Try invalid ingredients/catalysts: rejected items must remain recoverable,
  not vanish. Verify shift-click and output extraction.
- Save, quit and reopen: items, fluids, cards, settings and valid job state persist.

Generators: check combustion fuel panel stays clear of player inventory, accepted
fuel indicators, burn/progress and FE output. Check Solar/Fusion Flux-module
sockets and **output** faces; Solar is a generator, not a machine needing normal
incoming power to run. Report whether the fault is a module slot, connection,
generation or display—not just “no flux.”

## 7. Cards, cells, tanks and transport

- Inspect all19 distinct card icons and tier colours. Native processors support
  Acceleration/Energy Coil/Compact tiers1–6 and Void; Geno/Splicer/Centrifuge/
  Starmetal Smelter support Acceleration/Energy Coil only. Do not assume every
  machine supports every card. Configured speed/energy caps remain bounded.
- Native Compact storage must never expose oversized visible item stacks.
  Remove/reinsert the card and reload: stored inputs must remain recoverable.
- Void: set a ghost output filter, process matching and nonmatching items,
  then remove the card. Only newly produced selected outputs may be discarded;
  old outputs, inputs, catalysts, fluids and cursor items must not be destroyed.
- Cells: charge/discharge and inspect actual progress/colour indicator at empty,
  partial and full charge. Fake full levels or missing gauges are failures.
- Tanks: fill/empty with buckets and pipes; upgrade and reload without fluid loss.
  Verify appropriate liquid names/colours in the liquid inventory category.
- Networks: test successful flow and a blocked destination. Look for directional
  power pulses, fluid waves and traveling item visuals only on committed movement.
  Mixed-tier power/fluid/gas networks must respect their weakest connected tier.
  Item transport has its separate contract.
- Oxygen/hydrogen are measured in mB. Test labelled canisters/tubes/tanks without
  mixing gas types or inserting gas into a liquid-only line. Do not assume a
  survival gas-production chain or every future chemistry recipe is complete.

## 8. South — apiary/alveary and genetics

1. Inspect each formed example's controller terminal face and readable GUI.
2. Verify bottom exterior service positions can accept two item ports, two liquid
   ports and one energy port. The controller belongs in a second-row casing
   location. Use the labelled examples; do not place ports in the internal cavity.
3. Connect cables to the energy port, not directly to the controller. Test item
   and fluid transfers through the appropriate ports. Move one service port in
   a test copy, reform and check that old connections no longer route incorrectly.
4. Add supported bees/frames and power. Check comb outputs and honey reaching
   its tank/port together. Empty or blocked output paths must not duplicate goods.
5. Break one required casing in a test copy: formation should fail with a useful
   error; restore it and recheck. Capture missing/incompatible-position messages.
6. Test genetics with supported bee/cage samples, correct catalyst and power;
   compare input consumption, result and save/reload. Don't infer success merely
   from an animated helix or glowing terminal.

Advanced biology/research milestone rules, seven-wide layouts and exact survival
costs remain pending. Do not assume sealed/unavailable controls implement them.

## 9. Planets — artwork and ecology checklist

Repeat first on the six Sol worlds, then the seven Galaxy2 slots. Sample later
slots afterward. Record dimension and biome with F3; travel beyond old terrain.

- Distinct terrain/biomes; safe return platform; no mirrored-only appearance.
- Trees, leaves, vines, flowers, shrubs, tall grass, crops and cave decor.
- Farming: crop appearance/growth stages, slow dark growth, wet/dry farmland;
  dirt/farmland should not contain painted ore or gems.
- Caves: carving, mineshafts, mushrooms, hanging vines, stalagmites and aquatic
  plants where appropriate. Not every proposed environmental addition is finished.
- Ores: correct textures, raw/dust/ingot/block sprites and correct-tool drops.
- Planetary fluids: placed/flowing appearance, collectable buckets, names and
  compatible tank/pipe behaviour. Try pack/shader-off and then normal settings.
- Mobs: especially Mars Rust Beetle, Dune Burrower and Dust Grazer textures.
  Check eye placement, scale, animation, spawning and loot separately.
- Equipment: Moonsteel tool facing in both hands/first and third person; inspect
  four Sol3D armour sets and the other vanilla-fit sets. Record the exact piece
  and view when reporting clipping or backwards geometry.
- Sky: vanilla-style sky with enlarged coloured stars, no old galaxy-image overlay.
  Inspect both with and without Iris shaders. Weather admin tools are in
  **Z-Admintools**; test precipitation/lightning only in an expendable area.
- Comet impacts can damage terrain. Do not deliberately test one over the hub.
  Wait a full Minecraft day for cycle tests; `/time add` alone does not reliably
  reproduce server tick scheduling or prove an impact system is broken.

## 10. Story and final save/quit

Use a separate fresh survival test world for the first-Nullifite/Courier/gate
storyline. Creative-given items or admin travel can bypass the intended checks.
Read Codex pages before and after real milestones: no future-act spoilers,
Moon/Mars arrival pages only when their unlock conditions are met. Right-click
opens GuideME; sneak-right-click opens Echo's native story pages.
Do not destroy the hub to test Courier impacts or gate construction.

Finally return to the Overworld hub, save/quit, record how long it takes, reopen
and inspect machine contents/settings, gate return links and your inventory.
If it hangs/crashes, retain `logs/latest.log` and the matching crash report.
Do not reset the world before collecting those files.

## Feedback to send before further changes

For each problem send:

```text
Build: Prism Spire1.0.12-dev (SHA begins3fe1deb1)
World/seed:
Dimension/biome and coordinates:
Machine/item/mob ID or exact displayed name:
What I clicked/inserted/connected:
Expected:
Observed:
Shaders/resource packs and GUI scale:
Screenshot saved as an actual file / relevant log:
```

Priorities for approval: gate travel/return, new Spire access/chest, machine GUIs,
ports/transfer, inventory/armour/mob art, then broader ecology and story/combat.
Mark each pass/fail/not-tested. Unperformed tests and known pending features are
not approved merely because this guide lists them.
