# Gate construction guidance — 9 October 2026

This is a guidance-only implementation batch. Flexible controller/port placement
remains pending: the structure still requires the established service positions.
No energy costs, tier geometry, registry IDs or save terrain were changed.

## Controller controls

- **Align:** on an incomplete gate, orient the controller toward the closest
  matching existing plan. It cannot replace missing parts.
- **Preview:** identify missing/mismatched blocks by section, material and count.
  Reports distinguish base rings, landing floor, individual pylon columns,
  rear arch columns/crossbeams/lenses, focus/core and service blocks. Raw world
  coordinates are no longer the construction instructions.
- **Ghost:** toggle the current-tier wireframe; an unformed gate shows Tier1.
  Green means the correct block, cyan means air/missing, red means a wrong block.
  Close the menu to walk around and inspect it. It expires after60seconds,
  clears on logout/dimension change or when moving48blocks away, and never
  places blocks, grants power or retains loaded chunks.

A completed current gate is explicitly called **complete / alignment valid**.
Any next-tier Preview requirements are **optional upgrades**, not defects in the
current gate. Tier6 reports that the maximum tier is reached. Ghost shows the
current tier, not an upgrade plan. Colours supplement the text report; actual
client legibility and screenshot approval remain pending.

## Verification

- Test-first compilation failed specifically for the not-yet-created grouped
  requirements method: `20261008_205336_compileJava.log` (UTC filenames).
- First disposable run passed the gate checks but failed an unrelated weather
  fixture because Mars was not loaded; preserved as evidence, not counted green.
- Rerun with planetary fixtures: **all12 checks passed**, clean server shutdown:
  `20261008_205629_runWorkflowTests.log`. Includes24 tier/rotation combinations,
  real generator/conduit charging, simulation/conservation, removed-handler
  revocation, grouped requirements and schematic packet round-trip/bounds.
- No Minecraft client was launched. Headless tests do not certify rendering.
- Clean production build passed: `20261008_205835_clean.log`. Asset audit found
  zero errors across7977models,1528blockstates,3962PNGs and129animation metadata
  files. No test classes ship in the production JAR.
- Published same-version candidate:
  `docs/jars/zerog-tweaks-1.21.1-1.0.12-dev-gate-guidance-20261009.jar`, SHA256
  `4aa4ddcd90a9a8f4648d523302f3645e26ee235283ac70ed3b024e8915d56b46`.
  Per the owner's repository-only instruction, the installed JAR and hub were
  left untouched. This archive is not an installation receipt.

## Remaining gate work, before recipe-page/upgrade work

Infer centre/orientation independently of the controller's visual front; define
legal horizontal service positions; preserve1/1/2/2/4/4port counts; reject ambiguous
or duplicate bindings; revalidate cached handlers immediately. Apply the resolved
geometry to passengers, launch effects, holograms, remote-home and return pads.
Run moved-service matrices, reload/adjacent-gate/home-return tests; update diagrams
and generators together. Do not reset the owner's recently played hub.

The full approved contract is [gate-guidance-spec-2026-10-09.md](gate-guidance-spec-2026-10-09.md).
The spec workflow's packaged references/scripts were absent; its nine-section
contract was checked manually and real Java/NeoForge tests were used instead.
