"""Original static Concord impact remnants, not the timed comet event."""
import argparse, importlib.util, json
from pathlib import Path

spec = importlib.util.spec_from_file_location('writer', Path(__file__).resolve().parents[1] / 'survival-gates/generate_sol_structures.py')
writer = importlib.util.module_from_spec(spec); spec.loader.exec_module(writer)
Z = 'zerog_tweaks:'

def impact(variant):
    blocks = {}
    def put(x, y, z, state, nbt=None):
        blocks[x,y,z] = (state if ':' in state else Z+state, nbt)
    for x in range(1,20):
        for z in range(1,20):
            d = (x-10)**2 + (z-10)**2
            if d > 90: continue
            put(x,0,z,'craterstone' if (x+z+variant)%4 else 'cobbled_craterstone')
            if d >= 56:
                put(x,1,z,'cobbled_craterstone')
            else:
                for y in range(1,5): put(x,y,z,'minecraft:air')
    # Low, broken hull fragments stay out of the north approach and chest lid.
    for x,z in ((5,8),(6,8),(6,9),(14,9),(15,9),(15,10)):
        put(x,1,z,'hull_plating')
        if (x+z+variant)%2: put(x,2,z,'hull_plating')
    for x,z in ((7,12),(8,12),(13,13),(14,13)):
        put(x,1,z,'meteorite_fragment')
    for z in range(1,15):
        put(10,0,z,'craterstone')
        for y in range(1,4): put(10,y,z,'minecraft:air')
    put(10,1,14,'minecraft:chest[facing=north,type=single,waterlogged=false]',
        {'id':'minecraft:chest','LootTable':Z+'chests/impact_site'})
    return writer.template((21,7,21), blocks)

def resources():
    name = 'impact_site'
    return {
        f'worldgen/structure/{name}.json':{'type':Z+'dry_land_jigsaw','biomes':'#'+Z+'has_structure/'+name,
            'step':'surface_structures','spawn_overrides':{},'terrain_adaptation':'beard_box','start_pool':Z+name+'/start',
            'size':1,'start_height':-1,'max_distance_from_center':48,'max_height_difference':6,'search_radius':32,'always_place':False},
        f'worldgen/structure_set/{name}.json':{'structures':[{'structure':Z+name,'weight':1}],
            'placement':{'type':'minecraft:random_spread','spacing':40,'separation':20,'salt':19477406}},
        f'worldgen/template_pool/{name}/start.json':{'fallback':'minecraft:empty','elements':[{'weight':1,'element':{
            'element_type':'minecraft:single_pool_element','location':Z+name+'/small_'+str(v),
            'projection':'rigid','processors':'minecraft:empty'}} for v in (0,1)]},
        f'tags/worldgen/biome/has_structure/{name}.json':{'replace':False,'values':[Z+b for b in (
            'wasteland_cratered_plains','wasteland_dust_badlands','wasteland_canyon_scars')]}}

if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('--resources',type=Path,required=True); a=p.parse_args()
    for root in (a.resources/'data/zerog_tweaks',Path(__file__).parent/'generated/data/zerog_tweaks'):
        for relative,data in resources().items():
            path=root/relative; path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(data,indent=2)+'\n')
        for v in (0,1):
            path=root/f'structure/impact_site/small_{v}.nbt'; path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(impact(v))
    print('Generated two static Impact Sites; unchanged loot, no story text or timed event changes.')
