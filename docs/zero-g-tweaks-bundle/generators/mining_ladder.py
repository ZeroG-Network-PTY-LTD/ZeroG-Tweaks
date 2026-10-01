"""ZeroG mining ladder: single source for tool levels, ore requirements, tags, the design-doc section and the ladder sheet.
Allthemodium-style: Nullifite (first ZeroG ore) needs a netherite pickaxe; every later ore needs the pick before it.
Usage: python3 mining_ladder.py <bundle_dir>   (writes pending-data/tags, the doc section, data-manifest key, sheet)"""
import json, os, sys, re

# level: (pick sets at that level, world, lore line for the pick)
VANILLA = {0: 'wooden', 1: 'stone', 2: 'iron', 3: 'diamond', 4: 'netherite'}
LEVELS = [
    (5,  ['nullifite'],               'Sol (Overworld)', 'Void-glass edge: the first pick that can bite into off-world rock.'),
    (6,  ['ferrox'],                  'Mars',            'Rust-hardened iron oxide; tough enough for lunar metal.'),
    (7,  ['moonsteel'],               'Moon',            'Forged in low gravity, so its edge holds against crystal and Olympus basalt.'),
    (8,  ['olympium'],                'Mars',            'Heavy Olympus metal alloyed with Moonsteel; opens the T2 gate materials.'),
    (9,  ['cobaltium', 'aurelion'],   'Cerulon',         'Cerulon\'s workhorse metals. Aurelion is gold-style: same level, faster, fragile.'),
    (10, ['cyrrium'],                 'Cerulon',         'Tempered casing steel; cuts the Cerulite geodes.'),
    (11, ['cerulite'],                'Cerulon',         'Crystal edge (T3). The only pick that survives Skarn heat.'),
    (12, ['ruskite', 'pyrium'],       'Skarn',           'Heat-scaled metals. Pyrium is gold-style: same level, faster, fragile.'),
    (13, ['tectium'],                 'Skarn',           'Plate metal heavy enough to crack Skarnite seams.'),
    (14, ['skarnite'],                'Skarn',           'Ember gem edge (T4); stays sharp in Eidolon\'s cold.'),
    (15, ['salvium', 'palladine'],    'Eidolon',         'Salvaged wreck steel. Palladine is gold-style: same level, faster, fragile.'),
    (16, ['wraithsteel'],             'Eidolon',         'Ghost-pale steel that reaches Eidolite through permafrost.'),
    (17, ['eidolite'],                'Eidolon',         'Phantom gem edge (T5); does not melt near a dying star.'),
    (18, ['photium', 'radiantine'],   'Solvane',         'Light metals of the fading sun. Radiantine is gold-style: same level, faster, fragile.'),
    (19, ['astrium'],                 'Solvane',         'Star-forged steel; the last step before the heart of Solvane.'),
    (20, ['solvanite'],               'Solvane',         'Endgame (T6). Mines everything in the mod.'),
]
SET_LEVEL = {s: L for L, sets, _, _ in LEVELS for s in sets}
PRECIOUS = {'aurelion', 'pyrium', 'palladine', 'radiantine'}
CANON = {L: sets[0] for L, sets, _, _ in LEVELS}            # tag name used for "needs level L"
def pick_name(L): return VANILLA.get(L) or CANON[L]

