# Flexible gate service placement — approved, not implemented

Owner requirement,8October2026: the controller or energy port may be on any side
of the gate multiblock, provided the full structure for that tier is complete.
This supersedes fixed service locations in existing tier building diagrams.
The installed1.0.12-dev JAR still uses those fixed locations; this document is
not a delivery claim.

## Next implementation

- Infer the gate's actual centre and structural orientation from the assembled
  pad/frame/pylon/lens geometry, independently of the controller's outward face.
- Permit service positions on all four horizontal sides. Retain required solid
  geometry; do not silently let a controller replace a mandatory pylon or lens.
  Existing port counts remain1/1/2/2/4/4 across tiers1–6 until explicitly changed.
- Resolve energy ports to exactly one valid controller and one shared FE buffer.
  Reject ambiguous overlapping structures and duplicate controllers. Removing
  required parts or ports must immediately revoke charging, including cached
  capability handlers. Preserve finite energy, rate limits and simulation.
- Use the discovered centre/orientation consistently for launch passengers,
  pylon effects, previews, remote home footprint loading and return platforms.
  Admin privileges remain limited to designated hub gates, not arbitrary blocks.
- Cache or bound discovery without allowing stale formation after a block edit;
  do not repeat expensive whole-area scans on every menu/capability query.
- Update in-game Codex building instructions, Docs layer diagrams and Design
  generators. Keep branch ownership separate and do not rename saved IDs.

## Required verification before installation

Real server tests must move controllers and ports independently across every
horizontal side, all six tiers and all four structural orientations. Check
formed tier, pad centre, exact menu FE, real generator/conduit transfers,
simulation/conservation, port/part removal, stale handlers, save/reload,
adjacent gates and safe home return. Legacy authored layouts must still work.
Add a public Align/Preview check that distinguishes current-tier completion
from missing next-tier upgrade parts. Client travel/graphics remain separate.

## Evidence from latest playtest

Read-only inspection of the closed client's compact save found the new survival
controller at66,65,-28 facing North with a complete Tier1 layout and0savedFE.
The exact reported Align message was not supplied, so no definite cause of that
message is claimed. Current Preview computes `formed + 1`, potentially listing
Tier2 requirements for a completed Tier1 gate; that needs clearer wording.

## Resume boundary

Account usage was94%used when checked. The owner previously instructed light
verification/notes and publication below10%remaining. No runtime code, installed
JAR, player inventory or world terrain was changed for this new requirement.
Resume from this contract after reset; keep exact survival costs and undefined
biology/research rules pending. Do not reset the recently played hub to add this.
