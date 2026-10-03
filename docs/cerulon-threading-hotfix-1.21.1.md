# Cerulon hive world-generation threading hotfix — 1.0.2-dev

The 1.0.1-dev candidate could crash while generating occupied planetary hives:
`IllegalStateException: Accessing LegacyRandomSource from multiple threads`.
The reported server crash occurred in Cerulon on 2026-10-03.

## Cause and correction

`DimensionEcologyFeature` constructed a live `AlienGlowbug` (a vanilla Bee
subclass) on a world-generation worker. Vanilla `BeeGoToHiveGoal` initializes
its travelling timer with `Bee.this.level().random.nextInt(10)`, accessing the
shared server-level random generator while the server may be ticking chunks.

Hive generation now stores serialized occupant data, following vanilla's
`BeehiveDecorator` pattern, instead of constructing an entity. Each occupant
keeps its registered custom species ID and vanilla 600-tick no-nectar residence
time. The hive constructs the bee later, on the normal server-thread release
path. Existing registry IDs, saved bees, textures and honey products are unchanged.

## Verification and limits

A deterministic worker regression drives the real ecology feature against a
sparse in-memory world-generation region and guards the server-level RNG.
Before the correction, it failed at:

```
Bee$BeeGoToHiveGoal.<init>
Bee.registerGoals
AlienGlowbug.<init>
EntityType.create
DimensionEcologyFeature.place
```

After the correction, all 53 isolated Java/NeoForge server GameTests passed.
The new test also checks that both hive occupants survive serialization and
can be created on the server thread with their custom species and hive position.
This is an invariant regression with deterministic instrumentation, not a
replay of the user's saved world or a full parallel chunk-generation stress test.
The earlier 52-test suite did not cover worker-thread hive population.

The normal candidate JAR excludes test classes. Minecraft Java 1.21.1,
NeoForge 21.1.252 and GeckoLib 4.9.3 were used. Existing worlds and configs are
not edited. No client/modpack retest is claimed; back up your world and retest
Cerulon in the CurseForge Java/NeoForge client.

## Candidate

[zerog-tweaks-1.21.1-1.0.2-dev.jar](jars/zerog-tweaks-1.21.1-1.0.2-dev.jar)
and [SHA-256 checksums](jars/SHA256SUMS.txt).
Install only one `zerog_tweaks` JAR. The previous candidate is retained in the
documentation archive; local installation moves the previous installed version
to a recoverable backup outside `mods`. Other mods remain untouched.