# ore block id -> required pick level, with the lore reason
ORES = {
    'deepslate_nullifite_ore': (4, 'Deep Overworld void veins; diamond shatters on them, so netherite is the minimum.'),
    'regolith_ore': (2, 'Loose lunar dust in rock; any iron pick.'),
    'ferrox_ore': (5, 'First Mars metal; needs the Nullifite pick you came with.'),
    'moonsteel_ore': (6, 'Lunar steel is harder than Martian rust; mine it with Ferrox.'),
    'selenite_ore': (7, 'Pale lens crystal splinters under anything weaker than Moonsteel.'),
    'olympium_ore': (7, 'Olympus basalt needs a low-gravity Moonsteel edge.'),
    'aresite_ore': (8, 'The red T2 core grows inside Olympium veins; mine it with Olympium.'),
    'nebulite_ore': (2, 'Fuel: iron pick, so power is never blocked.'),
    'pulsar_dust_ore': (2, 'Energy dust: iron pick, so power is never blocked.'),
    'cobaltium_ore': (8, 'First Cerulon metal; needs the Olympium pick from Sol.'),
    'aurelion_ore': (9, 'Soft precious metal in hard blue stone; Cobaltium or better.'),
    'starlite_ore': (9, 'Lore gem; Cobaltium or better.'),
    'lumenite_ore': (9, 'Trade gem; Cobaltium or better.'),
    'cyrrium_ore': (9, 'Casing steel; Cobaltium or better.'),
    'cerulite_ore': (10, 'Crystal geodes need a tempered Cyrrium pick.'),
    'emberite_ore': (2, 'Fuel: iron pick, so power is never blocked.'),
    'tremor_dust_ore': (2, 'Energy dust: iron pick, so power is never blocked.'),
    'ruskite_ore': (11, 'First Skarn metal; only Cerulite survives the heat.'),
    'pyrium_ore': (12, 'Fire-gold; Ruskite or better.'),
    'rift_opal_ore': (12, 'Lore gem; Ruskite or better.'),
    'cinnabrite_ore': (12, 'Trade gem; Ruskite or better.'),
    'tectium_ore': (12, 'Heavy plate metal; Ruskite or better.'),
    'skarnite_ore': (13, 'Ember seams crack only under Tectium.'),
    'cryocite_ore': (2, 'Fuel: iron pick, so power is never blocked.'),
    'spectral_dust_ore': (2, 'Energy dust: iron pick, so power is never blocked.'),
    'salvium_ore': (14, 'First Eidolon metal (wreck scrap); needs the Skarnite pick.'),
    'palladine_ore': (15, 'White precious metal; Salvium or better.'),
    'remnant_shard_ore': (15, 'Lore gem; Salvium or better.'),
    'rimeglass_ore': (15, 'Trade gem; Salvium or better.'),
    'wraithsteel_ore': (15, 'Ghost steel; Salvium or better.'),
    'eidolite_ore': (16, 'Phantom gem deep in permafrost; Wraithsteel only.'),
    'coronite_ore': (2, 'Fuel: iron pick, so power is never blocked.'),
    'fusion_dust_ore': (2, 'Energy dust: iron pick, so power is never blocked.'),
    'photium_ore': (17, 'First Solvane metal; needs the Eidolite pick.'),
    'radiantine_ore': (18, 'Light-gold; Photium or better.'),
    'nova_pearl_ore': (18, 'Lore gem; Photium or better.'),
    'dawnstone_ore': (18, 'Trade gem; Photium or better.'),
    'astrium_ore': (18, 'Star-forged steel; Photium or better.'),
    'solvanite_ore': (19, 'Dying-star gem; Astrium only.'),
}

def mining_speed(s):
    L = SET_LEVEL[s]; base = 9.0 + 0.5 * (L - 4)          # netherite 9, +0.5 per level
    return base + (4.0 if s in PRECIOUS else 0.0)

def needs_tag(L):
    if L <= 3: return f'minecraft:needs_{VANILLA[L]}_tool' if L >= 1 else None
    return f'zerog_tweaks:needs_{pick_name(L)}_tool'

def build_tags():
    """returns {relative path: json} for data/<ns>/tags/block/..."""
    out = {}
    by_level = {}
    for ore, (L, _) in ORES.items(): by_level.setdefault(L, []).append(f'zerog_tweaks:{ore}')
    for L in range(4, 21):                                  # one needs tag per ZeroG level (empty ones kept for future blocks)
        out[f'zerog_tweaks/tags/block/needs_{pick_name(L)}_tool.json'] = {'replace': False, 'values': sorted(by_level.get(L, []))}
    out['minecraft/tags/block/needs_iron_tool.json'] = {'replace': False, 'values': sorted(by_level.get(2, []))}
    out['minecraft/tags/block/needs_diamond_tool.json'] = {'replace': False, 'values': []}   # Nullifite moved to needs_netherite
    above = lambda L: [f'#zerog_tweaks:needs_{pick_name(x)}_tool' for x in range(max(L + 1, 4), 21)]
    for L, name in VANILLA.items():                         # lock vanilla tools out of everything above them
        out[f'minecraft/tags/block/incorrect_for_{name}_tool.json'] = {'replace': False, 'values': above(L)}
    out['minecraft/tags/block/incorrect_for_gold_tool.json'] = {'replace': False, 'values': above(0)}
    for s, L in SET_LEVEL.items():                           # ZeroG tiers
        vals = above(L)
        if L < 20: pass
        out[f'zerog_tweaks/tags/block/incorrect_for_{s}_tool.json'] = {'replace': False, 'values': vals}
    return out

