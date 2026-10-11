# Gate reload regression: test-fixture correction

The isolated `zerog_galaxy_access` run reproduced `Reload changed moon access` in `20261011_041644_runWorkflowTests.log`: eight required tests passed and the reload test failed.

The failing fixture deserialized a second controller and attached its level, but did not install it at that position. The production formation check intentionally requires the queried instance to be the currently installed block entity. A detached or replaced controller cannot acquire routing permissions from another live controller's structure.

The corrected test explicitly checks detached-instance rejection, saves and replaces the actual controller, loads the saved data into the installed replacement, checks energy and formation, and rejects access through the removed instance. Tier upgrade, downgrade and galaxy destination checks then use the replacement. This preserves the stale-controller protection rather than weakening production behavior to satisfy an obsolete fixture.

Production gate logic, assets, registry IDs, saves and the installed JAR are unchanged in this test-only batch. A combined rerun includes both the gate-access tests and the new wreck tests. This is block-entity save/load and world-replacement evidence, not a whole-server restart or new client travel approval.

All eleven required combined tests passed in `20261011_041843_runWorkflowTests.log` (9.232 seconds of test execution, 58 seconds including startup/build). The disposable server saved and stopped normally. This supersedes the unresolved reload assertion recorded in the wreck delivery notes, while keeping natural wreck discovery and visual approval pending.

The normal clean build passed in 43 seconds (`20261011_041958_clean.log`). No gameplay or design source changes were needed.
