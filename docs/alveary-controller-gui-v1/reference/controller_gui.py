"""Alveary Controller screen: layout data -> GUI textures, mockups, annotated layout sheet and the text spec.
One source of truth: every coordinate in the spec comes from LAYOUT / SPRITES below.
Usage: python3 controller_gui.py <out_dir>"""
import os, sys, math, random, json
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
FP = '/usr/share/fonts/truetype/dejavu/'
F = lambda s, b=False: ImageFont.truetype(FP + ('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'), s)
FM = lambda s: ImageFont.truetype(FP + 'DejaVuSansMono.ttf', s)

# ------------------------------------------------------------------ palette (classic 1.12 bee-mod GUI: vanilla grey + honey)
C = dict(bg=(198, 198, 198), hi=(255, 255, 255), sh=(85, 85, 85), edge=(0, 0, 0), slot=(139, 139, 139), slot_d=(55, 55, 55),
         well=(120, 116, 106), well_d=(46, 44, 40), honey=(232, 168, 44), honey_d=(176, 112, 22), honey_l=(255, 214, 120),
         wax=(240, 214, 150), comb=(214, 160, 52), text=(64, 64, 64))

TIERS = [(1, 'Rustic Alveary', 3, '#9a7a4a'), (2, 'Controlled Alveary', 4, '#7d8f5a'), (3, 'Industrial Alveary', 6, '#8a8f99'),
         (4, 'Aeronautic Alveary', 8, '#5f8fb5'), (5, 'ATM Star Alveary', 12, '#d9b23a'), (6, 'Nebula Refractory', 18, '#9a5fd0'),
         (7, 'Quantum Queen Chamber', 27, '#3fd0c8')]

W, H = 256, 250
# ------------------------------------------------------------------ LAYOUT: every element on the screen (x, y, w, h relative to the screen's top-left)
# kind: window, panel, slot, royal, gauge, bar, tank, lamp, button, grid, box, text, lamp_status, badge
LAYOUT = [
    ('window', 'window', 0, 0, W, H, 1, 'Screen background (vanilla window bevel).'),
    ('title', 'text', 8, 5, 120, 9, 1, 'Title: "Alveary Controller". Code draws it (font colour #404040, no shadow).'),
    ('tier_badge', 'badge', 131, 3, 64, 12, 1, 'Tier badge: tier number + short name on the tier colour. Sprite per tier.'),
    ('status_lamp', 'lamp_status', 199, 4, 10, 10, 1, 'Status icon (see Status codes). Tooltip gives the full reason.'),
    ('status_text', 'text', 211, 5, 38, 9, 1, 'Short status word ("Working", "No Queen", ...). Code draws it, clipped to 38 px.'),
    # -- HIVE panel
    ('p_hive', 'panel', 7, 16, 58, 78, 1, 'HIVE panel.'),
    ('queen', 'royal', 12, 22, 26, 26, 1, 'Queen / Princess slot (slot 0). Large "royal" frame; item drawn at +5,+5. Accepts Productive Bees queens and princesses only.'),
    ('drone', 'slot', 16, 54, 18, 18, 1, 'Drone slot (slot 1). Ghost drone icon when empty.'),
    ('analyze', 'button', 19, 76, 12, 12, 1, 'Analyze button: opens the bee\'s genome page (Beealyzer view) without the Portable Beealyzer.'),
    ('life_bar', 'bar', 44, 22, 6, 66, 1, 'Queen lifespan, fills from the bottom; green > amber > red as life runs out.'),
    ('cycle_bar', 'bar', 54, 22, 6, 66, 1, 'Work cycle progress, fills from the bottom in honey colour; one product roll per full bar.'),
    # -- CLIMATE panel
    ('p_climate', 'panel', 69, 16, 62, 78, 1, 'CLIMATE panel.'),
    ('ic_temp', 'icon', 75, 19, 10, 10, 1, 'Thermometer icon.'),
    ('ic_hum', 'icon', 95, 19, 10, 10, 1, 'Droplet icon.'),
    ('ic_grav', 'icon', 115, 19, 10, 10, 1, 'Gravity icon (orbit ring). ZeroG planets have their own gravity.'),
    ('g_temp', 'gauge', 75, 31, 10, 50, 1, 'Temperature gauge: needle bar from the bottom (Icy .. Hellish, 7 steps). Tolerance band drawn on its left edge.'),
    ('g_hum', 'gauge', 95, 31, 10, 50, 1, 'Humidity gauge (Arid .. Damp, 3 steps, shown as 5 sub-steps).'),
    ('g_grav', 'gauge', 115, 31, 10, 50, 1, 'Gravity gauge (0.5 g .. 1.3 g). Overworld = 1.0. Bees outside their gravity tolerance work at half speed.'),
    ('m_heater', 'lamp', 73, 84, 9, 8, 2, 'Heater module lamp (lit when a Heater is part of the structure and running).'),
    ('m_fan', 'lamp', 87, 84, 9, 8, 2, 'Fan lamp (cooling).'),
    ('m_humid', 'lamp', 101, 84, 9, 8, 2, 'Humidifier lamp.'),
    ('m_dryer', 'lamp', 115, 84, 9, 8, 2, 'Dryer lamp.'),
    # -- OUTPUT panel
    ('p_output', 'panel', 135, 16, 62, 78, 1, 'OUTPUT panel.'),
    ('out_grid', 'grid', 139, 22, 54, 54, 1, 'Product buffer, 3 x 3 (slots 2-10). Output Hatch (T3+) pulls from here.'),
    ('eject', 'button', 139, 79, 12, 12, 3, 'Auto-eject toggle: push products into the Output Hatch every 20 ticks.'),
    ('void', 'button', 153, 79, 12, 12, 1, 'Void-excess toggle: when the buffer is full, destroy new products instead of stopping (off by default).'),
    ('sort', 'button', 181, 79, 12, 12, 1, 'Sort/compact the product buffer.'),
    # -- POWER panel
    ('p_power', 'panel', 201, 16, 48, 78, 1, 'POWER and FLUIDS panel. Sealed plate over each part below its tier.'),
    ('fe', 'tank', 205, 22, 8, 62, 3, 'FE buffer (Energy Ports, T3+). Red > amber fill. Tooltip: "12,400 / 50,000 FE".'),
    ('honey_tank', 'tank', 216, 22, 14, 62, 3, 'Honey tank (Honey Port, T3+). 8,000 mB. Gauge ticks overlay every 1,000 mB.'),
    ('fluid_tank', 'tank', 233, 22, 12, 62, 6, 'Catalyst fluid tank (Fluid Port, T6+): Liquid Starlight etc. for mutation boosts. 4,000 mB.'),
    ('ic_fe', 'icon', 205, 86, 8, 6, 3, 'Bolt icon.'),
    ('ic_honey', 'icon', 219, 86, 8, 6, 3, 'Honey drop icon.'),
    ('ic_fluid', 'icon', 235, 86, 8, 6, 6, 'Fluid drop icon.'),
    # -- FRAMES panel
    ('p_frames', 'panel', 7, 96, 242, 58, 1, 'FRAMES panel.'),
    ('frame_grid', 'grid', 11, 98, 162, 54, 1, 'Frame housings, 9 x 3 (slots 11-37). Unlocked left to right, top to bottom: 3/4/6/8/12/18/27 by tier; the rest show the sealed-housing overlay.'),
    ('mods_box', 'box', 177, 98, 68, 54, 1, 'Modifiers box: combined effect of all frames and modules. Code draws the numbers.'),
    ('ic_prod', 'icon', 180, 101, 9, 9, 1, 'Productivity icon + "x1.80".'),
    ('ic_life', 'icon', 180, 114, 9, 9, 1, 'Lifespan icon + "x0.60".'),
    ('ic_mut', 'icon', 180, 127, 9, 9, 1, 'Mutation icon + "x2.00".'),
    ('ic_terr', 'icon', 180, 140, 9, 9, 1, 'Territory icon + "x1.50".'),
    # -- player inventory
    ('inv_label', 'text', 47, 158, 60, 9, 1, '"Inventory" label (vanilla).'),
    ('inv', 'grid', 47, 168, 162, 54, 1, 'Player inventory 9 x 3 (menu slots 38-64).'),
    ('hotbar', 'grid', 47, 226, 162, 18, 1, 'Hotbar 9 x 1 (menu slots 65-73).'),
]
L = {e[0]: e for e in LAYOUT}

