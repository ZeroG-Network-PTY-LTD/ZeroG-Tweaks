"""GUIs for the Geno Station and Genetic Splicer: layout data -> background textures, shared widget atlas, mockups, layout maps, spec.
Same look as the Alveary Controller screen (vanilla bevel + honey strips). Usage: python3 gene_gui.py <out_dir>"""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
FP = '/usr/share/fonts/truetype/dejavu/'
F = lambda s, b=False: ImageFont.truetype(FP + ('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf'), s)
FM = lambda s: ImageFont.truetype(FP + 'DejaVuSansMono.ttf', s)
C = dict(bg=(198, 198, 198), hi=(255, 255, 255), sh=(85, 85, 85), edge=(0, 0, 0), slot=(139, 139, 139), slot_d=(55, 55, 55),
         honey=(232, 168, 44), honey_d=(176, 112, 22), honey_l=(255, 214, 120), well=(36, 34, 31), text=(64, 64, 64),
         cyan=(95, 243, 255), amber=(255, 179, 71), violet=(156, 122, 224), green=(124, 240, 138), glass=(20, 34, 40))

# kind: slot, slot_out (big 26 x 26 output), panel, well, bar, tank, button, text, arrow, list, scroll, display
GENO = dict(id='geno_station', title='Geno Station', W=196, H=226, layout=[
    ('p_in', 'panel', 6, 15, 26, 72, 'Inputs panel.'),
    ('specimen', 'slot', 10, 19, 18, 18, 'Slot 0: bee to read (queen, princess or drone). Ghost: bee.'),
    ('vial', 'slot', 10, 42, 18, 18, 'Slot 1: blank Serum Vial (Sample mode only). Ghost: vial.'),
    ('reagent', 'slot', 10, 65, 18, 18, 'Slot 2: Honey Drop or honey bottle, 1 per job. Ghost: drop.'),
    ('p_genome', 'panel', 36, 15, 124, 88, 'Genome panel.'),
    ('genes', 'list', 39, 19, 112, 80, 'Gene list, 8 rows of 10 px: gene name (code text, 6 px from the left), active allele bar and inactive allele bar on the right. Click a row to select it for sampling.'),
    ('scroll', 'scroll', 152, 19, 6, 80, 'Scrollbar for the gene list (about 12 genes).'),
    ('p_out', 'panel', 164, 15, 26, 88, 'Outputs panel.'),
    ('specimen_out', 'slot', 168, 19, 18, 18, 'Slot 3: the bee after reading (genome now known).'),
    ('arrow', 'arrow', 172, 41, 10, 12, 'Small down arrow, fills as the job runs.'),
    ('serum_out', 'slot', 168, 56, 18, 18, 'Slot 4: Trait Serum with the sampled gene.'),
    ('energy', 'bar', 170, 78, 14, 22, 'FE buffer (10,000 FE), fills from the bottom. Tooltip shows FE and FE/t.'),
    ('progress', 'bar', 36, 106, 124, 6, 'Job progress, fills left to right in honey.'),
    ('b_analyse', 'button', 36, 115, 60, 14, 'Analyse mode: read the genome only (uses reagent).'),
    ('b_sample', 'button', 100, 115, 60, 14, 'Sample mode: copy the selected gene into a Serum Vial. Disabled until a gene is selected.'),
    ('inv_label', 'text', 17, 133, 60, 9, 'Inventory label.'),
    ('inv', 'grid', 17, 144, 162, 54, 'Player inventory (menu slots 5-31).'),
    ('hotbar', 'grid', 17, 202, 162, 18, 'Hotbar (menu slots 32-40).'),
])
SPLICER = dict(id='genetic_splicer', title='Genetic Splicer', W=196, H=212, layout=[
    ('p_in', 'panel', 6, 15, 26, 76, 'Inputs panel.'),
    ('bee', 'slot', 10, 19, 18, 18, 'Slot 0: queen or princess to splice. Ghost: crown.'),
    ('serum', 'slot', 10, 43, 18, 18, 'Slot 1: Trait Serum. Ghost: vial.'),
    ('catalyst', 'slot', 10, 67, 18, 18, 'Slot 2: Royal Jelly (75%) or Cosmic Jelly (100%). Ghost: jelly.'),
    ('a_in', 'arrow_r', 33, 49, 8, 7, 'Feed arrow into the chamber (lit while working).'),
    ('chamber', 'display', 42, 15, 92, 76, 'Chamber window: the helix animation (8 frames, 24 x 56) centred; serum colour tints the strands; success chance top-right in code text.'),
    ('jelly', 'tank', 138, 15, 14, 76, 'Royal Jelly fluid from the back conduit, 4,000 mB. Used instead of the catalyst slot when present (250 mB per attempt).'),
    ('a_out', 'arrow_r', 153, 49, 8, 7, 'Output arrow.'),
    ('p_out', 'panel', 162, 15, 28, 76, 'Outputs panel.'),
    ('bee_out', 'slot', 167, 25, 18, 18, 'Slot 3: spliced bee.'),
    ('vial_out', 'slot', 167, 55, 18, 18, 'Slot 4: empty Serum Vial.'),
    ('energy', 'bar', 170, 77, 12, 11, 'FE buffer (40,000 FE), small gauge. Tooltip shows FE and FE/t.'),
    ('progress', 'bar', 42, 94, 92, 6, 'Splice progress.'),
    ('preview', 'well', 6, 103, 184, 12, 'Preview line (code text): "Speed: Fast  ->  Forest Queen" or the reason it cannot start.'),
    ('inv_label', 'text', 17, 120, 60, 9, 'Inventory label.'),
    ('inv', 'grid', 17, 130, 162, 54, 'Player inventory (menu slots 5-31).'),
    ('hotbar', 'grid', 17, 188, 162, 18, 'Hotbar (menu slots 32-40).'),
])


