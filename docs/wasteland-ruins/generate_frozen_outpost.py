"""Original small Concord cold-weather shelter; existing blocks and unchanged loot."""
import argparse, importlib.util, json
from pathlib import Path

spec=importlib.util.spec_from_file_location('writer',Path(__file__).resolve().parents[1]/'survival-gates/generate_sol_structures.py')
writer=importlib.util.module_from_spec(spec);spec.loader.exec_module(writer)
Z='zerog_tweaks:'

def outpost(variant):
    blocks={}
    def put(x,y,z,state,nbt=None):blocks[x,y,z]=(state if ':' in state else Z+state,nbt)
    for x in range(2,15):
        for z in range(1,16):
            put(x,0,z,'permafrost')
            put(x,1,z,'permafrost_bricks' if x in (2,14) else 'hoarwood_planks')
    # Deliberate air clearing gives the doorway and interior usable headroom.
    for x in range(4,13):
        for z in range(4,14):
            for y in range(2,6):put(x,y,z,'minecraft:air')
    for x in range(3,14):
        for z in range(3,15):
            if x not in (3,13) and z not in (3,14):continue
            for y in range(2,6):
                if z==3 and x in (7,8,9):continue
                put(x,y,z,'hoarwood_planks' if y<5 else 'hull_plating')
    for x,z in ((3,3),(13,3),(3,14),(13,14)):
        for y in range(2,7):put(x,y,z,'hoarwood_log[axis=y]')
    for x in range(3,14):
        for z in range(3,15):
            if variant==1 and x>10 and z>10:continue
            put(x,6,z,'hull_plating')
            if (x+z+variant)%3:put(x,7,z,'minecraft:snow[layers=1]')
    for x in (5,11):put(x,4,4,'spectral_lantern')
    for z in range(1,14):
        for y in (2,3):put(8,y,z,'minecraft:air')
    put(8,2,13,'minecraft:chest[facing=north,type=single,waterlogged=false]',
        {'id':'minecraft:chest','LootTable':Z+'chests/frozen_outpost'})
    return writer.template((17,9,17),blocks)

def resources():
    name='frozen_outpost'
    return {
        f'worldgen/structure/{name}.json':{'type':Z+'dry_land_jigsaw','biomes':'#'+Z+'has_structure/'+name,
            'step':'surface_structures','spawn_overrides':{},'terrain_adaptation':'beard_box','start_pool':Z+name+'/start',
            'size':1,'start_height':-1,'max_distance_from_center':48,'max_height_difference':6,'search_radius':32,'always_place':False},
        f'worldgen/structure_set/{name}.json':{'structures':[{'structure':Z+name,'weight':1}],
            'placement':{'type':'minecraft:random_spread','spacing':40,'separation':20,'salt':19477405}},
        f'worldgen/template_pool/{name}/start.json':{'fallback':'minecraft:empty','elements':[{'weight':1,'element':{
            'element_type':'minecraft:single_pool_element','location':Z+name+'/small_'+str(v),'projection':'rigid','processors':'minecraft:empty'}} for v in (0,1)]},
        f'tags/worldgen/biome/has_structure/{name}.json':{'replace':False,'values':[Z+b for b in (
            'hoarwood_taiga','phantom_ice_sheets','wasteland_glaciers',
            'wasteland_ice_spike_forest','wasteland_frozen_canyons')]}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--resources',type=Path,required=True);a=p.parse_args()
    for root in (a.resources/'data/zerog_tweaks',Path(__file__).parent/'generated/data/zerog_tweaks'):
        for relative,data in resources().items():
            path=root/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2)+'\n')
        for v in (0,1):
            path=root/f'structure/frozen_outpost/small_{v}.nbt';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(outpost(v))
    print('Generated two Frozen Outposts; no lore text or reward changes.')
