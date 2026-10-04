# Orbital-Bees genetics machines v1: Genetic Splicer and Geno Station

**Later user revision (2026-10-05):** the assembled/helix block geometry below is
archived concept work. Runtime models must now be single full cubes with face
textures, as authored in [single-block-machines-v1](../single-block-machines-v1/README.md).
Do not ship the assembled models or external helix from this folder. The genetics
behaviour and five-slot GUI descriptions remain future backend specifications,
not implemented features in the current four-/two-slot addon menus.

Redesign of `aeroapiary:genetic_splicer` and `aeroapiary:geno_station` (ZeroG Orbital-Bees), with new GUIs. Registry ids are unchanged.

**Status: design input.** All previews are software renders made by the generator, not in-game captures. Nothing here is installed in a jar.

## Why

- The shipped models were a grey cabinet with a hidden helix (Splicer) and a box with a stretched cyan swatch (Geno Station), with flat swatch textures.
- The shipped code is placeholder. `ZeroGMachines.tick` runs the frame-infusion recipe for the Splicer and the stardust-smelter recipe for the Geno Station. Neither touches genes.

## Design

- **Geno Station (read and sample):** analyse a bee with a Honey Drop, or copy one chosen gene into a blank Serum Vial to make a Trait Serum.
- **Genetic Splicer (write):** queen/princess + Trait Serum + Royal Jelly (75%) or Cosmic Jelly (100%) gives the spliced bee and an empty vial. Species cannot be spliced.
- Full slot rules, timings, ContainerData, packets and the code fix are in `reference/genetics_machines_spec.md`.

## Art (follows ../art-direction-lock.md)

- Native 32 px per block: 128 x 128 atlases at 2 px per model pixel, one island per face, authored by the generator (no upscaling).
- Materials: dark steel with bevels and rivets, brass trim, copper coil, glass with edge highlights, honeycomb doors. Bright accents only on screens, crystals, vials, the helix and the lens.
- Palette: steel #4a5060 / #6f788b / #2a2e36, brass #c99a3a / #efc76c / #8a6420, copper #b8673c / #e39a62, honey #e8a82c / #ffd27a, genome cyan #5ff3ff, amber #ffb347, violet #9c7ae0, green #7cf08a.
- Machine fronts: Splicer = splice screen on the console; Geno Station = genome monitor. Both are unmistakable terminals.
- Glow: elements carry `neoforge_data` block/sky light 15 (glowmasks provided for shaders). Painted glow is not proof of runtime light until tested.
- Models are translucent render type (glass). Blockstates now have `facing` (`ZeroGMachineBlock` already has `HORIZONTAL_FACING`).
- Splicer helix: the baked model omits the rungs; `geo/machines/genetic_splicer_helix.geo.json` + `animations/genetic_splicer_helix.animation.json` are drawn by a GeckoLib block renderer. The item model keeps the rungs.

## GUIs

- `textures/gui/geno_station.png` (screen 196 x 226) and `genetic_splicer.png` (196 x 212), sharing `genetics_widgets.png` (27 sprites, overlap-checked by the generator).
- Same look as the Alveary Controller screen. No baked text.

## Files

| Path | What |
| --- | --- |
| `generated/` | Before/after, two reference sheets (views, labelled parts, atlas, glowmask), GUI mockups, GUI layout maps |
| `source/assets/aeroapiary/` | Block/item models, blockstates, textures, glowmasks, helix geo, animation and texture, GUI textures |
| `reference/genetics_machines_spec.md` | Behaviour, slots, GUI element tables, widget atlas, code fix |
| `reference/gene_machines.py`, `gene_gui.py`, `mcrender.py` | Generators: `python3 gene_machines.py <out> <old_jar_extract>` then `python3 gene_gui.py <out>` |

## Not yet checked

UVs and face rotations are validated by the renderer only; check in Blockbench and in game (inventory, hands, placed, at night) before replacing the shipped art. Review all resource-pack layers so the old `genetic_splicer_hd` and `other/geno_station` textures do not override these.
