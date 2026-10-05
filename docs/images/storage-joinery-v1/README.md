# Native storage and joinery source — v1

Original repository-authored textures, native indexed 32px faces. Run
`python docs/storage-joinery-v1/generate.py --code PATH_TO_1.21.x` after the main
art rollouts. No external artwork, provider jobs, Mekanism texture copying,
geometry upscaling, Java registration, loot or recipe mutation is performed.
The unavailable `game-dev` CLI means canonical package admission is neither
performed nor claimed; this is the approved repository-native source workflow.

`generate_storage_data.py --resources PATH_TO_1.21.x/src/main/resources` is the
separate gameplay-data companion: recipes, loot, additive vanilla/common tags and
localized item/menu names. It preserves existing IDs and tag entries. Run it after
art export; it does not create filled-tank upgrade recipes or mutate save files.

## Stable engine contracts

Four woods: `shardwood`, `charwood`, `hoarwood`, `gildwood`. Each adds:

- `{wood}_panel_door`: vanilla two-block door state/property matrix, native carved
  panels and genuinely transparent upper windows. Eight vanilla-parented models.
- `{wood}_lattice_trapdoor`: vanilla facing/half/open matrix, three model forms.
  Transparent diamond lattice with outlined wood rails; not painted dark holes.
- `{wood}_chest`: original single-block container, no vanilla ChestBER.
  North-facing latch and carved lid seam; facing north/east/south/west variants.
  A client block-entity renderer now hinges the upper section from synchronized
  OPEN state. The source body remains 14×14×14; interpolation is bounded and tested.
  Double joining is not implemented and GPU/client approval remains pending.
- `{wood}_barrel`: six directional facings plus open=true/false, with its lid
  recess facing the selected direction. Twelve variants and two block models.

Existing `{wood}_door` and `{wood}_trapdoor` assets are never overwritten. Native
door inventory sprites depict the same panels/window proportions. Storage and
tank icons inherit the placed block model, with GUI rotation `[30,225,0]`.

`storage_expansion_module` has an original 32px magitech chip sprite and editable
two-sided texture source. Runtime storage is 27 slots, expanded to 54 by one module;
this art generator does not implement the storage backend or its server checks.
`generator_flux_module` has a separate coiled-copper/energy-bolt magitech chip
sprite, not a recoloured storage capacity chip; runtime generator upgrades live
in code. Both use the approved Moonsteel/copper/glow six-tone ramps.

Six `{tier}_fluid_tank` IDs: copper, nullifite, cyrrium, tectium, wraithsteel,
astrium. States are facing=north/east/south/west and level=0..8. Each has nine
model/texture levels and a machined top cap. Transparent panes, outlined frames,
graduated inlay gauges indicate fullness. Panes have no painted neutral backing:
the client renderer fills them from the synchronized stored fluid's sprite, tint,
amount and luminosity. Empty tanks are transparent; no arbitrary fluid is depicted.
Runtime fluid
capability, routing, buckets, capacity and synchronized GUI values live in code.

## GUI boundary

`textures/gui/fluid_tank.png` is 176×204. Runtime draws pale labels, fluid identity,
amount/capacity and face-control buttons. Fillbar interior: x8/y58, 160×10. Six
buttons: x8/62/116, y76/97. Player item positions: x8 plus 18px columns, y124/142/160;
hotbar y182. Slot surrounds are painted only once by this panel. The native panel
preview is the background **without** runtime labels, values or buttons.

`textures/gui/combustion_generator.png` is 176×184. Fuel slot item at x48/y36;
flame/progress region x72/y37, 14×14; FE fillbar x128/y22, 12×56. Player inventory
items start x8/y102 with 18px columns/rows and hotbar y160. Text regions y6,24,
65,78,89 remain unpainted; fuel, flame, FE fill and upgrade values are synchronized
runtime overlays, not baked into the artwork. Use pale text on the dark panels.

## Palette and material anatomy

Only exact six-tone `docs/art-direction/generator/style_kit.py` colours are used:
shardwood uses the cyan Cerulite/green-leaf role, charwood brown wood/copper,
hoarwood cool Moonsteel/Cerulite, gildwood gold Solvanite/brown wood. Regardless
of hue, all four depict wood grain, separated staves, framed panels, latch pins
and carved seams—not noise or featureless recolouring. Tank roles preserve the
six tier identities within named canonical ramps. Selective violet inlays have
pale centres; painted highlights alone are not a runtime emission claim.

## Source and validation

`source/` mirrors all new engine resource paths. `blockbench/` contains 24 embedded
editable sources: four full two-part doors, four lattice trapdoors, four chests,
four barrels, six tanks and both module sprites. Door/trapdoor face geometry and
UV contracts use Minecraft's inherited templates; new texture artwork is original.

`manifest.json` records generator/style hashes, every resource SHA256, active
override-layer bytes, palette roles, editable-source hashes and validation errors.
108 PNGs and 110 block models are exported. All new model texture references,
Java UV ranges and nonempty alpha bounds are checked. Native contact sheets show
real final texture pixels, not concept art or in-game captures. Client lighting,
placement and gameplay approval remain separate checks.
