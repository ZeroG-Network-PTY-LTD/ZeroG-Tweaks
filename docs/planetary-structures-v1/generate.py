"""Block-exact first translation of the approved water/hot/ice concept sheet.

Produces source specifications only. Structure Workshop validates/exports NBT.
Not an image-identical render, natural-generation activation or gameplay proof.
"""
import json
import math
import argparse
from pathlib import Path

PALETTES = {
    'water_bio_habitat': ('cerulon', 'cerulean_stone_bricks', 'minecraft:purpur_block', 'cerulon_soil', 'cerulon_grass_block', 'minecraft:sea_lantern', 'minecraft:prismarine', 'minecraft:drowned'),
    'hot_ring_monolith': ('skarn', 'skarn_rock_bricks', 'minecraft:red_nether_bricks', 'skarn_soil', 'skarn_grass_block', 'minecraft:shroomlight', 'minecraft:blackstone', 'minecraft:magma_cube'),
    'ice_spire_outpost': ('eidolon', 'frostrock_bricks', 'minecraft:packed_ice', 'eidolon_soil', 'eidolon_grass_block', 'minecraft:sea_lantern', 'minecraft:dark_prismarine', 'minecraft:stray'),
}


def make(name):
    theme, wall, trim, soil, grass, glow, rib, mob = PALETTES[name]
    cells, palette, indices = {}, [], {}

    def put(x, y, z, block, nbt=None):
        if not 0 <= x < 49 or not 0 <= z < 49 or not 0 <= y < 64:
            raise ValueError((x, y, z))
        block = block if ':' in block else 'zerog_tweaks:' + block
        if block not in indices:
            indices[block] = len(palette)
            palette.append({'Name': block})
        entry = {'pos': [x, y, z], 'state': indices[block]}
        if nbt:
            entry['nbt'] = nbt
        cells[x, y, z] = entry

    def box(x0, y0, z0, x1, y1, z1, block):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    put(x, y, z, block)

    # Irregular rounded terrain edge, local soil, no full square artificial lawn.
    for x in range(49):
        for z in range(49):
            radius = math.hypot(x - 24, z - 24)
            if radius > 23 + ((x * 7 + z * 11) % 3 - 1):
                continue
            for y in range(11, 13):
                put(x, y, z, soil if y == 11 else grass)
            if theme == 'eidolon':
                put(x, 13, z, 'minecraft:snow_block')
    # Hollow underground galleries, explicit clearance and two connected rooms.
    box(9, 3, 9, 39, 10, 39, wall)
    box(11, 4, 11, 37, 8, 37, 'minecraft:air')
    box(23, 4, 9, 25, 7, 39, rib)
    box(23, 4, 11, 25, 7, 37, 'minecraft:air')
    for x in (12, 36):
        for z in (12, 36):
            box(x, 4, z, x, 8, z, rib)
            put(x, 8, z, glow)
    table = f'zerog_tweaks:chests/{name}_supplies'
    for x in (14, 34):
        put(x, 4, 14, 'minecraft:chest', {'LootTable': table})
    put(18, 4, 32, 'minecraft:spawner', {'mob': mob})
    # Accessible open staircase from the surface to the galleries.
    for i in range(10):
        y, z = 12 - i, 40 - i
        box(22, y, z, 26, y, z, trim)
        box(22, y + 1, z, 26, min(y + 4, 16), z, 'minecraft:air')
    # Central raised dais and stairs, glowing decorative core (no free machine).
    box(17, 13, 17, 31, 14, 31, rib)
    for i in range(6):
        box(22, 13 + i, 16 - i, 26, 13 + i, 16 - i, trim)
    box(21, 15, 21, 27, 17, 27, wall)
    for x, z in ((21, 21), (27, 21), (21, 27), (27, 27)):
        box(x, 18, z, x, 24, z, rib)
        put(x, 24, z, glow)
    box(23, 18, 23, 25, 21, 25, glow)
    # Stepped spires with ribs and separate heights instead of recoloured clones.
    towers = [(12, 24, 39), (36, 24, 35), (24, 35, 52)]
    if theme == 'skarn':
        towers = [(19, 24, 50), (29, 24, 46), (24, 35, 34)]
    for cx, cz, top in towers:
        for y in range(13, top + 1):
            width = 3 if y < top - 12 else 2 if y < top - 5 else 1 if y < top else 0
            box(cx - width, y, cz - width, cx + width, y, cz + width, wall)
            if width and (y - 13) % 8 == 0:
                box(cx - width - 1, y, cz - width - 1, cx + width + 1, y, cz + width + 1, trim)
            if width and y < top - 5:
                put(cx, y, cz - width, glow if y % 9 == 0 else rib)
    # Circular HOT ring supported by monoliths; WATER/ICE have pointed arches.
    if theme == 'skarn':
        for x in range(5, 44):
            for z in range(5, 44):
                r = math.hypot(x - 24, z - 24)
                if 17 <= r <= 19:
                    put(x, 33, z, trim)
                    put(x, 34, z, rib)
                    if (x + z) % 6 == 0:
                        put(x, 35, z, glow)
        for z in range(6, 25):
            put(19, 33, z, rib)
            put(29, 33, z, rib)
    else:
        for d in range(-17, 18):
            top = 38 - abs(d)
            for thickness in range(2):
                box(24 + d, top, 15 + thickness, 24 + d, top + 1, 15 + thickness, trim)
                box(15 + thickness, top, 24 + d, 15 + thickness, top + 1, 24 + d, trim)
        for x, z in ((7, 15), (41, 15), (15, 7), (15, 41)):
            box(x, 13, z, x + 1, 21, z + 1, rib)
    # Flora is original native material, restrained accents, no ore in soil.
    for x, z in ((7, 24), (40, 32), (32, 7), (10, 37)):
        put(x, 14 if theme == 'eidolon' else 13, z, glow)
    # Final clearance pass: later tower skirts otherwise seal the gallery stairs.
    for i in range(10):
        y,z=12-i,40-i
        box(22,y,z,26,y,z,trim)
        box(22,y+1,z,26,min(y+4,16),z,'minecraft:air')
    loot = {'type': 'minecraft:chest', 'pools': [{'rolls': 3, 'entries': [
        {'type': 'minecraft:item', 'name': 'minecraft:iron_ingot', 'weight': 4},
        {'type': 'minecraft:item', 'name': 'minecraft:copper_ingot', 'weight': 6},
        {'type': 'minecraft:item', 'name': 'minecraft:string', 'weight': 3},
        {'type': 'minecraft:item', 'name': 'minecraft:torch', 'weight': 3}]}]}
    return {'schema': 1, 'size': [49, 64, 49], 'palette': palette,
            'blocks': list(cells.values()), 'loot_tables': {table: loot},
            'metadata': {'concept': name, 'planet': theme, 'surface_layer': 12,
                         'status': 'first block translation; visual comparison pending',
                         'natural_generation': False, 'mob_balance': 'test spawner defaults only'}}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path(__file__).parent/'sources-v1')
    dest=parser.parse_args().output
    dest.mkdir(exist_ok=True)
    for name in PALETTES:
        path = dest / (name + '.json')
        if path.exists():
            raise SystemExit('Refuse to overwrite an authored source: ' + str(path))
        path.write_text(json.dumps(make(name), indent=2) + '\n', encoding='utf-8')
        print(path)
