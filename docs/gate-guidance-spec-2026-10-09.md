# Gate placement and construction guidance

## 1. Metadata

Status: owner-approved requirements; implementation and client review pending.
Approved in the 8–9 October 2026 gate-placement conversation. Runtime branch:
1.21.x; documentation: Docs; source artwork/generators: Design.

## 2. Context

Fixed service positions and Preview's automatic next-tier report can confuse
players whose current gate is complete. Preserve existing builds and saved IDs.

## 3. Functional requirements

- FR1: Identify the actual pad centre and structural orientation independently of
  the controller's visible front; support horizontal service positions on row two
  without replacing essential pylons, arches, frames or lenses.
- FR2: Preserve tier port requirements 1/1/2/2/4/4, ownership, admin restrictions
  and one conserved controller energy buffer; reject ambiguous ownership.
- FR3: Formation guidance names missing blocks, counts and structural sections,
  not world coordinates. A completed current tier is explicitly reported complete
  before any separately labelled next-tier requirements.
- FR4: A controller control toggles a client-only schematic showing required
  geometry and missing/mismatched parts. No automatic block placement occurs.
- FR5: Centre/orientation changes apply to passengers, energy ports, launch
  effects, remote return checks, Codex instructions and source generators.

## 4. Non-functional requirements

- Scans inspect loaded chunks only and have a fixed maximum tier-six footprint.
- Removing required blocks revokes charging on the next capability call, even
  within the same tick; simulation changes zero stored FE.
- Schematic data is bounded by the maximum gate plan and expires or clears on
  dimension change; no persistent chunk loading is added.
- Existing registry IDs and saved finite FE remain unchanged.

## 5. Acceptance criteria

- AC1 (FR1/FR5): Given each tier and orientation, when service blocks move to each
  legal side, then formed tier and passenger centre remain correct.
- AC2 (FR2): Given a formed gate, when a generator transfers through a conduit
  and port, then generated FE equals all buffers plus actual consumption; removed
  parts and ambiguous controllers accept no further charge.
- AC3 (FR3): Given a complete Tier1 gate, when Preview is used, then it says Tier1
  is complete and labels Tier2 separately as an upgrade, never an alignment fault.
- AC4 (FR3): Given missing structural blocks, when diagnostics are requested,
  then each group identifies section, required block and count without coordinates.
- AC5 (FR4): Given a nearby authorized viewer, when the schematic is toggled,
  then it renders the authoritative bounded plan without modifying the world;
  toggling off or changing dimension clears it.
- AC6 (FR2/FR5): Given saved gates and return platforms, when reloaded, then
  legacy builds, exact menu FE and safe home routing remain valid.

## 6. Edge cases

Duplicate controllers, overlapping valid gates, unloaded neighbours, missing
ports, extra nonessential decoration, tier upgrades/downgrades, controller-facing
changes, stale handlers, broken parts during countdown and disconnected viewers.

## 7. API contract

```ts
type Formation = { centre: BlockPos; orientation: HorizontalDirection;
  tier: 1|2|3|4|5|6; controller: BlockPos; ports: BlockPos[] };
type Requirement = { section: string; blockId: string; count: number };
type Guidance = { formedTier: number; targetTier: number;
  mode: 'repair'|'upgrade'; requirements: Requirement[] };
```

The server owns validation and requirements. Client controls cannot supply a
trusted formed tier, grant admin privileges, place blocks or create energy.

## 8. Data model

| Data | Persistence | Owner |
| --- | --- | --- |
| Gate owner, FE, upgrades and return binding | Existing block save | Server |
| Resolved formation | Revalidated runtime result | Server |
| Construction requirements | Derived from required geometry | Server |
| Schematic visibility and expiry | Temporary, not world save | Client |

## 9. Out of scope

New tier costs, survival recipes, research rule inventions, weather changes,
arbitrary vertical service placement, save regeneration and automatic builders.
Headless tests do not approve client visual appearance.
