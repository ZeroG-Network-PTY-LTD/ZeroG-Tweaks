"""Armor trims for ZeroG Tweaks (Minecraft 1.21.1, data-driven trims).

- 20 trim materials: the metal or gem of every ZeroG armor set (palette taken from the item texture)
- 10 ZeroG trim patterns, each themed on a world, with smithing templates, overlay textures and recipes
- Atlas sources so vanilla patterns work with our materials, and our patterns with vanilla + our materials
- Item model overrides so all 80 ZeroG armor pieces show the trim on their icon
"""
import json, os, re, math, random
from PIL import Image

REPO = '/home/claude/zerog-tweaks'
RES = f'{REPO}/src/main/resources'
A, D = f'{RES}/assets/zerog_tweaks', f'{RES}/data/zerog_tweaks'
MCA = f'{RES}/assets/minecraft'
NS = 'zerog_tweaks'
W = []
def w(p, o):
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w').write(json.dumps(o, indent=2) + '\n'); W.append(p)
def save(im, p):
    os.makedirs(os.path.dirname(p), exist_ok=True); im.save(p); W.append(p)

SETS = ['nullifite', 'ferrox', 'moonsteel', 'olympium', 'cobaltium', 'cyrrium', 'aurelion', 'cerulite', 'ruskite', 'tectium', 'pyrium',
        'skarnite', 'salvium', 'wraithsteel', 'palladine', 'eidolite', 'photium', 'astrium', 'radiantine', 'solvanite']
SLOTS = ['helmet', 'chestplate', 'leggings', 'boots']
VANILLA_MATS = [('quartz', 0.1), ('iron', 0.2), ('netherite', 0.3), ('redstone', 0.4), ('copper', 0.5), ('gold', 0.6),
                ('emerald', 0.7), ('diamond', 0.8), ('lapis', 0.9), ('amethyst', 1.0)]
VANILLA_PATTERNS = ['sentry', 'dune', 'coast', 'wild', 'ward', 'eye', 'vex', 'tide', 'snout', 'rib', 'spire', 'wayfinder',
                    'shaper', 'silence', 'raiser', 'host', 'flow', 'bolt']
LANG = json.load(open(f'{A}/lang/en_us.json'))

def ingredient(s):
    return f'{s}_ingot' if os.path.exists(f'{A}/textures/item/{s}_ingot.png') else s

# ============================================================== 1. trim materials
def palette_from(item):
    im = Image.open(f'{A}/textures/item/{item}.png').convert('RGBA')
    px = [p[:3] for p in im.getdata() if p[3] > 200]
    lum = lambda c: 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]
    px.sort(key=lum, reverse=True)
    lo, hi = int(len(px) * .02), max(3, int(len(px) * .7))   # skip the darkest outline pixels so trims stay readable
    core = px[lo:hi] or px
    out = []
    for i in range(8):  # light -> dark, 8 steps
        c = core[min(len(core) - 1, int(i / 7 * (len(core) - 1)))]
        out.append(c)
    # keep a readable spread even for flat textures
    base = out[3]
    for i in range(8):
        k = 1.28 - i * 0.09
        out[i] = tuple(max(0, min(255, int(0.55 * out[i][j] + 0.45 * base[j] * k))) for j in range(3))
    return out

MATS = []  # (set, asset, ingredient, index, palette)
for i, s in enumerate(SETS):
    item = ingredient(s)
    pal = palette_from(item)
    MATS.append((s, f'zerog_{s}', item, round(1.01 + i * 0.01, 2), pal))
    im = Image.new('RGBA', (8, 1)); im.putdata([c + (255,) for c in pal])
    save(im, f'{A}/textures/trims/color_palettes/{s}.png')
    col = '#%02x%02x%02x' % pal[2]
    w(f'{D}/trim_material/{s}.json', {'asset_name': f'zerog_{s}', 'description': {'color': col, 'translate': f'trim_material.{NS}.{s}'},
                                       'ingredient': f'{NS}:{item}', 'item_model_index': MATS[-1][3]})
    LANG[f'trim_material.{NS}.{s}'] = f'{s.capitalize()} Material'

def tag(path, vals):
    p = f'{RES}/data/{path}.json'
    old = json.load(open(p))['values'] if os.path.exists(p) else []
    w(p, {'replace': False, 'values': old + [v for v in vals if v not in old]})
tag('minecraft/tags/item/trim_materials', [f'{NS}:{m[2]}' for m in MATS])

# ============================================================== 2. trim patterns
# our own 8-step key palette (light -> dark); pattern textures are drawn only in these greys
KEY = [(236, 236, 236), (212, 212, 212), (188, 188, 188), (164, 164, 164), (140, 140, 140), (116, 116, 116), (92, 92, 92), (68, 68, 68)]
im = Image.new('RGBA', (8, 1)); im.putdata([c + (255,) for c in KEY]); save(im, f'{A}/textures/trims/color_palettes/trim_palette.png')

