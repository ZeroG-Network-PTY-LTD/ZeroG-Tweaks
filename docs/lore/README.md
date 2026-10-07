# ZeroG lore guide: follow this when building anything

This is the approved story of ZeroG Tweaks, gathered in one place so every tracker item, structure, mob, Codex page and line of text stays consistent. It only restates what's already approved, and each section names its source. When something isn't covered here, **don't invent canon**. Flag it as "lore needed" and ask the owner.

The build trackers link here. Their items carry a short **Lore** note wherever the story affects how something should be built.

## Premise: the Splintered Concord

Source: design doc, *Lore: The Splintered Concord*; `briefs/prologue_the_signal.md`.

- **The Concord** was a spacefaring civilisation that migrated through five galaxies. **Earth was meant to be their refuge.**
- **Archon Vael**, the Concord's leader, ordered the null experiments. He tore space open at Skarn and finally fused himself with Solvane's dying sun. He is the recurring villain, heard in logs and rift whispers and always one world ahead. Until Act V he is never met in person.
- **The Splinter creatures are the Concord.** They shattered themselves to hold Vael back. This is the Act V reveal, so earlier content may show Splinter creatures but must not explain them.
- **The player** is finishing the Concord's migration without knowing it, until Solvane.

## Characters

| Character | Who they are | Rules for content |
| --- | --- | --- |
| **Echo** | A friendly Splinter Wisp, the remnant of the Concord's chief navigator. She guides the player through the Codex. | She **remembers a world only after the player reaches it**. Her lines must never describe a place the player hasn't been. She speaks through Codex pages and advancement toasts, not a dialogue system. |
| **Archon Vael** | The Concord leader behind the null experiments. | Logs and rift whispers only, always one world ahead, until he is revealed as the Dying Star. |
| **The Keepers** | Guardian constructs still following the Concord's orders. | Concord-made guardians, such as the Prism Sentinel. They test and protect; they aren't evil. |
| **The Hollow Fleet** | Ghost crew on Eidolon waiting for a rescue that never came. | Mournful, not hostile by default. The Captain can be talked down. |

## Prologue: The Signal (Overworld), approved 4 Oct 2026

Source: `briefs/prologue_the_signal.md`. This is already built in code.

1. A Concord **Pathfinder** ship sent ahead crashed deep under Earth. Its shattered gate core seeded deepslate with **Nullifite**, and the ore's hum drew the sculk. Ancient cities were built around the wrecks.
2. The **Moon relay**, kept by the Lunari, has listened for that hum for thousands of years. Picking up the first Raw Nullifite makes it reply: a **Courier Pod** lands the next night near the player.
3. The pod holds **Echo's Dormant Wisp**, the **Concord Codex** (a refugee builder's template) and a **Broken Console**: *"Refuge signal received. Courier dispatched. Rebuild the gate. We are waiting."*
4. The **Gate Controller is built around Echo's wisp**; it's a required ingredient. On waking she asks, *"How long have I been asleep?"*
5. Her shattered memory holds only the Moon relay and the old Mars waystation, so **T1 reaches only the Moon and Mars**.
6. Recovery: a second pod after 7 in-game days, and a small Dormant Wisp chance in ancient-city chests. Never bypass claim protection to deliver a pod.

## The five acts

Source: design doc, *Acts*; villager lore in `generators/villagers/species.py`.

| Act | World | What happens | Must be true in content |
| --- | --- | --- | --- |
| I. The Falling Star | Sol: Moon, Mars | Meteor Maws bring Concord debris to the Moon. Echo wakes, wants to go home and can't remember where. Mars holds the first sign of the Concord: a hand-cut Aresite core. | The Lunari greet the player as "the one who answered the signal". The Rustborn keep an Aresite core shrine in every village; they're the first people who remember the Concord by name. |
| II. The Quiet Mines | Galaxy 2: Cerulon | The Concord's peaceful mining world. The Prism Sentinel is **a test, not a hunt**: it asks "Are you Concord?", fights in light-refracting phases, and once beaten accepts you as an **heir**. | The Vault and arena feel calm, precise and Concord-crafted. After the Sentinel, Glintfolk call the player "heir" in trade titles. |
| III. The Wound | Galaxy 3: Skarn | Where Vael tore space open. The **Rift Tyrant**, his lieutenant fused into the rift, pulls pieces of the arena into the void. Afterwards Echo remembers she plotted the course here. | Rift Glass marks the fracture zones. The Ashwrights descend from the Concord smiths caught at the forges; they **forged the first gate parts**. |
| IV. The Frozen Fleet | Galaxy 4: Eidolon | Survivors fled here and froze. The **Eidolon Captain** can be fought, *or* shown the crew's final log with enough Remnant Shards. Either way he yields the key, and the talk-down route adds a unique reward. | Wrecks are the Fleet's ships. Broken Consoles and Remnant Shards carry their memories (the main lore source). The Hollow Kin are the children thawed first. |
| V. The Last Light | Galaxy 5: Solvane | The Nova Pearl reveals Vael fused himself with the dying sun: **the Dying Star is Vael**. The Splinter creatures are the Concord. Earth was their refuge, so the player has been finishing their migration. | The Sunwardens kept their oaths through it all; what they think of the player depends on the ending. |

