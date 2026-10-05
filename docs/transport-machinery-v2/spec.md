# Original ZeroG industrial transport and diagnostic UI

User direction recorded 2026-10-06. Target: Minecraft Java 1.21.1 / NeoForge.
This is a design/workflow specification, not evidence that all features ship.
The reference was read from Downloads; follow its glass item tubes, green-core cells and side matrix alongside the approved A/C style lock.

## Style and ownership

Original ZeroG models, textures and code only. Mekanism is a usability reference,
not an asset/code source or dependency. Keep existing registry names. Equipment
and machinery use C magitech; vegetation keeps its approved A/C blend. Maintain
centered readable silhouettes, hue-shifted shade clusters, coherent pixel density
and matching inventory/placed artwork. Do not use painted fake liquid in tanks.

## Transport specification

| Family | Chassis | Active visual | Status |
| --- | --- | --- | --- |
| Power | Opaque reinforced casing, blue inlays | Directional energy pulses through junctions | Pending pulse renderer/art |
| Liquids | Glass-sided mechanical pipe | Actual fluid tint and directional waves | Transient routing cue exists; waves/art pending |
| Gas | Steel chambers | Swirling real stored gas texture | Pending gas registry, conserved transfer contracts and art |
| Items | Transparent framework | Small 3D items travelling through connected segments | Transient routing cue exists; client approval/art pending |

Animations must reflect committed server transfers, never simulations or blocked
operations; client visuals do not duplicate or own resources. Only loaded segments
participate. Energy/fluid transfer limits follow the actual network bottleneck;
item transfer retains its distinct existing contract. Gas rates/units must be defined
before implementation, not treated as fictional liquid IDs.

## Machinery and storage

- Existing crushing/smelting systems: heavy readable housings, articulated gears,
  furnace glow tied to actual processing state. Existing logic/GUI/ports first.
- Energy cells: green core and physical fullness gauge tied to synchronized FE.
  Existing GUI charge bars do not certify this in-world gauge.
- Holographic diagnostics: wiring and I/O overlays, distinguished from decorative
  preview geometry. Never present the current multiblock guide as live diagnostics.

## GUI contract

- Dark original panel with separate input, output and upgrade areas.
- Vertical gradient energy reserve with exact capacity/current-value tooltip.
- Horizontal processing arrow representing authoritative progress.
- Interactive color-coded 3×3 side matrix: explicitly map six actual faces;
  unused cells are inactive. Input/output/off states are server-validated.
- No second sneak-click menu. Held wrench/module/bucket actions remain intentional
  operations, not alternate decorative screens.

## Alveary service base

New 5×5×5 service-base layouts require two item ports, two fluid ports and one
energy port on the bottom perimeter. The matching controller may occupy any
second-row wall/corner casing position. Keep the tier roof and 18-block clear
flight chamber. Generic ZeroG ports work across all seven tiers; native hatches
remain usable where they actually exist. Input/output modes must be labelled.

Controller GUI access is independent of automation: cables, pipes and item tubes
must use service ports, not the controller. Existing corner-controller shells are
retained for save compatibility, not silently destroyed or rebuilt.

## Artwork queue

- [ ] Distinct original input/output hatch faces and shared tier trim.
- [ ] Blue energy socket, cyan fluid inlet and clearly differentiated honey outlet.
- [ ] Active/inactive port accents matching actual role/configuration.
- [ ] Inventory models centered and consistent with placed blocks.
- [ ] Update editable models/generators and both runtime resource layers together.
- [ ] Native texture/UV validation, preview sheet and player client approval.
- [ ] Power pulses, gas tubes, physical energy gauges and diagnostic overlays.

## Implemented local batch

Six item-tube, six cell-side, six cell-top and nine charge-gauge textures now use
editable native 32×32 source drawing (27 textures). Glass interiors retain alpha;
green gauges remain driven by actual charge. All 66 existing model UV contracts
stay in Minecraft's 0–16 coordinates. Runtime and existing resource-pack overrides
match the Design source byte-for-byte. `native-preview.png` is a texture contact
sheet, not a client render; player visual approval remains pending.

Transport and storage-tank screens share a functional six-face 3×3 matrix:
red input, green output, purple both, gray disabled. Unused cells are inactive.
Existing validated server commands remain authoritative. Other machine panels
still require their own configurable routing backend; they are not completed.

The required local game-asset-production CLI is unavailable. This batch uses
the repository's editable native generators and local alpha/UV/binding checks
instead; no paid generation or copied assets were substituted. Power/gas visuals
and diagnostic overlays remain pending.
Runtime fixes are server-tested separately. Publish artwork on Design, runtime on
1.21.x, and player guides/images/JAR/checksums on Docs; never merge their histories.
