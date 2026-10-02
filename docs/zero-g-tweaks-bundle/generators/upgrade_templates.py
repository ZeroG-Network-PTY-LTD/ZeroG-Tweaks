"""Netherite-style upgrade smithing templates for every set on the mining ladder (all except Nullifite, which is
crafted like diamond). Each set is made at the smithing table from the previous set's piece + its own material + its template.
Writes into <out>: data (smithing recipes, template copy recipes, chest loot), assets (template icons, models, lang),
java/ZGUpgradeTemplates.java, recipes_to_delete.txt, README.md.
Usage: python3 upgrade_templates.py <out_dir>   (reads the current files from the local branch ref peek/1.21.x)"""
import json, os, subprocess, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mining_ladder as ML

OUT = sys.argv[1]; REPO = '/home/claude/zerog-tweaks'; REF = 'peek/1.21.x'; R = 'src/main/resources'
def git(path, binary=False):
    return subprocess.run(['git', '-C', REPO, 'show', f'{REF}:{path}'], capture_output=True, check=True).stdout if binary else \
           subprocess.run(['git', '-C', REPO, 'show', f'{REF}:{path}'], capture_output=True, text=True, check=True).stdout
def ls(path):
    return subprocess.run(['git', '-C', REPO, 'ls-tree', '--name-only', f'{REF}', path + '/'], capture_output=True, text=True).stdout.split()

PIECES = ['helmet', 'chestplate', 'leggings', 'boots', 'sword', 'pickaxe', 'axe', 'shovel', 'hoe']
GEMS = {'cerulite', 'skarnite', 'eidolite', 'solvanite'}
def mat(s): return f'zerog_tweaks:{s}' if s in GEMS else f'zerog_tweaks:{s}_ingot'
def nice(s): return s.replace('zerog_tweaks:', '').replace('_', ' ').title()
# set -> (upgraded from, found in chest, world stone of that place)
CHAIN = {
 'ferrox':      ('nullifite',   'mars_crash_site', 'martian_stone'),
 'moonsteel':   ('ferrox',      'mars_crash_site', 'martian_stone'),
 'olympium':    ('moonsteel',   'mars_crash_site', 'martian_stone'),
 'cobaltium':   ('olympium',    'prism_spire',     'prismstone'),
 'aurelion':    ('olympium',    'prism_spire',     'prismstone'),
 'cyrrium':     ('cobaltium',   'prism_spire',     'prismstone'),
 'cerulite':    ('cyrrium',     'prism_spire',     'prismstone'),
 'ruskite':     ('cerulite',    'collapsed_forge', 'scoria'),
 'pyrium':      ('cerulite',    'collapsed_forge', 'scoria'),
 'tectium':     ('ruskite',     'collapsed_forge', 'scoria'),
 'skarnite':    ('tectium',     'collapsed_forge', 'scoria'),
 'salvium':     ('skarnite',    'derelict_wreck',  'permafrost'),
 'palladine':   ('skarnite',    'derelict_wreck',  'permafrost'),
 'wraithsteel': ('salvium',     'derelict_wreck',  'permafrost'),
 'eidolite':    ('wraithsteel', 'derelict_wreck',  'permafrost'),
 'photium':     ('eidolite',    'solar_shrine',    'solar_stone'),
 'radiantine':  ('eidolite',    'solar_shrine',    'solar_stone'),
 'astrium':     ('photium',     'solar_shrine',    'solar_stone'),
 'solvanite':   ('astrium',     'solar_shrine',    'solar_stone'),
}
EXISTING = {'olympium', 'cerulite', 'skarnite', 'eidolite', 'solvanite'}
PLACE = {'mars_crash_site': 'Mars Crash Site (Mars)', 'prism_spire': 'Prism Spire (crystal wasteland, Galaxy 2)',
         'collapsed_forge': 'Collapsed Forge (volcanic wasteland, Galaxy 3)', 'derelict_wreck': 'Derelict Wreck (Eidolon)',
         'solar_shrine': 'Solar Shrine (Solvane)'}
# sanity: every upgrade follows the ladder upward
for s, (b, _, _) in CHAIN.items(): assert ML.SET_LEVEL[b] < ML.SET_LEVEL[s], (s, b)

def w(rel, obj):
    p = f'{OUT}/{rel}'; os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, 'w'), indent=2) if not isinstance(obj, str) else open(p, 'w').write(obj)

recipes = set(n.split('/')[-1][:-5] for n in ls(f'{R}/data/zerog_tweaks/recipe'))
D = 'data/zerog_tweaks'
# 1. smithing upgrades (replace the 45 existing, add the rest)
for s, (b, _, _) in CHAIN.items():
    for pc in PIECES:
        w(f'{D}/recipe/{s}_{pc}_smithing.json', {'type': 'minecraft:smithing_transform',
          'template': {'item': f'zerog_tweaks:{s}_upgrade_smithing_template'}, 'base': {'item': f'zerog_tweaks:{b}_{pc}'},
          'addition': {'item': mat(s)}, 'result': {'id': f'zerog_tweaks:{s}_{pc}'}})
