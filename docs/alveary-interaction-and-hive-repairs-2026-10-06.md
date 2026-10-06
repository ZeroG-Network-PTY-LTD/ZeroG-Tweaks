# Controller interaction and planetary hive discovery repairs

Minecraft Java **1.21.1 / NeoForge**, unchanged **1.0.12-dev** version.
This batch repairs existing systems; it does not complete survival crafting,
honey production, advanced biology, research or the wider machine queue.

## Controller interaction

Ordinary held items now open the modern alveary controller instead of falling
through to the orbital addon's older menu. Wrenches and deliberate sneak-placement
retain their own actions. A real right-click event holding a stick reproduced
the failure before the fix and passed afterwards.

## Detailed formation diagnostics

The modern menu was previously excluded from the existing server status bridge.
It now receives the live structure result through the already registered status
message. Hover the top-right **Structure incomplete** status to read the full
reason. Stale information from another menu is discarded. Legacy sorting packets
cannot bypass the modern menu's validated output paging/sort controls.

The status regression reproduced the exclusion before repair. The server test
checks an incomplete controller exposes a nonempty formation reason; this is not
proof of client tooltip readability or a complete GUI redesign.

## Planetary hive discovery

All twelve original hive families now register point-of-interest types, covering
every facing and honey-level block state, and join Minecraft's `bee_home` tag.
The existing vanilla hive storage, block tags and bee behaviour remain in use.

A newly spawned Moon bee finds its hive without assigned coordinates. An offspring
created through the normal breeding-offspring interface also discovers it. Every
family's possible hive states are checked against the vanilla bee-home registry.
This is not a test of every planetary landscape or courtship animation. Vanilla
bee AI can choose any nearby tagged hive; species-exclusive ownership is not added.

## Verification and remaining work

The complete enabled isolated suite passed **76 required tests**, with Productive
Bees and the orbital addon present. Transcript:
`20261006_155526_runWorkflowTests.log`. These include existing mining, refinery,
transport, genetics, service-port and save/reload checks. The three new regressions
were first observed failing in isolated tests, then passed after their fixes.

User-approved honey production should retain combs and add honey alongside them.
The proposed initial amount is 250mB per cycle, matching the existing bottle
measure. Orbital species have no honey-fluid IDs of their own; planet-local honey
with Moon Honey outside the six planets was proposed and remains unanswered.
Do not invent that mapping or claim normal production reaches the tank yet.

Survival recipes for machines, frames and consumables remain pending. Dedicated
jelly artwork, research unlock mappings, advanced biology rules, gas definitions,
energy pulses, fluid waves, remaining sided-machine controls, story progression
and wider ecology checks remain in the [TODO ledger](storage-and-machinery-todo.json).

No new textures, model changes, planet regeneration or hub/save edits are included.
Production-build, JAR hash, installation and publication details are recorded in
the companion delivery receipt after verification.
