"""Original open Sunwarden shrine, existing artwork and unchanged reward table."""
import argparse
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('sol_writer', Path(__file__).resolve().parents[1] / 'survival-gates/generate_sol_structures.py')
writer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(writer)
Z = 'zerog_tweaks:'


def shrine(variant):
    blocks = {}
    def put(x, y, z, state, nbt=None):
        blocks[x, y, z] = (state if ':' in state else Z + state, nbt)
    # Circular grounded court, without rare mineral storage blocks or new hazards.
    for x in range(1, 18):
        for z in range(1, 18):
            distance = (x - 9) ** 2 + (z - 9) ** 2
            if distance > 64:
                continue
            put(x, 0, z, 'solar_stone')
            put(x, 1, z, 'radiant_bricks' if distance >= 45 else 'polished_solar_stone')
    for z in range(1, 18):
        put(9, 1, z, 'gildwood_planks')
    for x, z in ((5, 3), (13, 3), (3, 6), (15, 6), (3, 12), (15, 12), (5, 15), (13, 15)):
        for y in range(2, 7):
            put(x, y, z, 'chiseled_solar_stone')
        put(x, 7, z, 'fusion_lamp')
    for z in (3, 15):
        for x in range(6, 13):
            if (x + variant) % 4:
                put(x, 7, z, 'gildwood_log[axis=x]')
    # Uninscribed rear panel: story hymns need approved writing, not invented logs.
    for x in range(7, 12):
        for y in range(2, 6):
            put(x, y, 16, 'gildwood_planks')
    put(9, 4, 16, 'fusion_lamp')
    for x in (7, 11):
        put(x, 2, 11, 'radiant_bricks')
        put(x, 3, 11, 'gildwood_slab[type=bottom,waterlogged=false]')
    put(9, 2, 14, 'minecraft:chest[facing=north,type=single,waterlogged=false]',
        {'id': 'minecraft:chest', 'LootTable': Z + 'chests/solar_shrine'})
    return writer.template((19, 9, 19), blocks)


def resources():
    return {
        'worldgen/structure/solar_shrine.json': {
            'type': Z + 'dry_land_jigsaw', 'biomes': '#' + Z + 'has_structure/solar_shrine',
            'step': 'surface_structures', 'spawn_overrides': {}, 'terrain_adaptation': 'beard_box',
            'start_pool': Z + 'solar_shrine/start', 'size': 1, 'start_height': -1,
            'max_distance_from_center': 48, 'max_height_difference': 6,
            'search_radius': 32, 'always_place': False},
        'worldgen/structure_set/solar_shrine.json': {
            'structures': [{'structure': Z + 'solar_shrine', 'weight': 1}],
            'placement': {'type': 'minecraft:random_spread', 'spacing': 40, 'separation': 20, 'salt': 19477404}},
        'worldgen/template_pool/solar_shrine/start.json': {
            'fallback': 'minecraft:empty', 'elements': [{'weight': 1, 'element': {
                'element_type': 'minecraft:single_pool_element', 'location': Z + 'solar_shrine/small_' + str(v),
                'projection': 'rigid', 'processors': 'minecraft:empty'}} for v in (0, 1)]},
        'tags/worldgen/biome/has_structure/solar_shrine.json': {'replace': False,
            'values': [Z + b for b in ('corona_flats', 'sunspot_plateaus', 'gildwood_oasis')]},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resources', type=Path, required=True)
    args = parser.parse_args()
    for root in (args.resources / 'data/zerog_tweaks', Path(__file__).parent / 'generated/data/zerog_tweaks'):
        for relative, data in resources().items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, indent=2) + '\n')
        for v in (0, 1):
            path = root / ('structure/solar_shrine/small_' + str(v) + '.nbt')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(shrine(v))
    print('Generated two open Solar Shrines and Solvane placement resources.')
