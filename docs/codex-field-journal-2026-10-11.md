# Concord Codex — illustrated field journal

The Codex now opens as a dark Concord dossier around a warm paper reading panel, with cyan/violet accents, enlarged native item images, page controls and a scrollbar. It is a story journal first, not a machine inventory.

## Reading it

1. Right-click the Concord Codex. Your own milestone checklists and recovered memories come from the server on every open.
2. **Next task** finds the first journal page containing an unfinished checkbox. Checkboxes describe recorded milestones; they are not clickable rewards. Reopen after completing a task to refresh.
3. Use arrows to read recovered story pages. Scroll long text. Future personal chapters remain sealed by the existing arrivals/advancements.
4. **Field guide** opens the story-first expedition index: Signal → Courier → Build → Power → Launch → Moon → Mars → Return, with later memories in your personal journal.
5. **Gate layers** opens six illustrated construction guides. Each layer is separately rotatable, followed by a complete assembly and exact block counts.
6. **Machines** explains the existing refinery, forge, growth chamber, salvage station and generators, with native block illustrations and links to genetics/alveary/frame references.
7. **Impacts** shows a remnant cutaway and explains the Courier versus planetary comets/asteroids versus static ruins.

Sneak-right-click retains the native book viewer. Missing negotiated journal support falls back to the existing GuideME opening. Technical reference pages are public; they do not grant story progression or reveal another reader's recovered memories.

## Construction conventions

Pad level is y=0. Begin below it with the buried core where required, then the frame-ring foundation, pad, service row, pylons and rear arches. Each page shows the **full target tier**, not just new blocks. Service positions are valid examples: controller facing remains cosmetic and legal controllers/ports may move without replacing structural cells.

Every figure uses the actual registered block models/textures. This avoids concept art disagreeing with inventory or placed appearance. Painted backgrounds or new machine textures were not substituted. The gate tariff and existing formation rules were not changed.

## Lore boundaries

The impact diagram uses the actual ten-block spherical remnant's middle slice and a representative Moon palette. Rare central ores and random inclusions are not guaranteed in those exact quantities. Active-world placement may fail; one successful event per day is a limit, not a guarantee. No extra console loot, distress dialogue, hidden coordinates, boss ending or research milestone was invented.

## Verification and review

Isolated tests compare every pictured gate layer and final assembly against runtime geometry, parse the new GuideME pages, check illustrated item IDs, and preserve the existing cross-reader/arrival/reload story-unlock regression. Dedicated-server success does **not** prove client layout, GuideME GPU rendering or button appearance.

Both required tests passed in `20261011_100701_runWorkflowTests.log`; the earlier run also passed. They cover all six tiers, 15 parsed/referenced pages, arrival-gated late memories, borrowing another player's book and reload. The disposable servers stopped normally. None of these tests loaded your client or changed your saves.

Production clean build passed in47 seconds (`20261011_100942_clean.log`), without optional test classes/fixtures. Asset binding audit has zero errors across8,021 models,1,529 blockstates,4,005 PNGs and130 animation metadata files. [Asset receipt](reports/codex-journal-assets-20261011.json) · [Installation/backup receipt](reports/codex-journal-install-20261011.json) · [Same-version JAR](jars/zerog-tweaks-1.21.1-1.0.12-dev-codex-journal-20261011.jar). SHA-256: `fb4344f099e81c5c562aac3e345402c38f035d4b8d6b57dfe68096c24ddf8872`.

Please inspect the journal at your usual GUI scale: long pages scroll, navigation does not cover text, buttons open their intended guide pages, all six gate diagrams rotate, and your existing completed milestones remain correct. Client approval and a full GuideME compile/render across all addon configurations remain pending. Additional bespoke narrative scene artwork and localization of new interface labels can follow your visual review.