HEAD = {'top': (8, 0, 8, 8), 'right': (0, 8, 8, 8), 'front': (8, 8, 8, 8), 'left': (16, 8, 8, 8), 'back': (24, 8, 8, 8)}
BODY = {'right': (16, 20, 4, 12), 'front': (20, 20, 8, 12), 'left': (28, 20, 4, 12), 'back': (32, 20, 8, 12)}
ARM = {'right': (40, 20, 4, 12), 'front': (44, 20, 4, 12), 'left': (48, 20, 4, 12), 'back': (52, 20, 4, 12)}
LEG = {'right': (0, 20, 4, 12), 'front': (4, 20, 4, 12), 'left': (8, 20, 4, 12), 'back': (12, 20, 4, 12)}

def motif(name, x, y, fw, fh, gx, gy):
    """-> key index (0 light .. 7 dark) or None. x,y local in the face; gx,gy absolute (for continuity)."""
    cx, cy = (fw - 1) / 2, (fh - 1) / 2
    edge = y == fh - 1
    if name == 'fracture':      # jagged void crack down the middle + lit hem
        zig = int(cx) + (1 if (y // 2) % 2 else 0)
        if x == zig: return 1 if y % 3 == 0 else 3
        if edge: return 5
    elif name == 'crater':      # rings
        d = math.hypot(x - cx, y - cy)
        if fw >= 8 and abs(d - 2.6) < 0.45 and y > 1: return 2
        if fw < 8 and y % 6 == 3 and abs(x - cx) < 1: return 3
        if edge: return 5
    elif name == 'olympus':     # mountain chevrons
        if abs((y - 1) - abs(x - cx)) < .6 and y < fh * .6: return 2    # one chevron peak
        if edge: return 6
    elif name == 'geode':       # nested diamonds
        m = abs(x - cx) + abs(y - cy)
        if round(m) == 3 and fw >= 8: return 1
        if round(m) == 1 and fw < 8 and y % 6 == 3: return 2
        if edge: return 5
    elif name == 'rift':        # diagonal torn slashes
        if (gx + gy) % 9 == 0 and y % 4 != 3: return 2
        if edge: return 5
    elif name == 'hull':        # hull ribs and rivets
        if y in (0, fh - 1): return 5
        if x in (1, fw - 2) and y % 3 == 1: return 1           # two rivet columns
    elif name == 'corona':      # rays from the top centre
        ang = math.degrees(math.atan2(y + 1, x - cx))
        if round(ang) % 45 < 6 and 0 < y < 6: return 1 if y < 3 else 3
    elif name == 'surge':       # waves
        if y == int(cy + 1.4 * math.sin((gx) / 1.6)): return 2
        if edge: return 5
    elif name == 'prism':       # stacked triangles
        if fh - 1 - y < 4 and abs(x - cx) <= (fh - 1 - y) and abs(abs(x - cx) - (fh - 1 - y)) < .6: return 2
        if fh - 1 - y == 5 and abs(x - cx) < 1: return 0
    elif name == 'meteor':      # a streak with a burning head
        t = x - y
        if t == 0 and y < fh - 2: return 3 if y % 2 else 5
        if (x, y) in ((fw - 2, fh - 3), (fw - 3, fh - 2), (fw - 2, fh - 2)): return 0
    return None

# copy recipe: 7 x the pattern's main item + template + the stone of the world where the template is found
DUP = {'fracture': ('nullifite_ingot', 'sunbaked_stone'), 'crater': ('moonsteel_ingot', 'craterstone'), 'olympus': ('olympium_ingot', 'martian_stone'), 'geode': ('cerulite', 'prismstone'), 'rift': ('rift_opal', 'scoria'), 'hull': ('salvium_ingot', 'permafrost'), 'corona': ('coronite', 'solar_stone'), 'surge': ('brine_crystal', 'abyssal_stone'), 'prism': ('prism_cluster', 'prismstone'), 'meteor': ('meteorite_fragment', 'craterstone')}
PATTERNS = {  # id: (display, theme colour for the template icon, chest, duplication block)
    'fracture': ('Fracture', (180, 140, 255), 'buried_observatory', 'minecraft:cobbled_deepslate'),
    'crater': ('Crater', (200, 200, 208), 'impact_site', 'lunar_stone'),
    'olympus': ('Olympus', (200, 110, 70), 'mars_crash_site', 'martian_stone'),
    'geode': ('Geode', (80, 160, 230), 'prism_spire', 'cerulean_stone'),
    'rift': ('Rift', (255, 140, 50), 'collapsed_forge', 'skarn_rock'),
    'hull': ('Hull', (160, 220, 235), 'derelict_wreck', 'hull_plating'),
    'corona': ('Corona', (255, 200, 80), 'solar_shrine', 'solar_stone'),
    'surge': ('Surge', (70, 170, 190), 'sunken_relay', 'abyssal_stone'),
    'prism': ('Prism', (200, 170, 240), 'prism_spire', 'prismstone'),
    'meteor': ('Meteor', (230, 110, 60), 'impact_site', 'craterstone'),
}

def draw_layer(name, parts):
    """Keep trims light, like vanilla: the full motif only on the big front/back faces (head, torso);
    side faces and the narrow arm/leg faces just get a hem line and one accent, and the helmet top stays bare."""
    im = Image.new('RGBA', (64, 32), (0, 0, 0, 0)); p = im.load()
    for rects, rows in parts:
        for face, (fx, fy, fw, fh) in rects.items():
            if face == 'top': continue
            big = face in ('front', 'back') and fw >= 8
            for y in range(fh):
                gy = fy + y
                if rows and not (rows[0] <= gy <= rows[1]): continue
                last = gy == (rows[1] if rows else fy + fh - 1)
                for x in range(fw):
                    if big:
                        k = motif(name, x, y, fw, fh, fx + x, gy)
                    elif last:
                        k = 5                                            # hem along the bottom edge
                    elif face in ('front', 'back') and y == fh // 2 and x in (fw // 2 - 1, fw // 2):
                        k = 2                                            # a single accent on arms and legs
                    else:
                        k = None
                    if k is not None: p[fx + x, gy] = KEY[k] + (255,)
    return im

for pid in PATTERNS:
    save(draw_layer(pid, [(HEAD, None), (BODY, None), (ARM, None), (LEG, (26, 31))]), f'{A}/textures/trims/models/armor/{pid}.png')
    save(draw_layer(pid, [(BODY, (26, 31)), (LEG, (20, 29))]), f'{A}/textures/trims/models/armor/{pid}_leggings.png')

# template items (original art in the vanilla template layout: a dark tablet with a glowing emblem)
def template_icon(pid, col):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); p = im.load()
    dark, mid, rim = (40, 44, 58), (62, 68, 86), (96, 104, 128)
    for y in range(2, 15):
        for x in range(3, 13):
            p[x, y] = (rim if x in (3, 12) or y in (2, 14) else mid if (x + y) % 5 else dark) + (255,)
    for y in range(4, 13):  # emblem from the pattern's own motif, in the theme colour
        for x in range(5, 11):
            k = motif(pid, x - 5, y - 4, 6, 9, x, y)
            if k is not None:
                f = 1.15 - k * 0.08
                p[x, y] = tuple(max(0, min(255, int(c * f))) for c in col) + (255,)
    p[4, 3] = (150, 160, 190, 255)
    return im

import sys
sys.path.insert(0, '/home/claude/zg')
for pid, (disp, col, chest, block) in PATTERNS.items():
    item = f'{pid}_armor_trim_smithing_template'
    w(f'{D}/trim_pattern/{pid}.json', {'asset_id': f'{NS}:{pid}', 'description': {'translate': f'trim_pattern.{NS}.{pid}'},
                                       'template_item': f'{NS}:{item}', 'decal': False})
    save(template_icon(pid, col), f'{A}/textures/item/{item}.png')
    w(f'{A}/models/item/{item}.json', {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'{NS}:item/{item}'}})
    LANG[f'trim_pattern.{NS}.{pid}'] = f'{disp} Armor Trim'
    LANG[f'item.{NS}.{item}'] = 'Smithing Template'
    w(f'{D}/recipe/{pid}_armor_trim_smithing_template_smithing_trim.json', {'type': 'minecraft:smithing_trim',
        'template': {'item': f'{NS}:{item}'}, 'base': {'tag': 'minecraft:trimmable_armor'}, 'addition': {'tag': 'minecraft:trim_materials'}})
    blk = block if ':' in block else f'{NS}:{block}'
    w(f'{D}/recipe/{pid}_armor_trim_smithing_template_duplication.json', {'type': 'minecraft:crafting_shaped', 'category': 'misc',
        'pattern': ['#S#', '#C#', '###'], 'key': {'#': {'item': f'{NS}:{DUP[pid][0]}'}, 'S': {'item': f'{NS}:{item}'}, 'C': {'item': f'{NS}:{DUP[pid][1]}'}},
        'result': {'id': f'{NS}:{item}', 'count': 2}})
    # loot: ~1 in 6 chests of the matching structure, like vanilla trim templates
    lp = f'{D}/loot_table/chests/{chest}.json'; lt = json.load(open(lp))
    if not any(e.get('name') == f'{NS}:{item}' for pl in lt['pools'] for e in pl['entries']):
        lt['pools'].append({'rolls': 1, 'bonus_rolls': 0, 'entries': [{'type': 'minecraft:item', 'name': f'{NS}:{item}', 'weight': 1},
                                                                        {'type': 'minecraft:empty', 'weight': 5}]})
    w(lp, lt)
