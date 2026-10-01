# Abyssal Tidewraith — selected-model face repair

This is an updated copy of the supplied `tidewraith_abyssal_belly_roots_concept_finish.bbmodel`, **not** a replacement by the eight-eyed oval concept model. The original file is preserved, with a source snapshot here for repeatability.

The head's original rear edge was two units in front of the torso. The complete head subtree—geometry and all facial, jaw, fin and eye pivots—is moved +2.25 Z units toward the torso. Its rear now overlaps the torso by 0.25 unit, without moving the body, wings or tendrils. `updated_right.png` shows the closed joint in profile.

The supplied four-style sheet's Abyssal front tile is sampled on its 16×12 pixel grid. Its navy face, diagonal cyan eyes, violet central stripe, dark rectangular mouth and six shadowed teeth are mapped onto the selected model. Side/back patterns and body proportions are retained. The two eye planes use the original blink bones; static eye colours underneath are removed to prevent duplicate eyes showing during blinks. Mouth and teeth placements follow the reference, and the lower-rim movement uses an opening direction appropriate to Y-up coordinates. Mouth scaling fills the opening while the lower jaw moves.

The original 4096×4096 atlas remains a **single** texture. The facial tile is packed in an unused 128×128 lower-right corner, with overlap checks against all original UV islands. Other parts' geometry, rigging, animation clips and sampled texture pixels are preserved. The cropped reference is pixel art; enlarging it does not invent new HD details.

Open `tidewraith_abyssal_concept_face.bbmodel` in Blockbench. In Animate mode select **blink** or **mouth_open**, then Play. All 14 original clip names remain; only the mouth-open channels were corrected. `face_closeup.png`, `updated_front.png`, `updated_threequarter.png`, `blink.gif` and `mouth_open.gif` are software reviews, not native or in-game captures.

The face-only glowmask covers the cyan eyes and violet stripe. It is **not** a replacement for an existing full-body glowmask without merging that mask first. These files do not implement or test a Minecraft entity, renderer or animation controller.

Regenerate with `generators/update_tidewraith_abyssal_face.py --source <source.bbmodel> --reference <face_concept.png>` from the bundle's generators directory, or use the saved source snapshot and concept sheet in this folder. `manifest.json` records reference sampling, source/file hashes and checks. No paid generation was used; no additional rights to user-provided art are asserted.
