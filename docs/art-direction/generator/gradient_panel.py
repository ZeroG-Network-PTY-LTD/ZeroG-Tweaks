"""Expanded gradient section for the study sheet: 9 material ramps on spheres, plus technique comparisons."""
import math, sys, os
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_kit import R, ingot, to_image, inside, blank, outline
import colorsys
FP = '/usr/share/fonts/truetype/dejavu/'
F = lambda s, b=False: ImageFont.truetype(FP + ('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'), s)
INK, SUB, PANEL, BG = (233, 231, 242), (150, 146, 170), (30, 29, 40), (21, 20, 28)
L = (-.55, -.6, .58); _n = math.sqrt(sum(v * v for v in L)); L = tuple(v / _n for v in L)


def sphere(ramp, mode='ramp', size=32):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); c0 = (size - 1) / 2; rad = size * .41
    for y in range(size):
        for x in range(size):
            dx, dy = (x - c0) / rad, (y - c0) / rad; d2 = dx * dx + dy * dy
            if d2 > 1: continue
            lam = max(0, dx * L[0] + dy * L[1] + math.sqrt(1 - d2) * L[2])
            if mode == 'dither':                                   # checker dither between every band: noisy
                f = lam * 4.2 + 1; i = int(f); frac = f - i
                i = i + (1 if ((x + y) % 2 == 0 and frac > .5) else 0)
            elif mode == 'pillow':                                 # shaded from the outline inward, ignoring the light
                i = 1 + int((1 - math.sqrt(d2)) * 4.6)
            else:
                i = 1 + int(lam * 4.2)
                if d2 > .86: i = max(1, i - 1)
            im.putpixel((x, y), ramp[max(1, min(5, i))])
    px = im.load()
    for y in range(size):
        for x in range(size):
            if px[x, y][3] and any(not (0 <= x + a < size and 0 <= y + b < size) or not px[x + a, y + b][3] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = ramp[0]
    if mode != 'pillow':
        for (x, y) in ((10, 9), (11, 9), (10, 10)): px[x, y] = ramp[5] if ramp is not R['glow'] else (255, 255, 255, 255)
        for x in range(13, 20): px[x, 27] = ramp[2]                # bounce light on the shadow side
    return im


def tint(im, rgb):
    out = im.copy(); p = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = p[x, y]
            if a: p[x, y] = (r * rgb[0] // 255, g * rgb[1] // 255, b * rgb[2] // 255, a)
    return out


def pillow_ingot():
    m = ingot(); h = len(m)
    shape = {(x, y) for y in range(h) for x in range(h) if m[y][x] is not None and not (isinstance(m[y][x], int) and m[y][x] == 0)}
    for (x, y) in shape:
        if isinstance(m[y][x], tuple): continue
        dist = min(abs(x - a) + abs(y - b) for a, b in [(p[0], p[1]) for p in [(xx, yy) for xx in range(32) for yy in range(32) if (xx, yy) not in shape]][:1] + [(x, y + 99)])
        edge = sum(1 for a in range(-2, 3) for b in range(-2, 3) if (x + a, y + b) not in shape)
        m[y][x] = 5 if edge == 0 else (3 if edge < 6 else 2)
    return m


def build():
    W, H = 2000, 780
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 0, 1960, H - 20], 12, fill=PANEL)
    d.text((60, 16), '1. Gradients: one hue-shifted ramp per material', font=F(19, True), fill=INK)
    mats = [('moonsteel', 'Moonsteel'), ('copper', 'Copper (planet)'), ('nullifite', 'Nullifite'), ('solvanite', 'Solvanite gold'), ('cerulite', 'Cerulite crystal'),
            ('leaf', 'Leaf (A natural)'), ('glow', 'Glow accent (C)'), ('wood', 'Wood / grip'), ('tint_gray', 'Gray for galaxy tint')]
    cw = 208
    for i, (k, name) in enumerate(mats):
        x = 64 + i * cw
        sp = sphere(R[k]).resize((160, 160), Image.NEAREST); im.paste(sp, (x + 14, 54), sp)
        for j, c in enumerate(R[k]):
            d.rectangle([x + j * 31, 224, x + j * 31 + 27, 252], fill=c[:3])
        h0 = colorsys.rgb_to_hsv(*[v / 255 for v in R[k][1][:3]])[0] * 360; h4 = colorsys.rgb_to_hsv(*[v / 255 for v in R[k][4][:3]])[0] * 360
        d.text((x, 258), name, font=F(13, True), fill=INK)
        d.text((x, 276), f'shadow H{int(h0)}  ->  light H{int(h4)}' if k != 'tint_gray' else 'value only (tint adds hue)', font=F(11), fill=SUB)
    d.text((60, 312), 'Techniques', font=F(17, True), fill=INK)
    S = 5; y0 = 344
    cmp = [
        (sphere([(v, v, v, 255) for v in (20, 55, 95, 140, 190, 240)]), 'Value only: muddy grey', False),
        (sphere(R['moonsteel']), 'Hue-shifted: same values, colour in the shadows', True),
        (sphere(R['moonsteel'], 'dither'), 'Dither everywhere: noisy at 32 px', False),
        (sphere(R['moonsteel']), 'Clustered bands: clean steps', True),
        (sphere(R['moonsteel'], 'pillow'), 'Pillow shading: lit from the middle, wrong', False),
        (to_image(ingot(), 'moonsteel'), 'Directional: lit from the top-left, right', True),
        (sphere(R['tint_gray']), 'Gray texture as stored', None),
        (tint(sphere(R['tint_gray']), (120, 200, 255)), 'Same texture with Galaxy 2 tint', None),
    ]
    for i, (spr, cap, ok) in enumerate(cmp):
        x = 64 + i * 236
        sp = spr.resize((32 * S, 32 * S), Image.NEAREST); im.paste(sp, (x + 30, y0), sp)
        col = (111, 212, 152) if ok else ((255, 122, 110) if ok is False else SUB)
        mark = 'right' if ok else ('wrong' if ok is False else 'tint')
        d.rounded_rectangle([x + 30, y0 + 168, x + 30 + 52, y0 + 186], 4, fill=col); d.text((x + 36, y0 + 170), mark, font=F(11, True), fill=(20, 20, 26))
        for j, line in enumerate([cap[k:k + 30] for k in range(0, len(cap), 30)][:2]):
            pass
        words = cap.split(' '); lines, cur = [], ''
        for w in words:
            if len(cur + ' ' + w) > 30: lines.append(cur); cur = w
            else: cur = (cur + ' ' + w).strip()
        lines.append(cur)
        for j, line in enumerate(lines): d.text((x + 30, y0 + 194 + j * 16), line, font=F(12), fill=INK if ok is not False else SUB)
    rules = ['Every material gets its own 6-tone ramp; never darken by multiplying toward black.', 'Shadow tones lean to blue/violet (warm metals lean to deep red-brown).',
             'Glow ramps run dark rim -> saturated -> white core and are never shaded by the light.', 'Blocks tinted per galaxy store a gray value ramp; the tint supplies the hue.']
    for j, t in enumerate(rules): d.text((64 + (j % 2) * 940, 650 + (j // 2) * 24), '• ' + t, font=F(13), fill=INK)
    return im


if __name__ == '__main__':
    build().save(sys.argv[1])
