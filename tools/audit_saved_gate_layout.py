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
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'dev'))
from worldscan import _read
from generate_gate_build_guide import parts


def rotate(pos, facing):
    x, y, z = pos
    return {'north': (x,y,z), 'east': (-z,y,x),
            'south': (-x,y,-z), 'west': (z,y,-x)}[facing]


SIDES = ('north', 'east', 'south', 'west')
SERVICES = {'gate_controller', 'gate_energy_port'}


@lru_cache(None)
def core(tier, facing):
    return tuple((rotate(p, facing), 'zerog_tweaks:'+b)
                 for p,b in parts(tier).items() if b not in SERVICES)


@lru_cache(None)
def service_slots(tier, facing):
    occupied = {p for p,b in core(tier,facing)}
    r=tier+1
    return tuple(p for x in range(-r,r+1) for z in range(-r,r+1)
                 if max(abs(x),abs(z))>=2
                 if (p:=rotate((x,1,z),facing)) not in occupied)


def resolve_layout(state, controller, facing, controllers, shared_check=True):
    """Read-only mirror of SurvivalGateFormation; no terrain or entity creation."""
    def add(a,b): return tuple(a[i]+b[i] for i in range(3))
    def name(p): return state(p)['Name']
    shift=rotate((0,1,-2),facing)
    fallback={'centre':tuple(controller[i]-shift[i] for i in range(3)),
              'structural_facing':facing,'formed_tier':0,'core_tier':0,
              'ports':[], 'problem':'Required structure is incomplete.'}
    if name(controller)!='zerog_tweaks:gate_controller':return fallback
    directions=SIDES[SIDES.index(facing):]+SIDES[:SIDES.index(facing)]
    formed=None;outline=fallback;best_score=-1
    for dx in range(-7,8):
        for dz in range(-7,8):
            centre=add(controller,(dx,-1,dz))
            if name(centre)!='zerog_tweaks:gate_pad_plate':continue
            anchors=sum(name(add(centre,(x,0,z)))=='zerog_tweaks:gate_pylon'
                        for x in (-2,2) for z in (-2,2))
            if anchors<2:continue
            here=None
            for direction in directions:
                score=anchors*100+sum(name(add(centre,p))==b for p,b in core(2,direction))
                if score>best_score:
                    best_score=score;outline=dict(fallback,centre=centre,structural_facing=direction)
                if anchors<4:continue
                for tier in range(6,0,-1):
                    if here and tier<=here['formed_tier']:break
                    if not all(name(add(centre,p))==b for p,b in core(tier,direction)):continue
                    legal=service_slots(tier,direction);r=tier+1
                    count=sum(name(add(centre,(x,1,z)))=='zerog_tweaks:gate_controller'
                              for x in range(-r,r+1) for z in range(-r,r+1))
                    ports=[add(centre,p) for p in legal if name(add(centre,p))=='zerog_tweaks:gate_energy_port']
                    required=4 if tier>=5 else 2 if tier>=3 else 1
                    local=tuple(controller[i]-centre[i] for i in range(3))
                    problem=('Illegal controller service position.' if local not in legal else
                             'Duplicate or missing controller.' if count!=1 else
                             f'Need {required-len(ports)} more energy ports.' if len(ports)<required else '')
                    candidate={'centre':centre,'structural_facing':direction,
                               'formed_tier':0 if problem else tier,'core_tier':tier,
                               'ports':ports,'problem':problem}
                    if tier>outline['core_tier'] or tier==outline['core_tier'] and score>=best_score: outline=candidate
                    if not problem:here=candidate;break
            if here:
                if formed and formed['centre']!=here['centre']:
                    return dict(formed,formed_tier=0,problem='Controller matches multiple complete structures.')
                formed=here
    result=formed or outline
    if shared_check and result['formed_tier']:
        for other,other_facing in controllers:
            if other==controller or other[1]!=controller[1]:continue
            if not any(abs(p[0]-other[0])<=14 and abs(p[2]-other[2])<=14 for p in result['ports']):continue
            neighbour=resolve_layout(state,other,other_facing,controllers,False)
            if neighbour['formed_tier'] and set(neighbour['ports'])&set(result['ports']):
                return dict(result,formed_tier=0,problem='Energy port shared with another complete gate.')
    return result


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

    @lru_cache(None)
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
    service_controllers=[(tuple(be[k] for k in ('x','y','z')),
                          state(tuple(be[k] for k in ('x','y','z'))).get('Properties',{}).get('facing','north'))
                         for be in controllers]
    for be in controllers:
        pos = tuple(be[k] for k in ('x','y','z'))
        facing = state(pos).get('Properties',{}).get('facing','north')
        alternatives = {f:missing(pos,f,1) for f in ('north','east','south','west')}
        best = min([facing]+[f for f in alternatives if f != facing], key=lambda f:len(alternatives[f]))
        resolved=resolve_layout(state,pos,facing,service_controllers)
        result.append(dict(resolved,controller=pos,facing=facing,
                       saved_fe=be.get('FE',0),closest_facing=resolved['structural_facing'],
                       legacy_fixed_t1_missing=alternatives[best]))
    return {'world':world.name,'read_only':True,'gates':result}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--world',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(audit(args.world),indent=2))
