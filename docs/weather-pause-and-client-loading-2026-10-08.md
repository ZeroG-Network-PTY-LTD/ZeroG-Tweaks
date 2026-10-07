# Custom weather pause and client-loading investigation

Minecraft Java 1.21.1 / NeoForge; version stays **1.0.12-dev**.

Installed in the CurseForge ZeroG instance before publication. Clean production
build and asset checks passed (7,977 models, 1,528 blockstates, 3,962 PNGs,
129 animation metadata files, zero binding errors). SHA256:
`fcb3694bffdcb722a312b6d9a5b7d408e451c93baf03c947ebfb4fa6c0b7f9b1`.
The previous JAR is recoverably backed up outside `mods`; saves and dependencies
remain untouched. Delivery evidence is in `weather-shape-delivery-2026-10-08.json`.

## Owner-requested weather pause

The next build disables the custom server weather cycle, admin weather overrides,
custom lightning generation, client particles/funnels, additional storm fog,
green rain sheets and their splash/audio renderer. Creative weather controls
cannot bypass this build pause. The weather item and packet IDs remain registered
for save compatibility. Stale client settings cannot turn the effects back on.

Native precipitation rendering and rain sounds are delegated to Minecraft.
Vanilla weather is not forced clear, suppressed or cancelled. Custom ambient
vent smoke is paused; ordinary hazardous vent blocks and their existing gameplay
are not removed. Machine activity, bee-smoker puffs, water fog, mob glows and
the approved larger coloured stars are not weather and remain unchanged.

## Loading evidence and reproduced common-loading bottleneck

The client's 8 October 06:24 launch had a **265.602-second** interval between
the observed mod-setup marker and resource-reload marker. Its captured log does
not reach the block-atlas-ready marker. There are no ERROR/FATAL lines in that
captured latest log, invalid top-level JARs or duplicate top-level mod IDs.
These observations do not prove a deadlock or identify a responsible mod.

The preceding successful launch had the same phase take **131.915 seconds**,
then resources took **18.564 seconds** to sound initialization. Both selected
logs used ZeroG-Atmosphere-0.1.zip. The installed options are 32-chunk render
distance, 12-chunk simulation distance and mipmap level 4; those settings are
recorded, not changed speculatively. The later world-join stage is a different
performance boundary from title-screen loading.

At initial investigation time there was no live Minecraft client to sample.
The isolated no-Iris server then reproduced a long pause in registry freeze.
Two live thread snapshots show the loading worker repeatedly inside
`TransportBlock.Wire.shape`, voxel joins and `BlockStateBase.initCache`; one
snapshot reports 70.266 CPU seconds in that worker after79.62 elapsed seconds,
the later snapshot108.188 CPU seconds after120.84 elapsed seconds. This confirms
a common-loading pipe-shape bottleneck, independently of shaders.

The previous cache used each full BlockState as its key, separately per pipe.
Six directions with five connection states give15,625 states per block and
375,000 states across24 tier/family blocks. NORMAL/PUSH/PULL share exactly the
same shape, and tier changes don't alter the hitbox. The repaired cache keys
only width and geometric connections, shared across tiers and compatible families:
at most1,522 distinct shapes. Item connectors are geometrically contained within
their8x8 arms. No registered state/ID, artwork, wrench behavior or routing mode
is removed. Tests compare all375,000 states' sharing and2,916 representative
geometries against the original exact voxel union.

Actual client improvement remains **pending its next launch**; the isolated
reproduction does not establish every possible cause of client slowness.
The same isolated registry-to-recipe-loading phase fell from **183.088 seconds**
to **35.568 seconds** after the cache repair. The final run passed all **16 required
tests**, including the 24 gate tier/facing combinations, weather pause, exact
pipe shapes and existing transport flow/conservation boundaries. Its disposable
server saved and stopped cleanly. The first run had one test-fixture failure:
Minecraft's thunder getter includes rain strength; the fixture was corrected to
compare the actual getter values, not a raw setter value. No runtime weather
change was needed for that assertion. Optional addons and client graphics were
not exercised by this isolated run.
Iris is left installed, the shader ZIP
is preserved, and only `enableShaders` is changed to `false` for the next comparison.
The previous Iris configuration is retained locally. Shaders-off is a reversible
diagnostic setting, not the confirmed pipe-cache repair.

## Next client check

1. Start ZeroG normally through CurseForge. Leave shaders off for this first run.
2. Report whether the pause is before the title screen, opening the hub, or after
   entering a planet. Do not repeatedly launch a second client during the pause.
3. If it stalls again, capture two scoped thread samples with
   `tools/capture_zerog_client_threads.ps1` on `1.21.x`. It checks for exactly one
   Java process using this specific ZeroG game directory, never prints launcher
   account arguments, and neither kills a process nor edits a save.
4. Run `tools/audit_client_startup.py` against the new and earlier logs to compare
   the same stage boundaries. Missing completion markers alone are not deadlocks.
5. Once the cause is attributed, make one bounded change and repeat the same launch.

## Continued TODO verification

The gate-port regression now covers all six authored tiers in four horizontal
facings, all six accessible port faces, exact shared controller FE, simulation,
receive-only behavior and revoked cached handlers after required-port removal.
This does not certify client travel or optional-addon compatibility.

Pending: actual client loading comparison and GUI approval; wider optional-addon
gate coverage; remaining authored structures/signature mobs and natural ecology;
approved advanced bee research/biology rules; deferred recipe pages and exact
survival crafting costs. No additional structure artwork or gameplay is invented
while preparing this loading diagnostic build.
