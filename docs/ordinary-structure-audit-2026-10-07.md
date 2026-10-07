# Ordinary-server structure audit — 7 October

This run used a fresh disposable seed0 ordinary NeoForge server, not vanilla
GameTestServer. Saved world metadata confirms natural structures enabled.
The server bound game/RCON access to loopback, copied only an existing accepted
local EULA, and did not copy or modify client saves. No client launch or JAR
replacement. Both forced areas were released before a clean server shutdown.

## Cerulon: natural Concord Vault

The natural locator found the Vault at `[-32, -320]`. Its saved start at chunk
`[-2,-20]` contains84 pieces, including four planned key altars. Saved blocks
include one Concord Lock and common/uncommon/rare Vault chest loot bindings.
The uncommon fallback loot source therefore exists in a naturally generated
structure, not only a template or loot JSON. Actual player chest opening, template
rolls, traversal and completing the Sentinel encounter remain separate checks.

### High-priority finding: fourth key altar missing

Only three altar blocks were observed. The planned altar at `[-164,80,-280]`
lies in chunk `[-11,-18]`, nine chunks from the start on X. That chunk is FULL,
contains Cerulean Stone at the planned position, and has no Vault reference.
The other three planned positions contain their actual altar blocks and Vault
references. See [saved evidence](ordinary-vault-audit-20261007.json).

This establishes an incomplete natural key supply in this seed. The likely
boundary is vanilla's structure-reference search extent, but a repair must
verify the vanilla implementation and reproduce in a fresh ordinary world.
Do not patch the player's save or claim four-key progression verified. Possible
repairs must bound the whole layout/key selection relative to its start; choosing
a convenient test location or manually placing an altar is not a regression fix.
Keep future four-key gameplay tests separate from merely counting four planned
NBT pieces. Exact patch selection and broader seeds remain outstanding.

## Mars: natural Rustborn settlement

The seed-selected candidate in region0 at chunk `[31,32]` generated no settlement.
That is not evidence all villages are missing: terrain checks may reject a site.
The next sampled region's candidate at chunk `[67,28]` generated a settlement at
`[1080,37,456]`, with an Aresite shrine and saved resident counters6+2.
All residents use planetary species code, rather than adding vanilla villagers.
See [saved evidence](ordinary-mars-village-audit-20261007.json).

This proves one natural settlement and its resident initialization, not regional
frequency, every layout, terrain aesthetics, resident AI/trades or all planets.
The current placement code selects one candidate per50x50-chunk region, with
offsets16..33 and terrain rejection. Older TODO wording of one per256 chunks is
historical; it must not replace the owner's later50-chunk-region instruction.

## Reproduction

Code tooling: `tools/ordinary_structure_audit.py` and opt-in Gradle property
`ordinaryAuditDirectory`. The default development directory remains unchanged.
The tool refuses to overwrite an existing audit directory, never prints RCON
credentials, verifies seed/structure metadata and performs bounded saved-chunk
inspection. Inspect only after `save-all flush`; stop the server after releasing
forced areas. The ordinary run is `20261007_163408_runServer.log` and completed
with `BUILD SUCCESSFUL`; this is not a19-test or other GameTest pass count.

## Next priorities

1. Repair/retest the missing natural Vault altar before four-key progression.
2. Wider village spacing, biome/terrain, resident and other-planet checks.
3. Missing later structures, rewards, signature mobs and boss behavior.
4. Pending client visual approval, undefined biology and deferred exact costs.

Current installed JAR remains the verified wrench build from the previous
delivery. This batch adds audit tooling and records a bug; it does not contain
a gameplay repair or warrant another same-version installation.