tag('minecraft/tags/item/trim_templates', [f'{NS}:{p}_armor_trim_smithing_template' for p in PATTERNS])

# ============================================================== 3. atlases
VAN_PAL = {m: f'minecraft:trims/color_palettes/{m}' for m, _ in VANILLA_MATS}
VAN_PAL.update({f'{m}_darker': f'minecraft:trims/color_palettes/{m}_darker' for m in ('iron', 'gold', 'diamond', 'netherite')})
OUR_PAL = {a: f'{NS}:trims/color_palettes/{s}' for s, a, *_ in MATS}
def atlas(path, sources):
    # these atlas files belong to us: they only ADD sources; Minecraft merges them with the vanilla atlas
    w(f'{MCA}/atlases/{path}.json', {'sources': sources})
atlas('armor_trims', [
    {'type': 'paletted_permutations', 'textures': [f'minecraft:trims/models/armor/{v}{s}' for v in VANILLA_PATTERNS for s in ('', '_leggings')],
     'palette_key': 'minecraft:trims/color_palettes/trim_palette', 'permutations': OUR_PAL},
    {'type': 'paletted_permutations', 'textures': [f'{NS}:trims/models/armor/{p}{s}' for p in PATTERNS for s in ('', '_leggings')],
     'palette_key': f'{NS}:trims/color_palettes/trim_palette', 'permutations': {**VAN_PAL, **OUR_PAL}}])
