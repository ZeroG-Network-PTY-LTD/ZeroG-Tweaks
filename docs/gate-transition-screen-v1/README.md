# Gate transition screen v1: "zoom from galaxy to planet"

This answers the question "How should it look for now?" with designer art that is ready to wire in. It replaces the vanilla "Loading terrain…" screen whenever a ZeroG gate, landing platform or Recall/Group Anchor moves a player between dimensions. Design doc reference: *Energy, charging and launch animation*, step 4.

![Earth to Moon](previews/transition_earth_to_moon.gif)

| Route | Preview |
| --- | --- |
| Overworld → Moon (Sol, T1) | `previews/transition_earth_to_moon.gif` |
| Moon → Cerulon (Galaxy 2, T2) | `previews/transition_moon_to_cerulon.gif` |
| Into a Galaxy 3 volcanic wasteland (tinted sprite, seeded name) | `previews/transition_g3_wasteland.gif` |
| Every sprite in one sheet | `previews/transition_asset_sheet.png` |

The previews are mock-ups built only from the shipped sprites. In game, the text uses the Minecraft font; the previews use a pixel font that stands in for it.

All art follows `docs/art-direction-lock.md`:
- hue-shifted 6-tone ramps, with shading by ramp step and light from the top-left front;
- dark-hue outlines, never black;
- glowing (C) accents only on meaningful parts, never shaded;
- gray sprites for anything tinted per galaxy.

## The sequence

The stage is a fixed **480×270** pixel canvas. Draw it at the largest whole-number scale that fits the window, nearest-neighbour, centred, with a letterbox in `#0b0a16`. Timings assume 20 ticks per second.

| # | Time | Stage | What happens |
| --- | --- | --- | --- |
| 0 | 0.0–0.5 s | White-out | Continues the launch flash: full white fades to space. |
| 1 | 0.0–1.5 s | Galaxy | The destination galaxy (`galaxy_<n>`) is centred on drifting starfields. The reticle locks onto the destination system, shrinking from 3× to 1× between 0.4 and 1.0 s. Top-left label: `GALAXY <n> \| <catalog prefix>`, then `LOCKING COORDINATES`. |
| 2 | 1.5–2.5 s | Zoom | The galaxy scales from 1× to 10× about the reticle point, eased. Near stars become radial streaks. The galaxy fades out from 2.2 s. |
| 3 | 2.2–3.9 s | System | `star_<n>` sits at stage (190, 135), with 4–5 orbit ellipses (y squashed to 0.32). Off-target orbits are dotted `#3c4268`; the destination orbit is solid glow violet `#c48cff`. The destination planet dot carries the reticle. From 3.2 s the view zooms 1× to 4× into that dot, with streaks again. |
| 4 | 3.6–4.5 s | Planet | `planet_<id>` grows from 0.2× to 1× at stage (168, 128). The nameplate slides in from the right to x = 262. |
| 5 | 4.4 s until loaded | Hold loop | The planet rotates through its 16 frames at 6 fps, giving a 2.7 s loop. The progress bar fills with the real level-loading progress. Echo's line types out at 24 characters per second. Status reads `STABILISING RIFT…`, then `RIFT STABLE \| ARRIVING`. |
| 6 | when ready, 0.4 s | Exit | White-out over 0.4 s. The existing `GateArrivalEffects` violet edge fade then plays in the world. |

Rules:
- **Minimum time:** 4.4 s, so the zoom always finishes. If the world is ready sooner, jump to stage 6 as soon as stage 5 begins. If loading is slower, stage 5 loops for as long as it takes.
- **Repeat trips:** a `transitionScreen` client config with `full` (default), `short` and `off`. `short` plays stage 0, then stage 4 straight away, then 5 and 6, which is about 1.2 s. `off` keeps vanilla.
- **Never freeze.** Every stage keeps animating while chunks load.

## Layout on the 480×270 stage

| Element | Position and size | Asset |
| --- | --- | --- |
| Starfield layers | Tiled. Drift is 6 px/s (far), 12 px/s (mid) and 18 px/s (near), plus a slight vertical drift. | `starfield_far`, `starfield_mid`, `starfield_near`, `nebula` (very faint) |
| Galaxy | 192×192 at (144, 33) | `galaxy_1` … `galaxy_5` |
| Reticle | 24×24, centred on the target | `reticle` (4-frame strip) |
| Star | 48×48 at (166, 111) | `star_1` … `star_5` (4-frame strip) |
| Planet | 128×128 centred on (168, 128) | `planet_<id>` (16-frame strip) |
| Nameplate | 196×92 at (262, 82), 9-slice with 8 px borders | `nameplate` |
| Nameplate text, 3 lines (x + 12, y + 11 / 22 / 33) | Catalog id in grey `#9692b0`; planet name in white `#e8e4f6`; class in glow violet `#c48cff` | (text) |
| Hazard chips | y = 146, every 30 px from x + 6; 9×9 icon plus a short label | `hazard_icons` strip: gravity, heat, cold, acid, storm, void, safe |
| Echo line | (148, 206) | (text) |
| Progress bar | Frame 184×9 at (148, 226); fill 180×5 at (150, 228) | `progress_frame`, `progress_fill` |
| Echo wisp | 16×16 at (126, 221), bobbing | `echo_wisp` (2-frame strip) |

## What each destination shows

