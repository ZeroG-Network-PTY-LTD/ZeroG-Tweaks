# Black mob rendering: same-version hotfix

## Report and evidence

The player reported solid-black Rust Beetles, Dune Burrowers and Dust Grazers on Mars, including with shaders disabled and resources refreshed. Supplied screenshots also show a solid-black Moon Hopper. This is not the pink-and-black missing-resource checkerboard.

The installed cardinal-hub JAR contains the correct base PNG, geometry and animation assets. The affected base PNGs contain coloured opaque pixels, match their declared atlas dimensions, and none of their non-empty mapped face rectangles is entirely transparent. These observations rule out simple missing files; they do not prove correct GPU rendering.

All four mobs use `ZGGeoMobRenderer`, which previously attached `AutoGlowingGeoLayer` unconditionally. None of the four supplies a `_glowmask.png` or glow metadata. Inspection of the installed GeckoLib 4.9.3 bytecode shows that `AutoGlowingTexture.loadTexture` returns no upload call when both are absent, while the automatic layer still submits a render pass. This is a concrete invalid-pass condition consistent with the silhouettes, not yet a client-confirmed root cause.

## Change

`OptionalGlowingGeoLayer` checks the active resource manager for either a glow-mask PNG or `GeoGlowingTextureMeta` before requesting the automatic pass. Without either, it returns no render type; the ordinary coloured texture remains the sole pass. Valid existing glow assets and valid metadata continue to use GeckoLib's emissive path. The check is not cached, so resource reloads can change the active glow assets.

Only the shared native mob renderer is changed. No texture, geometry, animation, armour, registry ID, dimension, save, shader configuration or hub layout is replaced. Version remains **1.0.12-dev**.

Code commit: [ba544335](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/commit/ba544335), on `1.21.x`. Design and Released are unchanged.

## Verification and limits

The clean production build passed. The packaged asset audit checked 7,937 models, 1,522 blockstates, 3,893 PNGs and 96 animation metadata files with zero errors. There is no automated client/GPU regression harness in this project that reproduces the supplied silhouette, so build or server results must not be described as visual proof. Server-only tests cannot validate this render pass and are not substituted for a client check.

Installed JAR: `zerog-tweaks-1.21.1-1.0.12-dev.jar`. SHA256: `65286f056875d9afb7cd864300a3117cd5e604599eca87ae7ddf04b1a69b291a`. The previous cardinal-hub JAR was moved to the instance's `zerog-mod-backups/20261006-195027-UTC/` before replacement. Productive Bees, GeckoLib and the Orbital Bees addon were preserved byte-for-byte. No client was launched by the agent.

The archived hotfix is [available here](jars/zerog-tweaks-1.21.1-1.0.12-dev-black-mob-hotfix-20261007.jar); older published builds are preserved in the same directory and checksum ledger.

After installation, restart the Java/NeoForge client and inspect Rust Beetle, Dune Burrower, Dust Grazer and Moon Hopper with shaders off, then on. Check adult/baby appearance and resource reload; also check a genuinely emissive mob to verify its glow remains intact. Client confirmation is pending until the player performs these checks.

## Separate contributor changes still needing identification

At the repository check, `1.21.x` was at `6290d4cd`, Design at `d37440fb`, and Docs at `e1999ac1`. No later published code head or identifiable new Starmetal armour/weapon commit was found. A contributor commit URL or exact branch/file names are needed to reconcile that report; no substitute armour or guessed weapon transform is included in this hotfix.

## Prevention

Asset-presence audits do not cover renderer passes that reference optional resources. Keep glow layers conditional on usable glow resources and add a real client visual regression harness when available. Preserve the existing broader machinery, ecology, progression and survival-cost TODOs; this narrowly scoped hotfix does not complete them.
