# Tidewraith face textures

Front-face redesign for the Tidewraith head in the Blockbench build. Preview: `../sheets/tidewraith_face_redesign.png`.

| File | Option |
| --- | --- |
| `tidewraith_face_manta.png` (+ `_glowmask`) | **A Manta (recommended):** slanted slit eyes at the outer corners, wide filter mouth with dark gill rakers (no teeth), pale chin, violet splinter crack |
| `tidewraith_face_wraith.png` (+ `_glowmask`) | **B Wraith:** hollow sockets with pin-point pupils, ragged open jaw with a faint glow |
| `tidewraith_face_reef.png` (+ `_glowmask`) | **C Reef:** round eyes under a coral brow, closed mouth, gill slits on the cheeks |

## Applying in Blockbench

1. Paint the chosen 16 x 12 image onto the **north (front) face** of the head cube in the main texture, replacing the goggle eyes and grin. If the head front is a different size, scale it with nearest-neighbour. Keep whole pixels.
2. Paste the matching `_glowmask` in the same spot on the glowmask texture. Only the eyes and crack glow.
3. Delete the separate grin/teeth cubes if the grin was modelled with cubes rather than painted.
4. Sides and top stay the current teal skin. The top two rows of the face are darker, so the top edge reads as a bevel.

Colours are the build's own teal (skin `#123e42`, glow `#71d0b2`), plus the violet splinter `#c9a8ff` shared with the rest of the mob.
Generator: `docs/zero-g-tweaks-bundle/generators/tidewraith_face.py`.
