# Trim patterns v2

Improved art for the 10 ZeroG trim patterns, done one armor piece at a time.

| Step | Status | Preview |
| --- | --- | --- |
| Helmets | **done** | `../sheets/gear/trims_v2_helmets.png` |
| Chestplates | next | |
| Leggings | | |
| Boots | | |

`textures/trims/models/armor/<pattern>.png` are full replacement files: only the helmet area (head UV 0,0 to 32,16) changed so far. The chestplate, arm and boot areas are the same as `1.21.x`.
Generator: `../generators/trims_helmet.py`. Each helmet is hand-drawn as 8 x 8 grids (top, front, side, back) in the 8-step trim key palette.

## Helmet rules
- Every helmet has a feature on the crown, the part you see most in third person.
- The front frames the face: rows 2-6 and columns 2-5 stay clear, so visors and faces still read.
- The two sides mirror each other, and lines continue across the edges between faces.

## Install (goes on `1.21.x`)
Copy `textures/` onto `src/main/resources/assets/zerog_tweaks/textures/`. No JSON or Java changes are needed; the atlas and trim pattern files stay the same.
