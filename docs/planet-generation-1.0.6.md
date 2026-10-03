# Beyond the landing pad — ZeroG 1.0.6 development field guide

Minecraft **Java 1.21.1** · NeoForge **21.1.252** · Java **21** · GeckoLib **4.9.3**.
This is a development candidate, not a declaration that every design is finished.

## Fresh planets, preserved history

The new local showcase is **ZeroG Planet Showcase 1.0.6 — Seed 0**, folder
`saves/ZeroG_Planet_Showcase_1_0_6_Seed0`. Its seed is **0**, hub spawn **62 / 65 / 0**.
The old `ZeroG_Planet_Test_Hub_Seed0` save remains untouched. Open the **new** save
to inspect fresh terrain; upgrading a JAR cannot retroactively regenerate old chunks.
No existing dimension directories or player builds were deleted.

Each of the 34 planetary destinations now has its own density-function and noise
registry. Minecraft's world seed still controls generation, but destinations no
longer reuse the same terrain noise under different block colours. Primary planets
retain their authored surface/ecology identities: broad lunar relief, Martian
uplands, Cerulon's ocean terrain, rugged Skarn/Solvane and frozen Eidolon.
Galaxy destinations retain the repository's thematic mappings while receiving
independent terrain. This does not create 34 entirely bespoke biome ecosystems.

Use the **ZeroG Planet Test Hub** preset to create another hub with any seed.
Seed 0 with the ordinary Overworld preset is not the hub. `/zerog hub status`
reports readiness. The exported showcase starts at time 17,000, before the first
impact opportunity at 18,000; time and normal mob spawning resume after loading.

## Colonies, inhabitants and excavated foundations

Four three-house settlement arrangements are selected during world generation.
Each cleans and levels a 39×39 footprint, removes terrain above foundations,
fills support soil, connects paths and adds two cultivated crop beds. Ocean
settlements have support pylons toward the seabed. Houses use reinforced frames
with clear or planetary tinted glass — **not Star Glass** — beds, job blocks and
lighting. Gardens include themed flowers and occupied miniature-bee hives.

Six persistent vanilla villagers inhabit each colony. Their faces, noses, heads,
AI and profession system remain vanilla. Twenty-four original clothing overlays
provide four suit palettes for each of six planetary themes. Residents are created
on the server thread, never world-generation workers; saved anchors avoid duplicate
population. This does not implement bespoke alien trades or a new villager species.

The showcase deliberately contains one demonstration colony at **X=136, Z=136**
on each destination; its height is recorded in the [test report](planet-generation-1.0.6-test-report.json).
Those are review fixtures. Separately, natural colonies attempt placement at
approximately one in 36 chunks, subject to safe-footprint checks; they are not
guaranteed in every nearby chunk. Player-inhabited chunks, block entities and
protected gate volumes are excluded from destructive schematic preparation.

## Caves and abandoned mining works

Independent terrain noise also drives the existing cave graphs. New dry crossing
mineshafts attempt generation at approximately one in 18 chunks underground:
37-block galleries, corroded hull floors, supports, rails, lighting and a loot
chest. Wet or obstructed footprints are rejected. This is a compact mining-work
layout, not a full vanilla jigsaw mineshaft network or completed boss arena.

Existing cave fungi, draping vegetation, stalagmite-like decorations, aquatic
plants and biome tree assignments are retained. Small automated samples still
contained no tree logs/vines/mushrooms: **whole-planet ecology is not certified**.
Do not confuse an assigned species with proof that every biome has healthy forest
density. Existing Cerulon regional cave work is retained rather than overwritten.

## Wildlife and daily impacts

Existing live mobs have additional matching planetary biome assignments. Dune
Burrowers and Rust Beetles can use sturdy themed natural ground rather than
requiring ordinary grass; Frost Yaks can use frozen terrain. Woodland and aquatic
creatures retain their appropriate habitat rules. Unimplemented catalogue creatures
have not silently become live mobs. Tidewraith eggs remain functional; automatic
Tidewraith spawning and campaign boss phases remain pending.

Cosmic Blazes remain rare: low spawn weights, an additional eligibility gate,
spacing and loaded-world limits. Rod colour variants and emissive accents are
preserved. Higher habitat coverage is not a promise of constant visible spawns.

Daily terrain-damaging impacts target solid seabeds as well as land, allow liquid
terrain, and try more candidates. One successful impact per **active planet per
24,000-tick day** is attempted from dusk, with a player in the dimension and a safe
loaded footprint. Players, block entities, construction and arrival zones exclude
sites; therefore a successful strike is not guaranteed each day. Remnants keep
10-block spherical bounds, weaker outer materials and a rare central ore core.
Back up worlds. This is real terrain damage, unlike cosmetic weather.

