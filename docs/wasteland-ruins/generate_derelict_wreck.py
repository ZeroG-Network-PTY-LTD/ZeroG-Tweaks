"""First small Hollow Fleet wreck; existing blocks and unchanged approved loot.

No new story text, textures, mobs, console behavior or boss encounter.
"""
import argparse
import importlib.util
import json
from pathlib import Path

WRITER = Path(__file__).resolve().parents[1] / 'survival-gates/generate_sol_structures.py'
spec = importlib.util.spec_from_file_location('sol_writer', WRITER)
writer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(writer)
Z = 'zerog_tweaks:'


def wreck(variant):
    blocks = {}
    def put(x, y, z, state, nbt=None):
        blocks[x, y, z] = (state if ':' in state else Z + state, nbt)
    # Grounded narrow ship, tapering prow and a broken stern. Interior air is explicit.
    for z in range(2, 25):
        width = 3 if z < 5 or z > 22 else 5
        for x in range(9 - width, 10 + width):
            put(x, 0, z, 'frozen_regolith')
            put(x, 1, z, 'corroded_hull' if (x + z + variant) % 5 == 0 else 'hull_plating')
        for x in (9 - width, 9 + width):
            for y in range(2, 6):
                if z not in (10, 11, 12) and (z + y + variant) % 7 != 0:
                    put(x, y, z, 'corroded_hull')
    # Four surviving ribs outline the vessel without sealing access or loot.
    for z in (5, 9, 15, 21):
        for y in range(2, 7):
            put(4, y, z, 'hull_plating')
            put(14, y, z, 'hull_plating')
        for x in range(5, 14):
            if (x + z + variant) % 4:
                put(x, 7 if 7 <= x <= 11 else 6, z, 'corroded_hull')
    # Two-wide side breach opens directly onto the central walkable corridor.
    for x in range(4, 15):
        for y in (2, 3, 4):
            for z in (10, 11):
                put(x, y, z, 'minecraft:air')
    for x, z in ((6, 6), (12, 6), (6, 19), (12, 19)):
        put(x, 2, z, 'cryo_pod')
    put(7, 2, 22, 'broken_console')
    put(11, 2, 22, 'broken_console')
    put(9, 2, 4, 'spectral_lantern')
    put(9, 2, 20, 'spectral_lantern')
    # Debris remains inside the declared footprint; no container is hidden below terrain.
    for x, z in ((1, 8), (16, 17), (2, 20), (15, 3)):
        put(x, 0, z, 'frozen_regolith')
        put(x, 1, z, 'corroded_hull')
    put(9, 2, 16, 'minecraft:chest[facing=north,type=single,waterlogged=false]',
        {'id': 'minecraft:chest', 'LootTable': Z + 'chests/derelict_wreck'})
    return writer.template((19, 9, 27), blocks)


def resources():
    return {
        'worldgen/structure/derelict_wreck.json': {
            'type': Z + 'dry_land_jigsaw', 'biomes': '#' + Z + 'has_structure/derelict_wreck',
            'step': 'surface_structures', 'spawn_overrides': {}, 'terrain_adaptation': 'beard_box',
            'start_pool': Z + 'derelict_wreck/start', 'size': 1, 'start_height': -1,
            'max_distance_from_center': 48, 'max_height_difference': 6,
            'search_radius': 32, 'always_place': False},
        'worldgen/structure_set/derelict_wreck.json': {
            'structures': [{'structure': Z + 'derelict_wreck', 'weight': 1}],
            'placement': {'type': 'minecraft:random_spread', 'spacing': 40,
                          'separation': 20, 'salt': 19477402}},
        'worldgen/template_pool/derelict_wreck/start.json': {
            'fallback': 'minecraft:empty', 'elements': [{'weight': 1, 'element': {
                'element_type': 'minecraft:single_pool_element',
                'location': Z + 'derelict_wreck/small_' + str(variant),
                'projection': 'rigid', 'processors': 'minecraft:empty'}} for variant in (0, 1)]},
        'tags/worldgen/biome/has_structure/derelict_wreck.json': {
            'replace': False, 'values': [Z + 'frozen_graveyard']},
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
        for variant in (0, 1):
            path = root / ('structure/derelict_wreck/small_' + str(variant) + '.nbt')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(wreck(variant))
    print('Generated two small derelict wrecks and Frozen Graveyard placement resources.')
