"""ZeroG Tweaks — extra data: recipes, worldgen, tags, loot, advancements, damage types, data maps.

Writes straight into the repo's src/main/resources. Everything here is plain vanilla/NeoForge
1.21.1 JSON, so it loads without extra Java. Content that references things that are still
Java-only (entities, structures) goes to docs/zero-g-tweaks-bundle/pending-data instead.
"""
import json, os, re

REPO = '/home/claude/zerog-tweaks'
RES = f'{REPO}/src/main/resources'
PENDING = f'{REPO}/docs/zero-g-tweaks-bundle/pending-data'
NS = 'zerog_tweaks'
D = f'{RES}/data/{NS}'
MC = f'{RES}/data/minecraft'
NEO = f'{RES}/data/neoforge'
WRITTEN = []

def w(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(json.dumps(obj, indent=2) + '\n')
    WRITTEN.append(path)

def z(n): return n if ':' in n else f'{NS}:{n}'
def ing(n): return {'tag': n[1:]} if n.startswith('#') else {'item': z(n) if not n.startswith('minecraft:') else n}

bi = open(f'{REPO}/src/main/java/net/zerog/tweaks/registry/BlockInit.java').read()
ii = open(f'{REPO}/src/main/java/net/zerog/tweaks/registry/ItemInit.java').read()
BLOCKS = set(re.findall(r'BLOCKS\.register\w*\("(\w+)"', bi)) | {f'potted_{n}' for n in re.findall(r'potted\("(\w+)"', bi)}
ITEMS = set(re.findall(r'ITEMS\.\w+\("(\w+)"', ii))
ALL = BLOCKS | ITEMS

def check(*names):
    for n in names:
        if n.startswith('#') or n.startswith('minecraft:'): continue
        assert n in ALL, f'unknown id {n}'

# ============================================================== RECIPES
R = f'{D}/recipe'

def shaped(out, pattern, key, count=1, cat='misc', name=None):
    check(out, *key.values())
    w(f'{R}/{name or out}.json', {'type': 'minecraft:crafting_shaped', 'category': cat, 'pattern': pattern,
        'key': {k: ing(v) for k, v in key.items()}, 'result': {'id': z(out), 'count': count}})

def shapeless(out, ingredients, count=1, cat='misc', name=None):
    check(out, *ingredients)
    w(f'{R}/{name or out}.json', {'type': 'minecraft:crafting_shapeless', 'category': cat,
        'ingredients': [ing(i) for i in ingredients], 'result': {'id': z(out), 'count': count}})

def cook(out, inp, xp=0.1, t=200, kinds=('smelting',), cat='blocks', name=None):
    check(out, inp)
    for k in kinds:
        tt = t if k == 'smelting' else t // 2
        w(f'{R}/{name or out}_from_{k}.json', {'type': f'minecraft:{k}', 'category': cat, 'ingredient': ing(inp),
            'result': {'id': z(out)}, 'experience': xp, 'cookingtime': tt})

def cut(out, inp, count=1):
    check(out, inp)
    w(f'{R}/{out}_from_{inp}_stonecutting.json', {'type': 'minecraft:stonecutting', 'ingredient': ing(inp),
        'result': {'id': z(out), 'count': count}})

# --- machine casings: each tier's casing wraps the previous one (vanilla-netherite style chain)
CASINGS = [('cyrrium', 'pulsar_dust', 'minecraft:iron_block'), ('tectium', 'tremor_dust', 'cyrrium_casing'),
           ('wraithsteel', 'spectral_dust', 'tectium_casing'), ('astrium', 'fusion_dust', 'wraithsteel_casing')]
for metal, dust, core in CASINGS:
    shaped(f'{metal}_casing', ['IDI', 'D#D', 'IDI'], {'I': f'{metal}_ingot', 'D': dust, '#': core}, 2, 'building')

# --- teleporter gate: frame ring per tier, in that tier's metal/gem + its planet bricks
FRAMES = [('nullifite', 'nullifite_ingot', 'minecraft:polished_deepslate'), ('moonsteel', 'moonsteel_ingot', 'lunar_stone_bricks'),
          ('cerulite', 'cerulite', 'cerulean_stone_bricks'), ('skarnite', 'skarnite', 'skarn_rock_bricks'),
          ('eidolite', 'eidolite', 'permafrost_bricks'), ('solvanite', 'solvanite', 'solar_stone_bricks')]
for t, mat, brick in FRAMES:
    shaped(f'{t}_gate_frame', ['MBM', 'B B', 'MBM'], {'M': mat, 'B': brick}, 4, 'building')
shaped('gate_controller', ['NGN', 'RFR', 'NBN'], {'N': 'nullifite_ingot', 'G': 'minecraft:tinted_glass', 'R': 'minecraft:redstone',
       'F': 'nullifite_gate_frame', 'B': 'minecraft:redstone_block'})
shaped('gate_energy_port', ['NRN', 'RFR', 'NRN'], {'N': 'nullifite_nugget', 'R': 'minecraft:redstone', 'F': 'nullifite_gate_frame'})
shaped('gate_pad_plate', ['SSS', 'NFN'], {'S': 'minecraft:polished_deepslate_slab', 'N': 'nullifite_ingot', 'F': 'nullifite_gate_frame'}, 4, 'building')
shaped('gate_pylon', [' A ', 'NFN', 'NFN'], {'A': 'minecraft:amethyst_shard', 'N': 'nullifite_ingot', 'F': 'nullifite_gate_frame'}, 2, 'building')
shaped('gate_lens_housing', ['MSM', 'SGS', 'MSM'], {'M': 'moonsteel_ingot', 'S': 'selenite', 'G': 'lunar_glass'})
shaped('crystal_cell', ['GSG', 'SRS', 'GSG'], {'G': 'minecraft:glass', 'S': 'selenite', 'R': 'minecraft:redstone_block'})
shaped('landing_platform', ['PPP', 'NCN'], {'P': 'gate_pad_plate', 'N': 'nullifite_ingot', 'C': 'crystal_cell'})
shaped('refracting_lens', [' G ', 'GSG', ' G '], {'G': 'refracting_glass', 'S': 'stardust'})

# --- machines (design: Machines section; casing tier = machine tier)
shaped('combustion_generator', ['III', 'IFI', 'D#D'], {'I': 'cyrrium_ingot', 'F': 'minecraft:furnace', 'D': 'pulsar_dust', '#': 'cyrrium_casing'})
shaped('solar_array', ['GGG', 'ADA', 'I#I'], {'G': 'crystal_glass', 'A': 'aurelion_ingot', 'D': 'pulsar_dust', 'I': 'cyrrium_ingot', '#': 'cyrrium_casing'})
shaped('ore_refinery', ['IPI', 'D#D', 'IBI'], {'I': 'cyrrium_ingot', 'P': 'minecraft:piston', 'D': 'pulsar_dust', '#': 'cyrrium_casing', 'B': 'minecraft:blast_furnace'})
shaped('crystal_growth_chamber', ['GCG', 'S#S', 'IDI'], {'G': 'crystal_glass', 'C': 'cerulite_cluster', 'S': 'starlite', '#': 'cyrrium_casing',
       'I': 'aurelion_ingot', 'D': 'pulsar_dust'})
shaped('alloy_forge', ['TTT', 'B#B', 'TDT'], {'T': 'tectium_ingot', 'B': 'minecraft:blast_furnace', 'D': 'tremor_dust', '#': 'tectium_casing'})
shaped('salvage_station', ['WAW', 'S#S', 'WWW'], {'W': 'wraithsteel_ingot', 'A': 'minecraft:anvil', 'S': 'salvium_ingot', '#': 'wraithsteel_casing'})
shaped('fusion_reactor', ['AFA', 'R#R', 'AHA'], {'A': 'astrium_ingot', 'F': 'fusion_dust', 'R': 'radiantine_ingot', '#': 'astrium_casing', 'H': 'solvanite'})

# --- lights (redstone-lamp / lantern shapes)
shaped('selenite_lamp', [' S ', 'SGS', ' S '], {'S': 'selenite', 'G': 'lunar_glass'}, cat='building')
shaped('pulsar_lamp', [' D ', 'DGD', ' D '], {'D': 'pulsar_dust', 'G': 'minecraft:glowstone'}, cat='building')
shaped('tremor_lamp', [' D ', 'DGD', ' D '], {'D': 'tremor_dust', 'G': 'minecraft:glowstone'}, cat='building')
shaped('spectral_lantern', ['NNN', 'NDN', 'NNN'], {'N': 'wraithsteel_nugget', 'D': 'spectral_dust'}, cat='building')
shaped('fusion_lamp', ['RDR', 'DGD', 'RDR'], {'R': 'radiantine_nugget', 'D': 'fusion_dust', 'G': 'minecraft:sea_lantern'}, cat='building')

# --- derelict / industrial decor
shaped('hull_plating', ['SSS', 'S S', 'SSS'], {'S': 'salvium_ingot'}, 8, 'building')
shaped('polished_hull', ['HH', 'HH'], {'H': 'hull_plating'}, 4, 'building')
shaped('hull_bricks', ['HH', 'HH'], {'H': 'polished_hull'}, 4, 'building')
shaped('chiseled_hull', ['H', 'H'], {'H': 'hull_plating_slab'}, 1, 'building')
shapeless('corroded_hull', ['hull_plating', 'minecraft:water_bucket'], 1, 'building')
for o in ('polished_hull', 'hull_bricks', 'chiseled_hull'):
    cut(o, 'hull_plating')
shaped('olympium_plating', ['OO', 'OO'], {'O': 'olympium_ingot'}, 4, 'building')
shaped('radiant_bricks', ['BNB', 'NBN', 'BNB'], {'B': 'solar_stone_bricks', 'N': 'radiantine_nugget'}, 5, 'building')
shaped('refracting_glass', ['GCG', 'CGC', 'GCG'], {'G': 'shimmer_glass', 'C': 'prism_cluster'}, 5, 'building')
shaped('cryo_pod', ['HGH', 'HCH', 'HHH'], {'H': 'hull_plating', 'G': 'minecraft:glass', 'C': 'cryocite'}, 1, 'building')
cook('slag_glass', 'slag', kinds=('smelting',))
cook('glacial_ice', 'crater_ice', kinds=('smelting',))

# --- upgrade template duplication (netherite-template shape): 7 of the tier's standard metal + planet stone
TEMPLATES = [('olympium', 'moonsteel_ingot', 'martian_stone'), ('cerulite', 'cyrrium_ingot', 'cerulean_stone'),
             ('skarnite', 'tectium_ingot', 'skarn_rock'), ('eidolite', 'wraithsteel_ingot', 'permafrost'),
             ('solvanite', 'astrium_ingot', 'solar_stone')]
for t, metal, stone in TEMPLATES:
    tp = f'{t}_upgrade_smithing_template'
    shaped(tp, ['MTM', 'MSM', 'MMM'], {'M': metal, 'T': tp, 'S': stone}, 2, name=f'{tp}_duplication')

# --- forage / dyes / seeds
shapeless('solflower_seeds', ['solflower'], 2, name='solflower_seeds_from_solflower')
shapeless('minecraft:light_blue_dye', ['starbloom'], 1, name='light_blue_dye_from_starbloom')
shapeless('minecraft:white_dye', ['ghostbloom'], 1, name='white_dye_from_ghostbloom')
shapeless('minecraft:orange_dye', ['cinder_cap'], 1, name='orange_dye_from_cinder_cap')
shapeless('minecraft:string', ['yak_wool'], 4, name='string_from_yak_wool')
shapeless('minecraft:white_wool', ['yak_wool', 'yak_wool', 'yak_wool', 'yak_wool'], 1, name='white_wool_from_yak_wool')
shapeless('minecraft:feather', ['azure_feather'], 1, name='feather_from_azure_feather')
shapeless('minecraft:leather', ['grazer_hide'], 1, name='leather_from_grazer_hide')
shapeless('minecraft:bone_meal', ['boar_tusk'], 3, name='bone_meal_from_boar_tusk')
shapeless('minecraft:slime_ball', ['leech_gel'], 1, name='slime_ball_from_leech_gel')

# ============================================================== DATA MAPS (NeoForge 1.21.1)
FUELS = {'nebulite': 3200, 'emberite': 4000, 'cryocite': 4800, 'coronite': 8000}
fuel_vals = {}
for f, t in FUELS.items():
    fuel_vals[z(f)] = {'burn_time': t}
    fuel_vals[z(f'{f}_block')] = {'burn_time': t * 10}
for wood in ('charwood', 'gildwood', 'hoarwood', 'shardwood'):
    pass  # planks/logs already burn via #minecraft:logs_that_burn / #planks
check(*[k.split(':')[1] for k in fuel_vals])
w(f'{NEO}/data_maps/item/furnace_fuels.json', {'replace': False, 'values': fuel_vals})

COMPOST = {'starbloom': .65, 'ghostbloom': .65, 'solflower': .65, 'frostfern': .65, 'emberthorn': .3, 'cinder_cap': .65,
           'lunar_lichen': .5, 'rust_lichen': .5, 'glowkelp': .3, 'pyrefruit': .3, 'skyberries': .3, 'rust_tuber': .65,
           'solflower_seeds': .3, 'azure_moss': .65, 'blightmoss': .65}
for wood in ('charwood', 'gildwood', 'hoarwood', 'shardwood'):
    COMPOST[f'{wood}_sapling'] = .3; COMPOST[f'{wood}_leaves'] = .3
check(*COMPOST)
w(f'{NEO}/data_maps/item/compostables.json', {'replace': False, 'values': {z(k): {'chance': v} for k, v in COMPOST.items()}})

# ============================================================== DAMAGE TYPES
DMG = {'ember_crust': ('burning', 0.1), 'corona_crust': ('burning', 0.1), 'flare_vent': ('burning', 0.1),
       'vent_rock': ('burning', 0.1), 'acid': ('hurt', 0.0), 'polar_frost': ('freezing', 0.0), 'void_rift': ('hurt', 0.0)}
for k, (eff, ex) in DMG.items():
    w(f'{D}/damage_type/{k}.json', {'message_id': f'{NS}.{k}', 'scaling': 'when_caused_by_living_non_player',
                                    'exhaustion': ex, 'effects': eff})
w(f'{MC}/tags/damage_type/is_fire.json', {'replace': False, 'values': [z(k) for k in ('ember_crust', 'corona_crust', 'flare_vent', 'vent_rock')]})
w(f'{MC}/tags/damage_type/is_freezing.json', {'replace': False, 'values': [z('polar_frost')]})
w(f'{MC}/tags/damage_type/bypasses_armor.json', {'replace': False, 'values': [z('acid'), z('void_rift')]})
w(f'{MC}/tags/damage_type/no_knockback.json', {'replace': False, 'values': [z(k) for k in DMG]})

# ============================================================== TAGS
def tag(path, values, required=True):
    p = f'{RES}/data/{path}.json'
    old = json.load(open(p))['values'] if os.path.exists(p) else []
    vals = list(old)
    for v in values:
        if v not in vals: vals.append(v)
    w(p, {'replace': False, 'values': vals})

SETS = ['nullifite', 'olympium', 'cerulite', 'skarnite', 'eidolite', 'solvanite', 'ferrox', 'moonsteel', 'cobaltium', 'cyrrium',
        'aurelion', 'ruskite', 'tectium', 'pyrium', 'salvium', 'wraithsteel', 'palladine', 'photium', 'astrium', 'radiantine']
TOOLS = {'sword': 'swords', 'pickaxe': 'pickaxes', 'axe': 'axes', 'shovel': 'shovels', 'hoe': 'hoes'}
ARMOR = {'helmet': 'head_armor', 'chestplate': 'chest_armor', 'leggings': 'leg_armor', 'boots': 'foot_armor'}
for piece, t in {**TOOLS, **ARMOR}.items():
    ids = [f'{s}_{piece}' for s in SETS]; check(*ids)
    tag(f'minecraft/tags/item/{t}', [z(i) for i in ids])
tag('minecraft/tags/item/trimmable_armor', [z(f'{s}_{p}') for s in SETS for p in ARMOR])
tag('minecraft/tags/item/coals', [z(f) for f in FUELS])
INGOTS = [f'{s}_ingot' for s in SETS if f'{s}_ingot' in ITEMS]
GEMS = ['aresite', 'selenite', 'cerulite', 'skarnite', 'eidolite', 'solvanite', 'starlite', 'lumenite', 'rift_opal', 'cinnabrite',
        'remnant_shard', 'rimeglass', 'nova_pearl', 'dawnstone']
check(*INGOTS, *GEMS)
tag('minecraft/tags/item/beacon_payment_items', [z(i) for i in INGOTS + ['cerulite', 'skarnite', 'eidolite', 'solvanite']])
tag('minecraft/tags/item/piglin_loved', [z(i) for i in ['aurelion_ingot', 'pyrium_ingot', 'palladine_ingot', 'radiantine_ingot']])
tag('minecraft/tags/item/meat', [z(i) for i in ['crawler_leg', 'hopper_meat', 'grazer_steak', 'stag_venison', 'fowl', 'boar_chop',
    'yak_meat', 'burrower_steak', 'lurker_leg', 'skitter_leg', 'roasted_crawler_leg', 'cooked_hopper', 'seared_grazer_steak',
    'cooked_venison', 'roast_fowl', 'smoked_boar_chop', 'yak_roast', 'cooked_burrower_steak', 'crispy_lurker_leg', 'roasted_skitter_leg']])
tag('minecraft/tags/item/fishes', [z(i) for i in ['glimmerfish', 'cooked_glimmerfish', 'eel_fillet', 'cooked_eel']])
tag('minecraft/tags/item/villager_plantable_seeds', [z('rust_tuber'), z('solflower_seeds')])

STONES = ['lunar_stone', 'mare_basalt', 'martian_stone', 'cerulean_stone', 'skarn_rock', 'scorched_marble', 'permafrost', 'solar_stone',
          'abyssal_stone', 'sunbaked_stone', 'scoria', 'frostrock', 'sludgestone', 'prismstone', 'craterstone']
SURF = ['regolith', 'rustsand', 'oxide_crust', 'polar_frost', 'crystal_sand', 'azure_moss', 'slag', 'ember_crust', 'frozen_regolith',
        'corona_crust', 'sunspot_rock', 'tidesand', 'dunesand', 'salt_crust', 'shimmer_sand', 'toxic_mud', 'blightmoss', 'crater_dust',
        'glacial_ice', 'crater_ice', 'vent_rock', 'glassy_obsidian', 'rift_glass', 'phantom_ice', 'slag_glass', 'ruinstone', 'snowpack', 'ashfall']
check(*STONES, *SURF)
tag('minecraft/tags/block/overworld_carver_replaceables', [z(s) for s in STONES + SURF if s not in ('snowpack', 'ashfall')])
tag('minecraft/tags/block/base_stone_overworld', [z(s) for s in STONES])
tag('minecraft/tags/block/dirt', [z('azure_moss'), z('blightmoss'), z('toxic_mud')])
tag('minecraft/tags/block/sand', [z(s) for s in ['regolith', 'rustsand', 'crystal_sand', 'tidesand', 'dunesand', 'shimmer_sand', 'crater_dust']])
tag('minecraft/tags/block/ice', [z(s) for s in ['crater_ice', 'glacial_ice', 'phantom_ice', 'polar_frost']])
tag('minecraft/tags/block/infiniburn_overworld', [z('ember_crust'), z('corona_crust'), z('vent_rock')])
tag('minecraft/tags/block/snow', [z('snowpack')])
tag('minecraft/tags/item/stone_crafting_materials', [z(f'cobbled_{s}') for s in STONES])
tag('minecraft/tags/item/stone_tool_materials', [z(f'cobbled_{s}') for s in STONES])
check(*[f'cobbled_{s}' for s in STONES])
# planet-ground tag used by worldgen/saplings
tag(f'{NS}/tags/block/planet_ground', [z(s) for s in STONES + SURF])

# ============================================================== LOOT
L = f'{D}/loot_table'
def item(n, lo=1, hi=1, w_=1, extra=None):
    e = {'type': 'minecraft:item', 'name': z(n), 'weight': w_}
    fs = []
    if (lo, hi) != (1, 1): fs.append({'function': 'minecraft:set_count', 'count': {'type': 'minecraft:uniform', 'min': lo, 'max': hi}})
    if extra: fs += extra
    if fs: e['functions'] = fs
    check(n); return e

def chest(name, pools):
    w(f'{L}/chests/{name}.json', {'type': 'minecraft:chest', 'pools': pools, 'random_sequence': f'{NS}:chests/{name}'})

def pool(rolls, entries):
    r = rolls if isinstance(rolls, (int, float)) else {'type': 'minecraft:uniform', 'min': rolls[0], 'max': rolls[1]}
    return {'rolls': r, 'bonus_rolls': 0, 'entries': entries}

COMMON = [item('minecraft:iron_ingot', 1, 4, 10), item('minecraft:bread', 1, 3, 8), item('ration_pack', 1, 2, 6), item('minecraft:torch', 4, 12, 8)]
chest('sunken_relay', [pool(1, [item('abyssal_pearl')]), pool((3, 6), COMMON + [item('glimmer_scale', 1, 4, 6), item('eel_skin', 1, 3, 5),
      item('brine_crystal', 1, 3, 5), item('remnant_shard', 1, 2, 2)])])
chest('buried_observatory', [pool((1, 2), [item('star_map_fragment')]), pool((3, 6), COMMON + [item('starlite', 1, 4, 6),
      item('minecraft:spyglass', 1, 1, 2), item('minecraft:map', 1, 1, 4), item('ruinstone', 2, 8, 5)])])
chest('collapsed_forge', [pool(1, [item('heatproof_plating')]), pool((3, 6), COMMON + [item('tectium_ingot', 1, 3, 6), item('pyrium_nugget', 2, 6, 6),
      item('slag', 2, 8, 5), item('skarnite_upgrade_smithing_template', 1, 1, 1)])])
chest('frozen_outpost', [pool(1, [item('cryo_core')]), pool((3, 6), COMMON + [item('frost_milk', 1, 2, 5), item('yak_wool', 1, 4, 6),
      item('cryocite', 2, 6, 6), item('frost_crystal', 1, 3, 4)])])
chest('sunken_lab', [pool(1, [item('neutralizer')]), pool((3, 6), COMMON + [item('venom_gland', 1, 2, 5), item('leech_gel', 1, 3, 5),
      item('minecraft:glass_bottle', 1, 4, 6), item('remnant_shard', 1, 2, 3)])])
chest('prism_spire', [pool(1, [item('refracting_lens')]), pool((3, 6), COMMON + [item('prism_cluster', 1, 3, 6), item('shimmer_sand', 2, 8, 5),
      item('starlite', 1, 3, 5), item('cerulite_upgrade_smithing_template', 1, 1, 1)])])
chest('impact_site', [pool((2, 4), [item('stardust', 1, 3)]), pool((3, 6), COMMON + [item('meteorite_fragment', 1, 3, 6),
      item('minecraft:iron_nugget', 3, 9, 6), item('star_map_fragment', 1, 1, 1)])])
chest('derelict_wreck', [pool((3, 7), COMMON + [item('salvium_ingot', 1, 4, 8), item('ration_pack', 1, 3, 6), item('remnant_shard', 1, 3, 6),
      item('hull_plating', 2, 6, 5), item('spectral_dust', 1, 4, 4), item('eidolite_upgrade_smithing_template', 1, 1, 1)])])
chest('mars_crash_site', [pool((3, 6), COMMON + [item('ferrox_ingot', 1, 4, 8), item('olympium_nugget', 2, 6, 6), item('aresite', 1, 1, 2),
      item('olympium_upgrade_smithing_template', 1, 1, 3), item('rust_tuber', 1, 4, 5)])])
chest('solar_shrine', [pool((3, 6), COMMON + [item('photium_ingot', 1, 4, 8), item('radiantine_nugget', 2, 6, 6), item('coronite', 1, 3, 6),
      item('solvanite_upgrade_smithing_template', 1, 1, 2), item('pyrefruit', 1, 4, 5)])])

SILK = {'condition': 'minecraft:match_tool', 'predicate': {'predicates': {'minecraft:enchantments': [
        {'enchantments': 'minecraft:silk_touch', 'levels': {'min': 1}}]}}}
def block_alt(block, entries):
    w(f'{L}/blocks/{block}.json', {'type': 'minecraft:block', 'pools': [{'rolls': 1, 'bonus_rolls': 0, 'entries': [{
        'type': 'minecraft:alternatives', 'children': [dict(item(block), conditions=[SILK])] + entries}]}],
        'random_sequence': f'{NS}:blocks/{block}'})
FORT = [{'function': 'minecraft:apply_bonus', 'enchantment': 'minecraft:fortune', 'formula': 'minecraft:ore_drops'},
        {'function': 'minecraft:explosion_decay'}]
block_alt('meteorite_fragment', [item('stardust', 1, 2, extra=FORT)])
block_alt('broken_console', [item('remnant_shard', 1, 3, extra=FORT)])
w(f'{L}/blocks/cryo_pod.json', {'type': 'minecraft:block', 'pools': [pool(1, [item('cryo_pod')]) | {'conditions': [{'condition': 'minecraft:survives_explosion'}]},
    pool(1, [item('ration_pack', 1, 1, 3), item('frost_milk', 1, 1, 2), {'type': 'minecraft:empty', 'weight': 5}])],
    'random_sequence': f'{NS}:blocks/cryo_pod'})

# boss/mini-boss template drops (the smithing chain needs one template per tier)
for ent, tp in [('prism_sentinel', 'cerulite_upgrade_smithing_template'), ('rift_tyrant', 'skarnite_upgrade_smithing_template'),
                ('eidolon_captain', 'eidolite_upgrade_smithing_template'), ('sun_colossus', 'solvanite_upgrade_smithing_template'),
                ('dying_star', 'solvanite_upgrade_smithing_template')]:
    p = f'{L}/entities/{ent}.json'; j = json.load(open(p))
    if not any(e.get('name') == z(tp) for pl in j['pools'] for e in pl['entries']):
        j['pools'].append(pool(1, [item(tp)]))
    w(p, j)

# ============================================================== WORLDGEN
WG = f'{D}/worldgen'
def st(n, props=None):
    s = {'Name': z(n) if not n.startswith('minecraft:') else n}
    if props: s['Properties'] = props
    return s

# ---- ores: (ore, host stone, role) ; role ranges follow the design doc's ore-generation table
ROLE = {  # (min_y, max_y, count, size, air_discard, shape)
    'fuel': (0, 192, 20, 15, 0.0, 'uniform'), 'common': (-16, 112, 16, 10, 0.0, 'trapezoid'),
    'standard': (-24, 56, 10, 9, 0.0, 'trapezoid'), 'precious': (-64, 32, 4, 8, 0.5, 'trapezoid'),
    'dust': (-64, 16, 6, 8, 0.0, 'uniform'), 'lore': (-32, 32, 2, 6, 0.0, 'trapezoid'),
    'rare': (-64, 16, 1, 3, 1.0, 'trapezoid'), 'trade': (-16, 96, 3, 3, 0.0, 'uniform')}
PLANET_ORES = {
    'moon': ('lunar_stone', [('regolith', 'fuel'), ('moonsteel', 'standard'), ('selenite', 'lore')]),
    'mars': ('martian_stone', [('ferrox', 'common'), ('olympium', 'precious'), ('aresite', 'rare')]),
    'cerulon': ('cerulean_stone', [('nebulite', 'fuel'), ('cobaltium', 'common'), ('cyrrium', 'standard'), ('aurelion', 'precious'),
                ('pulsar_dust', 'dust'), ('starlite', 'lore'), ('cerulite', 'rare'), ('lumenite', 'trade')]),
    'skarn': ('skarn_rock', [('emberite', 'fuel'), ('ruskite', 'common'), ('tectium', 'standard'), ('pyrium', 'precious'),
              ('tremor_dust', 'dust'), ('rift_opal', 'lore'), ('skarnite', 'rare'), ('cinnabrite', 'trade')]),
    'eidolon': ('permafrost', [('cryocite', 'fuel'), ('salvium', 'common'), ('wraithsteel', 'standard'), ('palladine', 'precious'),
                ('spectral_dust', 'dust'), ('remnant_shard', 'lore'), ('eidolite', 'rare'), ('rimeglass', 'trade')]),
    'solvane': ('solar_stone', [('coronite', 'fuel'), ('photium', 'common'), ('astrium', 'standard'), ('radiantine', 'precious'),
                ('fusion_dust', 'dust'), ('nova_pearl', 'lore'), ('solvanite', 'rare'), ('dawnstone', 'trade')]),
}
TWIST = {'salvium': 0.4, 'cerulite': 1.0}  # Eidolon salvium mostly from wrecks; Cerulite also in geodes
ORE_FEATURES = {}
def height(shape, lo, hi):
    return {'type': f'minecraft:{shape}', 'min_inclusive': {'absolute': lo}, 'max_inclusive': {'absolute': hi}}

def ore_feature(name, ore_block, target, role, count_mult=1.0):
    lo, hi, cnt, size, air, shape = ROLE[role]
    check(ore_block)
    w(f'{WG}/configured_feature/ore_{name}.json', {'type': 'minecraft:ore', 'config': {
        'size': size, 'discard_chance_on_air_exposure': air,
        'targets': [{'target': target, 'state': st(ore_block)}]}})
    cnt = max(1, round(cnt * count_mult))
    mods = ([{'type': 'minecraft:count', 'count': cnt}] if cnt > 1 else []) + [
        {'type': 'minecraft:in_square'}, {'type': 'minecraft:height_range', 'height': height(shape, lo, hi)}, {'type': 'minecraft:biome'}]
    if role == 'rare':
        mods = [{'type': 'minecraft:rarity_filter', 'chance': 2}] + mods[0 if cnt > 1 else 0:]
    w(f'{WG}/placed_feature/ore_{name}.json', {'feature': z(f'ore_{name}'), 'placement': mods})
    return z(f'ore_{name}')

for planet, (stone, ores) in PLANET_ORES.items():
    tgt = {'predicate_type': 'minecraft:block_match', 'block': z(stone)}
    ORE_FEATURES[planet] = [ore_feature(o, f'{o}_ore', tgt, r, TWIST.get(o, 1.0)) for o, r in ores]

# Nullifite: Y -64..-40, deepslate only, veins 1-2, rarer than diamond; extra pass in the Deep Dark
check('deepslate_nullifite_ore')
w(f'{WG}/configured_feature/ore_nullifite.json', {'type': 'minecraft:ore', 'config': {'size': 2, 'discard_chance_on_air_exposure': 0.7,
    'targets': [{'target': {'predicate_type': 'minecraft:tag_match', 'tag': 'minecraft:deepslate_ore_replaceables'},
                 'state': st('deepslate_nullifite_ore')}]}})
w(f'{WG}/placed_feature/ore_nullifite.json', {'feature': z('ore_nullifite'), 'placement': [
    {'type': 'minecraft:rarity_filter', 'chance': 2}, {'type': 'minecraft:in_square'},
    {'type': 'minecraft:height_range', 'height': height('uniform', -64, -40)}, {'type': 'minecraft:biome'}]})
w(f'{WG}/placed_feature/ore_nullifite_deep_dark.json', {'feature': z('ore_nullifite'), 'placement': [
    {'type': 'minecraft:count', 'count': 2}, {'type': 'minecraft:in_square'},
    {'type': 'minecraft:height_range', 'height': height('uniform', -64, -40)}, {'type': 'minecraft:biome'}]})
BM = f'{D}/neoforge/biome_modifier'
w(f'{BM}/add_nullifite_ore.json', {'type': 'neoforge:add_features', 'biomes': '#minecraft:is_overworld',
    'features': z('ore_nullifite'), 'step': 'underground_ores'})
w(f'{BM}/add_nullifite_ore_deep_dark.json', {'type': 'neoforge:add_features', 'biomes': 'minecraft:deep_dark',
    'features': z('ore_nullifite_deep_dark'), 'step': 'underground_ores'})

# ---- Cerulon geodes (vanilla amethyst geode feature with Cerulon blocks)
check('cerulean_geode_shell', 'budding_cerulite', 'cerulite_cluster', 'cerulite_block')
w(f'{WG}/configured_feature/cerulite_geode.json', {'type': 'minecraft:geode', 'config': {
    'blocks': {'filling_provider': {'type': 'minecraft:simple_state_provider', 'state': st('minecraft:air')},
               'inner_layer_provider': {'type': 'minecraft:simple_state_provider', 'state': st('cerulite_block')},
               'alternate_inner_layer_provider': {'type': 'minecraft:simple_state_provider', 'state': st('budding_cerulite')},
               'middle_layer_provider': {'type': 'minecraft:simple_state_provider', 'state': st('cerulean_geode_shell')},
               'outer_layer_provider': {'type': 'minecraft:simple_state_provider', 'state': st('cerulean_stone')},
               'inner_placements': [st('cerulite_cluster')],
               'cannot_replace': '#minecraft:features_cannot_replace', 'invalid_blocks': '#minecraft:geode_invalid_blocks'},
    'layers': {'filling': 1.7, 'inner_layer': 2.2, 'middle_layer': 3.2, 'outer_layer': 4.2},
    'crack': {'generate_crack_chance': 0.95, 'base_crack_size': 2.0, 'crack_point_offset': 2},
    'use_potential_placements_chance': 0.35, 'use_alternate_layer0_chance': 0.083, 'placements_require_layer0_alternate': True,
    'outer_wall_distance': {'type': 'minecraft:uniform', 'min_inclusive': 4, 'max_inclusive': 6},
    'distribution_points': {'type': 'minecraft:uniform', 'min_inclusive': 3, 'max_inclusive': 4},
    'point_offset': {'type': 'minecraft:uniform', 'min_inclusive': 1, 'max_inclusive': 2},
    'min_gen_offset': -16, 'max_gen_offset': 16, 'noise_multiplier': 0.05, 'invalid_blocks_threshold': 1}})
w(f'{WG}/placed_feature/cerulite_geode.json', {'feature': z('cerulite_geode'), 'placement': [
    {'type': 'minecraft:rarity_filter', 'chance': 18}, {'type': 'minecraft:in_square'},
    {'type': 'minecraft:height_range', 'height': height('uniform', -48, 32)}, {'type': 'minecraft:biome'}]})

# ---- vegetation helpers
def patch(name, block, tries=32, rarity=4, props=None, place_on=None):
    check(block)
    pl = [{'type': 'minecraft:block_predicate_filter', 'predicate': {'type': 'minecraft:matching_blocks', 'blocks': 'minecraft:air'}}]
    w(f'{WG}/configured_feature/{name}.json', {'type': 'minecraft:random_patch', 'config': {'tries': tries, 'xz_spread': 7, 'y_spread': 3,
        'feature': {'feature': {'type': 'minecraft:simple_block', 'config': {'to_place': {'type': 'minecraft:simple_state_provider',
                    'state': st(block, props)}}}, 'placement': pl}}})
    w(f'{WG}/placed_feature/{name}.json', {'feature': z(name), 'placement': [
        {'type': 'minecraft:rarity_filter', 'chance': rarity}, {'type': 'minecraft:in_square'},
        {'type': 'minecraft:heightmap', 'heightmap': 'MOTION_BLOCKING'}, {'type': 'minecraft:biome'}]})
    return z(name)

def lichen(name, block, on):
    check(block, *on)
    w(f'{WG}/configured_feature/{name}.json', {'type': 'minecraft:multiface_growth', 'config': {'block': z(block), 'search_range': 20,
        'chance_of_spreading': 0.5, 'can_place_on_floor': True, 'can_place_on_ceiling': True, 'can_place_on_wall': True,
        'can_be_placed_on': [z(b) for b in on]}})
    w(f'{WG}/placed_feature/{name}.json', {'feature': z(name), 'placement': [
        {'type': 'minecraft:count', 'count': {'type': 'minecraft:uniform', 'min_inclusive': 20, 'max_inclusive': 40}},
        {'type': 'minecraft:in_square'}, {'type': 'minecraft:height_range', 'height': height('uniform', -48, 256)},
        {'type': 'minecraft:biome'}]})
    return z(name)

def tree(wood, ground, h=5, r=2, rarity=3):
    check(f'{wood}_log', f'{wood}_leaves', f'{wood}_sapling', ground)
    w(f'{WG}/configured_feature/{wood}_tree.json', {'type': 'minecraft:tree', 'config': {
        'trunk_placer': {'type': 'minecraft:straight_trunk_placer', 'base_height': h, 'height_rand_a': 2, 'height_rand_b': 0},
        'trunk_provider': {'type': 'minecraft:simple_state_provider', 'state': st(f'{wood}_log', {'axis': 'y'})},
        'foliage_placer': {'type': 'minecraft:blob_foliage_placer', 'radius': r, 'offset': 0, 'height': 3},
        'foliage_provider': {'type': 'minecraft:simple_state_provider',
                             'state': st(f'{wood}_leaves', {'distance': '7', 'persistent': 'false', 'waterlogged': 'false'})},
        'dirt_provider': {'type': 'minecraft:simple_state_provider', 'state': st(ground)},
        'minimum_size': {'type': 'minecraft:two_layers_feature_size', 'limit': 1, 'lower_size': 0, 'upper_size': 1},
        'decorators': [], 'ignore_vines': True, 'force_dirt': False}})
    w(f'{WG}/placed_feature/{wood}_trees.json', {'feature': z(f'{wood}_tree'), 'placement': [
        {'type': 'minecraft:rarity_filter', 'chance': rarity}, {'type': 'minecraft:in_square'},
        {'type': 'minecraft:surface_water_depth_filter', 'max_water_depth': 0},
        {'type': 'minecraft:heightmap', 'heightmap': 'OCEAN_FLOOR'}, {'type': 'minecraft:biome'},
        {'type': 'minecraft:block_predicate_filter', 'predicate': {'type': 'minecraft:would_survive', 'state': st(f'{wood}_sapling', {'stage': '0'})}}]})
    return z(f'{wood}_trees')

def pyrevines():
    body = lambda b: {'weight': 4 if b == 'false' else 1, 'data': st('pyrevine_plant', {'berries': b})}
    head = lambda b: {'weight': 4 if b == 'false' else 1, 'data': st('pyrevine', {'age': '0', 'berries': b})}
    w(f'{WG}/configured_feature/pyrevine.json', {'type': 'minecraft:block_column', 'config': {
        'direction': 'down', 'allowed_placement': {'type': 'minecraft:matching_blocks', 'blocks': 'minecraft:air'}, 'prioritize_tip': True,
        'layers': [{'height': {'type': 'minecraft:weighted_list', 'distribution': [
                        {'weight': 2, 'data': {'type': 'minecraft:uniform', 'min_inclusive': 0, 'max_inclusive': 19}},
                        {'weight': 3, 'data': {'type': 'minecraft:uniform', 'min_inclusive': 0, 'max_inclusive': 2}},
                        {'weight': 10, 'data': {'type': 'minecraft:uniform', 'min_inclusive': 0, 'max_inclusive': 6}}]},
                    'provider': {'type': 'minecraft:weighted_state_provider', 'entries': [body('false'), body('true')]}},
                   {'height': 1, 'provider': {'type': 'minecraft:weighted_state_provider', 'entries': [head('false'), head('true')]}}]}})
    w(f'{WG}/placed_feature/pyrevine.json', {'feature': z('pyrevine'), 'placement': [
        {'type': 'minecraft:count', 'count': 120}, {'type': 'minecraft:in_square'},
        {'type': 'minecraft:height_range', 'height': height('uniform', -64, 256)},
        {'type': 'minecraft:environment_scan', 'direction_of_search': 'up', 'max_steps': 12,
         'target_condition': {'type': 'minecraft:solid'}, 'allowed_search_condition': {'type': 'minecraft:matching_blocks', 'blocks': 'minecraft:air'}},
        {'type': 'minecraft:random_offset', 'xz_spread': 0, 'y_spread': -1}, {'type': 'minecraft:biome'}]})
    return z('pyrevine')

def glowkelp():
    w(f'{WG}/configured_feature/glowkelp.json', {'type': 'minecraft:block_column', 'config': {
        'direction': 'up', 'allowed_placement': {'type': 'minecraft:matching_blocks', 'blocks': 'minecraft:water'}, 'prioritize_tip': True,
        'layers': [{'height': {'type': 'minecraft:uniform', 'min_inclusive': 2, 'max_inclusive': 12},
                    'provider': {'type': 'minecraft:simple_state_provider', 'state': st('glowkelp_plant')}},
                   {'height': 1, 'provider': {'type': 'minecraft:simple_state_provider', 'state': st('glowkelp', {'age': '0'})}}]}})
    w(f'{WG}/placed_feature/glowkelp.json', {'feature': z('glowkelp'), 'placement': [
        {'type': 'minecraft:count', 'count': 40}, {'type': 'minecraft:in_square'},
        {'type': 'minecraft:heightmap', 'heightmap': 'OCEAN_FLOOR_WG'},
        {'type': 'minecraft:block_predicate_filter', 'predicate': {'type': 'minecraft:matching_blocks', 'blocks': 'minecraft:water'}},
        {'type': 'minecraft:biome'}]})
    return z('glowkelp')

def scatter(name, block, host, size=4, count=6, lo=40, hi=200, props=None):
    """signature blocks set into the surface stone (ore feature near the top)."""
    check(block, host)
    w(f'{WG}/configured_feature/{name}.json', {'type': 'minecraft:ore', 'config': {'size': size, 'discard_chance_on_air_exposure': 0.0,
        'targets': [{'target': {'predicate_type': 'minecraft:block_match', 'block': z(host)}, 'state': st(block, props)}]}})
    w(f'{WG}/placed_feature/{name}.json', {'feature': z(name), 'placement': [
        {'type': 'minecraft:count', 'count': count}, {'type': 'minecraft:in_square'},
        {'type': 'minecraft:height_range', 'height': height('uniform', lo, hi)}, {'type': 'minecraft:biome'}]})
    return z(name)

V = {}  # planet/wasteland -> list of vegetation placed features
V['moon'] = [lichen('lunar_lichen', 'lunar_lichen', ['lunar_stone', 'mare_basalt', 'regolith'])]
V['mars'] = [lichen('rust_lichen', 'rust_lichen', ['martian_stone', 'rustsand', 'oxide_crust'])]
V['cerulon'] = [patch('patch_starbloom', 'starbloom'), tree('shardwood', 'crystal_sand', 5, 2, 4)]
V['skarn'] = [patch('patch_emberthorn', 'emberthorn', rarity=3), patch('patch_cinder_cap', 'cinder_cap', rarity=6), tree('charwood', 'slag', 4, 2, 6)]
V['eidolon'] = [patch('patch_frostfern', 'frostfern', rarity=2), patch('patch_ghostbloom', 'ghostbloom', rarity=8), tree('hoarwood', 'frozen_regolith', 6, 2, 5)]
V['solvane'] = [patch('patch_solflower', 'solflower', rarity=5), pyrevines(), tree('gildwood', 'sunspot_rock', 5, 3, 7)]
V['ocean'] = [glowkelp(), scatter('brine_crystal_scatter', 'brine_crystal', 'abyssal_stone', 3, 8, -32, 120)]
V['desert'] = [scatter('ruinstone_scatter', 'ruinstone', 'sunbaked_stone', 12, 3, 40, 200)]
V['volcanic'] = [scatter('vent_rock_scatter', 'vent_rock', 'scoria', 6, 8, 40, 200), scatter('glassy_obsidian_scatter', 'glassy_obsidian', 'scoria', 10, 2, 20, 120)]
V['frozen'] = [scatter('frost_crystal_scatter', 'frost_crystal', 'frostrock', 3, 8, 0, 200)]
V['toxic'] = []
V['crystal'] = [scatter('prism_cluster_scatter', 'prism_cluster', 'prismstone', 3, 10, -32, 200), scatter('refracting_glass_scatter', 'refracting_glass', 'prismstone', 6, 3, 0, 160)]
V['barren'] = [scatter('meteorite_scatter', 'meteorite_fragment', 'craterstone', 3, 4, 50, 220)]
V['cerulon'].append(z('cerulite_geode'))
V['skarn'].append(scatter('rift_glass_scatter', 'rift_glass', 'skarn_rock', 8, 3, -32, 96))
V['skarn'].append(scatter('scorched_marble_blobs', 'scorched_marble', 'skarn_rock', 33, 6, 0, 200))
V['eidolon'].append(scatter('phantom_ice_scatter', 'phantom_ice', 'permafrost', 12, 3, 40, 200))
V['solvane'].append(scatter('flare_vent_scatter', 'flare_vent', 'solar_stone', 1, 10, 50, 220))
V['solvane'].append(scatter('slag_glass_scatter', 'slag_glass', 'solar_stone', 16, 3, 40, 200))

# ---- worlds: stone, top, under, sea level, fluid, biomes[(id, temp, humid, sky, fog, water, extra-top-override)]
BLACK = 0x000000
WORLDS = {
 'moon':    dict(stone='lunar_stone', top='regolith', under='regolith', sea=-64, fluid='minecraft:air', gravity=0.5,
                 biomes=[('lunar_highlands', -.5, 0, BLACK, 0x0a0a10, 0x3f4a5a, None), ('lunar_mare', .5, 0, BLACK, 0x0a0a10, 0x3f4a5a, 'mare_basalt'),
                         ('shadowed_craters', -.9, .5, BLACK, 0x05050a, 0x3f4a5a, 'crater_ice')]),
 'mars':    dict(stone='martian_stone', top='rustsand', under='oxide_crust', sea=-64, fluid='minecraft:air', gravity=0.7,
                 biomes=[('rust_plains', .3, 0, 0xc98a5a, 0xd09a6a, 0x6a4a3a, None), ('oxide_badlands', .8, .2, 0xc98a5a, 0xc08050, 0x6a4a3a, 'oxide_crust'),
                         ('polar_caps', -.9, .5, 0xd8c0b0, 0xe0d0c8, 0x6a4a3a, 'polar_frost')]),
 'cerulon': dict(stone='cerulean_stone', top='azure_moss', under='crystal_sand', sea=63, fluid='minecraft:water', gravity=0.9,
                 biomes=[('azure_plains', .2, .5, 0x4a7ad8, 0x6a9ae8, 0x2a6ad8, None), ('crystal_shores', .6, .8, 0x4a7ad8, 0x6a9ae8, 0x2a8ae8, 'crystal_sand'),
                         ('shardwood_grove', -.3, .8, 0x3a6ac8, 0x5a8ad8, 0x2a6ad8, None)]),
 'skarn':   dict(stone='skarn_rock', top='slag', under='skarn_rock', sea=-64, fluid='minecraft:air', gravity=1.2,
                 biomes=[('ember_fields', .8, 0, 0x3a1a10, 0x4a2010, 0x5a3a2a, 'ember_crust'), ('marble_contact_zone', .2, .3, 0x4a2a1a, 0x5a3020, 0x5a3a2a, 'scorched_marble'),
                         ('charwood_barrens', -.4, .6, 0x3a1a10, 0x4a2a1a, 0x5a3a2a, None)]),
 'eidolon': dict(stone='permafrost', top='frozen_regolith', under='permafrost', sea=63, fluid='minecraft:water', gravity=0.8,
                 biomes=[('frozen_graveyard', -.9, .2, 0xa8d8e8, 0xc8e8f0, 0x3a7a9a, None), ('phantom_ice_sheets', -.7, .8, 0xa8d8e8, 0xd8f0f8, 0x3a7a9a, 'phantom_ice'),
                         ('hoarwood_taiga', -.3, .6, 0x98c8d8, 0xb8d8e8, 0x3a7a9a, None)]),
 'solvane': dict(stone='solar_stone', top='sunspot_rock', under='solar_stone', sea=-64, fluid='minecraft:air', gravity=1.3,
                 biomes=[('corona_flats', .9, 0, 0xffb040, 0xffd080, 0x8a5a2a, 'corona_crust'), ('sunspot_plateaus', .4, .3, 0xff9a30, 0xffc070, 0x8a5a2a, None),
                         ('gildwood_oasis', .1, .8, 0xffa040, 0xffd090, 0x8a5a2a, None)]),
}
WASTE = {
 'ocean':    dict(stone='abyssal_stone', top='tidesand', under='tidesand', sea=110, fluid='minecraft:water',
                  biomes=[('deep_trenches', 0, 0), ('kelp_jungles', .5, .8), ('island_chains', .9, .3)], sky=0x5a8ab8, water=0x1a4a8a),
 'desert':   dict(stone='sunbaked_stone', top='dunesand', under='dunesand', sea=-64, fluid='minecraft:air',
                  biomes=[('dune_seas', .9, 0), ('mesa_canyons', .6, .3), ('salt_flats', .3, .6)], sky=0xe8c890, water=0x7a8a6a),
 'volcanic': dict(stone='scoria', top='scoria', under='scoria', sea=-64, fluid='minecraft:air',
                  biomes=[('basalt_fields', .5, 0), ('ash_plains', .8, .5), ('lava_lakes', .95, .9)], sky=0x4a2a2a, water=0x4a3a2a),
 'frozen':   dict(stone='frostrock', top='snowpack', under='frostrock', sea=63, fluid='minecraft:water',
                  biomes=[('glaciers', -.9, 0), ('ice_spike_forest', -.7, .6), ('frozen_canyons', -.5, .3)], sky=0xc8e0f0, water=0x3a6a9a),
 'toxic':    dict(stone='sludgestone', top='blightmoss', under='toxic_mud', sea=63, fluid='minecraft:water',
                  biomes=[('acid_swamps', .6, .9), ('mud_flats', .4, .5), ('moss_bogs', .2, .8)], sky=0x8aa84a, water=0x6a8a2a),
 'crystal':  dict(stone='prismstone', top='shimmer_sand', under='shimmer_sand', sea=-64, fluid='minecraft:air',
                  biomes=[('prism_fields', .2, .2), ('crystal_caverns', .5, .7)], sky=0xb89ae8, water=0x6a5ab8),
 'barren':   dict(stone='craterstone', top='crater_dust', under='craterstone', sea=-64, fluid='minecraft:air',
                  biomes=[('cratered_plains', 0, 0), ('dust_badlands', .6, .2), ('canyon_scars', .3, .7)], sky=0x1a1a24, water=0x3a3a4a),
}
TOP_OVERRIDE_W = {'salt_flats': 'salt_crust', 'lava_lakes': 'vent_rock', 'ash_plains': 'ashfall', 'glaciers': 'glacial_ice',
                  'mud_flats': 'toxic_mud', 'mesa_canyons': 'sunbaked_stone'}

def biome_json(features_ores, veg, sky, fog, water, temp, humid, precip=False, spawns=None):
    feats = [[] for _ in range(11)]
    feats[6] = list(features_ores)          # underground_ores
    feats[9] = list(veg)                    # vegetal_decoration
    return {'has_precipitation': precip, 'temperature': temp, 'downfall': max(0.0, humid),
            'effects': {'sky_color': sky, 'fog_color': fog, 'water_color': water, 'water_fog_color': water,
                        'mood_sound': {'sound': 'minecraft:ambient.cave', 'tick_delay': 6000, 'block_search_extent': 8, 'offset': 2.0}},
            'spawners': spawns or {}, 'spawn_costs': {},
            'carvers': {'air': ['minecraft:cave', 'minecraft:cave_extra_underground', 'minecraft:canyon']},
            'features': feats}

def surface_rule(top, under, stone_default, biome_tops):
    """vanilla-shaped surface rule: bedrock floor, per-biome top block, then 3 blocks of under-layer."""
    def blk(b): return {'type': 'minecraft:block', 'result_state': st(b)}
    per_biome = [{'type': 'minecraft:condition', 'if_true': {'type': 'minecraft:biome', 'biome_is': [z(bid)]}, 'then_run': blk(b)}
                 for bid, b in biome_tops.items()]
    return {'type': 'minecraft:sequence', 'sequence': [
        {'type': 'minecraft:condition', 'if_true': {'type': 'minecraft:vertical_gradient', 'random_name': 'minecraft:bedrock_floor',
            'true_at_and_below': {'above_bottom': 0}, 'false_at_and_above': {'above_bottom': 5}}, 'then_run': blk('minecraft:bedrock')},
        {'type': 'minecraft:condition', 'if_true': {'type': 'minecraft:above_preliminary_surface'}, 'then_run': {
            'type': 'minecraft:sequence', 'sequence': [
                {'type': 'minecraft:condition', 'if_true': {'type': 'minecraft:stone_depth', 'offset': 0, 'surface_type': 'floor',
                    'add_surface_depth': False, 'secondary_depth_range': 0},
                 'then_run': {'type': 'minecraft:sequence', 'sequence': per_biome + [blk(top)]}},
                {'type': 'minecraft:condition', 'if_true': {'type': 'minecraft:stone_depth', 'offset': 0, 'surface_type': 'floor',
                    'add_surface_depth': True, 'secondary_depth_range': 0}, 'then_run': blk(under)}]}}]}

def noise_router():
    """vanilla overworld terrain shape, referencing vanilla's named density functions (no noodle caves / ore veins)."""
    shifted = lambda n: {'type': 'minecraft:shifted_noise', 'noise': n, 'xz_scale': 0.25, 'y_scale': 0.0,
                         'shift_x': 'minecraft:shift_x', 'shift_y': 0.0, 'shift_z': 'minecraft:shift_z'}
    initial = {'type': 'minecraft:add', 'argument1': 0.1171875, 'argument2': {'type': 'minecraft:mul',
        'argument1': {'type': 'minecraft:y_clamped_gradient', 'from_y': -64, 'to_y': -40, 'from_value': 0.0, 'to_value': 1.0},
        'argument2': {'type': 'minecraft:add', 'argument1': -0.1171875, 'argument2': {'type': 'minecraft:add', 'argument1': -0.078125,
            'argument2': {'type': 'minecraft:mul',
                'argument1': {'type': 'minecraft:y_clamped_gradient', 'from_y': 240, 'to_y': 256, 'from_value': 1.0, 'to_value': 0.0},
                'argument2': {'type': 'minecraft:add', 'argument1': 0.078125, 'argument2': {'type': 'minecraft:clamp', 'min': -64.0, 'max': 64.0,
                    'input': {'type': 'minecraft:add', 'argument1': -0.703125, 'argument2': {'type': 'minecraft:mul', 'argument1': 4.0,
                        'argument2': {'type': 'minecraft:quarter_negative', 'argument': {'type': 'minecraft:mul',
                            'argument1': 'minecraft:overworld/depth', 'argument2': {'type': 'minecraft:cache_2d', 'argument': 'minecraft:overworld/factor'}}}}}}}}}}}}
    final = {'type': 'minecraft:min',
             'argument1': {'type': 'minecraft:squeeze', 'argument': {'type': 'minecraft:mul', 'argument1': 0.64,
                 'argument2': {'type': 'minecraft:interpolated', 'argument': {'type': 'minecraft:blend_density',
                     'argument': 'minecraft:overworld/sloped_cheese'}}}},
             'argument2': 'minecraft:overworld/caves/entrances'}
    return {'barrier': 0.0, 'fluid_level_floodedness': 0.0, 'fluid_level_spread': 0.0, 'lava': 0.0,
            'temperature': shifted('minecraft:temperature'), 'vegetation': shifted('minecraft:vegetation'),
            'continents': 'minecraft:overworld/continents', 'erosion': 'minecraft:overworld/erosion',
            'depth': 'minecraft:overworld/depth', 'ridges': 'minecraft:overworld/ridges',
            'initial_density_without_jaggedness': initial, 'final_density': final,
            'vein_toggle': 0.0, 'vein_ridged': 0.0, 'vein_gap': 0.0}

def noise_settings(name, stone, fluid, sea, rule):
    check(stone)
    w(f'{WG}/noise_settings/{name}.json', {'sea_level': sea, 'disable_mob_generation': False, 'aquifers_enabled': False,
        'ore_veins_enabled': False, 'legacy_random_source': False, 'default_block': st(stone), 'default_fluid': {'Name': fluid, 'Properties': {'level': '0'}} if fluid != 'minecraft:air' else {'Name': 'minecraft:air'},
        'noise': {'min_y': -64, 'height': 384, 'size_horizontal': 1, 'size_vertical': 2},
        'noise_router': noise_router(), 'spawn_target': [], 'surface_rule': rule})

def dim_type(name, ultrawarm=False, ceiling=False, ambient=0.0, fixed_time=None):
    o = {'ultrawarm': ultrawarm, 'natural': False, 'coordinate_scale': 1.0, 'has_skylight': True, 'has_ceiling': ceiling,
         'ambient_light': ambient, 'monster_spawn_light_level': {'type': 'minecraft:uniform', 'min_inclusive': 0, 'max_inclusive': 7},
         'monster_spawn_block_light_limit': 0, 'piglin_safe': False, 'bed_works': True, 'respawn_anchor_works': False,
         'has_raids': False, 'logical_height': 384, 'min_y': -64, 'height': 384,
         'infiniburn': '#minecraft:infiniburn_overworld', 'effects': 'minecraft:overworld'}
    if fixed_time is not None: o['fixed_time'] = fixed_time
    w(f'{D}/dimension_type/{name}.json', o)

def param_point(t, h, cont=(-1.0, 1.0)):
    rng = lambda v: [max(-1.0, v - .35), min(1.0, v + .35)]
    return {'temperature': rng(t), 'humidity': rng(h), 'continentalness': list(cont), 'erosion': [-1.0, 1.0],
            'weirdness': [-1.0, 1.0], 'depth': 0.0, 'offset': 0.0}

def dimension(name, dtype, settings, biomes):
    w(f'{D}/dimension/{name}.json', {'type': z(dtype), 'generator': {'type': 'minecraft:noise', 'settings': z(settings),
        'biome_source': {'type': 'minecraft:multi_noise', 'biomes': [{'biome': z(b), 'parameters': param_point(t, h)} for b, t, h in biomes]}}})

dim_type('planet'); dim_type('planet_hot', ultrawarm=True); dim_type('airless', fixed_time=18000)
GRAV = {}
for world, c in WORLDS.items():
    tops = {}
    for bid, t, h, sky, fog, water, top in c['biomes']:
        if top: check(top); tops[bid] = top
        w(f'{WG}/biome/{bid}.json', biome_json(ORE_FEATURES[world], V[world], sky, fog, water, t, h,
                                               precip=world in ('cerulon', 'eidolon')))
    noise_settings(world, c['stone'], c['fluid'], c['sea'], surface_rule(c['top'], c['under'], c['stone'], tops))
    dimension(world, {'moon': 'airless', 'solvane': 'planet_hot', 'skarn': 'planet_hot'}.get(world, 'planet'), world,
              [(b[0], b[1], b[2]) for b in c['biomes']])
    GRAV[world] = c['gravity']

for wt, c in WASTE.items():
    tops = {}
    for bid, t, h in c['biomes']:
        top = TOP_OVERRIDE_W.get(bid)
        if top: check(top); tops[bid] = top
        w(f'{WG}/biome/wasteland_{bid}.json', biome_json([], V[wt], c['sky'], c['sky'], c['water'], t, h,
                                                        precip=wt in ('ocean', 'frozen', 'toxic')))
    noise_settings(f'wasteland_{wt}', c['stone'], c['fluid'], c['sea'],
                   surface_rule(c['top'], c['under'], c['stone'], {f'wasteland_{k}': v for k, v in tops.items()}))

# Galaxy slot dimensions g2..g5 _p1.._p6 (wastelands) + one shared moon dimension per galaxy.
# The seeded ChunkGenerator (Java, milestone M5) will pick the type per seed; until then each slot
# has a deterministic default so the worlds are enterable and testable.
ORDER = list(WASTE)
SLOTS = {}
for g in range(2, 6):
    for p in range(1, 7):
        wt = ORDER[(g * 3 + p) % len(ORDER)]
        SLOTS[f'g{g}_p{p}'] = wt
        c = WASTE[wt]
        dimension(f'g{g}_p{p}', 'planet', f'wasteland_{wt}', [(f'wasteland_{b}', t, h) for b, t, h in c['biomes']])
    SLOTS[f'g{g}_moons'] = 'barren'
    dimension(f'g{g}_moons', 'airless', 'wasteland_barren', [(f'wasteland_{b}', t, h) for b, t, h in WASTE['barren']['biomes']])

# ============================================================== ADVANCEMENTS (Codex, voiced by Echo)
ADV = f'{D}/advancement/codex'
def adv(name, parent, icon, title, desc, criteria, frame='task', hidden=False):
    o = {'display': {'icon': {'id': z(icon) if not icon.startswith('minecraft:') else icon}, 'title': {'translate': f'advancements.{NS}.{name}.title'},
                     'description': {'translate': f'advancements.{NS}.{name}.description'}, 'frame': frame,
                     'show_toast': True, 'announce_to_chat': True, 'hidden': hidden},
         'criteria': criteria, 'requirements': [[k] for k in criteria]}
    if parent: o['parent'] = f'{NS}:codex/{parent}'
    else: o['display']['background'] = 'minecraft:textures/block/deepslate_tiles.png'
    w(f'{ADV}/{name}.json', o); LANG[f'advancements.{NS}.{name}.title'] = title; LANG[f'advancements.{NS}.{name}.description'] = desc

def has(*items): return {f'has_{i}': {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': z(i)}]}} for i in items}
def enter(dim): return {f'enter_{dim}': {'trigger': 'minecraft:changed_dimension', 'conditions': {'to': z(dim)}}}

LANG = {}
adv('root', None, 'raw_nullifite', 'ZeroG Tweaks', 'Something humming fell from the sky. Pick up a piece of Nullifite.', has('raw_nullifite'))
adv('first_gate', 'root', 'gate_controller', 'Awaiting Coordinates', '"How long have I been asleep?" Craft a Gate Controller.', has('gate_controller'))
adv('the_moon', 'first_gate', 'regolith', 'Act I: The Falling Star', 'Step onto the Moon.', enter('moon'), 'goal')
adv('mars', 'the_moon', 'aresite', 'A Hand-Cut Core', 'Reach Mars and find Aresite, cut by someone who came before.', {**enter('mars')})
adv('aresite_core', 'mars', 'aresite', 'Not Natural', 'Hold an Aresite gem. The facets are too clean.', has('aresite'))
adv('cerulon', 'aresite_core', 'cerulite', 'Act II: The Quiet Mines', 'Arrive on Cerulon, the Concord\'s mining world.', enter('cerulon'), 'goal')
adv('cerulite', 'cerulon', 'cerulite', 'Blue Heart', 'Mine Cerulite.', has('cerulite'))
adv('prism_sentinel', 'cerulite', 'sentinel_prism', 'Heir of the Concord', 'Pass the Prism Sentinel\'s test.', has('sentinel_prism'), 'challenge')
adv('skarn', 'prism_sentinel', 'skarnite', 'Act III: The Wound', 'Walk where Vael tore space open.', enter('skarn'), 'goal')
adv('rift_tyrant', 'skarn', 'rift_heart', 'Echo Remembers', 'Defeat the Rift Tyrant. Echo remembers she plotted this course.', has('rift_heart'), 'challenge')
adv('eidolon', 'rift_tyrant', 'eidolite', 'Act IV: The Frozen Fleet', 'Reach the frozen graveyard of the Hollow Fleet.', enter('eidolon'), 'goal')
adv('remnants', 'eidolon', 'remnant_shard', 'Final Log', 'Collect a Remnant Shard from a Broken Console.', has('remnant_shard'))
adv('captain', 'remnants', 'captains_lantern', 'Rescue That Never Came', 'Settle things with the Eidolon Captain.', has('galaxy_5_gate_key'), 'challenge')
adv('solvane', 'captain', 'solvanite', 'Act V: The Last Light', 'Stand beneath the dying sun.', enter('solvane'), 'goal')
adv('nova_pearl', 'solvane', 'nova_pearl', 'The Truth in the Pearl', 'Hold a Nova Pearl. The Dying Star is Vael.', has('nova_pearl'))
adv('heart_of_solvane', 'nova_pearl', 'heart_of_solvane', 'Rekindle or Release', 'Take the Heart of Solvane and choose the Concord\'s ending.', has('heart_of_solvane'), 'challenge')
adv('wanderer', 'cerulon', 'star_map_fragment', 'Beyond the Chart', 'Find a Star Map Fragment in a Buried Observatory.', has('star_map_fragment'))
adv('all_rewards', 'wanderer', 'stardust', 'Every Wasteland Has a Gift', 'Collect all seven wasteland rewards.',
    has('abyssal_pearl', 'star_map_fragment', 'heatproof_plating', 'cryo_core', 'neutralizer', 'refracting_lens', 'stardust'), 'challenge')
adv('nullifite_gear', 'root', 'nullifite_chestplate', 'Null Step', 'Wear a full set of Nullifite armor.',
    {'armor': {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': z(f'nullifite_{p}')} for p in ARMOR]}}})
adv('solvanite_gear', 'nullifite_gear', 'solvanite_chestplate', 'Starborne', 'Wear a full set of Solvanite armor.',
    {'armor': {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': z(f'solvanite_{p}')} for p in ARMOR]}}}, 'challenge')

# death messages for damage types
DEATH = {'ember_crust': '%1$s stood too long on Ember Crust', 'corona_crust': '%1$s was seared by Corona Crust',
         'flare_vent': '%1$s was caught by a Flare Vent eruption', 'vent_rock': '%1$s was scalded by Vent Rock',
         'acid': '%1$s dissolved in acid', 'polar_frost': '%1$s froze solid on Polar Frost', 'void_rift': '%1$s fell through a void rift'}
for k, v in DEATH.items():
    LANG[f'death.attack.{NS}.{k}'] = v
    LANG[f'death.attack.{NS}.{k}.player'] = v + ' whilst fighting %2$s'
DIM_NAMES = {'moon': 'The Moon', 'mars': 'Mars', 'cerulon': 'ZG-855 b "Cerulon"', 'skarn': 'Skarn', 'eidolon': 'Eidolon', 'solvane': 'Solvane'}
for d, n in DIM_NAMES.items(): LANG[f'dimension.{NS}.{d}'] = n
for world, c in WORLDS.items():
    for b in c['biomes']: LANG[f'biome.{NS}.{b[0]}'] = b[0].replace('_', ' ').title()
for wt, c in WASTE.items():
    for b in c['biomes']: LANG[f'biome.{NS}.wasteland_{b[0]}'] = b[0].replace('_', ' ').title()

lp = f'{RES}/assets/{NS}/lang/en_us.json'
LJ = json.load(open(lp)); LJ.update(LANG)
open(lp, 'w').write(json.dumps(LJ, indent=2, ensure_ascii=False) + '\n')

# ============================================================== PENDING (needs Java registries first)
MOBS = {'moon': [('moon_hopper', 'creature', 10, 2, 4), ('regolith_crawler', 'monster', 60, 1, 2), ('meteor_maw', 'monster', 20, 1, 1)],
        'mars': [('dust_grazer', 'creature', 10, 3, 6), ('rust_beetle', 'creature', 8, 1, 3), ('stormbitten_wyvern', 'monster', 5, 1, 1)],
        'cerulon': [('azure_fowl', 'creature', 10, 2, 4), ('crystal_stag', 'creature', 6, 1, 3), 
                    ('prismling', 'monster', 60, 2, 4), ('glimmerfish', 'water_ambient', 15, 4, 8)],
        'skarn': [('slag_boar', 'creature', 10, 2, 4), ('cinder_hound', 'monster', 50, 3, 5), ('scorch_wyrmling', 'monster', 30, 1, 2),
                  ('slagjaw', 'monster', 10, 1, 1), ('shardmother', 'monster', 3, 1, 1)],
        'eidolon': [('frost_yak', 'creature', 10, 2, 4), ('ice_leech', 'monster', 40, 1, 3), ('hollow_sentinel', 'monster', 30, 1, 2)],
        'solvane': [('gildcrab', 'creature', 10, 2, 4), ('flare_sprite', 'monster', 50, 1, 3)]}
WMOBS = {'ocean': [('tidewraith', 'monster', 40, 1, 2), ('deep_eel', 'water_creature', 20, 1, 2)],
         'desert': [('dune_burrower', 'monster', 40, 1, 2), ('sand_skitter', 'monster', 40, 2, 4)],
         'volcanic': [('ash_strider', 'monster', 50, 1, 3)], 'frozen': [('rime_stalker', 'monster', 50, 1, 2)],
         'toxic': [('bog_lurker', 'monster', 50, 1, 2)], 'crystal': [('amethyst_stalker', 'monster', 50, 1, 2)],
         'barren': [('crater_drifter', 'monster', 50, 1, 3)]}
import glob as _g
GEO = {f.split('/')[-1][:-9] for f in _g.glob(f'{RES}/assets/{NS}/geckolib/models/entity/*.geo.json')}
def spawn_mod(name, biomes, mobs):
    # Shattered Skies mobs (meteor_maw, mossback, ...) live in the shared mob library's namespace, not ours
    mobs = [m for m in mobs if m[0] in GEO]
    if not mobs: return
    o = {'type': 'neoforge:add_spawns', 'biomes': biomes,
         'spawners': [{'type': z(m), 'weight': wt, 'minCount': lo, 'maxCount': hi} for m, cat, wt, lo, hi in mobs]}
    os.makedirs(f'{PENDING}/neoforge/biome_modifier', exist_ok=True)
    open(f'{PENDING}/neoforge/biome_modifier/{name}.json', 'w').write(json.dumps(o, indent=2) + '\n')
for world, mobs in MOBS.items():
    spawn_mod(f'spawns_{world}', [z(b[0]) for b in WORLDS[world]['biomes']], mobs)
for wt, mobs in WMOBS.items():
    spawn_mod(f'spawns_wasteland_{wt}', [z(f'wasteland_{b[0]}') for b in WASTE[wt]['biomes']], mobs)

# machine-readable manifest for the build LLM
MAN = {'planets': {k: {'dimension': z(k), 'gravity': v, 'base_stone': WORLDS[k]['stone'], 'biomes': [b[0] for b in WORLDS[k]['biomes']],
                       'ores': ORE_FEATURES[k]} for k, v in GRAV.items()},
       'wasteland_types': {k: {'noise_settings': z(f'wasteland_{k}'), 'biomes': [f'wasteland_{b[0]}' for b in c['biomes']]} for k, c in WASTE.items()},
       'galaxy_slots_default_type': SLOTS,
       'structure_loot_tables': sorted(f'{NS}:chests/{os.path.basename(p)[:-5]}' for p in WRITTEN if '/loot_table/chests/' in p),
       'damage_types': [z(k) for k in DMG]}
open(f'{REPO}/docs/zero-g-tweaks-bundle/data-manifest.json', 'w').write(json.dumps(MAN, indent=2) + '\n')
print('wrote', len(WRITTEN), 'files')
