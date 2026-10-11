# Bog projectile regression checkpoint

The isolated no-addon server completed all 17 required tests successfully,
including the new `spit_expires_without_leaving_a_hazard` regression. A stationary,
gravity-free acid projectile is removed after its 100-tick lifetime even when it
does not hit an entity or block. Existing projectile collision, poison/acid
immunity, habitat/egg and wasteland creature checks remained successful.

Evidence: `20261011_151553_runWorkflowTests.log`. The disposable server shut down
normally; no installed client or existing save was launched or changed.
The normal production `clean build` passed in 48 seconds
(`20261011_151743_clean.log`); the optional regression source is not shipped.

This checkpoint changes test coverage, not gameplay or artwork. The installed
Bog Lurker build remains valid; a redundant local JAR replacement is unnecessary.
Research mappings, seven-wide shells, Moon impact wrecks and exact survival costs
remain inactive proposals awaiting owner approval.

## Remaining verification work

- Strengthen the eleven-machine coverage test: its cached-handler rejection uses
  dirt, which may already be an invalid input. Use valid recipe inputs to prove
  disabled and restored faces independently of recipe filtering.
- Verify Bog Lurker navigation in real custom-acid pools, not only its direct
  acid-damage immunity and vanilla biome spawn lists.
- Installed-client animation, GUI and natural population approval remains separate
  from successful server regressions.

Fetched code, Design and Docs heads matched the local checkouts at this checkpoint.
No contributor changes were silently omitted or inactive proposals activated.
