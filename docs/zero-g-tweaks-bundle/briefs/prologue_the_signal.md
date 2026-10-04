# Prologue: The Signal (Overworld)

Status: lore and hard-gate decision approved by the user on 2026-10-04.
Implemented and locally installed in the verified 1.0.12-dev build. This brief
is not executable game data. Native book/read
advancement, hard recipe, appended 5% ancient-city backup loot, two-delivery
schedule/recovery ledger and safe 73-block Courier template have isolated tests.
Full survival gate-tier UI/progression and arbitrary claim integrations remain
unfinished; the approved lore must guide their later implementation.

## Governing lore

Earth was intended to be the Concord's refuge. A Pathfinder ship sent ahead
crashed in the deep rock; its shattered gate core seeded deepslate with Nullifite.
The ore's constant hum attracted vibration-sensitive sculk. Ancient city builders
settled around the wrecks, explaining the deposits and the Warden's presence.
Retain existing ore placement: this explains world generation, not a redesign.

The Moon relay, maintained by the Lunari left to watch it, has listened for the
Pathfinder's Nullifite resonance for thousands of years. The player's discovery
prompts a reply: a Courier Pod fired toward Earth, arriving the following night
within approximately 100 blocks of the player on an open surface.

The pod contains a Dormant Wisp (Echo), the Concord Codex, and a Broken Console.
The console's first log reads:

> Refuge signal received. Courier dispatched. Rebuild the gate. We are waiting.

The Codex is a refugee builder's template. Echo supplies the expertise needed
to rebuild alien technology from scratch. The Gate Controller is built around
her Dormant Wisp. On waking she asks, "How long have I been asleep?"

Her shattered memory initially retains only the Moon relay and the old Mars
waystation. T1 therefore reaches only Moon and Mars. Preserve the established
later-tier memory/progression story, rather than inventing new coordinates.
On the Moon, Lunari recognise "the one who answered the signal"; on Mars the
Rustborn's hand-cut Aresite core supplies the first proof of the Concord.

## Approved requirement: hard gate

A Dormant Wisp is a mandatory ingredient in the Gate Controller recipe, not
merely a recipe-book unlock or optional dialogue trigger. Recovery routes are
part of this requirement, not optional extras:

- First Raw Nullifite pickup schedules one Courier Pod for the next nightfall,
  once per player, on an open surface outside protected claims.
- If the player has neither a Dormant Wisp nor a controller after seven in-game
  days, dispatch a second pod.
- Ancient-city chests have a small Dormant Wisp chance as a server/lost-item
  backup. Implementation starts at 5% per not-yet-generated chest; this is a
  tunable balance choice rather than a previously locked lore value.

The first mining discovery is the story trigger; first Raw Nullifite pickup is
the proposed Java detection hook. Do not silently treat repeated pickups as
repeatable pod farming.

## Pending implementation scope

New item IDs: `dormant_wisp`, `concord_codex`. New structure ID:
`concord_courier`, containing a small crater, meteorite fragments, pod shell,
chest, and Broken Console. Preserve existing IDs; confirm actual registry names
before writing executable recipe, advancement, structure or loot data.

Change the Codex root wording from "fell from the sky" to
"It hums. Pick up a piece of Nullifite."
Add "Falling Star" (find the pod) and "Builder's Template" (read the Codex)
between the root and existing `first_gate` step without renaming existing IDs.

Before implementation, verify persistence across logout/restart, offline-player
delivery handling, claim integrations and safe-site selection, multiplayer
ownership/eligibility, the seven-day recovery clock, and what happens when no
unclaimed surface is available. Never bypass protection to force delivery.
Test actual crafting, recovery and story progression in disposable worlds.

## Branch ownership

This approved design brief belongs on **Design**. Executable Java, recipes,
advancements, language entries, loot and shipped assets belong on **1.21.x**.
Published player-facing lore and guides belong on **Docs**. Do not merge these
unrelated branch histories, rename existing IDs, or change ore placement for
this Prologue. Commit/push only when publication is requested.