def doc_section():
    t = ['**Mining ladder (v1.3, locked)**', '',
         'Allthemodium-style: every ZeroG pickaxe out-mines netherite, and every ZeroG ore needs at least a netherite pickaxe. '
         'Nullifite, the first ZeroG ore, needs netherite; after that, each world\'s first metal needs the best pickaxe from the world before, '
         'and inside a world the order is common metal, then standard metal, then the rare gem. Precious (gold-style) picks share their world\'s common level but mine faster. '
         'Fuels and energy dusts only need an iron pickaxe, so power is never blocked.', '',
         '| Level | Pickaxe | World | Opens these ores | Mining speed | Lore |', '| --- | --- | --- | --- | --- | --- |',
         '| 4 | Netherite (vanilla) | Overworld | Nullifite | 9 | The entry ticket to space. |']
    for L, sets, world, lore in LEVELS:
        ores = [o.replace('_ore', '').replace('deepslate_', '').replace('_', ' ').title() for o, (r, _) in ORES.items() if r == L]
        speed = ', '.join(f'{mining_speed(s):g}' + (' (gold-style)' if s in PRECIOUS else '') for s in sets)
        t.append(f"| {L} | {' / '.join(s.capitalize() for s in sets)} | {world} | {', '.join(ores) if ores else 'everything'} | {speed} | {lore} |")
    t += ['', '| Ore | Needs | Why |', '| --- | --- | --- |']
    for o, (L, why) in ORES.items():
        if L < 4: continue
        t.append(f"| {o.replace('_', ' ').title()} | {pick_name(L).capitalize()} pickaxe or better | {why} |")
    t += ['', 'Code: each set\'s `SimpleTier` uses `zerog_tweaks:incorrect_for_<set>_tool`; ores are in `zerog_tweaks:needs_<pick>_tool`, and the vanilla '
          '`incorrect_for_*_tool` tags lock wood to netherite out of everything above them. The tags are generated in `pending-data/mining-tags/` (copy `data/` onto `src/main/resources/data/`).']
    return '\n'.join(t)

if __name__ == '__main__':
    B = sys.argv[1]
    tags = build_tags()
    for rel, j in tags.items():
        p = f'{B}/pending-data/mining-tags/data/' + rel
        os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(j, open(p, 'w'), indent=2)
    # data manifest
    mp = f'{B}/data-manifest.json'; m = json.load(open(mp))
    m['mining_ladder'] = {'vanilla_levels': VANILLA, 'set_level': SET_LEVEL, 'precious_sets': sorted(PRECIOUS),
                          'mining_speed': {s: mining_speed(s) for s in SET_LEVEL},
                          'ore_required_level': {f'zerog_tweaks:{o}': L for o, (L, _) in ORES.items()}}
    json.dump(m, open(mp, 'w'), indent=2)
    # design doc: replace the old Mining gates bullet + insert section before "**Armor upgrades**"
    dp = f'{B}/ZeroG_Tweaks_Design_Doc.md'; d = open(dp).read()
    d = re.sub(r'\*\*Mining ladder \(v1\.3, locked\)\*\*.*?(?=\n\*\*Armor upgrades\*\*)', '', d, flags=re.S)
    d = d.replace("- Mining gates: each planet's rare ore needs the previous tier's pickaxe, via tool-tier tags.",
                  "- Mining gates: see the Mining ladder below. Nullifite needs netherite; each later ore needs the pickaxe before it.")
    d = d.replace('**Armor upgrades**', doc_section() + '\n\n**Armor upgrades**', 1)
    open(dp, 'w').write(d)
    print(len(tags), 'tag files; levels', min(SET_LEVEL.values()), '-', max(SET_LEVEL.values()))