def px(d, x, y, c): d.point((x, y), fill=c)


def rect(d, x, y, w, h, c): d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)


def slot(d, x, y, w=18, h=18):
    rect(d, x, y, w, h, C['slot'])
    d.line([(x, y), (x + w - 2, y)], fill=C['slot_d']); d.line([(x, y), (x, y + h - 2)], fill=C['slot_d'])
    d.line([(x + 1, y + h - 1), (x + w - 1, y + h - 1)], fill=C['hi']); d.line([(x + w - 1, y + 1), (x + w - 1, y + h - 1)], fill=C['hi'])


def well(d, x, y, w, h, inner=None):
    rect(d, x, y, w, h, inner or C['well'])
    d.line([(x, y), (x + w - 1, y)], fill=C['slot_d']); d.line([(x, y), (x, y + h - 1)], fill=C['slot_d'])
    d.line([(x + 1, y + h - 1), (x + w - 1, y + h - 1)], fill=C['hi']); d.line([(x + w - 1, y + 1), (x + w - 1, y + h - 1)], fill=C['hi'])


def panel(d, x, y, w, h):
    rect(d, x, y, w, h, (182, 180, 172))
    d.line([(x, y), (x + w - 2, y)], fill=C['sh']); d.line([(x, y), (x, y + h - 2)], fill=C['sh'])
    d.line([(x + 1, y + h - 1), (x + w - 1, y + h - 1)], fill=C['hi']); d.line([(x + w - 1, y + 1), (x + w - 1, y + h - 1)], fill=C['hi'])
    d.line([(x + 1, y + 1), (x + w - 2, y + 1)], fill=C['honey_d']); d.line([(x + 1, y + 2), (x + w - 2, y + 2)], fill=C['honey'])


def bevel(d, x, y, w, h, fill, raised=True):
    tl, br = (C['hi'], C['sh']) if raised else (C['slot_d'], C['hi'])
    rect(d, x, y, w, h, fill)
    d.line([(x, y), (x + w - 2, y)], fill=tl); d.line([(x, y), (x, y + h - 2)], fill=tl)
    d.line([(x + 1, y + h - 1), (x + w - 1, y + h - 1)], fill=br); d.line([(x + w - 1, y + 1), (x + w - 1, y + h - 1)], fill=br)


def window(d, W, H):
    rect(d, 1, 1, W - 2, H - 2, C['bg'])
    d.line([(2, 0), (W - 3, 0)], fill=C['edge']); d.line([(2, H - 1), (W - 3, H - 1)], fill=C['edge'])
    d.line([(0, 2), (0, H - 3)], fill=C['edge']); d.line([(W - 1, 2), (W - 1, H - 3)], fill=C['edge'])
    for (a, b) in ((1, 1), (W - 2, 1), (1, H - 2), (W - 2, H - 2)): px(d, a, b, C['edge'])
    for o in (1, 2):
        d.line([(2, o), (W - 3 - o, o)], fill=C['hi']); d.line([(o, 2), (o, H - 3 - o)], fill=C['hi'])
        d.line([(2 + o, H - 1 - o), (W - 3, H - 1 - o)], fill=C['sh']); d.line([(W - 1 - o, 2 + o), (W - 1 - o, H - 3)], fill=C['sh'])


