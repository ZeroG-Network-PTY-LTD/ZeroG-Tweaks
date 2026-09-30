# Prepared runtime integration · not yet admitted

This source snapshot preserves the local Tidewraith implementation that compiled
with Minecraft 1.21.1 / NeoForge 21.1.252 / GeckoLib 4.9.3 and passed three server
GameTests. It is intentionally **not wired into this data-only commit's `src/`**:
publishing registered renderers without their admitted model/texture resources
would leave a broken client spawn path.

The Java files belong in the corresponding `net.zerog.tweaks.entity`, `client`
and `registry` package folders. `integration.patch` preserves the exact existing
registry/build/dependency changes. `src/gametest/` holds the three server tests
and their generated empty NBT scene. Keep these changes separate from unrelated
mob implementations and never rename existing registry IDs.

The patch has zero context so it can be stored without whitespace-only context
lines. Before any approved integration, verify the base commit and use
`git apply --check --unidiff-zero integration.patch`; do not apply it to unrelated
source versions or bypass a failed preflight.

Integration still requires the explicitly named project-specific import and
unverified reference-art licence exception, then runtime model export, a fresh
build, server tests and client rendering/animation checks. This source snapshot
is not a certified package, tested client build, release jar or permission to
deploy to the user's CurseForge instance.

Server evidence: regular/boss entity lifecycle and attributes, actual use of
both spawn eggs, clamped/saved boss palettes. See the parent `verification.json`
for the scope, initial isolated-server warning and pending checks.
