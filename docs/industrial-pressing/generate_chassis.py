"""Native one-block open press chamber, reuse original approved metal/terminal art.
Geometry only; concept comparison/client appearance still requires review.
"""
import argparse,json
from pathlib import Path


def cube(a,b,texture):
    return {'from':a,'to':b,'faces':{side:{'texture':'#'+texture} for side in ('north','south','east','west','up','down')}}


def generate(resources):
    elements=[]
    for a,b in [([0,0,12],[16,16,16]),([0,0,0],[3,16,12]),([13,0,0],[16,16,12]),
                ([3,0,0],[13,3,12]),([3,13,0],[13,16,12])]:elements.append(cube(a,b,'dark'))
    for x in (0,14):
        for z in (0,14):elements.append(cube([x,0,z],[x+2,16,z+2],'silver'))
    elements.append(cube([3,0,0],[13,3,.2],'terminal'))
    elements.append(cube([3,3,1],[13,3.5,11],'silver'))
    model={'parent':'minecraft:block/block','textures':{'particle':'zerog_tweaks:block/alloy_forge_side',
        'dark':'zerog_tweaks:block/alloy_forge_side','silver':'minecraft:block/iron_block',
        'terminal':'zerog_tweaks:block/gate_controller_front'},'elements':elements}
    target=resources/'assets/zerog_tweaks/models/block/industrial_compressor.json'
    target.write_text(json.dumps(model,indent=2)+'\n')
    # Robust reusable die: four raised rails and recessed bed, not a finished cog.
    for kind in ('plate','cog'):
        parts=[cube([2,6,2],[14,7,14],'metal')]
        for a,b in [([2,7,2],[14,9,4]),([2,7,12],[14,9,14]),([2,7,4],[4,9,12]),([12,7,4],[14,9,12])]:parts.append(cube(a,b,'metal'))
        if kind=='cog':
            for x,z in ((5,5),(8,4),(10,5),(11,8),(10,10),(8,11),(5,10),(4,8)):
                parts.append(cube([x,7,z],[x+2,8,z+2],'metal'))
        die={'parent':'minecraft:block/block','textures':{'particle':'minecraft:block/iron_block','metal':'minecraft:block/iron_block'},
            'elements':parts,'display':{'gui':{'rotation':[30,225,0],'scale':[.9,.9,.9]}}}
        (resources/f'assets/zerog_tweaks/models/item/{kind}_press.json').write_text(json.dumps(die,indent=2)+'\n')
        (Path(__file__).parent/f'models/item/{kind}_press.json').write_text(json.dumps(die,indent=2)+'\n')
    return model


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--resources',type=Path,required=True)
    model=generate(parser.parse_args().resources)
    (Path(__file__).parent/'models/block/industrial_compressor.json').write_text(json.dumps(model,indent=2)+'\n')
    print('Open chassis and two recessed reusable die models exported; no new texture claims.')
