"""Approved starting fabrication costs and selected progression casings.

Owner14October: machine-only fabrication with reusable dies. Two ingots make a
plate; four ingots directly make a cog. Never regenerate crafting-table routes.
"""
import argparse, json
from pathlib import Path
from generate import GROUPS

def generate(resources):
    root=resources/'data/zerog_tweaks'
    def emit(relative,data):
        path=root/relative;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(data,indent=2)+'\n')
    for _,metals in GROUPS.values():
        for metal in metals:
            for kind,count in [('plate',2),('cog',4)]:
                identifier=metal+'_'+kind
                emit('recipe/pressing/'+identifier+'.json',{'type':'zerog_tweaks:pressing',
                    'inputs':[{'ingredient':{'item':'minecraft:copper_ingot' if metal=='copper' else 'zerog_tweaks:'+metal+'_ingot'},'count':count}],
                    'catalyst':{'ingredient':{'item':'zerog_tweaks:'+kind+'_press'},'count':1,'consumed':False},
                    'outputs':[{'stack':{'id':'zerog_tweaks:'+identifier,'count':1}}],
                    'energy':2000 if kind=='plate' else 4000,'time':100 if kind=='plate' else 160})
            emit('advancement/recipes/manufacturing/'+metal+'.json',{
                'parent':'minecraft:recipes/root',
                'criteria':{'has_ingot':{'trigger':'minecraft:inventory_changed','conditions':{
                    'items':[{'items':'minecraft:copper_ingot' if metal=='copper' else 'zerog_tweaks:'+metal+'_ingot'}]}}},
                'requirements':[['has_ingot']],
                'rewards':{'recipes':['zerog_tweaks:pressing/'+metal+'_plate','zerog_tweaks:pressing/'+metal+'_cog']}})
    emit('tags/item/manufacturing/star_glass.json',{'replace':False,'values':[
        'zerog_tweaks:star_glass','zerog_tweaks:star_glass_blue','zerog_tweaks:star_glass_teal']})
    # Existing chain and two-casing output are preserved. Two empty lower corners
    # leave design room for future components; they do not accept extra items now.
    for metal,dust,core in [('cyrrium','pulsar_dust','minecraft:iron_block'),
                            ('tectium','tremor_dust','zerog_tweaks:cyrrium_casing'),
                            ('wraithsteel','spectral_dust','zerog_tweaks:tectium_casing'),
                            ('astrium','fusion_dust','zerog_tweaks:wraithsteel_casing')]:
        emit('recipe/'+metal+'_casing.json',{'type':'minecraft:crafting_shaped','category':'building',
            'pattern':['PCP','D#D',' G '],
            'key':{'P':{'item':'zerog_tweaks:'+metal+'_plate'},'C':{'item':'zerog_tweaks:'+metal+'_cog'},
                   'D':{'item':'zerog_tweaks:'+dust},'#':{'item':core},
                   'G':{'tag':'zerog_tweaks:manufacturing/star_glass'}},
            'result':{'id':'zerog_tweaks:'+metal+'_casing','count':2}})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--resources',type=Path,required=True);a=p.parse_args()
    generate(a.resources)
    generate(Path(__file__).parent/'generated')
    print('Machine-only pressing recipes and unlocks regenerated; no crafting-table component routes.')