STATUS = [('working', 'Working', '#3fbf5f', 'All good.'),
          ('no_queen', 'No Queen', '#8b8b8b', 'Queen slot empty, or a princess without a drone.'),
          ('too_hot', 'Too Hot', '#e2553a', 'Temperature above the queen\'s tolerance. Add a Fan (T2+) or move biome.'),
          ('too_cold', 'Too Cold', '#4fa7e8', 'Temperature below tolerance. Add a Heater (T2+).'),
          ('too_wet', 'Too Damp', '#3f6fd0', 'Humidity above tolerance. Add a Dryer (T2+).'),
          ('too_dry', 'Too Arid', '#d9b44a', 'Humidity below tolerance. Add a Humidifier (T2+).'),
          ('gravity', 'Gravity', '#9a5fd0', 'Gravity outside tolerance: works at half speed (not stopped). Aeronautic rotor (T4+) shifts it one step.'),
          ('no_sky', 'No Sky', '#6f7b86', 'Bee needs open sky and the roof blocks it (Glass parts count as open).'),
          ('night', 'Resting', '#3a3f6e', 'Diurnal bee at night or nocturnal bee by day. Not an error.'),
          ('rain', 'Rain', '#5a7fa0', 'Raining and the bee is not tolerant. Not an error.'),
          ('full', 'Full', '#e9a03a', 'Product buffer full and Void is off.'),
          ('no_power', 'No Power', '#d6342a', 'T3+ needs FE every tick; buffer empty.'),
          ('incomplete', 'Broken', '#ff4f8a', 'Structure incomplete. The controller projects a ghost of the missing parts.')]

MODULES = [('heater', '#e2553a'), ('fan', '#4fa7e8'), ('humid', '#3f6fd0'), ('dryer', '#d9b44a')]


# ------------------------------------------------------------------ drawing primitives
def px(d, x, y, c): d.point((x, y), fill=c)


def rect(d, x, y, w, h, c): d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)


def bevel(d, x, y, w, h, fill, raised=True, depth=1):
    tl, br = (C['hi'], C['sh']) if raised else (C['slot_d'], C['hi'])
    rect(d, x, y, w, h, fill)
    for i in range(depth):
        d.line([(x + i, y + i), (x + w - 2 - i, y + i)], fill=tl); d.line([(x + i, y + i), (x + i, y + h - 2 - i)], fill=tl)
        d.line([(x + 1 + i, y + h - 1 - i), (x + w - 1 - i, y + h - 1 - i)], fill=br); d.line([(x + w - 1 - i, y + 1 + i), (x + w - 1 - i, y + h - 1 - i)], fill=br)
    px(d, x + w - 1, y, C['bg']); px(d, x, y + h - 1, C['bg'])


def slot(d, x, y, w=18, h=18):
    rect(d, x, y, w, h, C['slot'])
    d.line([(x, y), (x + w - 2, y)], fill=C['slot_d']); d.line([(x, y), (x, y + h - 2)], fill=C['slot_d'])
    d.line([(x + 1, y + h - 1), (x + w - 1, y + h - 1)], fill=C['hi']); d.line([(x + w - 1, y + 1), (x + w - 1, y + h - 1)], fill=C['hi'])
    px(d, x + w - 1, y, C['slot']); px(d, x, y + h - 1, C['slot'])


def window(d):
    rect(d, 0, 0, W, H, (0, 0, 0, 0))
    rect(d, 1, 1, W - 2, H - 2, C['bg'])
    d.line([(2, 0), (W - 3, 0)], fill=C['edge']); d.line([(2, H - 1), (W - 3, H - 1)], fill=C['edge'])
    d.line([(0, 2), (0, H - 3)], fill=C['edge']); d.line([(W - 1, 2), (W - 1, H - 3)], fill=C['edge'])
    for (a, b) in ((1, 1), (W - 2, 1), (1, H - 2), (W - 2, H - 2)): px(d, a, b, C['edge'])
    d.line([(2, 1), (W - 4, 1)], fill=C['hi']); d.line([(1, 2), (1, H - 4)], fill=C['hi'])
    d.line([(2, 2), (W - 5, 2)], fill=C['hi']); d.line([(2, 2), (2, H - 5)], fill=C['hi'])
    d.line([(3, H - 2), (W - 3, H - 2)], fill=C['sh']); d.line([(W - 2, 3), (W - 2, H - 3)], fill=C['sh'])
    d.line([(4, H - 3), (W - 3, H - 3)], fill=C['sh']); d.line([(W - 3, 4), (W - 3, H - 3)], fill=C['sh'])
    px(d, 2, H - 3, C['bg']); px(d, W - 3, 2, C['bg'])


