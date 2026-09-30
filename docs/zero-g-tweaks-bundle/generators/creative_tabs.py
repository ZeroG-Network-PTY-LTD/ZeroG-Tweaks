"""Sort every ZeroG item into vanilla-style creative tabs, in vanilla-like order.
Writes src/main/java/net/zerog/tweaks/registry/ZGCreativeTabContents.java (ordered id lists)
and a CSV so agents/people can see where everything went."""
import re, csv, os

REPO = '/home/claude/zerog-tweaks'
ii = open(f'{REPO}/src/main/java/net/zerog/tweaks/registry/ItemInit.java').read()
bi = open(f'{REPO}/src/main/java/net/zerog/tweaks/registry/BlockInit.java').read()
BLOCKS = set(re.findall(r'BLOCKS\.register\w*\("(\w+)"', bi))
ITEMS = re.findall(r'ITEMS\.\w+\("(\w+)"', ii)
EGGS = sorted(k + '_spawn_egg' for k in re.findall(r'egg\("(\w+)", 0x', open(f'{REPO}/src/main/java/net/zerog/tweaks/registry/ZGSpawnEggs.java').read()))
ITEMS += EGGS
TRIMS = [k + '_armor_trim_smithing_template' for k in re.findall(r'template\("(\w+)"\);', open(f'{REPO}/src/main/java/net/zerog/tweaks/registry/ZGTrims.java').read())]
ITEMS += TRIMS
ITEMSET = set(ITEMS)
FOODS = [n.lower() for n in re.findall(r'FoodProperties (\w+) =', open(f'{REPO}/src/main/java/net/zerog/tweaks/item/ZGFoods.java').read())]

# ---------------------------------------------------------------- progression orders
PLANETS = [  # (planet, stones..., materials in role order)
    ('sol', ['nullifite', 'regolith', 'moonsteel', 'selenite', 'ferrox', 'olympium', 'aresite']),
    ('cerulon', ['nebulite', 'cobaltium', 'cyrrium', 'aurelion', 'pulsar_dust', 'starlite', 'cerulite', 'lumenite']),
    ('skarn', ['emberite', 'ruskite', 'tectium', 'pyrium', 'tremor_dust', 'rift_opal', 'skarnite', 'cinnabrite']),
    ('eidolon', ['cryocite', 'salvium', 'wraithsteel', 'palladine', 'spectral_dust', 'remnant_shard', 'eidolite', 'rimeglass']),
    ('solvane', ['coronite', 'photium', 'astrium', 'radiantine', 'fusion_dust', 'nova_pearl', 'solvanite', 'dawnstone']),
]
MATERIALS = [m for _, ms in PLANETS for m in ms]
GEAR = ['nullifite', 'ferrox', 'moonsteel', 'olympium', 'cobaltium', 'cyrrium', 'aurelion', 'cerulite', 'ruskite', 'tectium', 'pyrium',
        'skarnite', 'salvium', 'wraithsteel', 'palladine', 'eidolite', 'photium', 'astrium', 'radiantine', 'solvanite']
STONES = ['lunar_stone', 'mare_basalt', 'martian_stone', 'cerulean_stone', 'skarn_rock', 'scorched_marble', 'permafrost', 'solar_stone',
          'abyssal_stone', 'sunbaked_stone', 'scoria', 'frostrock', 'sludgestone', 'prismstone', 'craterstone']
WOODS = ['shardwood', 'charwood', 'hoarwood', 'gildwood']
SHAPES = ['', '_stairs', '_slab', '_wall']
TOOLS = ['shovel', 'pickaxe', 'axe', 'hoe']
ARMOR = ['helmet', 'chestplate', 'leggings', 'boots']

TABS = {k: [] for k in ('building_blocks', 'natural_blocks', 'functional_blocks', 'tools_and_utilities', 'combat', 'food_and_drinks', 'ingredients', 'spawn_eggs')}
PLACED = {}
def add(tab, *ids):
    for i in ids:
        if i in ITEMSET and i not in TABS[tab]:
            TABS[tab].append(i); PLACED.setdefault(i, []).append(tab)

