# Step-by-step Concord Codex and clean compact hub

Same **1.0.12-dev**, Minecraft 1.21.1 / NeoForge. No new story factions,
coordinates or registry IDs are invented. Pages summarize the approved Concord lore.

## Read the book again after completing a task

The server refreshes the Concord Codex for its current reader whenever it is opened. Normal right-click opens the contributor's GuideME walkthrough; sneak-right-click opens these unlocked story pages in the book viewer.
Pages unlock from completed advancements and recorded planetary arrivals, not from
another player's written-book contents. Merely owning a late-game item cannot reveal
an unvisited world's story. Older Moon/Mars arrival flags remain compatible; all six
world memories are copied across player death/clone events and saved normally.

| Completed task | Newly available instructions or memory |
| --- | --- |
| Pick up Raw Nullifite | Watch the following night for the Courier crater |
| Find the Courier | Read its console and recover Wisp/Codex |
| Read the Codex | Build the controller around the required Dormant Wisp |
| Obtain the controller | Form, charge and inspect the first gate |
| Reach Moon | Lunari relay, Moon materials and Star Map Fragment guidance |
| Reach Mars | Rustborn Aresite shrine and core milestone |
| Record Aresite after Mars arrival | Prepare the next gate tier |
| Reach Cerulon | Quiet Mines chapter; seek the guardian test |
| Complete Sentinel milestone after arrival | Heir memory and onward preparation |
| Reach Skarn, then complete Rift Heart milestone | Wound chapter, then Echo's course memory |
| Reach Eidolon, then record Remnants/key milestones | Fleet chapter, shard guidance and onward instructions |
| Reach Solvane | Last Light chapter without the final revelation |
| Complete Nova Pearl milestone after arrival | Vael/Concord revelation |
| Complete Heart milestone after those requirements | Approved ending options, explicitly marked mechanically unfinished |

Existing advancement definitions remain authoritative. Some support an item reward
as their completion criterion; this journal does not replace them with a new boss
kill rule. Existing survival recipe balance, research unlock mechanics, Captain
talk-down and ending outcomes remain tracked separately rather than silently claimed.

For precise gate counts and layers, retain the
[six-tier building guide](gate-building-tiers-1.21.1.md). Hub gates stay ADMIN;
their free travel is not proof of completing survival progression.

## Hub reset

The accidentally modified **ZeroG_Planet_Showcase_1_0_12_Compact_Hub_Seed0** is
recoverably archived outside `saves`. A validated clean seed-0 hub takes its place.
The reset starts fresh player inventory/exploration and removes the accidentally
placed arena. The ten deliberately authored eastern showcase exhibits remain.

Six tiered gates are north, supplied machinery/transport west, apiary/alveary
examples south and structural exhibits east. Landing pads are gate-only. No
planetary terrain or permanent forced chunks are copied; planets generate upon
first visit. This is not a claim that all 34 destinations were pre-generated.

The [delivery receipt](codex-clean-hub-delivery-2026-10-07.json) records tests,
the same-version installed JAR and hub-reset evidence. Client book layout and
travel approval remain your playtest.

The final runtime preserves the newly published contributor GuideME walkthrough.
Its matching NeoForge 1.21.1 dependency, GuideME 21.1.19, is installed locally.
Story-reader checks were rerun successfully after integration; client guide
rendering remains unapproved. This does not implement additional ending choices.

The first combined test attempt encountered Productive Bees' mock-client
handshake rejection before book assertions. Book-reader tests therefore use a
separate no-addon world; hub formation/routing/workshop checks run with the
installed optional addon present. The isolated Solvane book fixture is deliberately
flat and proves arrival/memory gating, not planetary terrain or real portal travel.
