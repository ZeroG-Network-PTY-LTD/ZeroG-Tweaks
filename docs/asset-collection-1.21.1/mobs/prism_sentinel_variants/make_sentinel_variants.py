"""Prism Sentinel variant textures (owner's choice 2026-10-03: 3 common + 1 rare, recolours on the one model).

Writes textures/entity/prism_sentinel_<variant>.png and _glowmask.png next to the base texture. Each texel is sorted by
hue/brightness into the design sheet's palette groups (crystal, core, stone, gold band) and each group is mapped to the
variant's colours, keeping the texel's light/dark shading. Glowmasks keep the base mask's alpha (same UV layout) with
the variant's crystal colour.
"""
import colorsys, os, sys
from PIL import Image

TEX = 'C:/zt-tmp/w/src/main/resources/assets/zerog_tweaks/textures/entity/'
OUT = sys.argv[1] if len(sys.argv) > 1 else TEX

# per variant: target hue (0-1) and saturation/brightness scale for each group, or None to keep the group as it is
VARIANTS = {
    # gold-blue: crystals turn Aurelion gold, the stone body stays Cerulon blue
    'aurelion': {'crystal': (0.115, 0.95, 1.05), 'core': (0.13, 0.35, 1.0), 'stone': None, 'gold': None},
    # deep indigo: violet crystals over a near-black body
    'nebulite': {'crystal': (0.70, 0.85, 0.95), 'core': (0.72, 0.25, 1.0), 'stone': (0.68, 0.9, 0.75), 'gold': (0.75, 0.25, 0.85)},
    # rare: white-gold crystals, pale stone, bright gold band
    'radiant': {'crystal': (0.135, 0.80, 1.40), 'core': (0.14, 0.10, 1.05), 'stone': (0.12, 0.18, 2.6), 'gold': (0.115, 3.5, 1.10)},
}


def group(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    if v > 0.85 and s < 0.15:
        return 'core'
    if 0.10 <= h <= 0.20 and s < 0.45 and v > 0.55:
        return 'gold'
    if 0.45 <= h <= 0.58 and s >= 0.35 and v >= 0.45:
        return 'crystal'
    return 'stone'


def recolour(px, spec):
    r, g, b, a = px
    if a == 0:
        return px
    rule = spec[group(r, g, b)]
    if rule is None:
        return px
    hue, sat_k, val_k = rule
    _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    nr, ng, nb = colorsys.hsv_to_rgb(hue, min(1.0, s * sat_k), min(1.0, v * val_k))
    return (round(nr * 255), round(ng * 255), round(nb * 255), a)


base = Image.open(TEX + 'prism_sentinel.png').convert('RGBA')
glow = Image.open(TEX + 'prism_sentinel_glowmask.png').convert('RGBA')
counts = {}
for name, spec in VARIANTS.items():
    im = base.copy()
    data = [recolour(p, spec) for p in im.getdata()]
    im.putdata(data)
    im.save(os.path.join(OUT, f'prism_sentinel_{name}.png'))
    gm = glow.copy()
    gm.putdata([recolour(p, spec) if p[3] else p for p in gm.getdata()])
    gm.save(os.path.join(OUT, f'prism_sentinel_{name}_glowmask.png'))
for p in base.getdata():
    if p[3]:
        k = group(*p[:3]); counts[k] = counts.get(k, 0) + 1
print('texel groups in the base texture:', counts)
