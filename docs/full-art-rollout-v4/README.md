# Approved A/C native asset rollout v4

This source batch applies the approved equipment reference to existing registry
IDs. Equipment uses C metal bevels, layered armour plates, dark-hued outlines,
violet crystal channels and pale specular edges. Botanical artwork uses A leaf
volume with C restricted to buds, fruit and selected luminous features.

Run `python3 docs/full-art-rollout-v4/generate.py --code PATH_TO_1.21.x` **last**
after older source generators. This renderer is the final authoritative overlay:
running only an older generator is not the approved rollout. The named earlier
native drawing functions are loaded without executing their Java, recipe, lang or
model writers; their source hashes are recorded in `manifest.json`.

## Contracts preserved

- Twenty existing equipment-family IDs; native 32px inventory sprites.
- All twenty worn armour sets use vanilla Netherite-shaped humanoid geometry.
  Their 40 native 128×64 sheets preserve the normalized 1.21.1 Netherite alpha/UV coverage;
  original material colours and magitech surface accents are painted on that
  layout. The former bulky geo shells are inactive, not additional worn layers.
  The October 5 faceted pass paints new plates at twice the native density:
  diagonal metal planes, beveled edges, mirrored breastplate chevrons and recessed
  cyan/violet sockets. Only the alpha template is expanded; old artwork is not
  upscaled. Face openings and hand visibility are unchanged. Emissive-looking
  pixels are shading, not a claim that vanilla armour emits world light.
  `worn-front-fit-preview.png` maps actual exported front UVs onto a schematic
  humanoid; it is not a client screenshot or GPU approval.
- Moonsteel handheld geometry, pivot, position, scale and X-axis half-turn remain
  unchanged. The actually wielded 64px atlas is painted separately at its twelve
  fixed material swatches, so the runtime tool does not remain on an old atlas.
- Dry/wet farmland and dirt retain the previous coherent soil source, with no
  mineral or crystal decorations added. No ore is added to plant textures.
- Existing growth-stage model bindings and animation frame counts/timing remain
  intact. PNG animation changes glistening highlights, not geometric plant sway.
- Every existing active resource-pack override is updated to the same source
  bytes. Hash equality is checked by the renderer.

## Crop anatomy and growth

The final plant review rejected a shared recoloured fern silhouette. Seven native
32px anatomical families now have distinct growth sequences: low root rosettes
(carrots/turnips/onions), thin climbing pea/bean stems with pendant pods, branching
pepper/okra/tomato bushes with visible hanging fruit, wide leafy cabbage/artichoke
heads, narrow cereal seedheads, separate asparagus spears, and ground-running
melon/pumpkin vines. Juvenile foliage precedes pale young fruit and full-colour
harvest forms; ripe food colours follow the matching inventory sprites. Existing
age bindings, transparent crossed-plane contracts and harvest IDs are preserved.
Twenty-four older cereal growth-stage textures and eight gourd stem/attached-stem
textures are included rather than leaving them on the old template. These painted
vine silhouettes do not claim new spreading mechanics or a new support/stake item.

Six planetary kelp families include head/body animated textures, matching inventory
sprites, crossed-plane models, collectible-head loot and dried-kelp cooking data.
The separate language fragment must be merged by the coordinating code workflow.

## Transport source boundary

The supplied `docs/transport-next-stage/reference/zerog_transport_assets.zip` is a
legacy user-supplied Minecraft pack without a canonical Game Development Studio
package receipt. The required `game-dev` package-admission CLI is unavailable;
**canonical package vendoring was not performed or claimed**. No loose downloaded
provider artwork was installed. Instead, the repository's supplied `transport.py`
project source was retained under `transport-source/`, and reviewed named native
drawing/model functions generate fresh engine-native resources. The source hash
and resulting PNG/JSON hashes are recorded.

Six tier palettes, 4/6/8-unit family widths, transparent glass portions, connection
mode colours, gauge coordinates and original narrow-pipe 16px UV budget are kept.
These are verified legacy UV contracts—not upscaled textures advertised as HD.
Recall/Group Anchor icons are original 32px sources on existing requested IDs.

## Evidence and limitations

Final consistency pass: 1,123 native PNGs include 120 shared native 32px item-trim
overlays for four armour pieces and thirty material palettes. All 2,400 existing
item overrides reference their updated base plus an aligned 32px overlay; trim
material IDs, predicates and worn pattern assets are unchanged. This avoids both
vanilla 16px overlays floating across the new silhouettes and 2,400 duplicate
coloured base sprites. `trim-alignment-audit.json` records each binding.

Olympium has a selective same-size worn inlay glowmask plus correct GeckoLib
`glowsections.sections` metadata using inclusive `x1/y1/x2/y2` bounds and alpha.
The format was checked against the installed GeckoLib serializer, not invented.
No custom geo armour shell is active after the user's Netherite-shape correction.
The twenty historical geo atlases and eleven masks remain archived resources;
the runtime uses the forty standard humanoid sheets, preserving IDs/stats/trims.

Twelve planetary/bee honeycomb sprites now form one connected wax cluster with
shared cell rims, recessed centres and upper-left highlights. The old separate
flower-like hexagons are replaced. Each retains its bee-family colour and ID.
The installed orbital addon was inspected: its comb PNGs are white64px tint masks,
not shaded examples. Minecraft1.21.1 honeycomb topology and Netherite UV coverage
were inspected read-only; their PNG colours are not copied into the original art.
`vanilla-netherite-uv-coverage.json` records source hashes and coverage coordinates.
`honeycombs-native-01.png` and `worn-native-01.png` show actual exported pixels.

The incoming approved six-tone source ramps from Design `844a6d44` are recorded in
the manifest. Named Moonsteel, Nullifite, Solvanite, Cerulite, leaf, glow, wood and
rock aliases now use exact ramp-index shading; other previously approved planetary
palettes keep their identities and native forms. Moonsteel's material-cell source
and runtime remain identical. No grip, blade, pivot or hand-transform changes.

`baseline-head-textures.json` is an immutable snapshot of original code HEAD
`dd5776cbbf160a378f97231544a2c176b03cb156`. Per-file `baseline_sha256` and
`previous_sha256` mean that pre-work baseline, never the last generator run.
`baseline_changed_count`/`changed_bytes_count` give the actual baseline delta;
`rerun_changed_count` separately describes the most recent regeneration.

`manifest.json` records source/output SHA256, exact coverage, retained texture
inventory, alpha bounds, atlas face bounds, animation checks and resource layers.
The `*-native-*.png` contact sheets show real generated runtime PNG pixels at
inventory size and enlarged with nearest-neighbour sampling. They are **not**
concept images or in-game captures. Changes still require client visual approval.

This batch does not rewrite entity art, every decorative building block, fluid
textures, GUI semantics, shader materials, vanilla trim patterns or machine-front
designs. Their unchanged inventory is explicit. A texture outside this batch is
not automatically broken: many are already approved source batches or intentional
vanilla-format inherited artwork. Never describe the entire resource tree as
re-authored from the texture count alone.