def shaped(base):
    """vanilla pattern: block, stairs, slab, wall (bricks use '_brick_' for shapes)"""
    out = [base]
    stem = base[:-7] + '_brick' if base.endswith('_bricks') else base
    out += [stem + s for s in SHAPES[1:]]
    return out

# ================================================================ BUILDING BLOCKS
for w in WOODS:  # vanilla: log, wood, stripped log, stripped wood, planks, stairs, slab, fence, gate, door, trapdoor, plate, button
    add('building_blocks', f'{w}_log', f'{w}_wood', f'stripped_{w}_log', f'stripped_{w}_wood', f'{w}_planks', f'{w}_stairs', f'{w}_slab',
        f'{w}_fence', f'{w}_fence_gate', f'{w}_door', f'{w}_trapdoor', f'{w}_pressure_plate', f'{w}_button')
for s in STONES:  # vanilla stone family order
    for base in (s, f'cobbled_{s}', f'smooth_{s}', f'polished_{s}', f'{s}_bricks', f'cracked_{s}_bricks', f'chiseled_{s}',
                 f'polished_black_{s}', f'polished_black_{s}_bricks', f'chiseled_polished_black_{s}'):
        add('building_blocks', *shaped(base))
for b in ('hull_plating', 'corroded_hull', 'polished_hull', 'hull_bricks', 'chiseled_hull', 'olympium_plating', 'radiant_bricks',
          'oxide_crust', 'sunspot_rock', 'ruinstone', 'salt_crust', 'slag', 'frozen_regolith'):
    add('building_blocks', *shaped(b))
for m in MATERIALS:  # storage blocks, vanilla puts them at the end of Building Blocks
    add('building_blocks', f'{m}_block')
for g in ('lunar_glass', 'rust_glass', 'crystal_glass', 'frost_glass', 'tide_glass', 'dune_glass', 'shimmer_glass', 'refracting_glass',
          'slag_glass', 'rift_glass', 'glassy_obsidian'):
    add('building_blocks', g)

# ================================================================ NATURAL BLOCKS
SURFACE = ['regolith', 'crater_ice', 'rustsand', 'oxide_crust', 'polar_frost', 'azure_moss', 'crystal_sand', 'slag', 'ember_crust',
           'frozen_regolith', 'phantom_ice', 'sunspot_rock', 'corona_crust', 'flare_vent', 'tidesand', 'dunesand', 'salt_crust', 'ashfall',
           'vent_rock', 'snowpack', 'glacial_ice', 'toxic_mud', 'blightmoss', 'shimmer_sand', 'crater_dust', 'meteorite_fragment']
add('natural_blocks', *STONES)
add('natural_blocks', *SURFACE)
add('natural_blocks', 'deepslate_nullifite_ore')
for m in MATERIALS:
    add('natural_blocks', f'{m}_ore')
for m in MATERIALS:
    add('natural_blocks', f'raw_{m}_block')
add('natural_blocks', 'cerulean_geode_shell', 'budding_cerulite', 'cerulite_cluster', 'brine_crystal', 'frost_crystal', 'prism_cluster')
for w in WOODS:
    add('natural_blocks', f'{w}_log', f'{w}_leaves', f'{w}_sapling')
add('natural_blocks', 'starbloom', 'ghostbloom', 'solflower', 'frostfern', 'emberthorn', 'cinder_cap', 'lunar_lichen', 'rust_lichen',
    'glowkelp', 'rust_tuber', 'skyberries', 'solflower_seeds', 'pyrefruit')

