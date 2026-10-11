# Illustrated Concord journal

Run `write_guide.py` with the code branch's `src/main/resources/assets/zerog_tweaks` directory. It runs `illustrated_journal.enhance` last; do not rerun an older generator afterward. The helper locates `tools/generate_gate_build_guide.py` in that code checkout and uses its reviewed `parts(tier)` function.

Visual direction: a Concord dossier/navigation desk in dark navy, cyan/violet accents, warm paper reading area, enlarged current item icons. Technical illustrations use actual native block models through GuideME GameScene/BlockImage, not AI concept art passed off as gameplay screenshots. No new paid provider, GLB, copied third-party art or external asset package is involved.

The generator provides six exact gate plans: separate layers plus complete final scenes; a seven-machine purpose reference; a middle-slice remnant illustration from CometRemnant's sphere math; a story-first expedition index; and illustrated entries into existing practical pages. Counts are complete target structures, not incremental upgrade shopping lists. Flexible service positions remain examples.

Runtime `CodexJournalScreen` handles reading layout and scroll controls. `CodexJournalSync` carries only the current reader's server-selected localized pages, max64. Existing story gating and native sneak-book behavior remain untouched. Public technical references are not research or advancement unlocks.

Verification: `CodexIllustratedGameTests` compares every pictured block/layer with live SurvivalGateLayout geometry, parses GuideME source and checks item references. Existing CodexStoryGameTests protects arrival/reload and borrowed-book privacy. Client GPU rendering/layout review, new button-label localization and additional bespoke narrative scenery artwork remain separate TODOs.