## Arrival sanctuary

Generated test-hub landing gates have protected radius-10 arrival volumes. Break,
placement, piston, explosion, hostile-spawn and damage hooks protect the landing
area; loaded layouts are repaired on server ticks. Comet and explicit structure
placement exclude it. Protection does **not** apply automatically to every ordinary
survival gate, nor defeat every third-party mod or administrative command.

## Animated universe and connected Star Glass

![Original universe source artwork — not an in-game screenshot](images/planet-generation-1.0.6/universe_v2.png)

The original 1774×887 panorama uses filtered sampling on a denser sky sphere,
slow partial-tick-interpolated rotation and independently twinkling stars. Each
planet has a different starting orientation. The source is not a 4K image or a
captured game render. Shader/client/GPU appearance remains for human review.

Star Glass now has distinct **Purple, Blue and Teal** inventory entries. Dye
recipes, placed-state recolouring, pick-block and Silk Touch preserve colours.
Matching-colour coplanar neighbours share an animated galaxy projection, with
quartz trim along exposed outer edges rather than each joined tile. Different
colours do not join. The bounded model scan supports rectangular panels best;
irregular panels and live far-edge mesh updates need client review. No external
connected-texture mod is required by this implementation. Light level remains 12.

## T6 test gate — exact assembly

Coordinates are relative to the **centre of the pad**, with Y=0 at pad level.

| Part | Position / dimensions |
| --- | --- |
| Foundation | 17×17 landing-platform footprint, Y=-2 through 0 |
| Central pad | 7×7 gate-pad plates, X/Z=-3..3 at Y=0 |
| Six perimeter rings | Square Chebyshev radii 2..7; Nullifite, Moonsteel, Cerulite, Skarnite, Eidolite, Solvanite respectively; first two at Y=-1, others Y=0 |
| Pylons | X/Z=(±7,±7), Y=1..4 |
| Energy ports | (-6,1,7), (6,1,7), (-7,1,0), (7,1,0) |
| Standing arch | X=±4, Z=5, Y=1..10; top X=-4..4 at Y=11 |
| Lens | (0,12,5) |
| Controller | (0,1,-7) |

```text
SIDE VIEW (arch at Z=5)       PLAN (not to scale)
          Lens                    Arch + lens
    =======+=======             P  +---------+  P
    |             |             |   PAD     |
    |   open      |          E  |   7×7     |  E
    |   arch      |             |           |
    +-------------+             P E       E P
   === central pad ===                C
   === foundation ===              controller
```

Stand on the centre pad and right-click its controller. Both route ends must
have complete layouts. Generated hub gates use unlimited **test power only**.
An operator can bind an existing complete survival-style gate with
`/zerog gate bind <dimension-id> <centre-x> <centre-y> <centre-z>` and bind its
return separately. The present buffer and travel cost are **50,000,000 FE**;
energy simulation/persistence exist, but complete survival progression and a
polished gate GUI remain unfinished. Do not mistake the operator command for
a finished player progression system.

## Apiaries and the rest of the collection

Press **G** for the [eight apiary assemblies](multiblock-reference-guide.md):
Y=0-up layers, 360° rotation, exact coordinates and part quantities. Genetics
and cryo remain **separate external modules**. The viewer does not implement
machine formation, frame/bee processing slots or production exports.

The [illustrated collection](current-collection-guide-1.21.1.md) retains all
twenty fitted armour sets, tools, materials, apiary component/frame studies,
mob/drop/egg sheets and approved Tidewraith pair. [All current item-model artwork](runtime-item-catalog-1.0.6.md)
is indexed separately; model files and block inventory views are not counts of
unique registered items. Images are clearly labelled source art/texture references.

## Verification boundary

Isolated native server checks cover 34 distinct terrain sample arrays, 68 gate
routes/round trips, 204 demonstration residents, naturally generated Martian
colonies, clothing types, a supported mineshaft, glass item states/canonical item
mapping, gate repair and a positive layered-comet fixture. These are one composite
integration test with many assertions, **not 204 separate tests**. Static contracts
and a clean normal build complement it. No existing player save was used.

Client rendering, complete modpack compatibility, multiplayer play, all-seed
ecology, every boss arena and full Productive Bees integration are not certified.
The previous guides and galleries remain preserved as historical evidence.

The isolated fixture log contains non-fatal pending `DUMMY` block-entity warnings
where test construction replaced freshly generated blocks. The composite test
and server save/shutdown passed; this is not a claim of a warning-free runtime.
The actual vanilla `WorldOptions` serialized `generate_features` field controls
structure generation, not disabling biome decoration features. Natural colony
placement was checked separately from explicitly built showcase fixtures.
