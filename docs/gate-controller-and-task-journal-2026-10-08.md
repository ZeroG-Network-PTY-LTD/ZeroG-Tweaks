# Gate controllers, task journal and combustion spacing

Minecraft Java / NeoForge 1.21.1, same `1.0.12-dev` candidate.

## Saved-world diagnosis

A read-only comparison of the owner's Compact Hub found:

| Controller | Saved facing | Matching layout | Missing required port |
| --- | --- | --- | --- |
| Player build `-33,65,-15` | East | West | `-31,65,-17` |
| Spawn tier 1 `-22,65,-24` | South | North | `-20,65,-22` |

Both stored zero FE and had no valid formed tier. The other five admin gates
matched their expected tiers and retained their charged buffers. The comparison
uses `tools/audit_saved_gate_layout.py`; it reads region files without loading,
resetting or writing the user's world. Earlier advice implying the energy port
could be removed because the controller accepts FE was incomplete: direct
controller charging is supported, but the port remains a required structure part.

## Repair without rebuilding your gate

1. Open the unformed controller and press **Preview**. It reports the best-fitting
   orientation and up to four missing-block coordinates, with particle markers.
2. Press **Align** to turn only the controller to the matching layout direction.
   Ownership, energy and upgrade inventory remain on the same block entity.
3. Add the required **Gate Energy Port** at the reported position. For the two
   inspected gates, use the coordinates above. Keep all required frame/pad/pylon
   parts; neither Align nor admin travel bypasses physical formation.
4. Connect the generator's enabled output through ZeroG energy conduits to the
   port. It charges the controller's shared buffer, not a separate port battery.
5. Confirm the tier and FE. The display now synchronizes exact FE rather than
   rounding down to 10,000-FE steps. Hover the status for the full value.
6. Choose a reachable destination, stand above the pad and use Engage/Ready.
   Admin hub gates refill automatically; ordinary survival gates require energy.

Align is owner-controlled, only available when unformed and not launching. It
selects the direction with the fewest missing tier-1 parts, retaining the current
facing on ties. It never supplies missing blocks or weakens the formation rule.

## Concord Codex task journal

Sneak/right-click opens personal task pages before the story. `[x]` means a real
recorded advancement/arrival; `[ ]` means outstanding. Reopen to refresh. The
prologue tracks Nullifite, Courier discovery, Codex reading and obtaining a Gate
Controller. That existing advancement does not prove a physically formed gate.
The Moon/Mars list unlocks after gate progress or an actual arrival. Later-world
tasks only appear after that world's arrival. Reading a guide does not complete
tasks, and a borrowed book is rebuilt for its new reader.

Normal right-click still opens the GuideME walkthrough. Its index explains the
task journal; gate/power chapters now describe Align, required ports and conduits.
The matching page generator is retained on Design. Undefined biology research,
final endings and survival recipe costs are not invented by these checklists.

## Combustion GUI

The existing fuel artwork and slot indices are retained. The screen is now
278x210, with player slots moved down 26 pixels so machine information has its
own area. A horizontal burn gauge and remaining/total fuel-tick line are above a
separator, followed by the player inventory. Status labels are shortened;
module/output labels are bounded to 108 pixels, leaving the energy gauge clear.
Hover shows full burn ticks, module count and output rate. The Fuels button stays
within the screen bounds and the catalogue remains outside player inventory.
This is a layout overhaul and bounded text repair, not proof of every GUI scale
or a replacement artwork approval. Client visual review remains on the list.

## Evidence and remaining checks

Gate-only run `20261007_230629_runWorkflowTests.log`: four required tests passed,
including real combustion generation and public conduit/controller/port access,
conserved FE, malformed-layout rejection, Align and stale removed-port rejection.
The initial harness invocation selected no tests because its template namespace
was wrong; its Gradle success is not counted as a gameplay pass.

Combined run `20261007_231131_runWorkflowTests.log`: all eight required tests
passed, covering five gate/task tests, existing lore data checks, real Codex item
interaction, Moon/Mars arrival-based pages, borrowed-reader safety and reload.
Both disposable servers shut down cleanly. `tools/test_combustion_layout.py`
passes the native 37-slot/control/metric bounds contract; the existing 37 machine
profiles also pass their audit. These are static layout checks, not rendered text
or client approval. Clean production delivery is recorded in a separate receipt.
Client visual review, all higher-tier
orientations, actual player launch and optional-addon integration remain distinct
from these targeted no-Productive-Bees server checks. User saves are not edited.
