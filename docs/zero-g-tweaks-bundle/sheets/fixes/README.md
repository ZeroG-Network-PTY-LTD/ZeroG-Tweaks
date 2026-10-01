# In-game fixes: textures and models for plants and crystals

`ingame_fix_sheet.png` compares the in-game screenshots with what the `design/v1.2-assets` branch ships. For each block it shows:
- the screenshot;
- what's wrong and why;
- the texture/model rule to follow when generating art;
- the final texture (tinted blocks are shown with their tint).

## What was wrong

There were two separate causes.

1. **Old build (6 of 8 screenshots).** The screenshots were taken on `1.21.1-update`. That branch doesn't have the vanilla-counterpart plant work or the new art. **Build and test from `design/v1.2-assets`.** On that branch:
   - the saplings, Pyrevine, Glowkelp and the lichens already look and behave like their vanilla counterparts;
   - Glowkelp needs water;
   - lichen lies flat on faces.
2. **Grey crystals and wasteland blocks (Brine Crystal, Prism Cluster, Frost Crystal, and all 307 wasteland blocks).**
   - These textures are drawn in grayscale on purpose. Their models use `tintindex 0` so one texture can be recoloured per wasteland type and galaxy.
   - The colour handler (`ZGBlockColors`) was still only in `docs/`, so nothing coloured them and Minecraft rendered raw grey.
   - **Fixed:** it now lives at `src/main/java/net/zerog/tweaks/client/ZGBlockColors.java`.
   - Outside the galaxy slot dimensions (Overworld, Moon and the planets), it uses the Galaxy 2 colour.
   - The three crystal textures were also brightened (grey levels 175–225) so the tint doesn't look muddy.

## Texture and model rules (use these when generating or regenerating art)

| Block kind | Texture | Model | Notes |
| --- | --- | --- | --- |
| **Sapling** | 16×16, transparent background. 1–2 px stem rising from the bottom centre, a side twig, and a 3-tone leaf crown in the tree's own leaf and log colours. | `minecraft:block/cross`, `render_type: cutout` | The item uses `item/generated` with the block texture. The potted version uses `block/flower_pot_cross` with `plant` = the same texture. |
| **Flower / fern / mushroom / thorn bush** | 16×16 sprite rooted on the bottom row. | `block/cross`, cutout | Don't use `tinted_cross` unless the texture is grayscale **and** the block is registered in `ZGBlockColors`. |
| **Crystal cluster** (Cerulite, Brine, Frost, Prism) | One 16×16 sprite of 3–5 spikes rooted on the bottom row. Cerulite is coloured; Brine, Frost and Prism are grayscale (175–225) with white tips. | Coloured: `block/cross`. Grayscale: `block/tinted_cross`. Blockstate rotates by `facing` like `amethyst_cluster`. | The block class is `ZGCrystalClusterBlock` (extends `AmethystClusterBlock`). |
| **Cave vines** (Pyrevine) | Four textures. `pyrevine` and `pyrevine_lit` are the tip, with a curl at the bottom. `pyrevine_plant` and `pyrevine_plant_lit` are the body and must tile vertically: the top row matches the bottom row. The `_lit` textures add berries. | `block/cross`, cutout. The blockstate picks `_lit` when `berries=true`. | You plant it with Pyrefruit; there is no Pyrevine item. |
| **Kelp** (Glowkelp) | Two coloured textures, no tint. `glowkelp` is the tip with a bulb; `glowkelp_plant` is a stem that tiles vertically. | `block/cross`, cutout | The item uses `item/glowkelp`. The block only places in a full water source. |
| **Glow lichen** (Lunar and Rust Lichen) | A full 16×16 patchy face texture drawn edge to edge, with holes. It is **not** a standing sprite. | A single flat plane at z = 0.1, `ambientocclusion: false`, cutout. The blockstate is `multipart` with one rotated entry per face (north/south/east/west/up/down). | The item uses `item/generated` with the block texture. |
| **Wasteland stone family** | Grayscale 16×16. | The `zerog_tweaks:block/parent/tinted_*` parents | Every id must be listed in `ZGBlockColors`, or it renders grey. |

## Regenerating

These scripts are in `docs/zero-g-tweaks-bundle/generators/`:
- `plants_vanilla.py`: vines, kelp, lichens, Emberthorn and saplings.
- `ingame_fix_sheet.py`: this sheet. It reads the screenshots from the upload folder, so point `UP` at new screenshots before re-running.
