"""Original partially sand-buried Concord observation room, existing loot only."""
import argparse, importlib.util, json
from pathlib import Path

spec=importlib.util.spec_from_file_location('writer',Path(__file__).resolve().parents[1]/'survival-gates/generate_sol_structures.py')
writer=importlib.util.module_from_spec(spec);spec.loader.exec_module(writer)
Z='zerog_tweaks:'

def observatory(variant):
    blocks={}
    def put(x,y,z,state,nbt=None): blocks[x,y,z]=(state if ':' in state else Z+state,nbt)
    for x in range(2,19):
        for z in range(1,20):
            put(x,0,z,'sunbaked_stone_bricks')
            put(x,1,z,'ruinstone' if (x+z+variant)%5==0 else 'sunbaked_stone_bricks')
    for x in range(4,17):
        for z in range(4,18):
            for y in range(2,7): put(x,y,z,'minecraft:air')
    for x in range(3,18):
        for z in range(3,19):
            if x not in (3,17) and z not in (3,18): continue
            for y in range(2,7):
                if z==3 and x in (9,10,11): continue
                put(x,y,z,'ruinstone' if (x+y+z+variant)%4==0 else 'cracked_sunbaked_stone_bricks')
    for x in range(3,18):
        for z in range(3,19):
            if variant==1 and x>14 and z>15: continue
            put(x,7,z,'hull_plating')
            if x in (3,4,16,17) or z in (3,18): put(x,8,z,'rustsand')
    # Small roof lens and low instrument plinths, clear of the main approach.
    for x in range(9,12):
        for z in range(8,11): put(x,7,z,'crystal_glass')
    for x in (6,14):
        for z in (8,12):
            put(x,2,z,'hull_plating');put(x,3,z,'crystal_glass')
    # Supported side dunes suggest burial without sand falling into the room.
    for x in (2,18):
        for z in range(5,18):
            height=2+(z+variant)%3
            for y in range(2,height+1): put(x,y,z,'sunbaked_stone_bricks')
            put(x,height+1,z,'rustsand')
    for z in range(1,16):
        for y in (2,3): put(10,y,z,'minecraft:air')
    put(10,2,15,'minecraft:chest[facing=north,type=single,waterlogged=false]',
        {'id':'minecraft:chest','LootTable':Z+'chests/buried_observatory'})
    return writer.template((21,11,21),blocks)

def resources():
    name='buried_observatory'
    return {
        f'worldgen/structure/{name}.json':{'type':Z+'dry_land_jigsaw','biomes':'#'+Z+'has_structure/'+name,
            'step':'surface_structures','spawn_overrides':{},'terrain_adaptation':'beard_box','start_pool':Z+name+'/start',
            'size':1,'start_height':-1,'max_distance_from_center':48,'max_height_difference':6,'search_radius':32,'always_place':False},
        f'worldgen/structure_set/{name}.json':{'structures':[{'structure':Z+name,'weight':1}],
            'placement':{'type':'minecraft:random_spread','spacing':40,'separation':20,'salt':19477407}},
        f'worldgen/template_pool/{name}/start.json':{'fallback':'minecraft:empty','elements':[{'weight':1,'element':{
            'element_type':'minecraft:single_pool_element','location':Z+name+'/small_'+str(v),
            'projection':'rigid','processors':'minecraft:empty'}} for v in (0,1)]},
        f'tags/worldgen/biome/has_structure/{name}.json':{'replace':False,'values':[Z+b for b in (
            'wasteland_dune_seas','wasteland_mesa_canyons','wasteland_salt_flats')]}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--resources',type=Path,required=True);a=p.parse_args()
    for root in (a.resources/'data/zerog_tweaks',Path(__file__).parent/'generated/data/zerog_tweaks'):
        for relative,data in resources().items():
            path=root/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2)+'\n')
        for v in (0,1):
            path=root/f'structure/buried_observatory/small_{v}.nbt';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(observatory(v))
    print('Generated two original Observatory rooms; unchanged loot, no new coordinates or lore.')
