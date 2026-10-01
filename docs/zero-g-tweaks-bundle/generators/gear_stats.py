"""Gear stats v1.3: every set above netherite, scaled by its mining-ladder level (mining_ladder.py).
Rewrites the design doc's 'Gear stats and abilities' table + Strength wording, and data-manifest 'gear_stats'.
Usage: python3 gear_stats.py <bundle_dir>"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mining_ladder as ML

# netherite reference: armor 3/8/6/3 = 20, toughness 3, knockback 10%, tools 1.3x diamond durability, sword 8
SPLIT = {21: (4, 8, 6, 3), 22: (4, 8, 6, 4), 23: (4, 9, 6, 4), 24: (4, 9, 7, 4), 25: (5, 9, 7, 4), 26: (5, 9, 7, 5),
         27: (5, 10, 7, 5), 28: (5, 10, 8, 5), 29: (6, 10, 8, 5), 30: (6, 10, 8, 6)}
TOTAL = {5: 21, 6: 21, 7: 22, 8: 22, 9: 23, 10: 23, 11: 24, 12: 24, 13: 25, 14: 25, 15: 26, 16: 26, 17: 27, 18: 27, 19: 28, 20: 30}
ORDER = ['nullifite', 'olympium', 'cerulite', 'skarnite', 'eidolite', 'solvanite', 'ferrox', 'moonsteel', 'cobaltium', 'cyrrium',
         'aurelion', 'ruskite', 'tectium', 'pyrium', 'salvium', 'wraithsteel', 'palladine', 'photium', 'astrium', 'radiantine']
MAIN_TIER = {'nullifite': 'T1', 'olympium': 'T2', 'cerulite': 'T3', 'skarnite': 'T4', 'eidolite': 'T5', 'solvanite': 'T6'}

def stats(s):
    L = ML.SET_LEVEL[s]; prec = s in ML.PRECIOUS
    tot = TOTAL[L] - (1 if prec else 0); tot = max(21, tot)
    tough = 3 + 0.5 * (L - 4) - (1 if prec else 0)
    kb = 10 if prec else 10 + (L - 4)
    dur = round(1.3 + 0.1 * (L - 4), 2)
    if prec: dur = round(max(1.35, round(dur * 0.75 * 20) / 20), 2)
    sword = 8 + 0.5 * (L - 4)
    tier = MAIN_TIER.get(s, 'Precious' if prec else 'Metal')
    note = ''
    if s == 'tectium': note = ' (slower swing)'
    if prec: note = ' (faster swing)'
    return dict(set=s, level=L, tier=tier, armor=SPLIT[tot], toughness=tough, knockback=kb, durability=dur, sword=sword, note=note)

def fmt(x): return f'{x:g}'

def table_md():
    rows = ['| Set | Tier | Level | Armor (helm/chest/legs/boots) | Toughness | Knockback resist | Durability | Sword damage |',
            '| --- | --- | --- | --- | --- | --- | --- | --- |',
            '| *Netherite (vanilla)* | | 4 | 3/8/6/3 (20) | 3 | 10% | 1.3× | 8 |']
    for s in ORDER:
        t = stats(s); a = t['armor']
        rows.append(f"| {s.capitalize()} | {t['tier']} | {t['level']} | {'/'.join(map(str, a))} ({sum(a)}) | {fmt(t['toughness'])} | {t['knockback']}% | {fmt(t['durability'])}× | {fmt(t['sword'])}{t['note']} |")
    return '\n'.join(rows)

def strength_word(s):
    L = ML.SET_LEVEL[s]
    band = 'just above netherite' if L <= 6 else 'well above netherite' if L <= 11 else 'far above netherite' if L <= 17 else 'endgame' if L == 20 else 'near endgame'
    return f'Level {L}: {band}' + ('; gold-style' if s in ML.PRECIOUS else '')

if __name__ == '__main__':
    B = sys.argv[1]; dp = f'{B}/ZeroG_Tweaks_Design_Doc.md'; d = open(dp).read()
    # replace the stats table and its intro line
    start = d.index('**Gear stats and abilities')
    head_end = d.index('\n', start)
    tbl_start = d.index('| Set | Tier |', start); tbl_end = d.index('\n\n', tbl_start)
    intro = ('**Gear stats and abilities (v1.3, locked)**\n\n'
             'Every set is above netherite and gets stronger with its mining-ladder level. Netherite reference: armor 3/8/6/3 (20), toughness 3, '
             '10% knockback resistance, 1.3× diamond durability, sword damage 8. Armor stays at or under 30 points because Minecraft caps armor at 30; '
             'higher sets grow mostly in toughness. Durability is relative to diamond. Gold-style sets (Aurelion, Pyrium, Palladine, Radiantine) trade '
             'armor, toughness and durability for speed and enchantability.\n\n')
    d = d[:start] + intro + table_md() + d[tbl_end:]
    # strength wording in the two summary tables
    def fix_row(m):
        cells = [c.strip() for c in m.group(0).strip('|').split('|')]
        k = cells[0].lower()
        if k in ML.SET_LEVEL:
            if len(cells) == 4: cells[2] = strength_word(k)     # main sets: Set | Made from | Strength | Set bonus
            elif len(cells) == 5: cells[3] = strength_word(k)   # metal sets: Set | World | Role | Strength | Perk
        return '| ' + ' | '.join(cells) + ' |'
    for sec in ('## Gear', '**Metal gear sets**'):
        i = d.index(sec); j = d.index('\n\n', d.index('| ---', i))
        block = re.sub(r'^\|[^\n]*\|$', fix_row, d[i:j], flags=re.M)
        d = d[:i] + block + d[j:]
    d = d.replace('Strengths are starting points for playtesting.', 'Every set is above netherite; exact numbers are in the stats table below and are starting points for playtesting.')
    open(dp, 'w').write(d)
    mp = f'{B}/data-manifest.json'; m = json.load(open(mp))
    m['gear_stats'] = {s: {k: (list(v) if isinstance(v, tuple) else v) for k, v in stats(s).items() if k != 'set'} for s in ORDER}
    json.dump(m, open(mp, 'w'), indent=2)
    print(table_md())
