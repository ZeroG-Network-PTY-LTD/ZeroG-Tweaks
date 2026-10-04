# Real planetary rain and lightning — 1.0.10-dev

For **Minecraft Java 1.21.1 / NeoForge 21.1.252**. This supersedes the
cosmetic rain/lightning descriptions in the preserved
[1.0.9 atmosphere guide](planet-atmosphere-1.0.9.md). Existing mobs, bees, vines,
liquids, recipes, structures, IDs and previous galleries are retained.

## Test it

In Creative mode, open **Z-Admintools**, take **Planetary Weather Tester** and
right-click on a ZeroG planet. Select **Alien acid rain** or
**Lightning + thunder**. You can also use these commands as a creative player
or operator on a ZeroG planet:

```mcfunction
/zgweather acid
/zgweather electrical
/zgweather clear
/zgweather auto
```

This is now **planet-wide server weather**, synchronized to players in that
dimension. Forced weather is temporary: Auto resumes its normal cycle, and a
server restart forgets the manual override. No Overworld weather is changed.
Automatic cycles remain six minutes with 90-second active windows; airless
Moon worlds remain clear automatically. The creative tester can force weather
on airless planets for inspection.

## Rain, clouds and shelter

Acid rain now uses falling, animated **green rain sheets**, green native
droplet/splash particles and rain audio, not dust particles. Electrical storms
use ordinary rain. The precipitation layer follows the native 1.21.1 renderer's
roof-height clipping, scrolling texture coordinates, lighting and distance
fading. It uses the existing Minecraft/resource-pack rain texture with a local
colour tint; the Overworld's texture is not overwritten. Blizzards use native
snow sheets alongside windblown flakes.

The panorama and stars darken during precipitation, with native clouds in the
storm sky. Existing optional **ZeroG-Atmosphere-0.1.zip** volumetric clouds can
consume the real rain/thunder strengths when enabled in compatible Iris/Sodium.
Shaders are not required for rain or lightning. Default/Fast graphics uses a
five-block precipitation radius; Fancy uses ten blocks, following vanilla's
rain-sheet budget. Particle settings affect splash/ambient particles, not the
main rain sheets. Shelters block rain where their motion-blocking roof covers
the column. Acid damage remains **disabled**, as requested.

## Actual lightning

Harsh electrical storms spawn genuine server-side vanilla lightning bolts,
not client-only imitation entities. Visible branching bolts and native thunder
are synchronized. There is one additional strike attempt per occupied planet
every ten seconds, 32–96 blocks from a randomly chosen player. Attempts skip
unloaded chunks, roof-covered sites and protected arrival areas; no new chunks
are force-loaded. Native per-chunk thunderstorm strikes may also occur.

Lightning follows Minecraft's normal interactions: entity damage, transformations,
lightning-rod activation and possible fire where difficulty and game rules permit.
Keep vulnerable animals/buildings sheltered. Both custom attempts and native
lightning entity spawns are rejected within a 24-block horizontal buffer around
protected test arrival gates, at any height. This protects the prepared hub's
landings, not all survival player-built gates.

The local thunder toggle mutes thunder audio. Reduced flashes suppress the
additional planetary sky flash, not the visible bolt itself; neither option is
a photosensitivity safety guarantee. Ambient Off/Low/High affects fog/dust/steam
particle budgets; it does **not** turn off server storms or real strike damage.
Use **Clear** to stop the planet's test weather.

## Install and verification

Use [the new JAR](jars/zerog-tweaks-1.21.1-1.0.10-dev.jar), not both versions at
once. [SHA256 checksums](jars/SHA256SUMS.txt) cover every retained candidate.
The existing **ZeroG Planet Showcase 1.0.9 — Seed 0** and its active gates work
with this update; no new world or dimension reset is needed. Played saves are
not edited or erased by installation.

The identical checked JAR was installed **before repository publication** in
`C:\Users\jakem\curseforge\minecraft\Instances\ZeroG\mods`.
The old 1.0.9 JAR is recoverably backed up under
`ZeroG\zerog-mod-backups\20261004-0135-UTC`, outside `mods`. Existing shaders,
Iris/Sodium, other mods and save files were left unchanged; no client was launched.

The clean production build passed, and all seven isolated server tests passed
with a normal shutdown. The storm regression verifies real rain/thunder
strengths, native bolt spawning and actual cow damage, rejection at an existing
protected gate, and unchanged Overworld/airless automatic weather ownership.
The other checks cover all 34 dimensions/68 gates, villagers, foods/crops,
vines/vents and collected liquid buckets. Final packaged art/model reference
audits preserve all prior designs and reject shipped test classes.

Build: `20261004_013108_clean.log`; seven-test run:
`20261004_012752_-PplanetHubTests.log`. Final JAR SHA256:
`6178da46365b39c9d0eb3bba3fc256ba2b7d09dc02ec1519c2859c86394373f0`.

Client rendering
and optional shader appearance still require player review; source inspection
and headless server tests are not an in-game screenshot approval.
