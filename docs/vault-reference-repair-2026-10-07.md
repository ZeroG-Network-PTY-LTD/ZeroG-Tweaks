# Concord Vault reference-boundary repair

Status: verified on 8 October 2026 (Asia/Bangkok). Five server tests, the clean
production build, asset audit and fresh ordinary-world placement check passed.

## Reproduced cause

The original seed0 ordinary-world report plans four keys but places three.
The fourth key's FULL chunk is nine chunks from the start, has no Vault reference
and contains stone at the planned position. `ChunkGenerator.createReferences`
in the actual Minecraft1.21.1 source searches starts only within eight chunks.
The new real-jigsaw regression reproduced an escaping room on seed0 before the
repair; `20261007_165210_runWorkflowTests.log` failed one of five required tests.
That run is red evidence, not a passing suite.

## Repair contract

- After building a jigsaw attempt, fit its complete horizontal bounds inside
  the start chunk's inclusive eight-chunk reference window.
- Use the minimum necessary whole-layout X/Z translation, not cropped rooms,
  relocated individual keys, smaller artwork or modified vanilla reference code.
- Move template positions, bounding boxes and jigsaw-junction coordinates
  together. Preserve Y, room connections, relative spacing, rotations and loot.
- Reject attempts too wide to fit; do not emit a fallback with fewer rooms than
  the requested key count. Choose altar rooms only after the layout translation.
- No key, loot, recipe or registry IDs changed. No inventory/world retrofits.

The previous seed0 layout needs a15-block X and-2-block Z shift to fit. Tests
must verify the actual generated layout, not rely on these example offsets.

## Verification boundaries

- Passing regression transcript: `20261007_165712_runWorkflowTests.log` (five
  required tests, including the 32-layout-seed boundary check).
- Clean production build: `20261007_170354_clean.log`; no test flags were used.
- Fresh ordinary seed0 Cerulon: all four actual altars have `has_key=true`,
  all have Vault references, and the lock is placed. The structure retains84
  pieces. Evidence: `ordinary-vault-repaired-20261008.json`.
- Ordinary server stopped cleanly: `20261007_170516_runServer.log`. Forced
  chunks were released before shutdown; no player joined this disposable world.

- The generated-layout test uses real native Cerulon noise settings and jigsaw
  generation across32 layout seeds. It does not certify32 naturally explored
  worlds or override the GameTest natural-structure limitation.
- `ordinary_structure_audit.py --require-vault-keys` must observe four actual
  altar blocks, each with `has_key=true`, in a fresh ordinary seed0 world.
- Existing naturally generated Vaults retain their old saved layout. This repair
  applies to newly generated structures; do not erase player dimensions or claim
  old missing altars have been restored automatically.
- Player key collection, combat, the four-stage lock, graphical terrain fit and
  wider-seed ecology remain separate verification concerns.

The hub and all client saves remain untouched during these isolated checks.

## Delivery

The verified same-version `1.0.12-dev` JAR is installed in the ZeroG CurseForge
mods folder. Its SHA256 is
`ccea0e94cf91e1adc9ff1c74a9978de07f599caf5bbc50a806f26e9c61313295`.
The previous JAR is recoverable in `zerog-mod-backups/20261007-171155-UTC`.
Productive Bees, GeckoLib and the orbital-apiary addon were preserved unchanged.
See `vault-delivery-2026-10-08.json` and the archived JAR/checksums under `docs/jars/`.