# 2. template copies: 7 x the base set's material (as diamonds are to netherite) + template + stone of the place it's found
for s, (b, chest, stone) in CHAIN.items():
    t = f'zerog_tweaks:{s}_upgrade_smithing_template'
    w(f'{D}/recipe/{s}_upgrade_smithing_template_duplication.json', {'type': 'minecraft:crafting_shaped', 'category': 'misc',
      'pattern': ['MTM', 'MSM', 'MMM'], 'key': {'M': {'item': mat(b)}, 'T': {'item': t}, 'S': {'item': f'zerog_tweaks:{stone}'}},
      'result': {'id': t, 'count': 2}})
# 3. crafting-table recipes to delete: only the upgrade path makes these sets now (like netherite)
dele = sorted(f'{s}_{pc}' for s in CHAIN for pc in PIECES if f'{s}_{pc}' in recipes)
w('recipes_to_delete.txt', '\n'.join(f'{R}/data/zerog_tweaks/recipe/{n}.json' for n in dele) + '\n')
# 4. chest loot: every template in its structure's main pool, weight 3 (same as the existing ones)
for chest in sorted(set(c for _, c, _ in CHAIN.values())):
    j = json.loads(git(f'{R}/data/zerog_tweaks/loot_table/chests/{chest}.json'))
    pool = max(j['pools'], key=lambda p: len(p['entries']))
    have = {e.get('name') for e in pool['entries']}
    for s, (_, c, _) in CHAIN.items():
        n = f'zerog_tweaks:{s}_upgrade_smithing_template'
        if c == chest and n not in have: pool['entries'].append({'type': 'minecraft:item', 'name': n, 'weight': 3})
    w(f'{D}/loot_table/chests/{chest}.json', j)
# 5. art: recolour the existing frame with each set's trim palette
base = Image.open(__import__('io').BytesIO(git(f'{R}/assets/zerog_tweaks/textures/item/olympium_upgrade_smithing_template.png', True))).convert('RGBA')
def frame_mask(im):
    m = {}
    for (x, y), c in zip(((x, y) for y in range(im.height) for x in range(im.width)), im.getdata()):
        if c[3] and (max(c[:3]) - min(c[:3]) > 18): m[(x, y)] = sum(c[:3]) / 3
    return m
FM = frame_mask(base); lo, hi = min(FM.values()), max(FM.values())
lang = {}
for s, (b, chest, stone) in CHAIN.items():
    if s not in EXISTING:
        pal = [p[:3] for p in Image.open(__import__('io').BytesIO(git(f'{R}/assets/zerog_tweaks/textures/trims/color_palettes/{s}.png', True))).convert('RGBA').getdata()]
        im = base.copy(); px = im.load()
        for (x, y), lum in FM.items():
            k = int(round((1 - (lum - lo) / max(1, hi - lo)) * (len(pal) - 1))); px[x, y] = pal[k] + (255,)
        os.makedirs(f'{OUT}/assets/zerog_tweaks/textures/item', exist_ok=True)
        im.save(f'{OUT}/assets/zerog_tweaks/textures/item/{s}_upgrade_smithing_template.png')
        w(f'assets/zerog_tweaks/models/item/{s}_upgrade_smithing_template.json',
          {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'zerog_tweaks:item/{s}_upgrade_smithing_template'}})
    S = s.capitalize(); k = f'item.zerog_tweaks.smithing_template.{s}_upgrade.'
    lang[f'item.zerog_tweaks.{s}_upgrade_smithing_template'] = 'Smithing Template'
    lang[f'upgrade.zerog_tweaks.{s}_upgrade'] = f'{S} Upgrade'
    lang[k + 'applies_to'] = f'{b.capitalize()} Equipment'
    lang[k + 'ingredients'] = nice(mat(s))
    lang[k + 'base_slot_description'] = f'Add {b.capitalize()} armor, weapon, or tool'
    lang[k + 'additions_slot_description'] = f'Add {nice(mat(s))}'
