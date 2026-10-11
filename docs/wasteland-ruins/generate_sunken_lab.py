"""Original abandoned toxic-world laboratory; existing blocks and unchanged loot."""
import argparse,importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('writer',Path(__file__).resolve().parents[1]/'survival-gates/generate_sol_structures.py')
writer=importlib.util.module_from_spec(spec);spec.loader.exec_module(writer)
Z='zerog_tweaks:'

def lab(variant):
    blocks={}
    def put(x,y,z,state,nbt=None):blocks[x,y,z]=(state if ':' in state else Z+state,nbt)
    for x in range(2,27):
        for z in range(1,24):
            put(x,0,z,'sludgestone')
            put(x,1,z,'polished_sludgestone' if x not in (13,14,15) else 'hull_plating')
    for x in range(4,25):
        for z in range(4,22):
            for y in range(2,8):put(x,y,z,'minecraft:air')
    for x in range(3,26):
        for z in range(3,23):
            if x not in (3,25) and z not in (3,22):continue
            for y in range(2,8):
                if z==3 and x in (13,14,15):continue
                put(x,y,z,'hull_plating' if y in (2,7) else 'cracked_sludgestone_bricks')
    for x in range(3,26):
        for z in range(3,23):
            if x>21 and z>18 and variant==1:continue
            if 7<x<11 and 14<z<18 and variant==0:continue
            put(x,8,z,'hull_plating')
    # Chemistry benches: real, empty vanilla apparatus; no preloaded recipes.
    for x in range(5,12):
        put(x,2,6,'polished_sludgestone')
        put(x,2,12,'hull_plating')
    for x in (6,10):put(x,3,6,'minecraft:brewing_stand[has_bottle_0=false,has_bottle_1=false,has_bottle_2=false]')
    for x in (6,10):put(x,2,9,'minecraft:cauldron')
    for x in (5,9,11):put(x,3,12,'minecraft:potted_brown_mushroom' if x%3 else 'minecraft:potted_red_mushroom')
    # Four synthesis/containment chambers: solid bases, ring walls and exposed cap.
    for i,(cx,cz) in enumerate(((19,7),(23,7),(19,14),(23,14))):
        for dx in (-1,0,1):
            for dz in (-1,0,1):
                put(cx+dx,2,cz+dz,'chiseled_hull')
                put(cx+dx,7,cz+dz,'hull_plating')
                if dx or dz:
                    for y in range(3,7):
                        if i==(1 if variant==0 else 2) and dz==-1 and dx==0 and y in (4,5):continue
                        put(cx+dx,y,cz+dz,'minecraft:lime_stained_glass' if i<2 else 'minecraft:cyan_stained_glass')
        put(cx,3,cz,'minecraft:potted_red_mushroom' if i%2 else 'minecraft:potted_brown_mushroom')
    # Broken tube remnant: missing upper glass, bare structural rib beside aisle.
    put(17,2,10,'chiseled_hull');put(17,3,10,'minecraft:iron_bars')
    # Dead power cabinets and disconnected cable tray are scenery, not FE storage.
    for x in (5,8,11):
        for y in range(2,5):put(x,y,19,'chiseled_hull')
        put(x,3,18,'minecraft:iron_bars');put(x,5,19,'hull_plating')
    for x in range(5,12):
        if x!=7+variant:put(x,6,19,'minecraft:iron_bars')
    for x in (5,23):put(x,6,4,'pulsar_lamp')
    # Wide service spine and safe chest approach stay clear of apparatus.
    for x in (13,14,15):
        for z in range(1,21):
            for y in (2,3):put(x,y,z,'minecraft:air')
    put(14,2,20,'minecraft:chest[facing=north,type=single,waterlogged=false]',
        {'id':'minecraft:chest','LootTable':Z+'chests/sunken_lab'})
    return writer.template((29,12,25),blocks)

def resources():
    name='sunken_lab'
    return {
        f'worldgen/structure/{name}.json':{'type':Z+'dry_land_jigsaw','biomes':'#'+Z+'has_structure/'+name,
            'step':'surface_structures','spawn_overrides':{},'terrain_adaptation':'beard_box','start_pool':Z+name+'/start',
            'size':1,'start_height':-1,'max_distance_from_center':64,'max_height_difference':6,'search_radius':32,'always_place':False},
        f'worldgen/structure_set/{name}.json':{'structures':[{'structure':Z+name,'weight':1}],
            'placement':{'type':'minecraft:random_spread','spacing':40,'separation':20,'salt':19477408}},
        f'worldgen/template_pool/{name}/start.json':{'fallback':'minecraft:empty','elements':[{'weight':1,'element':{
            'element_type':'minecraft:single_pool_element','location':Z+name+'/small_'+str(v),'projection':'rigid','processors':'minecraft:empty'}} for v in (0,1)]},
        f'tags/worldgen/biome/has_structure/{name}.json':{'replace':False,'values':[Z+b for b in (
            'wasteland_acid_swamps','wasteland_mud_flats','wasteland_moss_bogs')]}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--resources',type=Path,required=True);a=p.parse_args()
    for root in (a.resources/'data/zerog_tweaks',Path(__file__).parent/'generated/data/zerog_tweaks'):
        for relative,data in resources().items():
            path=root/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2)+'\n')
        for v in (0,1):
            path=root/f'structure/sunken_lab/small_{v}.nbt';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(lab(v))
    print('Generated two laboratory ruins: chemistry, synthesis, biology and dead power scenery; unchanged loot.')
