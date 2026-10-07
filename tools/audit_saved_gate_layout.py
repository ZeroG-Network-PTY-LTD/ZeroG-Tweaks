"""Read-only saved Overworld gate comparison. No world loads or writes.

Uses the reviewed layout mirror in generate_gate_build_guide.py and the existing
NBT reader. Reports actual and best-fitting facings, missing blocks and saved FE.
Run against a closed client's save; this does not certify live power transfer.
"""
import argparse
import json
import struct
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'dev'))
from worldscan import _read
from generate_gate_build_guide import parts


def rotate(pos, facing):
    x, y, z = pos
    return {'north': (x,y,z), 'east': (-z,y,x),
            'south': (-x,y,-z), 'west': (z,y,-x)}[facing]


def audit(world):
    chunks = {}
    controllers = []
    for path in sorted((world / 'region').glob('*.mca')):
        raw = path.read_bytes()
        for i in range(1024):
            offset = struct.unpack_from('>I', raw, i*4)[0]
            if not offset:
                continue
            start = (offset >> 8)*4096
            length = struct.unpack_from('>I', raw, start)[0]
            if raw[start+4] != 2:
                raise ValueError(f'Unsupported region compression in {path.name}')
            payload = zlib.decompress(raw[start+5:start+4+length])
            chunk = _read(payload, 3+struct.unpack_from('>H', payload, 1)[0], 10)[0]
            chunks[chunk['xPos'], chunk['zPos']] = chunk
            controllers.extend(b for b in chunk.get('block_entities', [])
                               if b.get('id') == 'zerog_tweaks:survival_gate_controller')

    def state(pos):
        x,y,z = pos
        chunk = chunks.get((x//16,z//16))
        if chunk is None:
            return {'Name': 'unloaded_saved_chunk'}
        section = next((s for s in chunk['sections'] if
                        ((s['Y']+128)%256-128) == y//16), None)
        if not section or 'block_states' not in section:
            return {'Name': 'minecraft:air'}
        blocks = section['block_states']; palette = blocks['palette']
        if len(palette) == 1:
            return palette[0]
        index = (y%16)*256+(z%16)*16+x%16
        bits = max(4,(len(palette)-1).bit_length()); per = 64//bits
        return palette[(blocks['data'][index//per] >> ((index%per)*bits)) & ((1<<bits)-1)]

    def missing(controller, facing, tier):
        shift = rotate((0,1,-2), facing)
        centre = tuple(controller[i]-shift[i] for i in range(3))
        result = []
        for offset, block in parts(tier).items():
            delta = rotate(offset,facing)
            pos = tuple(centre[i]+delta[i] for i in range(3))
            actual = state(pos)['Name']; expected = 'zerog_tweaks:'+block
            if actual != expected:
                result.append({'pos':pos,'expected':expected,'actual':actual})
        return result

    result = []
    for be in controllers:
        pos = tuple(be[k] for k in ('x','y','z'))
        facing = state(pos).get('Properties',{}).get('facing','north')
        alternatives = {f:missing(pos,f,1) for f in ('north','east','south','west')}
        best = min([facing]+[f for f in alternatives if f != facing], key=lambda f:len(alternatives[f]))
        formed = max([0]+[tier for tier in range(1,7) if not missing(pos,facing,tier)])
        result.append({'controller':pos,'facing':facing,'formed_tier':formed,
                       'saved_fe':be.get('FE',0),'closest_facing':best,
                       'closest_t1_missing':alternatives[best]})
    return {'world':world.name,'read_only':True,'gates':result}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--world',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(audit(args.world),indent=2))