def glyph(d, x, y, rows, cmap):
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch in cmap: px(d, x + i, y + j, cmap[ch])


GHOST = {'bee': ['.##.##.', '#..#..#', '.#####.', '#.###.#', '..###..', '...#...'],
         'crown': ['#..#..#', '#.###.#', '#######', '#######'],
         'vial': ['.###.', '..#..', '.#.#.', '.#.#.', '#...#', '#...#', '.###.'],
         'drop': ['..#..', '.###.', '#####', '#####', '.###.'],
         'jelly': ['.###.', '#####', '#.#.#', '#####', '.###.']}
GHOST_FOR = {'specimen': 'bee', 'vial': 'vial', 'reagent': 'drop', 'bee': 'crown', 'serum': 'vial', 'catalyst': 'jelly'}


def background(g):
    W, H = g['W'], g['H']; img = Image.new('RGBA', (256, 256), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    window(d, W, H)
    for n, k, x, y, w, h, _ in g['layout']:
        if k == 'panel': panel(d, x, y, w, h)
    for n, k, x, y, w, h, _ in g['layout']:
        if k == 'slot':
            slot(d, x, y)
            if n in GHOST_FOR: glyph(d, x + 9 - len(GHOST[GHOST_FOR[n]][0]) // 2, y + 9 - len(GHOST[GHOST_FOR[n]]) // 2, GHOST[GHOST_FOR[n]], {'#': (120, 120, 120)})
        elif k == 'grid':
            for gy in range(y, y + h, 18):
                for gx in range(x, x + w, 18): slot(d, gx, gy)
        elif k in ('bar', 'tank', 'well', 'scroll'): well(d, x, y, w, h)
        elif k == 'list':
            well(d, x, y, w, h, (28, 30, 34))
            for r in range(8):
                rect(d, x + 1, y + 1 + r * 10, w - 2, 10, (34, 37, 42) if r % 2 else (28, 30, 34))
        elif k == 'display':
            well(d, x, y, w, h, C['glass'])
            for gy in range(y + 4, y + h - 2, 6): d.line([(x + 2, gy), (x + w - 3, gy)], fill=(26, 44, 52))
            for gx in range(x + 4, x + w - 2, 6): d.line([(gx, y + 2), (gx, y + h - 3)], fill=(26, 44, 52))
        elif k == 'button': bevel(d, x, y, w, h, C['bg'])
        elif k in ('arrow', 'arrow_r'):
            g_ = ['..#..', '..#..', '..#..', '#####', '.###.', '..#..'] if k == 'arrow' else ['...#...', '...##..', '######.', '#######', '######.', '...##..', '...#...']
            glyph(d, x + (w - len(g_[0])) // 2, y + (h - len(g_)) // 2, g_, {'#': (139, 139, 139)})
    if g['id'] == 'genetic_splicer':                                # jelly tank ticks
        _, _, x, y, w, h, _ = [e for e in g['layout'] if e[0] == 'jelly'][0]
        for i in range(1, 4): d.line([(x + 1, y + i * h // 4), (x + 3, y + i * h // 4)], fill=(90, 86, 80))
    return img


SPR = {}


def spr(n, x, y, w, h, note): SPR[n] = (x, y, w, h, note)


def widgets():
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    # helix frames 24 x 56, 8 frames in a row
    for f in range(8):
        ox = f * 26
        for j in range(56):
            ph = j / 56 * math.pi * 3 + f * math.pi / 4
            a = math.sin(ph); x1 = int(round(12 + a * 9)); x2 = int(round(12 - a * 9))
            front1 = math.cos(ph) > 0
            c1 = C['cyan'] if front1 else tuple(int(v * .55) for v in C['cyan']); c2 = C['amber'] if not front1 else tuple(int(v * .55) for v in C['amber'])
            if j % 6 == 0:
                for xx in range(min(x1, x2), max(x1, x2) + 1): px(d, ox + xx, j, (230, 236, 255) if xx % 2 else (160, 170, 200))
            for dx in (0, 1):
                px(d, ox + x1 + dx - 1, j, c1); px(d, ox + x2 + dx - 1, j, c2)
        spr(f'helix_{f}', ox, 0, 24, 56, f'Helix animation frame {f} (play 8 frames, 3 ticks each; tint strands with the serum colour in code)')
    # fills
    def vgrad(x, y, w, h, top, bot):
        for j in range(h):
            t = j / max(1, h - 1); c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
            for i in range(w): px(d, x + i, y + j, c if i not in (0, w - 1) else tuple(int(v * .8) for v in c))
    vgrad(0, 60, 12, 74, (255, 220, 120), (220, 120, 20)); spr('fill_jelly', 0, 60, 12, 74, 'Royal Jelly fluid fill (or use the fluid texture)')
    vgrad(14, 60, 12, 20, (255, 210, 80), (200, 40, 30)); spr('fill_energy', 14, 60, 12, 20, 'FE fill (bottom-up)')
    for i in range(122):
        for j in range(4):
            px(d, 28 + i, 60 + j, C['honey_l'] if j == 0 else (C['honey'] if (i + j) % 5 else C['honey_d']))
    spr('fill_progress', 28, 60, 122, 4, 'Progress fill (left to right)')
    for i, (n, col) in enumerate((('active', C['cyan']), ('inactive', (90, 150, 160)))):
        rect(d, 28, 66 + i * 5, 30, 3, col); spr(f'allele_{n}', 28, 66 + i * 5, 30, 3, f'Allele bar, {n} (tint per gene family in code)')
    rect(d, 62, 66, 110, 10, (80, 70, 30)); d.rectangle([62, 66, 171, 75], outline=C['honey']); spr('row_selected', 62, 66, 110, 10, 'Selected gene row highlight')
    rect(d, 62, 78, 110, 10, (44, 48, 56)); spr('row_hover', 62, 78, 110, 10, 'Hovered gene row')
    bevel(d, 176, 66, 6, 15, (170, 170, 170)); spr('scroll_thumb', 176, 66, 6, 15, 'Scrollbar thumb')
    bevel(d, 184, 66, 6, 15, (120, 120, 120)); spr('scroll_thumb_off', 184, 66, 6, 15, 'Scrollbar thumb, disabled')
    # arrows (lit)
    g = ['..#..', '..#..', '..#..', '#####', '.###.', '..#..']; glyph(d, 194, 66, g, {'#': C['honey']}); spr('arrow_down_on', 194, 66, 5, 6, 'Down arrow, lit (draw the top N rows by progress)')
    g = ['...#...', '...##..', '######.', '#######', '######.', '...##..', '...#...']; glyph(d, 202, 66, g, {'#': C['honey']}); spr('arrow_right_on', 202, 66, 7, 7, 'Right arrow, lit')
    # buttons 60 x 14: normal, hover, active, disabled
    for r, (state, fill) in enumerate((('normal', C['bg']), ('hover', (214, 214, 234)), ('active', (240, 200, 110)), ('disabled', (160, 160, 160)))):
        bevel(d, 0, 140 + r * 16, 60, 14, fill, raised=state != 'active'); spr(f'button_{state}', 0, 140 + r * 16, 60, 14, f'Mode button, {state} (text drawn by code)')
    # mode icons 9 x 9
    glyph(d, 64, 140, ['.###.....', '#...#....', '#...#....', '#...#....', '.###.#...', '.....##..', '......##.'], {'#': (40, 40, 40)}); spr('icon_analyse', 64, 140, 9, 9, 'Analyse icon (magnifier)')
    glyph(d, 76, 140, GHOST['vial'], {'#': (40, 40, 40)}); spr('icon_sample', 76, 140, 5, 7, 'Sample icon (vial)')
    # chance badge background 26 x 9
    bevel(d, 90, 140, 26, 9, (40, 60, 66), raised=False); spr('chance_badge', 90, 140, 26, 9, 'Success-chance badge in the chamber corner')
    # error overlay for the chamber
    for j in range(0, 76):
        for i in range(0, 92):
            if (i + j) % 8 < 2: px(d, 120 + i, 140 + j, (200, 60, 50, 90))
    spr('chamber_blocked', 120, 140, 92, 76, 'Red hatch over the chamber when the splice cannot start')
    rs = list(SPR.items())
    for i in range(len(rs)):
        for j in range(i + 1, len(rs)):
            (a, (x1, y1, w1, h1, _)), (b, (x2, y2, w2, h2, _)) = rs[i], rs[j]
            assert x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1, (a, b)
    return img


def L(g, n): return [e for e in g['layout'] if e[0] == n][0]


def item(d, x, y, kind, col=None):
    cmap = {'#': col or (40, 30, 20)}
    if kind == 'bee':
        glyph(d, x + 4, y + 4, ['....ww..', '...wwww.', '.bbsbsb.', 'bbbsbsbb', 'bbbsbsbb', '.bbsbsb.', '..k..k..'],
              {'w': (220, 235, 255), 'b': col or (240, 200, 70), 's': (60, 40, 20), 'k': (40, 30, 20)})
    elif kind == 'vial':
        glyph(d, x + 5, y + 2, ['.ccc.', '..c..', '.#.#.', '.#.#.', '#lll#', '#lll#', '#lll#', '#lll#', '.###.'], {'c': (200, 160, 70), '#': (220, 235, 240), 'l': col or (220, 235, 240)})
    elif kind == 'drop':
        glyph(d, x + 5, y + 3, ['...#...', '..###..', '.#####.', '#######', '#######', '.#####.', '..###..'], {'#': C['honey']})
    elif kind == 'jelly':
        glyph(d, x + 4, y + 4, ['.####.', '######', '#o##o#', '######', '.####.'], {'#': (250, 236, 200), 'o': (230, 200, 120)})


def mockup(g, wd, state):
    bg = background(g); img = bg.copy(); d = ImageDraw.Draw(img); W, H = g['W'], g['H']
    def blit(n, x, y, w=None, h=None, bottom=False):
        sx, sy, sw, sh_, _ = SPR[n]; w = sw if w is None else w; h = sh_ if h is None else h
        if w <= 0 or h <= 0: return
        part = wd.crop((sx, sy + (sh_ - h if bottom else 0), sx + w, sy + (sh_ if bottom else h))); img.alpha_composite(part, (x, y))
    texts = []
    if g['id'] == 'geno_station':
        item(d, *L(g, 'specimen')[2:4], 'bee'); item(d, *L(g, 'vial')[2:4], 'vial'); item(d, *L(g, 'reagent')[2:4], 'drop')
        item(d, *L(g, 'serum_out')[2:4], 'vial', C['violet'])
        _, _, x, y, w, h, _ = L(g, 'genes')
        genes = [('Species', 'Forest', 'Forest'), ('Lifespan', 'Normal', 'Short'), ('Speed', 'Fast', 'Normal'), ('Fertility', '3', '2'),
                 ('Temp. tol.', 'Both 1', 'None'), ('Humid. tol.', 'None', 'Up 1'), ('Nocturnal', 'No', 'Yes'), ('Flowers', 'Flowers', 'Flowers')]
        cols = [C['amber'], C['green'], C['cyan'], C['violet'], (255, 106, 90), (95, 160, 255), (180, 180, 200), (240, 220, 120)]
        for r, (gn, a, b) in enumerate(genes):
            ry = y + 1 + r * 10
            if r == 2: blit('row_selected', x + 1, ry)
            ca, cb = cols[r], tuple(int(v * .6) for v in cols[r])
            rect(d, x + 62, ry + 2, 22, 3, ca); rect(d, x + 62, ry + 6, 14, 2, cb)
            texts.append((x + 4, ry + 1, gn, (220, 220, 230), 6)); texts.append((x + 88, ry + 1, a, (220, 220, 230), 6))
        blit('scroll_thumb', L(g, 'scroll')[2], L(g, 'scroll')[3] + 2)
        _, _, x, y, w, h, _ = L(g, 'progress'); blit('fill_progress', x + 1, y + 1, int((w - 2) * .45), 4)
        _, _, x, y, w, h, _ = L(g, 'energy'); hh = int((h - 2) * .7); blit('fill_energy', x + 1, y + h - 1 - hh, 12, hh, bottom=True)
        _, _, x, y, w, h, _ = L(g, 'arrow'); blit('arrow_down_on', x + 2, y + 3, 5, 3)
        blit('button_normal', *L(g, 'b_analyse')[2:4]); blit('button_active', *L(g, 'b_sample')[2:4])
        blit('icon_analyse', L(g, 'b_analyse')[2] + 5, L(g, 'b_analyse')[3] + 2); blit('icon_sample', L(g, 'b_sample')[2] + 6, L(g, 'b_sample')[3] + 3)
        texts += [(L(g, 'b_analyse')[2] + 17, L(g, 'b_analyse')[3] + 2, 'Analyse', C['text'], 7), (L(g, 'b_sample')[2] + 16, L(g, 'b_sample')[3] + 2, 'Sample', C['text'], 7)]
    else:
        item(d, *L(g, 'bee')[2:4], 'bee'); item(d, *L(g, 'serum')[2:4], 'vial', C['cyan']); item(d, *L(g, 'catalyst')[2:4], 'jelly')
        if state == 'done': item(d, *L(g, 'bee_out')[2:4], 'bee'); item(d, *L(g, 'vial_out')[2:4], 'vial')
        _, _, x, y, w, h, _ = L(g, 'chamber')
        blit('helix_2', x + (w - 24) // 2, y + (h - 56) // 2 + 2)
        blit('chance_badge', x + w - 29, y + 3); texts.append((x + w - 27, y + 3, '75%', (220, 240, 245), 6))
        if state == 'blocked': blit('chamber_blocked', x, y)
        _, _, x, y, w, h, _ = L(g, 'jelly'); hh = int((h - 2) * .55); blit('fill_jelly', x + 1, y + h - 1 - hh, 12, hh, bottom=True)
        _, _, x, y, w, h, _ = L(g, 'energy'); hh = int((h - 2) * .8); blit('fill_energy', x + 1, y + h - 1 - hh, 10, hh, bottom=True)
        _, _, x, y, w, h, _ = L(g, 'progress'); blit('fill_progress', x + 1, y + 1, int((w - 2) * (.62 if state != 'blocked' else 0)), 4)
        if state != 'blocked': blit('arrow_right_on', *L(g, 'a_in')[2:4])
        _, _, x, y, w, h, _ = L(g, 'preview')
        texts.append((x + 4, y + 2, 'Speed: Fast  ->  Forest Queen' if state != 'blocked' else 'Species can\'t be spliced', (230, 220, 160) if state != 'blocked' else (255, 140, 120), 7))
    S = 3
    big = img.crop((0, 0, W, H)).resize((W * S, H * S), Image.NEAREST); bd = ImageDraw.Draw(big)
    bd.text((8 * S, 5 * S - 3), g['title'], font=F(8 * S - 6), fill=C['text']); bd.text((L(g, 'inv_label')[2] * S, L(g, 'inv_label')[3] * S - 3), 'Inventory', font=F(8 * S - 6), fill=C['text'])
    for x, y, t, col, sz in texts: bd.text((x * S, y * S - 2), t, font=F(sz * S - 6), fill=col)
    return big


def layout_map(g, bg):
    S = 4; pad = 30; W, H = g['W'], g['H']
    big = bg.crop((0, 0, W, H)).resize((W * S, H * S), Image.NEAREST)
    sheet = Image.new('RGB', (W * S + 2 * pad + 560, H * S + 2 * pad + 50), (246, 245, 242)); d = ImageDraw.Draw(sheet)
    d.text((pad, 10), f'{g["title"]} - screen layout (gui/{g["id"]}.png, screen {W} x {H})', font=F(20, True), fill=(34, 32, 40))
    sheet.paste(big, (pad, pad + 30), big)
    items = g['layout']
    for i, (n, k, x, y, w, h, _) in enumerate(items):
        X, Y = pad + x * S, pad + 30 + y * S; col = (230, 120, 40) if k == 'panel' else (124, 92, 230)
        d.rectangle([X, Y, X + w * S - 1, Y + h * S - 1], outline=col, width=2 if k == 'panel' else 1)
        lab = str(i + 1); tw = d.textlength(lab, font=F(11, True))
        if k != 'panel': d.rectangle([X, Y, X + tw + 4, Y + 13], fill=col); d.text((X + 2, Y), lab, font=F(11, True), fill=(255, 255, 255))
    lx = pad + W * S + 24; ly = pad + 30
    d.text((lx, ly - 22), '#   element        x    y    w    h', font=FM(13), fill=(34, 32, 40))
    for i, (n, k, x, y, w, h, _) in enumerate(items):
        d.text((lx, ly + i * 21), f'{i + 1:<3} {n:<13} {x:>4} {y:>4} {w:>4} {h:>4}', font=FM(13), fill=(200, 100, 30) if k == 'panel' else (34, 32, 40))
    return sheet


def spec():
    o = ['\n# GUIs\n', 'Both screens use the Alveary Controller look: vanilla window and slots, recessed panels with a honey strip, dark wells for gauges. '
         'No words are baked into textures. Backgrounds are `textures/gui/geno_station.png` and `textures/gui/genetic_splicer.png` (256 x 256); '
         'both blit sprites from `textures/gui/genetics_widgets.png`.\n']
    for g in (GENO, SPLICER):
        o.append(f'## {g["title"]} screen ({g["W"]} x {g["H"]})\n')
        o.append('| # | Element | Kind | x | y | w | h | Behaviour |\n| --- | --- | --- | --- | --- | --- | --- | --- |')
        for i, (n, k, x, y, w, h, note) in enumerate(g['layout']): o.append(f'| {i + 1} | `{n}` | {k} | {x} | {y} | {w} | {h} | {note} |')
        o.append('')
    o.append('Menu slots for both: 0-2 inputs, 3-4 outputs (take only), 5-31 player inventory, 32-40 hotbar. Item positions are the slot box + 1.\n')
    o.append('**Geno Station ContainerData:** 0 progress, 1 max, 2 energy/10, 3 energy max/10, 4 mode (0 analyse, 1 sample), 5 selected gene index (-1 none), 6 scroll offset.')
    o.append('Gene rows come from the specimen\'s genome, sent with the slot sync (the item already carries it). Buttons send `SetMode` and `SelectGene(index)`; Sample stays disabled until a gene is selected.\n')
    o.append('**Genetic Splicer ContainerData:** 0 progress, 1 max, 2 energy/10, 3 energy max/10, 4 jelly mB, 5 success chance %, 6 status (0 ready, 1 working, 2 no serum, 3 species blocked, 4 wrong bee, 5 no catalyst, 6 no power).')
    o.append('The chamber shows `helix_0..7` at 3 ticks per frame while working (frame 0 when idle); a status other than 0 or 1 draws `chamber_blocked` and the reason in the preview line.\n')
    o.append('## Widget atlas (`genetics_widgets.png`)\n')
    o.append('| Sprite | u | v | w | h | Use |\n| --- | --- | --- | --- | --- | --- |')
    for n, (x, y, w, h, note) in SPR.items(): o.append(f'| `{n}` | {x} | {y} | {w} | {h} | {note} |')
    o.append('\nLang: `screen.aeroapiary.geno_station`, `screen.aeroapiary.genetic_splicer`, `.analyse`, `.sample`, `.gene.<id>`, `.status.<n>`, `.chance` ("%s%% chance").\n')
    return '\n'.join(o)


if __name__ == '__main__':
    G = f'{OUT}/assets/aeroapiary/textures/gui'; os.makedirs(G, exist_ok=True)
    wd = widgets(); wd.save(f'{G}/genetics_widgets.png')
    for g in (GENO, SPLICER):
        bg = background(g); bg.save(f'{G}/{g["id"]}.png')
        layout_map(g, bg).save(f'{OUT}/gui_{g["id"]}_layout.png')
    m1 = mockup(GENO, wd, 'work'); m2 = mockup(SPLICER, wd, 'work'); m3 = mockup(SPLICER, wd, 'blocked')
    Wt = m1.width + m2.width + m3.width + 80; Ht = max(m1.height, m2.height) + 70
    sh = Image.new('RGB', (Wt, Ht), (246, 245, 242)); d = ImageDraw.Draw(sh)
    x = 20
    for m, cap in ((m1, 'Geno Station - Sample mode, Speed gene selected'), (m2, 'Genetic Splicer - splicing Speed: Fast'), (m3, 'Genetic Splicer - blocked (species serum)')):
        d.text((x, 14), cap, font=F(16, True), fill=(34, 32, 40)); sh.paste(m, (x, 46), m); x += m.width + 20
    sh.save(f'{OUT}/gui_mockups.png')
    open(f'{OUT}/genetics_machines_spec.md', 'a').write(spec())
    print('gui ok', len(SPR), 'sprites')
