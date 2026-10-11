"""Original small Concord smithy ruin using existing blocks and approved loot."""
import argparse
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('sol_writer', Path(__file__).resolve().parents[1] / 'survival-gates/generate_sol_structures.py')
writer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(writer)
Z = 'zerog_tweaks:'


def forge(variant):
    blocks = {}
    def put(x, y, z, state, nbt=None):
        blocks[x, y, z] = (state if ':' in state else Z + state, nbt)
    for x in range(2, 15):
        for z in range(2, 17):
            put(x, 0, z, 'scoria')
            put(x, 1, z, 'polished_scoria' if (x + z) % 4 else 'scorched_marble')
            if x in (2, 14) or z in (2, 16):
                for y in range(2, 5):
                    if (x + z + y + variant) % 6 != 0:
                        put(x, y, z, 'cobbled_scorched_marble')
    for x in (3, 13):
        for z in (3, 15):
            for y in range(2, 7):
                put(x, y, z, 'chiseled_scorched_marble')
    # Collapsed roof beams leave the floor and central passage open.
    for z in (3, 15):
        for x in range(4, 13):
            if (x + variant) % 3:
                put(x, 6, z, 'charwood_log[axis=x]')
    for x in range(7, 10):
        for y in range(2, 5):
            put(x, y, 2, 'minecraft:air')
            put(x, y, 16, 'minecraft:air')
    # A broken cold chimney, not an automatically running machine or hazard.
    for y in range(2, 7):
        for x, z in ((3, 13), (5, 13), (3, 14), (5, 14), (4, 15)):
            if y < 5 or (x + z + variant) % 2:
                put(x, y, z, 'scorched_marble')
    put(4, 2, 14, 'minecraft:blast_furnace[facing=north,lit=false]')
    put(4, 2, 8, 'minecraft:anvil[facing=north]')
    for z in (7, 8, 9):
        put(12, 2, z, 'charwood_slab[type=bottom,waterlogged=false]')
    put(4, 2, 5, 'tremor_lamp')
    put(12, 2, 14, 'minecraft:chest[facing=west,type=single,waterlogged=false]',
        {'id': 'minecraft:chest', 'LootTable': Z + 'chests/collapsed_forge'})
    for x, z in ((1, 7), (15, 12), (5, 17)):
        put(x, 0, z, 'scoria')
        put(x, 1, z, 'cobbled_scorched_marble')
    return writer.template((17, 8, 19), blocks)


def resources():
    return {
        'worldgen/structure/collapsed_forge.json': {
            'type': Z + 'dry_land_jigsaw', 'biomes': '#' + Z + 'has_structure/collapsed_forge',
            'step': 'surface_structures', 'spawn_overrides': {}, 'terrain_adaptation': 'beard_box',
            'start_pool': Z + 'collapsed_forge/start', 'size': 1, 'start_height': -1,
            'max_distance_from_center': 48, 'max_height_difference': 6,
            'search_radius': 32, 'always_place': False},
        'worldgen/structure_set/collapsed_forge.json': {
            'structures': [{'structure': Z + 'collapsed_forge', 'weight': 1}],
            'placement': {'type': 'minecraft:random_spread', 'spacing': 40, 'separation': 20, 'salt': 19477403}},
        'worldgen/template_pool/collapsed_forge/start.json': {
            'fallback': 'minecraft:empty', 'elements': [{'weight': 1, 'element': {
                'element_type': 'minecraft:single_pool_element', 'location': Z + 'collapsed_forge/small_' + str(v),
                'projection': 'rigid', 'processors': 'minecraft:empty'}} for v in (0, 1)]},
        'tags/worldgen/biome/has_structure/collapsed_forge.json': {'replace': False, 'values': [Z + b for b in (
            'ember_fields', 'marble_contact_zone', 'charwood_barrens', 'wasteland_basalt_fields', 'wasteland_ash_plains')]},
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
            path = root / ('structure/collapsed_forge/small_' + str(v) + '.nbt')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(forge(v))
    print('Generated two Collapsed Forge layouts and volcanic placement resources.')