| Destination | Galaxy sprite | Planet sprite | Catalog / name / class | Chips |
| --- | --- | --- | --- | --- |
| Overworld (going home) | 1 | `earth` | `SOL III` / Earth / Home | safe |
| Moon | 1 | `moon` | `SOL III a` / The Moon / Earth's moon \| Low gravity | gravity 0.5× |
| Mars | 1 | `mars` | `SOL IV` / Mars / Rust world | gravity 0.7×, storm |
| Cerulon | 2 | `cerulon` | `ZG-855 b` / Cerulon / Resource World | gravity 0.9× |
| Skarn | 3 | `skarn` | `ZG-<n> b` / Skarn / Resource World | gravity 1.2×, heat |
| Eidolon | 4 | `eidolon` | `ZG-<n> b` / Eidolon / Resource World | gravity 0.8×, cold |
| Solvane | 5 | `solvane` | `ZG-<n> b` / Solvane / Resource World | gravity 1.3×, heat |
| `g<N>_p<M>` wasteland | N | `wasteland_<type>`, tinted | `ZG-<n> <letter>` / seeded name / Wasteland \| <Type> | gravity plus the type's hazard |
| `g<N>_moons` | N | `wasteland_barren`, tinted | `ZG-<n> <letter> I` / seeded name / Moon | gravity |
| Hidden or unknown world | N | `unknown` | `ZG-??` / Unknown / Signal only | void |

Planet details:
- **Wasteland tinting:** tint the gray pixels with exactly the block-tint maths in `ZGBlockColors.tint(type, galaxy)`. Lava (ember) and crystal (glow) pixels are coloured already and must stay untinted. Separate them on load (gray means r = g = b), or ship them as a second layer.
- **Gravity chip:** show the value from `ZGProgressionConfig`.
- **Hazard chips:** use the planet type: volcanic is heat, frozen is cold, toxic is acid, desert or barren is storm, crystal or ocean is safe.
- **Names:** until the seeded generator exists, wastelands show `ZG-8<N>0 <letter>` with the type name in place of the seeded name.

**Echo lines:**
- Pick one at random from the planet's pool.
- A planet's line is unlocked only after its Codex advancement; before that, show `…signal acquired`.
- Pools live in lang keys `zerog_tweaks.transition.echo.<id>.<n>`.

## Assets

Every asset is in `assets/zerog_tweaks/textures/gui/transition/`. Copy the folder as-is into `src/main/resources` on the code branch. Strips are vertical; each has a `.png.mcmeta` with `frametime` for anything that wants the vanilla animation. The screen can also step frames itself.

| File | Size | Frames |
| --- | --- | --- |
| `planet_{earth,moon,mars,cerulon,skarn,eidolon,solvane,unknown}.png` | 128×128 | 16 (rotation) |
| `planet_wasteland_{ocean,desert,volcanic,frozen,toxic,crystal,barren}.png` | 128×128, gray | 16 |
| `galaxy_{1..5}.png` | 192×192 | 1 |
| `star_{1..5}.png` | 48×48 | 4 |
| `starfield_far.png`, `starfield_mid.png`, `starfield_near.png`, `nebula.png` | 256×256, tileable | 1 |
| `nameplate.png` | 32×32, 9-slice with 8 px borders | 1 |
| `progress_frame.png` / `progress_fill.png` | 184×9 / 180×5 | 1 |
| `reticle.png` | 24×24 | 4 |
| `hazard_icons.png` | 63×9 (7 × 9×9) | 1 |
| `echo_wisp.png` | 16×16 | 2 |

Galaxy palettes:

| Galaxy | Palette |
| --- | --- |
| Sol | Silver arms with a gold core |
| 2 | Cerulite blues |
| 3 | Ember |
| 4 | Ice and phantom cyan |
| 5 | Solvanite gold with four arms |

The target point of each destination system on its galaxy sprite (pixel coordinates):

| Galaxy | Target point |
| --- | --- |
| 1 | (126, 112) |
| 2 | (64, 76) |
| 3 | (132, 70) |
| 4 | (58, 118) |
| 5 | (130, 116) |

## Implementation notes for the code branch

- **Opening the screen:** NeoForge 21.1 has a registration event for custom dimension-transition screens (`RegisterDimensionTransitionScreenEvent`). Register an incoming effect for every `zerog_tweaks:*` dimension, and an outgoing one from them back to the Overworld. Check the exact factory signature against 21.1.252 before coding. The fallback is to replace `ReceivingLevelScreen` in `ScreenEvent.Opening` while a "gate jump in progress" flag is set.
- **Telling the client what to show:** before the teleport, the server sends a small packet with the destination id, galaxy, catalog text, planet type and gravity. This keeps the seeded names server-authoritative, and the screen never has to guess from the dimension id alone.
- **Locking the scale:** draw the whole stage into a 480×270 off-screen target, or with a pose scale of `floor(min(w/480, h/270))`. This keeps every sprite on the same pixel grid.
- **Zoom stages:** scaling the galaxy and system sprites with nearest-neighbour during the zoom is intended. It reads as a lens zoom, so don't smooth it.
- **Wasteland tinting:** either tint at load time into a dynamic texture per galaxy and type, or draw twice (gray layer tinted, then glow layer untinted).
- **Sound:** a rising rift hum during stages 1–3, and a soft chime when the nameplate lands. Placeholders are fine until sound design exists.

## Regenerating

The generator is in `generator/` and needs Python 3, Pillow and numpy. It imports the locked ramps from `docs/art-direction/generator/style_kit.py`.

```
python3 generator/transition_assets.py .          # writes assets/zerog_tweaks/textures/gui/transition/
python3 generator/transition_preview.py . previews  # GIF mock-ups + stills
```

Change planets, palettes or timings in the generator, not by hand-editing PNGs, so every sprite stays on the same ramps.
