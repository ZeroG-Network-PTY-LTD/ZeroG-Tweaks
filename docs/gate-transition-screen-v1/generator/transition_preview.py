"""Animated mock of the gate transition screen, built only from the shipped sprites.

Stage is a fixed 480x270 pixel canvas (the screen scales it by a whole number, nearest
neighbour). Text is drawn on the 2x preview with a pixel font standing in for Minecraft's.
Usage: python3 transition_preview.py <dir containing assets/> <out_dir>
"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont

SRC = os.path.join(sys.argv[1], 'assets/zerog_tweaks/textures/gui/transition')
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
W, H, UP, FPS = 480, 270, 2, 12
FONT = ImageFont.truetype('/usr/share/fonts/opentype/unifont/unifont.otf', 16) if os.path.exists(
    '/usr/share/fonts/opentype/unifont/unifont.otf') else ImageFont.truetype('/usr/share/fonts/opentype/unifont/unifont_jp.otf', 16)
SPACE = (11, 10, 22)
INK, SUB, GLOW, WARN = (232, 228, 246), (150, 146, 176), (196, 140, 255), (255, 176, 64)

img = lambda n: Image.open(f'{SRC}/{n}.png').convert('RGBA')
def frames(n, h):
    s = img(n); return [s.crop((0, i * h, s.width, (i + 1) * h)) for i in range(s.height // h)]

GALAXY_TINT = {1: 0xFFFFFF, 2: 0x9CB8F0, 3: 0x9CB8F0, 4: 0xF0A878, 5: 0xC8E6F0}  # ZGBlockColors.GALAXY
TYPE_TINT = {'ocean': 0x7C9CB8, 'desert': 0xE3CB94, 'volcanic': 0x9A7A6A, 'frozen': 0xDDEAF2,
             'toxic': 0x98AE6A, 'crystal': 0xC6AEE6, 'barren': 0xB0ACA6}


def game_tint(wtype, galaxy):
    """same maths as ZGBlockColors.tint(): type colour x softened galaxy colour"""
    g = GALAXY_TINT[galaxy]; t = TYPE_TINT[wtype]
    soft = ((g & 0xFEFEFE) >> 1) + 0x808080
    return tuple(((t >> s & 255) * (soft >> s & 255)) // 255 for s in (16, 8, 0))


def tinted(im, rgb):
    """multiply only gray pixels (the lava/crystal glow overlay keeps its own colour)"""
    px = im.load(); out = im.copy(); po = out.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and abs(r - g) < 6 and abs(g - b) < 6 and (r, g, b) != (11, 10, 26):
                po[x, y] = (r * rgb[0] // 255, g * rgb[1] // 255, b * rgb[2] // 255, a)
    return out


def ease(t): t = max(0, min(1, t)); return t * t * (3 - 2 * t)
def lerp(a, b, t): return a + (b - a) * t


def scaled(im, s):
    w, h = max(1, round(im.width * s)), max(1, round(im.height * s))
    return im.resize((w, h), Image.NEAREST)


def tile(canvas, layer, ox, oy, alpha=255):
    ox, oy = int(ox) % layer.width, int(oy) % layer.height
    for x in range(-ox, W, layer.width):
        for y in range(-oy, H, layer.height):
            canvas.alpha_composite(layer, (x, y))


def nine(slice_im, w, h, b=8):
    out = Image.new('RGBA', (w, h)); s = slice_im
    cw, ch = s.width - 2 * b, s.height - 2 * b
    mid = s.crop((b, b, b + cw, b + ch)).resize((w - 2 * b, h - 2 * b), Image.NEAREST)
    out.paste(mid, (b, b))
    for (sx, sy, dx, dy) in ((0, 0, 0, 0), (s.width - b, 0, w - b, 0), (0, s.height - b, 0, h - b), (s.width - b, s.height - b, w - b, h - b)):
        out.paste(s.crop((sx, sy, sx + b, sy + b)), (dx, dy))
    out.paste(s.crop((b, 0, b + cw, b)).resize((w - 2 * b, b), Image.NEAREST), (b, 0))
    out.paste(s.crop((b, s.height - b, b + cw, s.height)).resize((w - 2 * b, b), Image.NEAREST), (b, h - b))
    out.paste(s.crop((0, b, b, b + ch)).resize((b, h - 2 * b), Image.NEAREST), (0, b))
    out.paste(s.crop((s.width - b, b, s.width, b + ch)).resize((b, h - 2 * b), Image.NEAREST), (w - b, b))
    return out


def render(route, path):
    far, mid, near, neb = img('starfield_far'), img('starfield_mid'), img('starfield_near'), img('nebula')
    gal = img(f"galaxy_{route['galaxy']}")
    star = frames(f"star_{route['galaxy']}", 48)
    ret = frames('reticle', 24)
    planet = frames(f"planet_{route['sprite']}", 128)
    if route.get('tint'): planet = [tinted(p, game_tint(route['sprite'].split('_', 1)[1], route['galaxy'])) for p in planet]
    plate_src, pf, pfill, icons = img('nameplate'), img('progress_frame'), img('progress_fill'), img('hazard_icons')
    wisp = frames('echo_wisp', 16)
    ICON = ['gravity', 'heat', 'cold', 'acid', 'storm', 'void', 'safe']
    tx, ty = route['target']                       # destination system on the galaxy sprite
    gx0, gy0 = W // 2 - 96, H // 2 - 96 - 6        # galaxy sprite placement on the stage
    N = 96; out = []
    for f in range(N):
        t = f / FPS
        st = Image.new('RGBA', (W, H), (*SPACE, 255))
        z = 1 + 7 * ease((t - 1.5) / 1.0) + 30 * ease((t - 2.5) / 1.2) * 0  # galaxy zoom factor
        drift = t * 6
        tile(st, neb, drift * .5, 0); tile(st, far, drift, 0); tile(st, mid, drift * 2, drift * .3)
        # near layer streaks during the zooms (rift travel feeling)
        streak = ease((t - 1.5) / .4) * (1 - ease((t - 2.4) / .3)) + ease((t - 3.4) / .3) * (1 - ease((t - 3.9) / .3))
        if streak > .05:
            d = ImageDraw.Draw(st)
            nx = near.load()
            for y in range(0, near.height, 1):
                for x in range(0, near.width):
                    if nx[x, y][3] > 200:
                        sx, sy = (x * 2 + 7) % W, (y * 1 + 3) % H
                        vx, vy = sx - W / 2, sy - H / 2
                        L = streak * 22
                        n = math.hypot(vx, vy) or 1
                        d.line([(sx, sy), (sx + vx / n * L, sy + vy / n * L)], fill=nx[x, y][:3] + (200,))
        else:
            tile(st, near, drift * 3, drift * .5)
        dd = ImageDraw.Draw(st)
        # ---------------- stage 1-2: galaxy, lock-on, zoom into the target system (0.0 - 2.5 s)
        if t < 2.6:
            zz = 1 + 9 * ease((t - 1.5) / 1.0) ** 2
            g = scaled(gal, zz)
            px = W // 2 - tx * zz - (W // 2 - (gx0 + tx)) * (1 - ease((t - 1.5) / 1.0))
            py = H // 2 - ty * zz - (H // 2 - (gy0 + ty)) * (1 - ease((t - 1.5) / 1.0))
            fade = 1 - ease((t - 2.2) / .4)
            if fade < 1:
                a = g.getchannel('A').point(lambda v: int(v * fade)); g.putalpha(a)
            st.alpha_composite(g, (int(px), int(py)))
            if .4 < t < 1.6:   # reticle locks on, shrinking from 3x to 1x
                s = lerp(3, 1, ease((t - .4) / .6))
                r = scaled(ret[f % 4], s)
                st.alpha_composite(r, (int(gx0 + tx - r.width / 2), int(gy0 + ty - r.height / 2)))
        # ---------------- stage 3: star system, highlight destination orbit, zoom to the planet (2.2 - 3.9 s)
        if 2.2 < t < 4.0:
            a_in = ease((t - 2.2) / .4); a_out = 1 - ease((t - 3.6) / .3)
            zz = 1 + 3 * ease((t - 3.2) / .7) ** 2
            layer = Image.new('RGBA', (W, H)); ld = ImageDraw.Draw(layer)
            sx, sy = 190, H // 2
            orbits = route['orbits']; slot = route['slot']
            target = None
            for k, rr in enumerate(orbits):
                a = .3 + k * 1.37 + t * .15 / (k + 1)
                ex, ey = rr, rr * .32
                pts = [(sx + ex * math.cos(q / 60 * 2 * math.pi), sy + ey * math.sin(q / 60 * 2 * math.pi)) for q in range(61)]
                col = (196, 140, 255, 255) if k == slot else (60, 66, 104, 255)
                for q in range(0, 60, 1 if k == slot else 2): ld.line([pts[q], pts[q + 1]], fill=col)
                px_, py_ = sx + ex * math.cos(a), sy + ey * math.sin(a)
                r = 4 if k == slot else 2
                ld.ellipse([px_ - r, py_ - r, px_ + r, py_ + r], fill=(232, 228, 246, 255) if k == slot else (120, 126, 160, 255), outline=(11, 10, 26, 255))
                if k == slot: target = (px_, py_)
            layer.alpha_composite(star[f % 4], (sx - 24, sy - 24))
            rs = ret[f % 4]; layer.alpha_composite(rs, (int(target[0] - 12), int(target[1] - 12)))
            if zz > 1:
                layer = scaled(layer, zz)
                ox, oy = target[0] * zz - target[0], target[1] * zz - target[1]
                layer = layer.crop((int(ox), int(oy), int(ox) + W, int(oy) + H))
            al = layer.getchannel('A').point(lambda v: int(v * a_in * a_out)); layer.putalpha(al)
            st.alpha_composite(layer)
        # ---------------- stage 4-5: planet arrives, nameplate, hold loop while the world loads (3.6 s +)
        if t > 3.6:
            grow = ease((t - 3.6) / .7)
            s = lerp(.2, 1.0, grow)
            fr = planet[int(t * 6) % 16]
            p = scaled(fr, s)
            cx, cy = 168, 128
            st.alpha_composite(p, (int(cx - p.width / 2), int(cy - p.height / 2)))
            slide = ease((t - 4.0) / .5)
            plate = nine(plate_src, 196, 92)
            st.alpha_composite(plate, (int(lerp(W + 10, 262, slide)), 82))
            # hazard / gravity chips
            for n, ic in enumerate(route['chips']):
                k = ICON.index(ic)
                st.alpha_composite(scaled(icons.crop((k * 9, 0, k * 9 + 9, 9)), 1), (int(lerp(W + 10, 262, slide)) + 12 + n * 30, 146))
            # progress (world loading) bar
            prog = min(1, max(0, (t - 4.4) / 2.6))
            bx, by = 148, 226
            st.alpha_composite(pf, (bx, by))
            fill = pfill.crop((int((t * 8) % 24), 0, int((t * 8) % 24) + 180, 5)) if False else pfill
            st.alpha_composite(fill.crop((0, 0, max(1, int(180 * prog)), 5)), (bx + 2, by + 2))
            st.alpha_composite(wisp[(f // 6) % 2], (bx - 22, by - 5))
        # ---------------- white-out entry and exit
        wa = 0
        if t < .5: wa = 1 - ease(t / .5)
        if t > 7.4: wa = ease((t - 7.4) / .4)
        if wa > 0:
            st.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(255 * wa))))
        big = st.convert('RGB').resize((W * UP, H * UP), Image.NEAREST)
        d = ImageDraw.Draw(big)
        # text layer (Minecraft font in game; unifont stands in here)
        if .5 < t < 2.4:
            d.text((24, 22), f"GALAXY {route['galaxy']}  |  {route['galaxy_name']}", font=FONT, fill=SUB)
            if t > .9: d.text((24, 44), 'LOCKING COORDINATES', font=FONT, fill=GLOW)
        if 2.5 < t < 3.9:
            d.text((24, 22), route['system'], font=FONT, fill=SUB)
        if t > 4.2:
            ox = int(lerp(W + 10, 262, ease((t - 4.0) / .5))) * UP
            d.text((ox + 24, 82 * UP + 22), route['catalog'], font=FONT, fill=SUB)
            d.text((ox + 24, 82 * UP + 44), route['name'], font=FONT, fill=INK)
            d.text((ox + 24, 82 * UP + 66), route['klass'], font=FONT, fill=GLOW)
            for n, lab in enumerate(route['chip_labels']):
                d.text((ox + 24 + n * 60 + 22, 146 * UP - 2), lab, font=FONT, fill=SUB)
        if t > 4.4:
            line = route['echo']; k = min(len(line), int((t - 4.4) * 24))
            d.text((148 * UP, 226 * UP - 40), line[:k], font=FONT, fill=INK)
            done = (t - 4.4) / 2.6 >= 1
            d.text((148 * UP + 2, 226 * UP + 24), 'RIFT STABLE | ARRIVING' if done else 'STABILISING RIFT…', font=FONT, fill=GLOW if done else SUB)
        out.append(big)
    pal = out[40].convert('P', palette=Image.ADAPTIVE, colors=255)
    q = [o.quantize(palette=pal, dither=Image.Dither.NONE) for o in out]
    q[0].save(path, save_all=True, append_images=q[1:], duration=int(1000 / FPS), loop=0, disposal=1)
    for k, fr in ((10, 'galaxy'), (36, 'system'), (70, 'planet')):
        out[k].save(path.replace('.gif', f'_{fr}.png'))
    return out


ROUTES = {
    'earth_to_moon': dict(galaxy=1, galaxy_name='SOL', system='SOL SYSTEM  |  3RD PLANET > 1ST MOON', target=(126, 112),
                          sprite='moon', orbits=[34, 58, 86, 120], slot=2, catalog='SOL III a', name='The Moon',
                          klass='Earth\'s moon | Low gravity', chips=['gravity', 'safe'], chip_labels=['0.5×', 'calm'],
                          echo='Echo: "I know this rock. We left something here."'),
    'moon_to_cerulon': dict(galaxy=2, galaxy_name='ZG-855', system='ZG-855 SYSTEM  |  PLANET b', target=(64, 76),
                            sprite='cerulon', orbits=[40, 70, 100, 132], slot=0, catalog='ZG-855 b', name='Cerulon',
                            klass='Resource World', chips=['gravity', 'safe'], chip_labels=['0.9×', 'calm'],
                            echo='Echo: "The Quiet Mines. The Keepers still guard them."'),
    'g3_wasteland': dict(galaxy=3, galaxy_name='ZG-311', system='ZG-311 SYSTEM  |  PLANET e', target=(132, 70),
                         sprite='wasteland_volcanic', tint=True, orbits=[30, 52, 76, 102, 130], slot=3,
                         catalog='ZG-311 e', name='"Vorrhex"', klass='Wasteland | Volcanic', chips=['gravity', 'heat', 'storm'],
                         chip_labels=['1.1×', 'heat', 'ash'], echo='Echo: "Nothing the Concord wanted. Look anyway."'),
}

if __name__ == '__main__':
    for k, r in ROUTES.items():
        render(r, f'{OUT}/transition_{k}.gif'); print('ok', k)
