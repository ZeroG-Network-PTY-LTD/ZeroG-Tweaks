"""Compile pressing recipes and original cube models using existing approved metal textures.

No new pixel artwork is claimed: bespoke chassis/press art remains a design task.
Costs preserve the existing two-ingot plate/four-ingot cog material budget.
Survival recipes for the machine and tooling remain deferred for balance approval.
"""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'src/main/resources'
def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n')
source=(ROOT/'src/main/java/net/zerog/tweaks/registry/ZGManufacturingComponents.java').read_text()
metals=re.findall(r'"([a-z_]+)"',source.split('List.of(',1)[1].split(');',1)[0])
metals.append('copper')
for metal in metals:
    for mode,input_id,output_id,count,energy,ticks in (
        ('plate',metal+'_ingot',metal+'_plate',2,2000,100),
        ('cog',metal+'_ingot',metal+'_cog',4,4000,160)):
        write(RES/f'data/zerog_tweaks/recipe/pressing/{metal}_{mode}.json',{
            'type':'zerog_tweaks:pressing',
            'inputs':[{'ingredient':{'item':('minecraft:' if metal=='copper' else 'zerog_tweaks:')+input_id},'count':count}],
            'catalyst':{'ingredient':{'item':'zerog_tweaks:'+mode+'_press'},'count':1,'consumed':False},
            'outputs':[{'stack':{'id':'zerog_tweaks:'+output_id,'count':1}}],
            'energy':energy,'time':ticks})
assets=RES/'assets/zerog_tweaks'
write(assets/'blockstates/industrial_compressor.json',{'variants':{
    'facing='+face:{'model':'zerog_tweaks:block/industrial_compressor','y':angle}
    for face,angle in [('north',0),('east',90),('south',180),('west',270)]}})
# Chassis/die geometry belongs to Design/docs/industrial-pressing/generate_chassis.py.
# Preserve its open chamber and recessed dies; never restore older cube models.
write(assets/'models/item/industrial_compressor.json',{'parent':'zerog_tweaks:block/industrial_compressor'})
write(RES/'data/zerog_tweaks/loot_table/blocks/industrial_compressor.json',{'type':'minecraft:block',
    'pools':[{'rolls':1,'entries':[{'type':'minecraft:item','name':'zerog_tweaks:industrial_compressor'}],
              'conditions':[{'condition':'minecraft:survives_explosion'}]}]})
for tag in ['mineable/pickaxe','needs_iron_tool']:
    path=RES/f'data/minecraft/tags/block/{tag}.json'
    value=json.loads(path.read_text());value['values']=sorted(set(value['values']+['zerog_tweaks:industrial_compressor']))
    write(path,value)
path=assets/'lang/en_us.json';lang=json.loads(path.read_text())
lang.update({'block.zerog_tweaks.industrial_compressor':'Industrial Compressor',
             'item.zerog_tweaks.plate_press':'Plate Press','item.zerog_tweaks.cog_press':'Cog Press'})
write(path,lang)
print(f'{len(metals)*2} pressing recipes; reusable dies; existing metal/chassis artwork referenced')