atlas('blocks', [
    {'type': 'paletted_permutations', 'textures': [f'minecraft:trims/items/{s}_trim' for s in SLOTS],
     'palette_key': 'minecraft:trims/color_palettes/trim_palette', 'permutations': OUR_PAL}])

# ============================================================== 4. item model overrides for our 80 armor pieces
ALL_MATS = [(m, m, i) for m, i in VANILLA_MATS] + [(s, a, i) for s, a, _, i, _ in MATS]
for s in SETS:
    for slot in SLOTS:
        item = f'{s}_{slot}'
        overrides = []
        for mat, asset, idx in sorted(ALL_MATS, key=lambda t: t[2]):
            model = f'{NS}:item/{item}_{mat}_trim'
            w(f'{A}/models/item/{item}_{mat}_trim.json', {'parent': 'minecraft:item/generated',
                'textures': {'layer0': f'{NS}:item/{item}', 'layer1': f'minecraft:trims/items/{slot}_trim_{asset}'}})
            overrides.append({'model': model, 'predicate': {'trim_type': idx}})
        w(f'{A}/models/item/{item}.json', {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'{NS}:item/{item}'}, 'overrides': overrides})

open(f'{A}/lang/en_us.json', 'w').write(json.dumps(LANG, indent=2, ensure_ascii=False) + '\n')

# ============================================================== 5. Java: template items
J = f'{REPO}/src/main/java/net/zerog/tweaks/registry/ZGTrims.java'
rows = '\n'.join(f'    public static final DeferredItem<SmithingTemplateItem> {p.upper()} = template("{p}");' for p in PATTERNS)
open(J, 'w').write(f'''package net.zerog.tweaks.registry;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.SmithingTemplateItem;
import net.neoforged.neoforge.registries.DeferredItem;
import net.zerog.tweaks.ZeroGTweaks;

/**
 * GENERATED by docs/zero-g-tweaks-bundle/generators/trims.py; do not edit by hand.
 * Armor trim smithing templates for the {len(PATTERNS)} ZeroG trim patterns (data/zerog_tweaks/trim_pattern/*).
 * Trim materials (data/zerog_tweaks/trim_material/*) need no Java: they are data only.
 */
public final class ZGTrims {{
    private ZGTrims() {{}}

    public static final List<DeferredItem<SmithingTemplateItem>> ALL = new ArrayList<>();

    private static DeferredItem<SmithingTemplateItem> template(String pattern) {{
        ResourceKey<net.minecraft.world.item.armortrim.TrimPattern> key =
                ResourceKey.create(Registries.TRIM_PATTERN, ResourceLocation.fromNamespaceAndPath(ZeroGTweaks.MODID, pattern));
        DeferredItem<SmithingTemplateItem> item = ItemInit.ITEMS.register(pattern + "_armor_trim_smithing_template",
                () -> SmithingTemplateItem.createArmorTrimTemplate(key));
        ALL.add(item);
        return item;
    }}

{rows}

    /** Called from ItemInit so the static fields above are initialised before the register is frozen. */
    static void init() {{}}
}}
''')
print('files', len(W), 'materials', len(MATS), 'patterns', len(PATTERNS))