# ================================================================ FUNCTIONAL BLOCKS
add('functional_blocks', 'selenite_lamp', 'pulsar_lamp', 'tremor_lamp', 'spectral_lantern', 'fusion_lamp', 'captains_lantern',
    'combustion_generator', 'solar_array', 'fusion_reactor', 'ore_refinery', 'alloy_forge', 'crystal_growth_chamber', 'salvage_station',
    'cyrrium_casing', 'tectium_casing', 'wraithsteel_casing', 'astrium_casing',
    'gate_controller', 'gate_pad_plate', 'gate_pylon', 'gate_energy_port', 'gate_lens_housing',
    'nullifite_gate_frame', 'moonsteel_gate_frame', 'cerulite_gate_frame', 'skarnite_gate_frame', 'eidolite_gate_frame', 'solvanite_gate_frame',
    'landing_platform', 'crystal_cell', 'cryo_pod', 'broken_console')

# ================================================================ TOOLS & UTILITIES (tools by tier, then travel/upgrade items)
for s in GEAR:
    add('tools_and_utilities', *[f'{s}_{t}' for t in TOOLS])
add('tools_and_utilities', 'galaxy_3_gate_key', 'galaxy_4_gate_key', 'galaxy_5_gate_key', 'star_map_fragment', 'refracting_lens',
    'cryo_core', 'capacity_coil', 'sentinel_prism', 'colossus_core')

# ================================================================ COMBAT (vanilla: swords, axes, armor per tier)
for s in GEAR:
    add('combat', f'{s}_sword', f'{s}_axe')
for s in GEAR:
    add('combat', *[f'{s}_{p}' for p in ARMOR])
add('combat', 'abyssal_pearl', 'heatproof_plating', 'neutralizer', 'rust_shell')

# ================================================================ FOOD & DRINKS (vanilla-ish: produce, raw -> cooked pairs, dishes, drinks)
PAIRS = [('crawler_leg', 'roasted_crawler_leg'), ('hopper_meat', 'cooked_hopper'), ('grazer_steak', 'seared_grazer_steak'),
         ('beetle_grub', 'toasted_grub'), ('stag_venison', 'cooked_venison'), ('fowl', 'roast_fowl'), ('glimmerfish', 'cooked_glimmerfish'),
         ('boar_chop', 'smoked_boar_chop'), ('scorch_tail', 'grilled_scorch_tail'), ('yak_meat', 'yak_roast'), ('gildcrab_meat', 'cooked_gildcrab'),
         ('eel_fillet', 'cooked_eel'), ('burrower_steak', 'cooked_burrower_steak'), ('lurker_leg', 'crispy_lurker_leg'), ('skitter_leg', 'roasted_skitter_leg')]
add('food_and_drinks', 'skyberries', 'pyrefruit', 'rust_tuber', 'baked_tuber', 'roasted_solflower_seeds', 'lichen_crisps')
for a, b in PAIRS: add('food_and_drinks', a, b)
add('food_and_drinks', 'orbit_burger', 'nebula_pie', 'low_g_jelly', 'astronaut_ration', 'ration_pack', 'cinder_cap_stew', 'ember_chili',
    'cryo_chowder', 'starfall_feast', 'frostfern_tea', 'frost_milk', 'shardwood_syrup')
add('food_and_drinks', *FOODS)  # safety net: every food

# ================================================================ INGREDIENTS (vanilla: fuels, raw, nuggets, ingots, gems/dusts, mob drops, templates)
for _, ms in PLANETS:
    for m in ms:
        add('ingredients', f'raw_{m}', m, f'{m}_nugget', f'{m}_ingot')
add('ingredients', 'stardust', 'solar_spark', 'crystal_hide', 'cinder_pelt', 'frost_pelt', 'hopper_fluff', 'grazer_hide', 'azure_feather',
    'blue_egg', 'glimmer_scale', 'boar_tusk', 'scorch_scale', 'yak_wool', 'leech_gel', 'gildcrab_shell', 'eel_skin', 'burrower_scale',
    'skitter_carapace', 'venom_gland', 'rift_heart', 'heart_of_solvane')
