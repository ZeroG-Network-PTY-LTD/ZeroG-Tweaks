# AGENTS.md — ZeroG Tweaks (Docs branch)

You are on the `Docs` branch.

## Branch layout — read before committing

This repo keeps code, design work and documentation on separate branches.
Put every change on the branch it belongs to.

| Branch | What goes here |
| --- | --- |
| `Released` | Major released code only. Never commit or push here directly; it is updated only by merging a version dev branch (via a pull request) when a release ships. |
| `1.21.x` | Dev branch for Minecraft 1.21.x. **All code**: `src/`, Gradle files (`build.gradle`, `settings.gradle`, `gradle.properties`, `gradle/`, `gradlew*`), `tools/`, `AGENTS.md`, `.gitignore`. Future Minecraft versions get their own dev branch (`26.1.x`, `26.2.x`, …). |
| `Design` | **All design work**: Blockbench models (`*.bbmodel`), work-in-progress textures, art and reference sheets, asset collections, concept art, generator scripts, design notes (`docs/zero-g-tweaks-bundle/`, `docs/asset-collection-*`, `docs/shattered-skies/`, `docs/tidewraith-approved/`, …). |
| `Docs` | **All documentation / wiki**: README content, `docs/HELP.md`, `docs/images/` (diagrams, gallery, logo), `docs/jars/` (release jars + `SHA256SUMS.txt`), guides. |

Rules:

1. `git fetch` first, then check out the right branch for each change. If a task
   touches code *and* docs/images/design, make **separate commits on separate
   branches**.
2. `Design` and `Docs` have histories unrelated to the code branches. **Never merge
   `Design` or `Docs` into `1.21.x` or `Released`** (or the reverse), and never use
   `--allow-unrelated-histories`.
3. Never put game code under `docs/`, and never add `docs/` folders to a code branch.
   The code-branch README links to `Docs`/`Design` with absolute GitHub URLs; keep
   those links working.
4. Never commit directly to `Released`, never force-push, never delete branches or
   the `archive/*` tags (they are backups of the pre-cleanup branches).
5. Code changes must pass `./gradlew build` before pushing. When new release jars
   are built, commit them to `Docs` under `docs/jars/` and regenerate
   `docs/jars/SHA256SUMS.txt`.
6. `git pull --rebase` before pushing so you don't overwrite someone else's work.
7. When done, report which files went to which branch, with commit hashes.
