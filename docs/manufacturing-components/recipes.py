"""Approved starting fabrication costs and selected progression casings.

Manual bench fabrication is the initial route, not a working compressor machine.
Later machines can add processing routes without removing this source contract.
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
            for kind,pattern in [('plate',['I','I']),('cog',[' I ','I I',' I '])]:
                identifier=metal+'_'+kind
                emit('recipe/manufacturing/'+identifier+'.json',{'type':'minecraft:crafting_shaped','category':'misc',
                    'pattern':pattern,'key':{'I':{'item':'zerog_tweaks:'+metal+'_ingot'}},
                    'result':{'id':'zerog_tweaks:'+identifier,'count':1}})
            emit('advancement/recipes/manufacturing/'+metal+'.json',{
                'parent':'minecraft:recipes/root',
                'criteria':{'has_ingot':{'trigger':'minecraft:inventory_changed','conditions':{
                    'items':[{'items':'zerog_tweaks:'+metal+'_ingot'}]}}},
                'requirements':[['has_ingot']],
                'rewards':{'recipes':['zerog_tweaks:manufacturing/'+metal+'_plate','zerog_tweaks:manufacturing/'+metal+'_cog']}})
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
    print('42 fabrication recipes,21 recipe-book unlocks,4 progression casings and3 Star Glass alternatives.')
