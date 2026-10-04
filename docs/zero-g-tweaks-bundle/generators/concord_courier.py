"""Original 7x5x7 Courier crash schematic; existing ZeroG blocks, no external art.

Run using the project's Windows Python with nbtlib installed. Source lives on
Design; --runtime stages only the shipped NBT into a 1.21.x checkout.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, 'C:/Users/jakem/Documents/Codex/2026-09-29/blo/tools/planet-structure-python-deps')
import nbtlib
from nbtlib import Compound, List, Int, String


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--runtime', type=Path, required=True)
    args = parser.parse_args()
    output = Path(__file__).resolve().parents[1] / 'structures' / 'concord_courier'
    output.mkdir(parents=True, exist_ok=True)
    cells = {}
    def put(x, y, z, name, properties=None):
        cells[x, y, z] = (name, properties or {})
    # A shallow, safe crater: replaced topsoil only, not explosive excavation.
    for x in range(7):
        for z in range(7):
            radius = (x - 3) ** 2 + (z - 3) ** 2
            if radius <= 10:
                put(x, 0, z, 'zerog_tweaks:meteorite_fragment' if (x + z) % 3 == 0 else 'zerog_tweaks:corroded_hull')
                if radius >= 8 and (x + z) % 2 == 0:
                    put(x, 1, z, 'zerog_tweaks:meteorite_fragment')
    # Oval voxel hull with an open front and broken roof; chest stays reachable.
    for z in range(1, 6):
        for x in (1, 5):
            put(x, 1, z, 'zerog_tweaks:hull_plating')
            if z in (2, 3, 4):
                put(x, 2, z, 'zerog_tweaks:corroded_hull')
    for x in range(2, 5):
        put(x, 1, 1, 'zerog_tweaks:hull_plating')
    for z in range(2, 5):
        put(2, 3, z, 'zerog_tweaks:hull_plating_slab', {'type': 'bottom', 'waterlogged': 'false'})
        put(4, 3, z, 'zerog_tweaks:hull_plating_slab', {'type': 'bottom', 'waterlogged': 'false'})
    put(3, 1, 1, 'zerog_tweaks:broken_console')
    put(3, 1, 3, 'minecraft:chest', {'facing': 'south', 'type': 'single', 'waterlogged': 'false'})
    put(2, 2, 1, 'zerog_tweaks:selenite_lamp')
    put(4, 1, 5, 'zerog_tweaks:meteorite_fragment')
    palette = []
    blocks = []
    manifest = []
    for position, (name, properties) in sorted(cells.items()):
        state = Compound({'Name': String(name)})
        if properties:
            state['Properties'] = Compound({k: String(v) for k, v in properties.items()})
        if state not in palette:
            palette.append(state)
        block = Compound({'pos': List[Int]([Int(v) for v in position]), 'state': Int(palette.index(state))})
        if name == 'minecraft:chest':
            block['nbt'] = Compound({'id': String('minecraft:chest')})
        blocks.append(block)
        manifest.append({'pos': list(position), 'block': name, 'properties': properties})
    file = nbtlib.File({'DataVersion': Int(3955), 'size': List[Int]([7, 5, 7]),
        'palette': List[Compound](palette), 'blocks': List[Compound](blocks), 'entities': List[Compound]([])})
    source = output / 'concord_courier.nbt'
    file.save(source, gzipped=True)
    (output / 'cells.json').write_text(json.dumps({'size': [7, 5, 7], 'cells': manifest}, indent=2) + '\n')
    target = args.runtime / 'src/main/resources/data/zerog_tweaks/structure/concord_courier.nbt'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
    print(f'Courier: {len(blocks)} blocks, {len(palette)} states; source and runtime NBT identical')


if __name__ == '__main__':
    main()
