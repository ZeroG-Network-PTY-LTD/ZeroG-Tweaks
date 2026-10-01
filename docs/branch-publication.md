# Branch-separated development publication

The human approved creating three new branches and separating the completed
updates. Before publication, the exact branches appeared remotely with additional
work; this update therefore continues those branches rather than replacing them.
Existing branches and tags are preserved by this publication. No force push, release merge,
Minecraft launch, CurseForge deployment or world change is part of publication.

| Branch | Files |
| --- | --- |
| `1.21.x` | src/ including opt-in test source sets and runtime textures/models, Gradle/build configuration, tools/reference-java/, tools/design-code-archive/, AGENTS.md, .gitignore, short absolute-link README |
| `Design` | docs/asset-collection-1.21.1/, docs/zero-g-tweaks-bundle/ except archived Java, generators/export_tidewraith_models.py, generators/generate_multiblock_guides.py, DESIGN_NOTES.md |
| `Docs` | README.md, illustrated collection guide, runtime review, verification, multiblock guide, import receipt, this record, docs/HELP.md, docs/images/, docs/jars/ and SHA256SUMS.txt |

`1.21.x` continues remote code at `1800c4192f6c818f699ced19dbcc699d2359b4f9`;
Design continues `7d3c610237d9304b6be2980774347f58262de347`;
Docs continues `7b73ba449f283ff18b6cc6e81e439ab63840daef`.
All newer upstream mob, machine and art work is retained. This update overlays
the approved multiblock guide/test changes and documentation, plus a one-call
1.21.1 compatibility fix to the existing fern hitbox offset; no rollback
to the earlier local snapshot occurred. Design/Docs retain independent histories;
no cross-branch merges occurred.
The previous mixed snapshot branch is retained as historical backup.

The immutable original design roster has 1,381 entries. Its six archived Java
drafts move to `1.21.x/tools/design-code-archive/` with paths beneath the former docs/ root;
all 1,381 bytes/hashes remain resolvable across the new branches. Art and models
remain on Design. Ten bundle drafts and six standalone Tidewraith drafts also
move to tools/design-code-archive/ (22 archived Java sources total).
None of these drafts are compiled into the jar.

Twelve server tests and 32 guide rotation/layer poses previously passed in
isolated Java development instances. These are not CurseForge modpack tests or
human visual approval. See verification for the fresh normal build and jar hash.
The intended actual modpack test folder is
`C:\Users\jakem\curseforge\minecraft\Instances\ZeroG` (Java/NeoForge, not Bedrock).

Published jar is a development candidate, not a shipped release. Bees gameplay,
machine GUI/processing, multiblock formation and HD worn-armour mapping remain
unfinished. Read the illustrated guide before assuming an asset is functional.
