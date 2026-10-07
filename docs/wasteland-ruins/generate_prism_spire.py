"""Original climbable Concord ruin; existing blocks/loot, no new story or textures.

Reuses our deterministic NBT writer. Emits matching Design/runtime copies.
Spacing is a conservative starting value, not a final balance approval.
"""
import argparse
import importlib.util
import json
from pathlib import Path

WRITER = Path(__file__).resolve().parents[1] / 'survival-gates/generate_sol_structures.py'
spec = importlib.util.spec_from_file_location('sol_structure_writer', WRITER)
writer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(writer)
Z = 'zerog_tweaks:'


def spire():
    blocks = {}
    def put(x, y, z, state, nbt=None):
        blocks[x, y, z] = (state if ':' in state else Z + state, nbt)
    # Buried foundation and three walkable floors. Explicit air clears interiors.
    for x in range(2, 13):
        for z in range(2, 13):
            put(x, 0, z, 'prismstone')
    for y in (1, 7, 13):
        for x in range(3, 12):
            for z in range(3, 12):
                if (x, z) != (7, 11):
                    put(x, y, z, 'prismstone_bricks')
    # Four intact structural columns; wall damage leaves windows, not blocked access.
    for y in range(2, 18):
        for x, z in ((3, 3), (11, 3), (3, 11), (11, 11)):
            put(x, y, z, 'chiseled_prismstone' if y in (6, 12, 17) else 'prismstone_bricks')
        for x in range(4, 11):
            if (x + y) % 5 and not (x in (6, 7, 8) and y in (2, 3, 4)):
                put(x, y, 3, 'cracked_prismstone_bricks')
            if (x + y) % 4 or x == 7:
                put(x, y, 12, 'prismstone_bricks')
        for z in range(4, 12):
            if (z + y) % 4:
                put(3, y, z, 'cracked_prismstone_bricks')
                put(11, y, z, 'prismstone_bricks')
    # Continuous north-facing ladder, backed by south wall, including floor holes.
    for y in range(1, 16):
        put(7, y, 12, 'prismstone_bricks')
        put(7, y, 11, 'minecraft:ladder[facing=north,waterlogged=false]')
    for y in (5, 11, 17):
        put(3, y, 3, 'pulsar_lamp')
        put(11, y, 11, 'pulsar_lamp')
    # Tapered fractured crown above the loot chamber; does not obstruct chest lid.
    for x, z, height in ((5, 5, 3), (9, 5, 2), (5, 9, 2), (9, 9, 4)):
        for y in range(18, 18 + height):
            put(x, y, z, 'chiseled_prismstone')
    put(7, 14, 7, 'minecraft:chest[facing=north,type=single,waterlogged=false]',
        {'id': 'minecraft:chest', 'LootTable': Z + 'chests/prism_spire'})
    return writer.template((15, 23, 15), blocks)


def resources():
    return {
        'worldgen/structure/prism_spire.json': {
            'type': Z + 'dry_land_jigsaw', 'biomes': '#' + Z + 'has_structure/prism_spire',
            'step': 'surface_structures', 'spawn_overrides': {}, 'terrain_adaptation': 'beard_box',
            'start_pool': Z + 'prism_spire/start', 'size': 1, 'start_height': -1,
            'max_distance_from_center': 48, 'max_height_difference': 8,
            'search_radius': 32, 'always_place': False},
        'worldgen/structure_set/prism_spire.json': {
            'structures': [{'structure': Z + 'prism_spire', 'weight': 1}],
            'placement': {'type': 'minecraft:random_spread', 'spacing': 40,
                          'separation': 20, 'salt': 19477401}},
        'worldgen/template_pool/prism_spire/start.json': {
            'fallback': 'minecraft:empty', 'elements': [{'weight': 1, 'element': {
                'element_type': 'minecraft:single_pool_element', 'location': Z + 'prism_spire/tower',
                'projection': 'rigid', 'processors': 'minecraft:empty'}}]},
        'tags/worldgen/biome/has_structure/prism_spire.json': {
            'replace': False, 'values': [Z + 'wasteland_prism_fields', Z + 'wasteland_crystal_caverns']},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resources', type=Path, required=True)
    args = parser.parse_args()
    for root in (args.resources / 'data/zerog_tweaks', Path(__file__).parent / 'generated/data/zerog_tweaks'):
        for relative, data in resources().items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        path = root / 'structure/prism_spire/tower.nbt'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(spire())
    print('Generated Prism Spire template, pool, structure, placement and habitat tag.')
