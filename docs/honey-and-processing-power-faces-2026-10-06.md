# Honey by-products and processing power faces

Same-version candidate: Minecraft Java 1.21.1 / NeoForge, ZeroG Tweaks
**1.0.12-dev**. This is a focused delivery, not completion of the full machinery queue.

## Alveary honey

T3 and higher controllers produce **250 mB honey alongside their comb outputs**
per completed cycle. Combs are not consumed to obtain this by-product. The working
mapping uses Moon, Mars, Cerulon, Skarn, Eidolon or Solvane honey in the matching
ZeroG dimension, and Moon Honey elsewhere. Galaxy-slot dimensions currently use
that fallback rather than inventing additional honey registries.

The honey tank needs room for the complete measure and cannot mix different honey
types. A full or incompatible tank pauses the cycle without charging additional
power or discarding progress. Drain it through its physical honey port to resume.
The controller shows **Honey tank blocked**, with an explanation on hover.
Existing honey-bottle collection remains available. T1/T2 behavior is unchanged.

The disposable server checks exercise a real Productive Bees iron-bee cage recipe,
component-bearing comb results, actual production-to-port extraction, simulated
drains, full/mismatched tank pauses, resume and saved tank contents. This does not
prove production for every native orbital species or every planetary dimension.

## Processing power panel — explicitly power only

Ore Refinery, Alloy Forge, Crystal Growth Chamber and Salvage Station use the shared
processing screen. A six-world-face colour matrix now sits beside the original
slots, without shifting their input/output or inventory coordinates.

- Red **Input** accepts FE on that face.
- Grey **Off** rejects FE on that face, including cached handlers.
- Faces are labelled Down, Up, North, South, West and East, not camera-relative.
- Defaults preserve existing power access; the choices persist in machine NBT.
- The server validates button IDs, machine ownership and player distance.

This is **not** configurable item/fluid routing. Existing reagent/catalyst/output
sides remain unchanged. These processing machines have no fluid tank; the panel
does not pretend to configure one. Broader per-resource side modes for the remaining
machines are still pending. Client layout and automation readability need player review.

## Still pending

Survival recipes remain last, awaiting the user's exact ingredients, quantities and
tier requirements. Do not generate guessed starter costs. Also pending: remaining
item/fluid side controls, directional transport visuals, defined gas IDs/units,
Concord Codex research and verified advanced biology, larger alveary layouts,
recipe discovery, progression and ecology checks.

No textures, registry IDs, world generation or saves are changed by this delivery.
Existing approved A/C artwork is retained. Design and Released need no commit.

## Verification and delivery

All **77 required isolated server tests passed**, including power capability access
on every face of all four machines, synchronized control state, persisted choices,
remote-button rejection and cached-handler revocation after block replacement.
The production build passed; test classes and fixtures do not ship. The runtime
asset audit reported zero errors. Client rendering is still pending player approval.

Installed in the CurseForge ZeroG mods directory before branch publication. The old
same-version JAR is backed up in `zerog-mod-backups/20261006-162600-UTC`.
[Delivery receipt](honey-power-delivery-2026-10-06.json) records the candidate hash,
archive, test/build logs, scope and remaining work.