add('ingredients', 'olympium_upgrade_smithing_template', 'cerulite_upgrade_smithing_template', 'skarnite_upgrade_smithing_template',
    'eidolite_upgrade_smithing_template', 'solvanite_upgrade_smithing_template')
add('ingredients', *TRIMS)  # vanilla puts armor trim templates after the upgrade template in Ingredients

# ================================================================ SPAWN EGGS (vanilla: alphabetical)
add('spawn_eggs', *EGGS)

missing = [i for i in ITEMS if i not in PLACED]
if missing:
    print('UNPLACED', len(missing), missing)

# ================================================================ Java
TITLES = {'building_blocks': 'Building Blocks', 'natural_blocks': 'Natural Blocks', 'functional_blocks': 'Functional Blocks',
          'tools_and_utilities': 'Tools & Utilities', 'combat': 'Combat', 'food_and_drinks': 'Food & Drinks', 'ingredients': 'Ingredients', 'spawn_eggs': 'Spawn Eggs'}
ICONS = {'building_blocks': 'cerulean_stone_bricks', 'natural_blocks': 'cerulite_ore', 'functional_blocks': 'gate_controller',
         'tools_and_utilities': 'nullifite_pickaxe', 'combat': 'solvanite_sword', 'food_and_drinks': 'orbit_burger', 'ingredients': 'nullifite_ingot', 'spawn_eggs': 'mossback_spawn_egg'}
for t, i in ICONS.items(): assert i in TABS[t], (t, i)

def jarr(ids):
    lines, cur = [], '            '
    for i in ids:
        tok = f'"{i}", '
        if len(cur) + len(tok) > 130: lines.append(cur.rstrip()); cur = '            '
        cur += tok
    lines.append(cur.rstrip().rstrip(','))
    return '\n'.join(lines)

J = ['package net.zerog.tweaks.registry;', '',
     '/**', ' * GENERATED by docs/zero-g-tweaks-bundle/generators/creative_tabs.py; do not edit by hand.',
     ' * Ordered item ids for each ZeroG creative tab, laid out like the vanilla tabs:',
     ' * families together (block, stairs, slab, wall), wood sets in vanilla order, ores by planet and role,',
     ' * tools and armor by tier, raw food next to its cooked form. Re-run the generator after adding items.',
     ' */', 'public final class ZGCreativeTabContents {', '    private ZGCreativeTabContents() {}', '']
for t, ids in TABS.items():
    J += [f'    /** {TITLES[t]} ({len(ids)} entries) */', f'    public static final String[] {t.upper()} = {{', jarr(ids), '    };', '']
J += ['    /** Every list above, for the catch-all in CreativeTabs. */',
      '    public static final String[][] ALL = {' + ', '.join(t.upper() for t in TABS) + '};', '', '}', '']
open(f'{REPO}/src/main/java/net/zerog/tweaks/registry/ZGCreativeTabContents.java', 'w').write('\n'.join(J))

os.makedirs(f'{REPO}/docs/zero-g-tweaks-bundle/data', exist_ok=True)
with open(f'{REPO}/docs/zero-g-tweaks-bundle/data/creative_tabs.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['tab', 'position', 'item'])
    for t, ids in TABS.items():
        for n, i in enumerate(ids): w.writerow([t, n, f'zerog_tweaks:{i}'])
print({t: len(v) for t, v in TABS.items()}, 'unique items placed', len(PLACED), 'of', len(ITEMS))

# lang
import json
lp = f'{REPO}/src/main/resources/assets/zerog_tweaks/lang/en_us.json'
L = json.load(open(lp))
L.pop('itemGroup.zerog_tweaks', None)
for t, title in TITLES.items(): L[f'itemGroup.zerog_tweaks.{t}'] = f'ZeroG: {title}'
open(lp, 'w').write(json.dumps(L, indent=2, ensure_ascii=False) + '\n')