w('assets/zerog_tweaks/lang/en_us.additions.json', lang)
# 6. Java
sets = ', '.join(f'"{s}"' for s in CHAIN)
w('java/registry/ZGUpgradeTemplates.java', f'''package net.zerog.tweaks.registry;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.SmithingTemplateItem;
import net.neoforged.neoforge.registries.DeferredItem;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Netherite-style upgrade templates for every set on the mining ladder (generated by generators/upgrade_templates.py).
 * Replaces the five plain-Item templates in ItemInit (same ids, so saves and recipes keep working).
 */
public final class ZGUpgradeTemplates {{
    private ZGUpgradeTemplates() {{}}

    /** Ladder order; Nullifite has no template (crafted from ingots, like diamond). */
    public static final List<String> SETS = List.of({sets});

    private static final List<ResourceLocation> BASE_ICONS = List.of(
            ResourceLocation.withDefaultNamespace("item/empty_armor_slot_helmet"),
            ResourceLocation.withDefaultNamespace("item/empty_slot_sword"),
            ResourceLocation.withDefaultNamespace("item/empty_armor_slot_chestplate"),
            ResourceLocation.withDefaultNamespace("item/empty_slot_pickaxe"),
            ResourceLocation.withDefaultNamespace("item/empty_armor_slot_leggings"),
            ResourceLocation.withDefaultNamespace("item/empty_slot_axe"),
            ResourceLocation.withDefaultNamespace("item/empty_armor_slot_boots"),
            ResourceLocation.withDefaultNamespace("item/empty_slot_hoe"),
            ResourceLocation.withDefaultNamespace("item/empty_slot_shovel"));
    private static final List<ResourceLocation> ADDITION_ICONS = List.of(
            ResourceLocation.withDefaultNamespace("item/empty_slot_ingot"));

    public static final Map<String, DeferredItem<SmithingTemplateItem>> ALL = new LinkedHashMap<>();

    static {{
        for (String set : SETS) {{
            String k = "item.zerog_tweaks.smithing_template." + set + "_upgrade.";
            ALL.put(set, ItemInit.ITEMS.register(set + "_upgrade_smithing_template", () -> new SmithingTemplateItem(
                    Component.translatable(k + "applies_to").withStyle(ChatFormatting.BLUE),
                    Component.translatable(k + "ingredients").withStyle(ChatFormatting.BLUE),
                    Component.translatable("upgrade.zerog_tweaks." + set + "_upgrade").withStyle(ChatFormatting.GRAY),
                    Component.translatable(k + "base_slot_description"),
                    Component.translatable(k + "additions_slot_description"),
                    BASE_ICONS, ADDITION_ICONS)));
        }}
    }}

    /** Call from ItemInit.register() so the class loads before the registry is frozen. */
    public static void init() {{}}
}}
''')
# 7. README
rows = '\n'.join(f'| {s.capitalize()} | {b.capitalize()} piece + {nice(mat(s))} | {PLACE[c]} | 7 {nice(mat(b))} + {nice(stone)} |'
                 + (' existing id' if s in EXISTING else '') for s, (b, c, stone) in CHAIN.items())
w('README.md', f'''# Upgrade smithing templates (v1.3)

Every set after Nullifite is made at the smithing table, the same way netherite is made from diamond:
**template + the previous set's piece + the new set's ingot or gem**. Enchantments and trims carry over.
Nullifite is crafted from ingots, like diamond. The chain follows the mining ladder.
The precious sets (Aurelion, Pyrium, Palladine, Radiantine) branch off their world's entry set.

| Set | Smithing table | Template found in | Copy recipe (gives 2): ring x7 + middle |
| --- | --- | --- | --- |
{rows}

The copy recipe follows vanilla: 7 of the base set's material (as diamonds are to netherite), the template, and the stone of the place it's found.
Bosses still drop their tier's main template (Prism Sentinel: Cerulite, Rift Tyrant: Skarnite, and so on).

## Install (goes on `1.21.x`)
1. **Java:** copy `java/registry/ZGUpgradeTemplates.java` into `src/main/java/net/zerog/tweaks/registry/`.
   - In `ItemInit`, delete the five `registerSimpleItem("<set>_upgrade_smithing_template")` lines (`OLYMPIUM_`, `CERULITE_`, `SKARNITE_`, `EIDOLITE_`, `SOLVANITE_UPGRADE_SMITHING_TEMPLATE`).
   - Call `ZGUpgradeTemplates.init();` in `ItemInit.register()` next to `ZGTrims.init()`.
   - The ids don't change; the templates just become real `SmithingTemplateItem`s with the netherite-style tooltip and empty-slot icons.
2. **Data:** copy `data/` onto `src/main/resources/data/`, overwriting the existing files: {len(CHAIN) * 9} smithing recipes, {len(CHAIN)} copy recipes, and 5 chest loot tables.
3. **Old recipes:** delete the crafting-table recipes listed in `recipes_to_delete.txt` ({len(dele)} files). Those sets can now only be made by upgrading, like netherite.
4. **Assets:** copy `assets/` onto `src/main/resources/assets/` (14 new template icons and models). Merge `lang/en_us.additions.json` into `en_us.json`.
5. Re-run `generators/creative_tabs.py` so the new templates sit next to the old ones in the Ingredients tab.
6. Run `./gradlew build` and `runClient`. In the smithing table, check that a Ferrox piece + Moonsteel Ingot + Moonsteel Upgrade gives the Moonsteel piece and keeps its enchantments.
''')
print(len(CHAIN), 'templates;', len(CHAIN) * 9, 'smithing recipes;', len(dele), 'crafting recipes to delete')
