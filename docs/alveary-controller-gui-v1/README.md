# Orbital Bees controller GUI — 5 October 2026

The user-supplied specification and generator are preserved without edits in
`reference/`. Their mockups/coordinate atlas are in `generated/`; they are design
references, not screenshots of a working game. `runtime-manifest.json` records
their SHA256 hashes and the actual shipped texture hashes.

The native adaptation in `adapt_runtime.py` keeps the supplied honey/grey bevels,
recessed vanilla slots, grouped hive/climate/products/power/frame sections and
sealed overlays. The window and background match the reference exactly:
**256×250** visible screen inside a **256×256** sheet. The addon exposes up to
**18 products**; previous/next buttons page its original slots through the
reference's 3×3 output grid without losing storage. Source textures ship
under `assets/zerog_tweaks/textures/gui/`, with identical normal and built-in pack
copies. Labels are drawn from translation keys, not baked into the PNG.

## Real runtime coverage

`apiary_controller`, `zero_g_hive` and `tier1_controller` through
`tier7_controller` share the adapted screen. Client repositioning delegates to
the original filtered slots; numbering, backing handlers, insertion/pickup
rules and server shift-click logic remain unchanged. All 36 player slots remain
accessible. Slot wrappers hide only off-page output cells; hidden slots keep
their server indices and original contents. Atlas-backed Info/Climate/Energy/
Automation/Structure ledger buttons and panel/tooltips identify what belongs
where. The actual addon slot tables were executed in a Java-only contract
check, without starting Minecraft: counts are 12/15/18/21/24/27/27 for the seven
tiers, 12 for the apiary controller and 15 for the hive.

Formation/errors and work percentage are sent from the **server** once per
second while the matching menu is open. Broken-structure text wraps and has a
full tooltip. Sort sends a server request validated against the open menu ID,
real machine, distance, validity and exact slot count. Only copied product
stacks are reordered; inputs/frames are never touched or destroyed.

Biome temperature/humidity gauges use actual biome data, not invented bee
tolerances. Native controller front textures remain visible: full GeckoLib
models are only drawn for ENTITYBLOCK_ANIMATED blocks, not on top of baked
MODEL blocks.

## Deliberately sealed — not simulated

The addon does **not** currently supply the reference's 27-frame tier progression,
queen lifespan/genome view, climate-tolerance values, FE/honey/catalyst tank
state, auto-eject or destructive void toggles. Those require backend work,
not just a GUI texture. The existing 2–7 real frame slots are preserved; reserved
cells/tanks stay sealed. No fake active buttons or made-up modifier numbers are
presented as working. This is a completed compatibility layout, **not** a claim
that every gameplay system in the reference has been implemented.

The preview PNGs are offline layout examples with sample items and status, not
in-game captures. A 1080p display with GUI scale 3 or lower fits the window;
larger GUI scales need manual client review. Shader compatibility, drag/drop,
tooltips, resize and high-GUI-scale behaviour still require player testing.

## Regenerate

```text
python3 docs/alveary-controller-gui-v1/reference/controller_gui.py docs/alveary-controller-gui-v1/generated
python3 docs/alveary-controller-gui-v1/adapt_runtime.py --code ../zerog-code-integrated
```

The accompanying sky change delegates to vanilla rendering, including sun,
moon, sunrise and clouds. An AFTER_SKY overlay adds 480 deterministic scattered
larger stars, slow independent green→blue→yellow→purple gradients, and gentle
radial halos. The original small vanilla stars remain beneath this overlay.
Daylight/rain visibility and underwater/blindness/darkness exclusions apply.
The old universe panorama artwork is retained as historical source material but
is no longer referenced by the live renderer. World generation and weather
gameplay are not changed by the sky rollback.
