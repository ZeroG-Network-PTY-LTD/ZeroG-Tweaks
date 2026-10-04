"""GIFs: (1) block lighting - orbiting light and turntable; (2) floating dropped items with ground shadows and glow pulse.
Shading steps along the hue-shifted ramp instead of multiplying brightness. Usage: python3 anims.py <out_dir>"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_kit import *
from style_kit import _norm

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
FP = '/usr/share/fonts/truetype/dejavu/'
F = lambda s, b=False: ImageFont.truetype(FP + ('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'), s)
BG = (24, 23, 33); INK = (233, 231, 242); SUB = (150, 146, 170)


def save_gif(frames, path, ms=60):
    pal = frames[0].convert('P', palette=Image.ADAPTIVE, colors=255)
    q = [f.convert('RGB').quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    q[0].save(path, save_all=True, append_images=q[1:], duration=ms, loop=0, disposal=1, optimize=False)


def label(d, x, y, t, sub=None):
    d.text((x, y), t, font=F(15, True), fill=INK)
    if sub: d.text((x, y + 20), sub, font=F(12), fill=SUB)


def block_gif():
    tex_a = block_texture(); tex_b = block_texture()
    W, H, N = 900, 420, 48
    frames = []
    for f in range(N):
        t = f / N; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
        d.text((24, 16), 'Block lighting: shade moves along the ramp, so shadows turn violet instead of grey', font=F(16, True), fill=INK)
        # left: fixed camera, light orbits around the block
        ang = t * 2 * math.pi; light = _norm((math.cos(ang) * .9, .75, math.sin(ang) * .9))
        cam = Cam(-35, 28, 170)
        polys = lit_cube(tex_a, 'moonsteel', cam, light)
        sub = draw(polys, (420, 320), BG, (210, 175)); im.paste(sub, (20, 60))
        # light marker on an orbit ellipse
        cx, cy = 230, 300
        ox, oy = cx + math.cos(ang) * 170, cy + 40 + math.sin(ang) * 40
        d.ellipse([cx - 170, cy, cx + 170, cy + 80], outline=(60, 58, 80))
        d.ellipse([ox - 7, oy - 7, ox + 7, oy + 7], fill=(255, 226, 140)); d.ellipse([ox - 3, oy - 3, ox + 3, oy + 3], fill=(255, 255, 230))
        label(d, 60, 384, 'Light orbits a still block', 'lit faces step up the ramp; turned-away faces step toward violet')
        # right: fixed top-left light, block turns
        light2 = _norm((-.6, .8, -.45)); cam2 = Cam(-35, 28, 150)
        polys2 = lit_cube(tex_b, 'nullifite', cam2, light2, spin=t * 2 * math.pi, glow_boost=int(1 + math.sin(t * 4 * math.pi)) // 1)
        sub2 = draw(polys2, (420, 320), BG, (210, 170)); im.paste(sub2, (470, 60))
        label(d, 510, 384, 'Block turns under a fixed top-left light', 'the inlay stays bright (emissive) and pulses')
        frames.append(im)
    save_gif(frames, f'{OUT}/block_lighting.gif', 70)
    frames[0].save(f'{OUT}/block_lighting_frame.png')


def stone_texture():
    """32 px lunar stone: grain clusters over a 4-tone rock ramp, lighter toward the top-left"""
    import random as _r
    rnd = _r.Random(12); m = blank()
    for y in range(32):
        for x in range(32):
            v = 3 if (x + y) > 20 else 4
            if (x + y) > 44: v = 2
            m[y][x] = ('m', 'rock', v)
    for _ in range(140):
        x, y = rnd.randrange(32), rnd.randrange(32); dv = rnd.choice((-1, 1)); n = rnd.choice((1, 2, 2, 3))
        for k in range(n):
            xx, yy = (x + k) % 32, (y + (k // 2)) % 32
            v = m[yy][xx][2]; m[yy][xx] = ('m', 'rock', max(1, min(5, v + dv)))
    return m


def items_gif():
    items = [('Moonsteel ingot', ingot(), 'moonsteel'), ('Raw Moonsteel', raw_ore(), 'moonsteel'), ('Moonsteel dust', dust(), 'moonsteel'),
             ('Moonsteel sword', sword(), 'moonsteel'), ('Copper ingot (planet palette)', ingot(), 'copper')]
    W, H, N = 1200, 470, 60
    light = _norm((-.6, .8, -.5)); stone = stone_texture(); frames = []
    cam = Cam(-35, 24, 150)
    for f in range(N):
        t = f / N; im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im, 'RGBA')
        d.text((24, 16), 'Floating items: dropped-item bob and spin over lit blocks, extruded 1 px, light from the top-left', font=F(16, True), fill=INK)
        for i, (name, spr, mat) in enumerate(items):
            ox = 120 + i * 238; oy = 250
            phase = t * 2 * math.pi + i * .9; bob = (math.sin(phase) + 1) / 2; spin = t * 2 * math.pi + i * .5
            glow = 1 if math.sin(phase * 2) > .3 else 0
            block = lit_cube(stone, 'rock', cam, light, size=.72, center=(0, -.62, 0))
            for _, ps, c in sorted(block, key=lambda q: -q[0]): d.polygon([(x + ox, y + oy) for x, y in ps], fill=c)
            # contact shadow on the block top: smaller and darker when the item is low
            top = cam.tr((0, -.26, 0)); sw = 44 - 14 * bob; shh = sw * .42
            d.ellipse([ox + top[0] - sw, oy + top[1] - shh, ox + top[0] + sw, oy + top[1] + shh], fill=(8, 6, 18, int(150 - 60 * bob)))
            item = extruded(spr, mat, cam, light, spin, (0, .34 + bob * .14, 0), scale=1.25, glow_boost=glow)
            for _, ps, c in sorted(item, key=lambda q: -q[0]): d.polygon([(x + ox, y + oy) for x, y in ps], fill=c)
            d.text((ox - d.textlength(name, font=F(12)) / 2, oy + 175), name, font=F(12), fill=SUB)
        frames.append(im)
    save_gif(frames, f'{OUT}/floating_items.gif', 50)
    frames[8].save(f'{OUT}/floating_items_frame.png')


if __name__ == '__main__':
    block_gif(); items_gif(); print('ok')
