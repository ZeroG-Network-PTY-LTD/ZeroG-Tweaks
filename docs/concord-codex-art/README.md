# Concord Codex: approved native64 HD artwork

Owner approved the64x64 redraw on13October. `generate.py` now exports the native64
source/model by default. The32px study is preserved in `generate_32_legacy.py` for
history only; do not run it against production. The unchanged item ID and book
logic use the dedicated `zerog_tweaks:item/concord_codex` texture.

The asset-packaging CLI remains unavailable; this uses the disclosed local
repository generator and PNG/source/JAR checks, not a canonical GLB package.
Native64 artwork approval is recorded; installed-client appearance remains a
separate review. The earlier sections below document the design iterations.

Owner approved the navy/silver/cyan/violet concept, then requested a clearer native
sprite. `generate.py` authors a new transparent32x32 book from scratch using the
locked colour ramps. The concept is not cropped/downscaled into runtime artwork.

Clarity revision: thin separated orbital paths, larger four-point star, brighter
silver fittings and visible cream page bands. `native-preview.png` shows the
actual native sprite at inventory size and nearest-neighbour enlargement.

The same original item ID and generated-item model remain. Lore, Codex screens,
unlocking and interactions are untouched. Colours depict glow; no runtime light
emission, animation or GPU approval is claimed.

Generate:
`python3 generate.py <code assets/zerog_tweaks directory>`

Native RGBA/dimensions/padding/material checks pass; `manifest.json` binds source
PNG/model hashes. Packaging CLI is unavailable: existing local sprite-generator
fallback is disclosed, with no paid provider or canonical-package claim.

`approved-concept.png` was generated with the built-in image tool on13October.
Concept prompt: one three-quarter closed Concord book, navy cover, silver corners
and clasp, visible ivory pages, central white star with cyan/violet orbital chart;
enhanced-vanilla pixel shading, selective magitech accents, top-left lighting,
inventory-scale inset and explicit not-installed concept label. Owner approved
the concept. The native clarity revision still awaits visual approval.

The clarity revision is staged locally, not installed or published. Do not claim
an earlier build contains this final revised sprite; rebuild after approval and
check both resource layers/source hashes before same-version delivery.

## Owner-requested HD revision

Owner requested HD after the32px clarity review. `generate_hd.py` is a separate
native64 redraw with one-pixel bevels, inset corner rivets, individual page bands,
hinge/clasp detail and a clean star-map motif. No32px raster or concept sheet is
upscaled into the source. This explicit resolution exception is for the Codex
only, not a blanket rescale of other items.

`hd64/textures/item/concord_codex.png`, its model and validation manifest are
review assets. `hd64-preview.png` displays actual64px art, enlargement and a32px
inventory simulation. PNG dimension/alpha/padding/material checks pass. This
revision is not copied into the runtime assets or installed JAR yet; native64
appearance awaits owner review. Lore and book UI remain unchanged.