### Ending choice

Made per player, using the Heart of Solvane.

| Choice | Outcome |
| --- | --- |
| **Rekindle the star** | Solvane burns bright; radiant T6 gate crown; **Echo stays** as a companion. |
| **Let it fade** | Concord remnants go free; void-themed crown; **Echo says goodbye** in a final Codex entry. |

### Side quests

These are the only ones with approved story.

| Side quest | Story |
| --- | --- |
| Sunken Relay | A distress signal still broadcasting. |
| Buried Observatory | Leads to a hidden planet; this is where Star Map Fragments come from. |
| Collapsed Forge | The smith who built the first gate. It ties to the Ashwrights. |

Frozen Outpost, Sunken Lab, Prism Spire and Impact Site have **no written story yet**. Build them as Concord ruins or wildlife sites and flag any text for approval.

## Peoples (planet villagers)

Source: `generators/villagers/species.py`, `blockbench/villagers/README.md`. Gravity shapes their build.

| People | World | Signature profession and job site | Lore to keep |
| --- | --- | --- | --- |
| Lunari | Moon | Regolith Refiner (Ore Refinery) | The oldest stay-behinds, left to watch the Moon relay. Tall, light, wide dark eyes. Old pressure suits; a selenite sliver on the hood marks coming of age. |
| Rustborn | Mars | Rust Mechanic (Combustion Generator) | The families who stayed to work the Olympium seams. Ponchos and respirators outdoors; goggles pushed up only to show trust. They keep an Aresite core shrine in every village. |
| Glintfolk | Cerulon | Crystal Tender (Crystal Growth Chamber) | The miners who stayed with the Sentinel. Concord hard hats; Cerulite spurs on the shoulders, filed down for luck. They call the player "heir" after the Sentinel. |
| Ashwrights | Skarn | Ashwright Smith (Alloy Forge) | Descended from the Concord smiths changed by the rift; skin like skarn rock that still glows in the cracks. Scorched-marble masks, because showing your fire is rude. They forged the first gate parts. |
| Hollow Kin | Eidolon | Salvager (Salvage Station) | The children of the Fleet, thawed first. Everything they own is salvaged. Their lanterns burn with the ghosts' cold light. |
| Sunwardens | Solvane | Sun Keeper (Solar Array) | Tended Solvane's star long before it began to die, and kept their oaths. Corona halos are grown, not worn. Their attitude follows the ending. |

## Naming and catalog rules

Source: design doc, *Universe structure and naming*; *Galaxy generation rules*.

- **Catalog format:** `ZG-[galaxy number] [planet letter] "Name"` plus a class tag. Moons add a Roman numeral, e.g. `ZG-855 b I "Cinder"`. Planet letters start at b; a is the star.
- **Class tags:** Resource, Hostile, Stellar, Frozen, Derelict and similar.
- **Fixed names:** resource planets (Cerulon, Skarn, Eidolon, Solvane) never change between seeds, and each rare gem is named after its planet.
- **Seeded names:** only wasteland and moon names come from the seeded name pool. Never hand-write story names for wastelands.
- **Every wasteland** gives one small reward, so players don't skip them.

## How the story reaches the player

Source: design doc, *Delivery*.

- The **Codex fills one chapter per galaxy**, unlocked through advancements. Echo's lines appear as Codex pages and advancement toasts, so no dialogue system is needed.
- **Lore carriers:** Starlite, Remnant Shards, Broken Consoles, Star Map Fragments and the Nova Pearl.
- **Research gating** for genetics uses Concord Codex advancements (approved 6 Oct 2026).
- **Player-facing story text** goes in lang keys (`en_us.json`), never hardcoded strings.
- **No new canon:** don't invent coordinates, factions, characters or registry IDs, and don't reveal before Act V that the Splinter creatures are the Concord.

## Content that still needs approved lore

Build the mechanics, but get the words approved before shipping them.

- Echo's transition-screen lines in `docs/gate-transition-screen-v1`. These are placeholders I wrote, not canon.
- **Concord debris** plan approved7Oct2026: existing Star Map Fragment drops are the interim lore carrier. Small Moon impact wrecks remain pending, using approved crater, meteorite fragments, pod-shell and chest pieces without a Dormant Wisp, Concord Codex or Broken Console. Do not turn the Courier/Eidolon story console into mob loot; this is not a Sol progression blocker. Any later wreck logs still need approval.
- The Cinder Mite's origin, the Frozen Outpost, Sunken Lab, Prism Spire and Impact Site stories, and the Broken Console log texts for each act.
- Bespoke Echo dialogue for Acts II to V still needs wording approval. The owner's
  7 October step-by-step Codex request now ships localized factual summaries of
  the approved acts, gated by arrivals and existing milestones; see
  [step-unlock design](codex-step-unlocks.md). These pages do not implement pending
  Captain talk-down or final ending mechanics.
