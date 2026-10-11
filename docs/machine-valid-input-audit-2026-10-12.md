# Valid-input machine face audit

All six required addon-present tests passed on the corrected run, including
coverage of all eleven live legacy/genetics machines and exact recipe catalogue
checks. Evidence: `20261011_221942_runWorkflowTests.log` (UTC transcript date;
12 October locally). The disposable server shut down normally.
Normal production clean build passed in 50 seconds
(`20261011_222057_clean.log`). Optional GameTest classes are excluded from delivery.

For each of six faces on every machine, the audit selects an actually insertable
input through the public item handler, verifies rejection after disabling that
face, verifies the old cached handler stays revoked after restoring the face,
then inserts through a fresh handler. Ordinary machine inputs round-trip intact.
Genetics inputs deliberately cannot be extracted by automation and remain intact
in their slots. The initial test wrongly expected extraction there; that test
assumption was corrected without weakening production specimen protections.

No gameplay changes were necessary. No installed JAR, hub, save or weather was
changed. The old dirt-only assertion no longer stands in for valid-input rejection.
This is server transfer evidence, not client GUI/animation approval or proof of
unimplemented Compact/Void support on genetics machines.

The ledger also no longer calls Ash Strider, Rime Stalker, Bog Lurker or Crater
Drifter unregistered. Natural population density and broader biome surveys remain
pending. Research rules, seven-wide alvearies, Moon wrecks and exact crafting
costs remain inactive review proposals, not approved runtime features.