def comb_pattern(d, x, y, w, h, c1, c2, s=4):
    """faint honeycomb pattern for panel headers"""
    for yy in range(h):
        for xx in range(w):
            row = (yy // s); off = (s // 2) if row % 2 else 0
            if (xx + off) % s == 0 or yy % s == 0: px(d, x + xx, y + yy, c2)
            else: px(d, x + xx, y + yy, c1)


def panel(d, x, y, w, h):
    """recessed panel well with a 2 px honey strip along the top"""
    rect(d, x, y, w, h, (182, 180, 172))
    d.line([(x, y), (x + w - 2, y)], fill=C['sh']); d.line([(x, y), (x, y + h - 2)], fill=C['sh'])
    d.line([(x + 1, y + h - 1), (x + w - 1, y + h - 1)], fill=C['hi']); d.line([(x + w - 1, y + 1), (x + w - 1, y + h - 1)], fill=C['hi'])
    d.line([(x + 1, y + 1), (x + w - 2, y + 1)], fill=C['honey_d']); d.line([(x + 1, y + 2), (x + w - 2, y + 2)], fill=C['honey'])


def well(d, x, y, w, h):
    """dark recessed well for gauges and tanks"""
    rect(d, x, y, w, h, C['well_d'])
    d.line([(x, y), (x + w - 1, y)], fill=C['slot_d']); d.line([(x, y), (x, y + h - 1)], fill=C['slot_d'])
    d.line([(x + 1, y + h - 1), (x + w - 1, y + h - 1)], fill=C['hi']); d.line([(x + w - 1, y + 1), (x + w - 1, y + h - 1)], fill=C['hi'])
    rect(d, x + 1, y + 1, w - 2, h - 2, (36, 34, 31))


# ------------------------------------------------------------------ pixel glyphs (rows of '#'/'o'/'.'), for icons
def glyph(d, x, y, rows, cmap):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch in cmap: px(d, x + i, y + j, cmap[ch])


GL = {
    'temp': ['...##....', '..#oo#...', '..#oo#...', '..#oo#...', '..#rr#...', '..#rr#...', '.#rrrr#..', '.#rrrr#..', '..####...', '.........'],
    'hum': ['....#....', '...#o#...', '...#o#...', '..#ooo#..', '.#oooo##.', '.#ooooo#.', '.#oo.oo#.', '..#ooo#..', '...###...', '.........'],
    'grav': ['...###...', '..#ooo#..', '##o###o##', '#.#ooo#.#', '##o###o##', '..#ooo#..', '...###...', '.........', '.........', '.........'],
    'bolt': ['...##', '..##.', '.####', '..##.', '.##..', '##...'],
    'drop': ['..#...', '.#o#..', '#ooo#.', '#ooo#.', '.###..', '......'],
    'prod': ['....#....', '...###...', '..#####..', '....#....', '....#....', '..#####..', '.#######.', '.........', '.........'],
    'life': ['.#######.', '..#ooo#..', '...#o#...', '....#....', '...#.#...', '..#ooo#..', '.#######.', '.........', '.........'],
    'mut': ['.##...##.', '..#...#..', '...#.#...', '...ooo...', '...#.#...', '..#...#..', '.##...##.', '.........', '.........'],
    'terr': ['#.......#', '.#.....#.', '..#ooo#..', '..#o#o#..', '..#ooo#..', '.#.....#.', '#.......#', '.........', '.........'],
    'crown': ['#..#..#', '#.###.#', '#######', '#######', '.......'],
    'drone': ['.##.##.', '#..#..#', '.#####.', '#.###.#', '..###..', '...#...'],
    'frame': ['#######', '#.#.#.#', '#######', '#.#.#.#', '#######', '#.#.#.#', '#######'],
    'analyze': ['.###....', '#...#...', '#...#...', '#...#...', '.###.#..', '.....##.', '......##', '........'],
    'eject': ['...#....', '..###...', '.#####..', '...#....', '...#....', '.#####..', '........', '........'],
    'void': ['.#####..', '#.....#.', '#.#.#.#.', '#..#..#.', '#.#.#.#.', '#.....#.', '.#####..', '........'],
    'sort': ['#####...', '........', '####....', '........', '###.....', '........', '##......', '........'],
}


def status_icon(d, x, y, col, kind):
    """10 x 10 round status lamp with a tiny symbol"""
    for j in range(10):
        for i in range(10):
            dd = math.hypot(i - 4.5, j - 4.5)
            if dd <= 4.6:
                k = 1.25 - dd / 6
                c = tuple(max(0, min(255, int(v * k))) for v in col[:3])
                px(d, x + i, y + j, c)
            elif dd <= 5.2: px(d, x + i, y + j, (30, 30, 30))
    sym = {'working': ['......', '....#.', '...#..', '#.#...', '.#....'], 'no_queen': ['#..#..#', '#.###.#', '#######'],
           'full': ['####', '####', '####'], 'no_power': ['..#', '.##', '###', '.#.'], 'incomplete': ['#.#', '.#.', '#.#'],
           'too_hot': ['.#.', '###', '.#.'], 'too_cold': ['#.#', '.#.', '#.#']}.get(kind)
    if sym:
        sw, sh = len(sym[0]), len(sym)
        glyph(d, x + 5 - sw // 2, y + 5 - sh // 2, sym, {'#': (255, 255, 255)})


def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ------------------------------------------------------------------ 1. background texture
def background():
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    window(d)
    for e in LAYOUT:
        n, k, x, y, w, h, t, _ = e
        if k == 'panel': panel(d, x, y, w, h)
    for e in LAYOUT:
        n, k, x, y, w, h, t, _ = e
        if k == 'slot': slot(d, x, y)
        elif k == 'royal':
            slot(d, x, y, w, h)
            d.rectangle([x + 2, y + 2, x + w - 3, y + h - 3], outline=C['honey_d'])
            for (a, b) in ((x + 1, y + 1), (x + w - 2, y + 1), (x + 1, y + h - 2), (x + w - 2, y + h - 2)): px(d, a, b, C['honey'])
        elif k == 'grid':
            for gy in range(y, y + h, 18):
                for gx in range(x, x + w, 18): slot(d, gx, gy)
        elif k in ('gauge', 'bar', 'tank'): well(d, x, y, w, h)
        elif k == 'box':
            rect(d, x, y, w, h, (170, 168, 160)); d.rectangle([x, y, x + w - 1, y + h - 1], outline=C['sh'])
            for r in range(4): d.line([(x + 2, y + 13 * (r + 1) + 1), (x + w - 3, y + 13 * (r + 1) + 1)], fill=(188, 186, 178)) if r < 3 else None
        elif k == 'lamp': rect(d, x, y, w, h, (60, 58, 52)); d.rectangle([x, y, x + w - 1, y + h - 1], outline=C['sh'])
        elif k == 'button': bevel(d, x, y, w, h, C['bg'])
        elif k == 'lamp_status': rect(d, x, y, w, h, C['bg'])
    # icons baked into the background (static)
    ic = {'#': (70, 66, 60), 'o': (150, 146, 138), 'r': (200, 70, 50)}
    glyph(d, *L['ic_temp'][2:4], GL['temp'], {'#': (70, 66, 60), 'o': (230, 230, 230), 'r': (210, 60, 40)})
    glyph(d, *L['ic_hum'][2:4], GL['hum'], {'#': (40, 70, 140), 'o': (110, 160, 230)})
    glyph(d, *L['ic_grav'][2:4], GL['grav'], {'#': (90, 60, 140), 'o': (170, 130, 220)})
    for nm, g in (('ic_prod', 'prod'), ('ic_life', 'life'), ('ic_mut', 'mut'), ('ic_terr', 'terr')):
        glyph(d, *L[nm][2:4], GL[g], {'#': (70, 66, 60), 'o': C['honey_d']})
    # gauge scale ticks (right side of each gauge, outside the well)
    for nm in ('g_temp', 'g_hum', 'g_grav'):
        _, _, x, y, w, h, _, _ = L[nm]
        for i in range(0, h + 1, 7): px(d, x + w, y + h - 1 - i, C['sh'])
    # honey tank ticks every 1/8
    for nm in ('honey_tank',):
        _, _, x, y, w, h, _, _ = L[nm]
        for i in range(1, 8): d.line([(x + 1, y + h - 1 - i * (h - 2) // 8), (x + 3, y + h - 1 - i * (h - 2) // 8)], fill=(90, 86, 80))
    # ghost icons in queen/drone slots
    glyph(d, L['queen'][2] + 10, L['queen'][3] + 10, GL['crown'], {'#': (120, 120, 120)})
    glyph(d, L['drone'][2] + 6, L['drone'][3] + 6, GL['drone'], {'#': (120, 120, 120)})
    # small honeycomb flourish in the title bar gap
    comb_pattern(d, 250 - 1, 3, 1, 1, C['bg'], C['bg'])
    return img


# ------------------------------------------------------------------ 2. widgets atlas (sprites the code blits over the background)
SPRITES = {}


def spr(name, x, y, w, h, note):
    SPRITES[name] = (x, y, w, h, note)


def widgets():
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    # gauge fills (8 x 48: drawn inside the 10 x 50 wells at +1,+1)
    def vgrad(x, y, w, h, stops):
        for j in range(h):
            t = j / (h - 1)
            for a in range(len(stops) - 1):
                if stops[a][0] <= t <= stops[a + 1][0]:
                    u = (t - stops[a][0]) / (stops[a + 1][0] - stops[a][0] or 1)
                    c = tuple(int(stops[a][1][i] + (stops[a + 1][1][i] - stops[a][1][i]) * u) for i in range(3)); break
            for i in range(w):
                k = 1.15 if i == 0 else (0.8 if i == w - 1 else 1)
                px(d, x + i, y + j, tuple(min(255, int(v * k)) for v in c))
    vgrad(0, 0, 8, 48, [(0, (255, 90, 60)), (0.5, (240, 200, 80)), (1, (90, 160, 255))]); spr('fill_temp', 0, 0, 8, 48, 'Temperature fill (top = Hellish red, bottom = Icy blue). Draw the bottom N px.')
    vgrad(10, 0, 8, 48, [(0, (60, 110, 220)), (1, (200, 170, 110))]); spr('fill_hum', 10, 0, 8, 48, 'Humidity fill (top = Damp blue, bottom = Arid tan).')
    vgrad(20, 0, 8, 48, [(0, (230, 120, 255)), (1, (90, 50, 150))]); spr('fill_grav', 20, 0, 8, 48, 'Gravity fill (violet).')
    vgrad(30, 0, 4, 64, [(0, (90, 220, 90)), (0.6, (240, 200, 60)), (1, (220, 60, 40))]); spr('fill_life', 30, 0, 4, 64, 'Lifespan fill (full = green at the top of the bar; the code draws the remaining part from the bottom).')
    vgrad(36, 0, 4, 64, [(0, C['honey_l']), (1, C['honey_d'])]); spr('fill_cycle', 36, 0, 4, 64, 'Work cycle fill (honey).')
    vgrad(42, 0, 6, 60, [(0, (255, 210, 80)), (1, (200, 40, 30))]); spr('fill_fe', 42, 0, 6, 60, 'FE fill (amber to red).')
    # honey fluid (static frame; code may tint/scroll)
    for j in range(60):
        for i in range(12):
            n = (math.sin(i * 1.3 + j * .7) + math.sin(j * .31)) * 12
            c = (min(255, int(C['honey'][0] + n)), min(255, int(C['honey'][1] + n * .8)), int(C['honey'][2] + n * .3))
            if (i + j * 3) % 11 == 0: c = C['honey_l']
            px(d, 50 + i, j, c)
    spr('fill_honey', 50, 0, 12, 60, 'Honey fluid (use the fluid\'s own still texture in code if preferred).')
    # tolerance marker (3 x 1 tick, and a band end cap)
    rect(d, 64, 0, 3, 1, (255, 255, 255)); rect(d, 64, 2, 3, 1, (60, 230, 120)); spr('tol_tick', 64, 0, 3, 1, 'Tolerance band edge tick (white).'); spr('tol_band', 64, 2, 3, 1, 'Tolerance band body (green), repeat vertically left of a gauge (x-3).')
    rect(d, 68, 0, 10, 1, (255, 255, 255)); rect(d, 68, 1, 10, 1, (30, 30, 30)); spr('needle', 68, 0, 10, 2, 'Current-value needle line across a gauge.')
    # module lamps 9 x 8: off / on for each
    for i, (m, col) in enumerate(MODULES):
        x = 80 + i * 20
        rect(d, x, 0, 9, 8, (60, 58, 52)); rect(d, x + 1, 1, 7, 6, tuple(int(v * .35) for v in hexc(col)))
        rect(d, x + 10, 0, 9, 8, (60, 58, 52)); rect(d, x + 11, 1, 7, 6, hexc(col)); px(d, x + 12, 2, (255, 255, 255))
        spr(f'lamp_{m}_off', x, 0, 9, 8, f'{m} module lamp, off'); spr(f'lamp_{m}_on', x + 10, 0, 9, 8, f'{m} module lamp, on')
    # status icons 10 x 10
    for i, (k, name, col, _) in enumerate(STATUS):
        x = (i % 13) * 12; y = 68
        status_icon(d, x, y, hexc(col), k); spr(f'status_{k}', x, y, 10, 10, f'Status: {name}')
    # buttons 12 x 12: normal / hover / pressed, then glyphs
    for r, state in enumerate(('normal', 'hover', 'on')):
        y = 82 + r * 14
        for i, g in enumerate(('analyze', 'eject', 'void', 'sort')):
            x = i * 14
            fill = {'normal': C['bg'], 'hover': (214, 214, 234), 'on': (240, 200, 110)}[state]
            bevel(d, x, y, 12, 12, fill, raised=state != 'on')
            glyph(d, x + 2, y + 2, GL[g], {'#': (50, 50, 50)})
            spr(f'btn_{g}_{state}', x, y, 12, 12, f'{g} button, {state}')
    # sealed housing overlay 18 x 18 and sealed plate for locked tanks
    x, y = 60, 82
    for j in range(18):
        for i in range(18):
            if (i + j) % 4 < 2 and 1 <= i <= 16 and 1 <= j <= 16: px(d, x + i, y + j, (90, 86, 80, 170))
    d.rectangle([x + 1, y + 1, x + 16, y + 16], outline=(70, 66, 60, 220)); glyph(d, x + 6, y + 6, ['.##.', '#..#', '####', '####', '####'], {'#': (60, 56, 50)})
    spr('sealed_slot', x, y, 18, 18, 'Sealed frame housing (draw over locked frame slots).')
    x = 80
    for j in range(62):
        for i in range(14):
            c = (128, 124, 116) if (i + j // 2) % 6 else (105, 101, 94)
            if j in (0, 61) or i in (0, 13): c = (70, 66, 60)
            px(d, x + i, 82 + j, c)
    for j in (6, 54):
        for i in (3, 10): px(d, x + i, 82 + j, (200, 196, 186))
    spr('sealed_tank', x, 82, 14, 62, 'Sealed plate over a tank or bar whose part is not built yet (crop to the well size).')
    # ghost frame icon
    glyph(d, 100, 82, GL['frame'], {'#': (120, 120, 120)}); spr('ghost_frame', 100, 82, 7, 7, 'Ghost frame icon for empty unlocked frame slots.')
    # small icons for the power panel
    glyph(d, 110, 82, GL['bolt'], {'#': (230, 190, 40)}); spr('ic_bolt', 110, 82, 5, 6, 'Bolt')
    glyph(d, 118, 82, GL['drop'], {'#': C['honey_d'], 'o': C['honey']}); spr('ic_honey', 118, 82, 6, 6, 'Honey drop')
    glyph(d, 126, 82, GL['drop'], {'#': (60, 110, 200), 'o': (140, 200, 255)}); spr('ic_fluid', 126, 82, 6, 6, 'Fluid drop')
    # tier badges 64 x 12
    for i, (t, name, nf, col) in enumerate(TIERS):
        x, y = (i % 3) * 66, 148 + (i // 3) * 14
        cc = hexc(col)
        bevel(d, x, y, 64, 12, cc)
        for j in range(1, 11): px(d, x + 2 + (j % 2), y + j, tuple(min(255, v + 40) for v in cc))
        rect(d, x + 3, y + 2, 9, 8, (30, 30, 30)); glyph(d, x + 5, y + 3, {1: ['.#.', '##.', '.#.', '.#.', '.#.', '###'], 2: ['##.', '..#', '.#.', '#..', '#..', '###'],
                                                                            3: ['##.', '..#', '.#.', '..#', '..#', '##.'], 4: ['#.#', '#.#', '###', '..#', '..#', '..#'],
                                                                            5: ['###', '#..', '##.', '..#', '..#', '##.'], 6: ['.##', '#..', '##.', '#.#', '#.#', '.#.'],
                                                                            7: ['###', '..#', '.#.', '.#.', '#..', '#..']}[t], {'#': (255, 255, 255)})
        spr(f'badge_t{t}', x, y, 64, 12, f'Tier {t} badge ({name}); code writes the short name at +15,+2 in white with shadow.')
    # ledger tabs (Forestry-style): 24 x 24 collapsed, plus a 9-slice for expanded
    for i, (nm, col) in enumerate((('info', '#5f8fb5'), ('climate', '#e2553a'), ('energy', '#d9b23a'), ('automation', '#7d8f5a'), ('structure', '#9a5fd0'))):
        x, y = i * 26, 194
        rect(d, x, y, 24, 24, hexc(col)); d.rectangle([x, y, x + 23, y + 23], outline=(0, 0, 0))
        d.line([(x + 1, y + 1), (x + 22, y + 1)], fill=tuple(min(255, v + 60) for v in hexc(col))); d.line([(x + 1, y + 1), (x + 1, y + 22)], fill=tuple(min(255, v + 60) for v in hexc(col)))
        sym = {'info': ['.##.', '....', '.##.', '.##.', '.##.', '####'], 'climate': GL['temp'][:9], 'energy': GL['bolt'], 'automation': ['#.#.#', '.###.', '##.##', '.###.', '#.#.#'],
               'structure': ['###.###', '#.....#', '#.###.#', '#.#.#.#', '#.###.#', '#.....#', '###.###']}[nm]
        glyph(d, x + 12 - len(sym[0]) // 2, y + 12 - len(sym) // 2, sym, {'#': (255, 255, 255), 'o': (255, 255, 255), 'r': (255, 255, 255)})
        spr(f'tab_{nm}', x, y, 24, 24, f'Ledger tab: {nm} (collapsed). Expanded ledgers use the tab colour as a 9-slice: corners 4 px.')
    rs = list(SPRITES.items())
    for i in range(len(rs)):
        for j in range(i + 1, len(rs)):
            (a, (x1, y1, w1, h1, _)), (b, (x2, y2, w2, h2, _)) = rs[i], rs[j]
            assert x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1, ('sprites overlap', a, b)
    return img


# ------------------------------------------------------------------ 3. mockups (screen state per tier)
def bee_icon(d, x, y, body, stripe, wing=(220, 235, 255)):
    rows = ['....ww..', '...wwww.', '.bbsbsb.', 'bbbsbsbb', 'bbbsbsbb', '.bbsbsb.', '..k..k..', '........']
    glyph(d, x, y, rows, {'w': wing, 'b': body, 's': stripe, 'k': (40, 30, 20)})
    for (i, j) in ((1, 3),): px(d, x + i, y + j, (20, 20, 20))


def item_icon(d, x, y, kind, col):
    col = hexc(col) if isinstance(col, str) else col
    if kind == 'comb':
        for j in range(12):
            for i in range(14):
                if (i - 7) ** 2 / 49 + (j - 6) ** 2 / 36 <= 1:
                    c = col if (i + (j // 3) * 2) % 4 else tuple(int(v * .7) for v in col)
                    px(d, x + 1 + i, y + 2 + j, c)
    elif kind == 'frame':
        d.rectangle([x + 2, y + 1, x + 13, y + 14], outline=(110, 80, 40)); d.rectangle([x + 3, y + 2, x + 12, y + 13], outline=col)
        for j in range(3, 13, 2):
            for i in range(4, 12, 2): px(d, x + i, y + j, C['comb'])
    elif kind == 'drop':
        glyph(d, x + 4, y + 3, ['...#...', '..###..', '.#####.', '#######', '#######', '#######', '.#####.', '..###..'], {'#': col})


def mockup(tier, scale=3):
    bg = background(); wd = widgets(); img = bg.copy(); d = ImageDraw.Draw(img)
    t, tname, nframes, tcol = TIERS[tier - 1]
    def blit(name, x, y, w=None, h=None, crop_bottom=None):
        sx, sy, sw, sh, _ = SPRITES[name]
        w = w or sw; h = h or sh
        part = wd.crop((sx, sy + (sh - h if crop_bottom else 0), sx + w, sy + sh if crop_bottom else sy + h))
        img.alpha_composite(part, (x, y))
    blit(f'badge_t{tier}', L['tier_badge'][2], L['tier_badge'][3])
    status = {1: 'working', 3: 'working', 7: 'working', 2: 'too_hot', 4: 'gravity', 5: 'full', 6: 'no_power'}[tier]
    blit(f'status_{status}', L['status_lamp'][2], L['status_lamp'][3])
    # queen + drone
    bee_icon(d, L['queen'][2] + 9, L['queen'][3] + 9, (240, 200, 70), (60, 40, 20))
    if tier in (2, 5): bee_icon(d, L['drone'][2] + 5, L['drone'][3] + 5, (200, 200, 220), (80, 80, 120))
    # life / cycle bars
    for nm, fill, frac in (('life_bar', 'fill_life', .62), ('cycle_bar', 'fill_cycle', .35 + tier * .07)):
        _, _, x, y, w, h, _, _ = L[nm]; hh = int((h - 2) * min(1, frac))
        blit(fill, x + 1, y + h - 1 - hh, 4, hh, crop_bottom=True)
    # gauges + tolerance bands + needle
    vals = {'g_temp': .55, 'g_hum': .45, 'g_grav': (.3 if tier in (1, 2, 3) else .2)}
    tol = {'g_temp': (.40, .70), 'g_hum': (.30, .65), 'g_grav': (.25, .55) if tier != 4 else (.35, .65)}
    for nm, fill in (('g_temp', 'fill_temp'), ('g_hum', 'fill_hum'), ('g_grav', 'fill_grav')):
        _, _, x, y, w, h, _, _ = L[nm]; hh = int((h - 2) * vals[nm])
        blit(fill, x + 1, y + h - 1 - hh, 8, hh, crop_bottom=True)
        a, b = tol[nm]; ya, yb = y + h - 1 - int((h - 2) * b), y + h - 1 - int((h - 2) * a)
        for yy in range(ya, yb + 1): blit('tol_band', x - 4, yy)
        blit('tol_tick', x - 4, ya); blit('tol_tick', x - 4, yb)
        blit('needle', x, y + h - 1 - hh - 1)
    # module lamps
    for i, (m, col) in enumerate(MODULES):
        nm = ('m_heater', 'm_fan', 'm_humid', 'm_dryer')[i]
        if tier >= 2: blit(f'lamp_{m}_{"on" if (tier == 2 and m == "fan") or (tier >= 5 and m in ("heater", "humid")) else "off"}', L[nm][2], L[nm][3])
    # output products
    combs = ['#e9a82c', '#c9c9d9', '#9a5fd0', '#3fd0c8', '#e2553a']
    n_out = {1: 2, 2: 3, 3: 5, 4: 4, 5: 9, 6: 6, 7: 8}[tier]
    for i in range(n_out):
        x = L['out_grid'][2] + (i % 3) * 18 + 1; y = L['out_grid'][3] + (i // 3) * 18 + 1
        item_icon(d, x, y, 'comb', combs[(i + tier) % len(combs)])
    # buttons
    for nm, g in (('eject', 'eject'), ('void', 'void'), ('sort', 'sort')):
        if tier < L[nm][6]: continue
        blit(f'btn_{g}_{"on" if (g == "eject" and tier >= 3) else "normal"}', L[nm][2], L[nm][3])
    blit('btn_analyze_normal', L['analyze'][2], L['analyze'][3])
    # power panel: sealed plates below tier
    for nm, fill, frac in (('fe', 'fill_fe', .45 if tier != 6 else 0), ('honey_tank', 'fill_honey', .7), ('fluid_tank', 'fill_honey', .5)):
        _, _, x, y, w, h, t0, _ = L[nm]
        if tier < t0:
            sx, sy, sw, sh, _ = SPRITES['sealed_tank']; img.alpha_composite(wd.crop((sx, sy, sx + w, sy + h)), (x, y)); continue
        hh = int((h - 2) * frac)
        if nm == 'fluid_tank':
            part = Image.new('RGBA', (w - 2, hh), (150, 220, 255, 255))
            pd = ImageDraw.Draw(part)
            for j in range(hh):
                for i in range(w - 2):
                    if (i * 3 + j) % 9 == 0: pd.point((i, j), fill=(230, 250, 255))
            img.alpha_composite(part, (x + 1, y + h - 1 - hh))
        elif hh: blit(fill, x + 1, y + h - 1 - hh, w - 2, hh, crop_bottom=True)
    for nm, sp in (('ic_fe', 'ic_bolt'), ('ic_honey', 'ic_honey'), ('ic_fluid', 'ic_fluid')):
        if tier >= L[nm][6]: blit(sp, L[nm][2], L[nm][3])
    # frames
    _, _, gx, gy, _, _, _, _ = L['frame_grid']
    fcols = ['#e9a82c', '#5f8fb5', '#9a5fd0', '#3fd0c8', '#d9b23a']
    for i in range(27):
        x, y = gx + (i % 9) * 18, gy + (i // 9) * 18
        if i >= nframes: blit('sealed_slot', x, y)
        elif i < max(1, int(nframes * .7)): item_icon(d, x + 1, y + 1, 'frame', fcols[i % 5])
        else: blit('ghost_frame', x + 6, y + 6)
    # player inventory sample items
    for i in (0, 4, 11, 20):
        x, y = L['inv'][2] + (i % 9) * 18 + 1, L['inv'][3] + (i // 9) * 18 + 1
        item_icon(d, x, y, 'comb' if i % 2 else 'frame', combs[i % 5])
    for i in (0, 1, 2):
        x, y = L['hotbar'][2] + i * 18 + 1, L['hotbar'][3] + 1
        item_icon(d, x, y, 'drop', '#e9a82c')
    # scale up and draw text with a real font
    big = img.crop((0, 0, W, H)).resize((W * scale, H * scale), Image.NEAREST); bd = ImageDraw.Draw(big)
    f = F(8 * scale - 6)
    bd.text((L['title'][2] * scale, L['title'][3] * scale - 3), 'Alveary Controller', font=f, fill=C['text'])
    short = {1: 'Rustic', 2: 'Controlled', 3: 'Industrial', 4: 'Aeronautic', 5: 'ATM Star', 6: 'Nebula', 7: 'Quantum'}[tier]
    bd.text(((L['tier_badge'][2] + 15) * scale, (L['tier_badge'][3] + 2) * scale - 3), short, font=F(7 * scale - 5, True), fill=(255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0))
    st = [s for s in STATUS if s[0] == status][0][1]
    bd.text((L['status_text'][2] * scale, L['status_text'][3] * scale - 3), st, font=F(7 * scale - 5), fill=C['text'])
    bd.text((L['inv_label'][2] * scale, L['inv_label'][3] * scale - 3), 'Inventory', font=f, fill=C['text'])
    mods = {1: ('x1.10', 'x1.00', 'x1.00', 'x1.00'), 2: ('x1.25', 'x0.90', 'x1.10', 'x1.00'), 3: ('x1.60', 'x0.80', 'x1.20', 'x1.20'),
            4: ('x1.70', 'x0.75', 'x1.30', 'x1.50'), 5: ('x2.10', 'x0.70', 'x1.60', 'x1.50'), 6: ('x2.40', 'x0.60', 'x2.20', 'x1.80'), 7: ('x3.00', 'x0.50', 'x2.80', 'x2.00')}[tier]
    for i, v in enumerate(mods):
        bd.text(((L['ic_prod'][2] + 13) * scale, (L['ic_prod'][3] + i * 13) * scale - 4), v, font=F(7 * scale - 4), fill=C['text'])
    return big


# ------------------------------------------------------------------ 4. annotated layout sheet
def layout_sheet(bg):
    S = 4; pad = 40
    big = bg.resize((256 * S, 256 * S), Image.NEAREST)
    Wt, Ht = 256 * S + 2 * pad + 760, 256 * S + 2 * pad + 60
    sh = Image.new('RGB', (Wt, Ht), (246, 245, 242)); d = ImageDraw.Draw(sh)
    for yy in range(0, 256 * S, 16):
        for xx in range(0, 256 * S, 16):
            d.rectangle([pad + xx, pad + 40 + yy, pad + xx + 15, pad + 40 + yy + 15], fill=(236, 236, 236) if (xx // 16 + yy // 16) % 2 else (250, 250, 250))
    sh.paste(big, (pad, pad + 40), big)
    d.text((pad, 12), 'Alveary Controller - screen layout (gui/alveary_controller.png, 256 x 256, screen 256 x 250)', font=F(22, True), fill=(34, 32, 40))
    acc = (124, 92, 230)
    items = [e for e in LAYOUT if e[1] not in ('window',)]
    for i, (n, k, x, y, w, h, t, note) in enumerate(items):
        X, Y = pad + x * S, pad + 40 + y * S
        col = acc if k != 'panel' else (230, 120, 40)
        d.rectangle([X, Y, X + w * S - 1, Y + h * S - 1], outline=col, width=1 if k != 'panel' else 2)
        lab = str(i + 1); tw = d.textlength(lab, font=F(11, True))
        if k != 'panel':
            d.rectangle([X, Y, X + tw + 4, Y + 13], fill=col); d.text((X + 2, Y), lab, font=F(11, True), fill=(255, 255, 255))
        else:
            d.rectangle([X + w * S - tw - 6, Y + h * S - 15, X + w * S - 1, Y + h * S - 1], fill=col); d.text((X + w * S - tw - 4, Y + h * S - 15), lab, font=F(11, True), fill=(255, 255, 255))
    lx = pad + 256 * S + 30; ly = pad + 40
    d.text((lx, ly - 30), '#   element          x    y    w    h   tier', font=FM(13), fill=(34, 32, 40))
    for i, (n, k, x, y, w, h, t, note) in enumerate(items):
        d.text((lx, ly + i * 22), f'{i + 1:<3} {n:<15} {x:>4} {y:>4} {w:>4} {h:>4}   T{t}+', font=FM(13), fill=(34, 32, 40) if k != 'panel' else (200, 100, 30))
    d.text((pad, Ht - 40), 'Orange = panels, purple = elements. Numbers match the element table in the spec. Coordinates are in GUI pixels from the screen\'s top-left.', font=F(13), fill=(110, 108, 118))
    return sh


def widgets_sheet(wd):
    S = 4; pad = 40
    big = wd.resize((256 * S, 256 * S), Image.NEAREST)
    sh = Image.new('RGB', (256 * S + 2 * pad + 640, 256 * S + 2 * pad + 50), (246, 245, 242)); d = ImageDraw.Draw(sh)
    for yy in range(0, 256 * S, 16):
        for xx in range(0, 256 * S, 16):
            d.rectangle([pad + xx, pad + 40 + yy, pad + xx + 15, pad + 40 + yy + 15], fill=(60, 60, 66) if (xx // 16 + yy // 16) % 2 else (72, 72, 78))
    sh.paste(big, (pad, pad + 40), big)
    d.text((pad, 12), 'Alveary Controller - widget atlas (gui/alveary_controller_widgets.png, 256 x 256)', font=F(22, True), fill=(34, 32, 40))
    lx = pad + 256 * S + 30; ly = pad + 40
    groups = {}
    for n, (x, y, w, h, note) in SPRITES.items(): groups.setdefault(n.split('_')[0], []).append((n, x, y, w, h))
    for g, lst in groups.items():
        d.text((lx, ly), g, font=F(13, True), fill=(124, 92, 230)); ly += 18
        txt = ', '.join(f'{n} ({x},{y} {w}x{h})' for n, x, y, w, h in lst)
        for ln in [txt[i:i + 86] for i in range(0, len(txt), 86)]:
            d.text((lx + 10, ly), ln, font=FM(11), fill=(34, 32, 40)); ly += 15
        ly += 6
    return sh


# ------------------------------------------------------------------ 5. spec markdown, generated from the same data
def spec():
    out = []
    w = out.append
    w('# Alveary Controller: screen layout and textures\n')
    w('One controller screen serves all seven alveary tiers (Rustic to Quantum Queen Chamber). The screen is the same size at every tier; '
      'parts the structure does not have yet are shown sealed, so players can see what the next tier adds. Classic 1.12 bee-mod look: '
      'vanilla grey window and slots, recessed panels with a honey strip, Forestry-style ledger tabs on the right.\n')
    w('Generated by `controller_gui.py`: every number below comes from the same data that drew the textures.\n')
    w('## Files\n')
    w('| File | Size | Use |\n| --- | --- | --- |')
    w('| `textures/gui/alveary_controller.png` | 256 x 256 (screen 256 x 250) | Static background: window, panels, slots, wells, baked icons. |')
    w('| `textures/gui/alveary_controller_widgets.png` | 256 x 256 | Sprites the screen blits on top: fills, lamps, status icons, buttons, sealed overlays, tier badges, ledger tabs. |')
    w('| `alveary_controller_t1/t3/t7_mockup.png` | 768 x 750 | How the screen looks at tiers 1, 3 and 7 (3x scale). Not shipped. |')
    w('| `alveary_controller_layout.png`, `alveary_controller_widgets_sheet.png` | - | Annotated maps for the coder. Not shipped. |\n')
    w('## Screen\n')
    w(f'- Size {W} x {H} GUI px; `imageWidth = {W}`, `imageHeight = {H}`. Centre it like any container screen.')
    w('- Title at (8, 5), colour `0x404040`, no shadow. Inventory label at (47, 158).')
    w('- Fits the default GUI scale on 1080p; at GUI scale 4 on 1080p it is too tall, as with other large mod screens.\n')
    w('## Elements\n')
    w('Coordinates are in GUI px from the screen\'s top-left. "From" is the first tier the element works at; below that it is sealed or hidden.\n')
    w('| # | Element | Kind | x | y | w | h | From | Behaviour |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |')
    for i, (n, k, x, y, ww, h, t, note) in enumerate([e for e in LAYOUT if e[1] != 'window']):
        w(f'| {i + 1} | `{n}` | {k} | {x} | {y} | {ww} | {h} | T{t} | {note} |')
    w('\n## Menu slots (for `AlvearyControllerMenu`)\n')
    w('| Index | Slot | Position (item top-left) | Rule |\n| --- | --- | --- | --- |')
    w(f'| 0 | Queen / Princess | ({L["queen"][2] + 5}, {L["queen"][3] + 5}) | Queens and princesses only; stack 1. |')
    w(f'| 1 | Drone | ({L["drone"][2] + 1}, {L["drone"][3] + 1}) | Drones only; stacks to 64. |')
    w(f'| 2-10 | Products 3 x 3 | from ({L["out_grid"][2] + 1}, {L["out_grid"][3] + 1}), step 18 | Output only (no insert). |')
    w(f'| 11-37 | Frames 9 x 3 | from ({L["frame_grid"][2] + 1}, {L["frame_grid"][3] + 1}), step 18 | Frames only; stack 1; slot i usable when i-11 < unlocked count. |')
    w(f'| 38-64 | Player inventory | from ({L["inv"][2] + 1}, {L["inv"][3] + 1}) | Vanilla. |')
    w(f'| 65-73 | Hotbar | from ({L["hotbar"][2] + 1}, {L["hotbar"][3] + 1}) | Vanilla. |\n')
    w('Shift-click: queen/princess -> slot 0, drone -> 1, frame -> first free unlocked frame slot, products -> player inventory.\n')
    w('## Synced data (`ContainerData`)\n')
    fields = ['tier (1-7)', 'status code (index in Status codes)', 'unlocked frame count', 'module bitmask (1 heater, 2 fan, 4 humidifier, 8 dryer)',
              'queen life', 'queen life max', 'cycle progress', 'cycle max', 'temperature (0-48 px)', 'humidity (0-48 px)', 'gravity (0-48 px)',
              'temp tolerance min', 'temp tolerance max', 'humidity tolerance min', 'humidity tolerance max', 'gravity tolerance min', 'gravity tolerance max',
              'FE stored / 100', 'FE max / 100', 'honey mB / 10', 'catalyst mB / 10', 'toggles bitmask (1 eject, 2 void)']
    w('| Index | Value |\n| --- | --- |')
    for i, f in enumerate(fields): w(f'| {i} | {f} |')
    w('\nValues are pre-scaled to fit a short. Gauge values are already in pixels so the screen does no maths.\n')
    w('## Tiers\n')
    w('| Tier | Name | Frame slots | Climate modules | Power | Honey tank | Catalyst tank | Extra on screen |\n| --- | --- | --- | --- | --- | --- | --- | --- |')
    extra = {1: 'Basic. Lamps hidden; power panel sealed.', 2: 'Module lamps appear (heater, fan, humidifier, dryer).',
             3: 'FE bar and honey tank unseal; Eject button works (Output Hatch); Frame Loader shows an "auto" ledger line.',
             4: 'Gravity tolerance shifts one step with the rotor (shown on the gauge band).', 5: 'Stabilizers: climate lamps glow gold while held steady.',
             6: 'Catalyst tank unseals (Fluid Port); Lens/Focus line in the Structure ledger.', 7: 'Quantum: all 27 frame housings; Structure ledger shows coil charge.'}
    for t, name, nf, col in TIERS:
        w(f'| T{t} | {name} | {nf} | {"yes" if t >= 2 else "-"} | {"yes" if t >= 3 else "-"} | {"yes" if t >= 3 else "-"} | {"yes" if t >= 6 else "-"} | {extra[t]} |')
    w('\nThe Cosmic Alveary catalog model uses the T5 layout, so it shows the T5 screen.\n')
    w('## Gauges\n')
    w('- Each gauge well is 10 x 50; the fill is drawn from `fill_*` sprites at (+1, +1), bottom-up, height = synced value (0-48).')
    w('- The tolerance band is drawn 4 px left of the well with `tol_band` (repeat per px) and `tol_tick` at both ends. Green band = the queen can work.')
    w('- `needle` (10 x 2) is drawn across the well at the current value so the value reads even when it is inside the band.')
    w('- Temperature steps (bottom to top): Icy, Cold, Cool, Normal, Warm, Hot, Hellish (7 px each). Humidity: Arid, Normal, Damp. Gravity: 0.5 g at the bottom, 1.3 g at the top, Overworld 1.0 g at 30 px.')
    w('- Tooltips: "Temperature: Warm (queen tolerates Normal-Hot)", same pattern for the others.\n')
    w('## Status codes\n')
    w('| Code | Icon sprite | Word | Meaning / fix |\n| --- | --- | --- | --- |')
    for i, (k, name, col, note) in enumerate(STATUS): w(f'| {i} | `status_{k}` ({col}) | {name} | {note} |')
    w('\nPriority when several apply: Broken > No Power > No Queen > climate > No Sky > Full > Rain > Resting > Working.\n')
    w('## Buttons\n')
    w('| Button | Sprite | Action | Packet |\n| --- | --- | --- | --- |')
    w('| Analyze | `btn_analyze_*` | Opens the genome page for the queen (read-only). | none (client view of synced genome) |')
    w('| Eject (T3+) | `btn_eject_*` | Toggles auto-eject to the Output Hatch. | `ToggleEject` |')
    w('| Void | `btn_void_*` | Toggles destroying products when full. Asks for confirmation the first time. | `ToggleVoid` |')
    w('| Sort | `btn_sort_*` | Compacts the product buffer. | `SortOutput` |\n')
    w('States: normal, hover, on (pressed/active). Draw `on` while a toggle is enabled.\n')
    w('## Ledger tabs (right side, outside the window)\n')
    w('Forestry-style tabs stacked from y = 4, 2 px apart, at x = imageWidth - 1. Click to expand to 120 px wide; one open at a time.\n')
    w('| Tab | Sprite | Expanded content |\n| --- | --- | --- |')
    w('| Info | `tab_info` | Queen species, generation, work speed, products per cycle. |')
    w('| Climate | `tab_climate` | Biome base climate, module contributions, final values. |')
    w('| Energy (T3+) | `tab_energy` | FE/t use, buffer, ports connected. |')
    w('| Automation (T3+) | `tab_automation` | Hatch sides and redstone mode (ignore / high / low / pulse). |')
    w('| Structure | `tab_structure` | Tier, part counts (e.g. 6/6 frame housings), missing parts list, "Show ghost" button. |\n')
    w('## Widget atlas\n')
    w('| Sprite | u | v | w | h | Use |\n| --- | --- | --- | --- | --- | --- |')
    for n, (x, y, ww, h, note) in SPRITES.items(): w(f'| `{n}` | {x} | {y} | {ww} | {h} | {note} |')
    w('\n## Texture style rules\n')
    w('- Window: vanilla container bevel (1 px black outline, 2 px white top-left, 2 px #555555 bottom-right, fill #C6C6C6).')
    w('- Slots: vanilla 18 x 18 (#373737 top-left, white bottom-right, #8B8B8B inside). The queen slot is 26 x 26 with an amber inner ring.')
    w('- Panels: recessed #B6B4AC with a 2 px honey strip (#B07016 over #E8A82C) along the top, so each section reads as one unit.')
    w('- Wells (gauges, bars, tanks): near-black #24221F with the slot bevel, so fills pop.')
    w('- No baked text in any texture; all words come from lang keys, so the screen translates.')
    w('- Palette: honey #E8A82C / #B07016 / #FFD678, wax #F0D696, grey ramp #FFFFFF #C6C6C6 #8B8B8B #555555 #373737.\n')
    w('## Lang keys\n')
    w('`screen.aeroapiary.alveary_controller`, `.inventory`, `.status.<code>`, `.status.<code>.desc`, `.gauge.temperature|humidity|gravity`, '
      '`.tier.<1-7>`, `.button.analyze|eject|void|sort`, `.ledger.info|climate|energy|automation|structure`, `.modifier.productivity|lifespan|mutation|territory`.\n')
    return '\n'.join(out)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    bg = background(); wd = widgets()
    bg.save(f'{OUT}/alveary_controller.png'); wd.save(f'{OUT}/alveary_controller_widgets.png')
    for t in (1, 3, 7): mockup(t).save(f'{OUT}/alveary_controller_t{t}_mockup.png')
    layout_sheet(bg).save(f'{OUT}/alveary_controller_layout.png')
    widgets_sheet(wd).save(f'{OUT}/alveary_controller_widgets_sheet.png')
    open(f'{OUT}/alveary_controller_spec.md', 'w').write(spec())
    print('ok', len(LAYOUT), 'elements', len(SPRITES), 'sprites')
