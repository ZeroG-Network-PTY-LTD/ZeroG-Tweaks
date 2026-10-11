"""Original flooded relay ruin. Existing artwork/loot; no invented signal dialogue."""
import argparse, importlib.util, json
from pathlib import Path
spec=importlib.util.spec_from_file_location('writer',Path(__file__).resolve().parents[1]/'survival-gates/generate_sol_structures.py')
writer=importlib.util.module_from_spec(spec);spec.loader.exec_module(writer)
Z='zerog_tweaks:'

def relay(variant):
    b={}
    def put(x,y,z,state,nbt=None):b[x,y,z]=(state if ':' in state else Z+state,nbt)
    # Explicit source water keeps this underwater ruin flooded, not a giant air pocket.
    for x in range(19):
        for z in range(19):
            for y in range(12):put(x,y,z,'minecraft:water[level=0]')
            put(x,0,z,'abyssal_stone')
            put(x,1,z,'abyssal_stone_bricks')
    for x in range(3,16):
        for z in range(3,16):
            if x in (3,15) or z in (3,15):
                for y in range(2,7):
                    if z==3 and 8<=x<=10:continue
                    if variant==1 and x==15 and 9<=z<=11 and y>=3:continue
                    put(x,y,z,'corroded_hull' if (x+y+z)%4 else 'hull_plating')
            if not (variant==0 and x>=12 and z<=6):put(x,7,z,'corroded_hull')
    # Two decayed equipment benches, no working controller or free energy cells.
    for x in (5,13):
        for z in range(6,12):put(x,2,z,'chiseled_hull' if z%2 else 'corroded_hull')
        put(x,3,8,'minecraft:iron_bars[waterlogged=true]')
    # A damaged antenna on the rear roof, lit with an existing Pulsar Lamp.
    for y in range(8,11):put(9,y,13,'minecraft:iron_bars[waterlogged=true]')
    for x in range(6,13):
        if x!=6+variant:put(x,10,13,'minecraft:iron_bars[waterlogged=true]')
    for x in (6,12):put(x,6,4,'pulsar_lamp')
    for x in (8,9,10):
        for z in range(2,14):
            for y in (2,3,4):put(x,y,z,'minecraft:water[level=0]')
    put(9,2,14,'minecraft:chest[facing=north,type=single,waterlogged=true]',
        {'id':'minecraft:chest','LootTable':Z+'chests/sunken_relay'})
    return writer.template((19,12,19),b)

def resources():
    name='sunken_relay'
    return {
        f'worldgen/structure/{name}.json':{'type':Z+'submerged_jigsaw','biomes':'#'+Z+'has_structure/'+name,
            'step':'surface_structures','spawn_overrides':{},'terrain_adaptation':'beard_box',
            'start_pool':Z+name+'/start','max_height_difference':6},
        f'worldgen/structure_set/{name}.json':{'structures':[{'structure':Z+name,'weight':1}],
            'placement':{'type':'minecraft:random_spread','spacing':40,'separation':20,'salt':19477409}},
        f'worldgen/template_pool/{name}/start.json':{'fallback':'minecraft:empty','elements':[{'weight':1,'element':{
            'element_type':'minecraft:single_pool_element','location':Z+name+'/small_'+str(v),
            'projection':'rigid','processors':'minecraft:empty'}} for v in (0,1)]},
        f'tags/worldgen/biome/has_structure/{name}.json':{'replace':False,'values':[Z+n for n in (
            'wasteland_deep_trenches','wasteland_kelp_jungles','wasteland_island_chains')]}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--resources',type=Path,required=True);a=p.parse_args()
    for root in (a.resources/'data/zerog_tweaks',Path(__file__).parent/'generated/data/zerog_tweaks'):
        for relative,data in resources().items():
            path=root/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2)+'\n')
        for v in (0,1):
            path=root/f'structure/sunken_relay/small_{v}.nbt';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(relay(v))
    print('Generated two flooded relay layouts; existing Pearl loot, no new dialogue or working machine giveaways.')
