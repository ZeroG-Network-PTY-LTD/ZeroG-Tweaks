# Design branch — publication layout

Blockbench projects, texture studies, concepts, sheets and the HTML collection
are preserved here. Documentation/gallery and development jars are on
[Docs](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/Docs);
gameplay/runtime resources are on
[1.21.x](https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks/tree/1.21.x).
This branch has an independent root, never merged with code or Docs.

The collection's original 1,381-entry hash roster remains a historical snapshot.
All art bytes are unchanged. Its six archived Java drafts were relocated to
`1.21.x/tools/design-code-archive/` preserving paths beneath the former docs/ root and
bytes. Resolve those six roster entries there; do not interpret their removal
from Design as missing artwork. All 22 archived Java drafts (six collection,
six standalone Tidewraith and ten bundle drafts) are under
`1.21.x/tools/design-code-archive/`, not compiled.
Design-only JSON/resource studies remain here; runtime resources live in src/.

Generators are on this branch. From this checkout:

    python generators/export_tidewraith_models.py --code-root ../zerog-code-1.21.x
    python generators/generate_multiblock_guides.py --code-root ../zerog-code-1.21.x

The first command plans/verifies without writing. Approved import additionally
requires `--import-approved --receipt ../zerog-docs-publication/docs/runtime-tidewraith-import-receipt.json`.
The second regenerates runtime guide JSON from authored assembly coordinates;
it does not establish machine formation, validated service sockets or processing.
Never point either command at Released or create runtime code under docs/.
