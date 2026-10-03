"""Idempotent cooking + hide/leather + flower/dye integration data, 1.21.1."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];RES=ROOT/'src/main/resources';DATA=RES/'data/zerog_tweaks'
COOKING={
 'crawler_leg':'roasted_crawler_leg','hopper_meat':'cooked_hopper','grazer_steak':'seared_grazer_steak',
 'beetle_grub':'toasted_grub','stag_venison':'cooked_venison','fowl':'roast_fowl','glimmerfish':'cooked_glimmerfish',
 'boar_chop':'smoked_boar_chop','scorch_tail':'grilled_scorch_tail','yak_meat':'yak_roast',
 'gildcrab_meat':'cooked_gildcrab','eel_fillet':'cooked_eel','burrower_steak':'cooked_burrower_steak',
 'lurker_leg':'crispy_lurker_leg','skitter_leg':'roasted_skitter_leg','rust_tuber':'baked_tuber','solflower_seeds':'roasted_solflower_seeds'}
HIDES=['grazer_hide','crystal_hide','cinder_pelt','frost_pelt']
FLOWERS={'starbloom':'light_blue','solflower':'yellow','ghostbloom':'white','frostfern':'light_blue','emberthorn':'red','cinder_cap':'orange'}
for planet,dye in [('moon','purple'),('mars','orange'),('cerulon','blue'),('skarn','red'),('eidolon','light_blue'),('solvane','yellow')]:
 FLOWERS[planet+'_glow_flower']=dye;FLOWERS[planet+'_tall_blossom']=dye
def write(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n')
def convert(id,input,output,count=1):
 write(DATA/f'recipe/{id}.json',{'type':'minecraft:crafting_shapeless','category':'misc','ingredients':[{'item':'zerog_tweaks:'+input}],'result':{'id':output,'count':count}})
def main():
 for raw,cooked in COOKING.items():
  for kind,time in [('smelting',200),('smoking',100),('campfire_cooking',600)]:
   name=cooked if kind=='smelting' else cooked+'_from_'+kind
   write(DATA/f'recipe/{name}.json',{'type':'minecraft:'+kind,'category':'food','ingredient':{'item':'zerog_tweaks:'+raw},'result':{'id':'zerog_tweaks:'+cooked,'count':1},'experience':.35,'cookingtime':time})
 for hide in HIDES:convert('leather_from_'+hide,hide,'minecraft:leather')
 for flower,dye in FLOWERS.items():convert(dye+'_dye_from_'+flower,flower,'minecraft:'+dye+'_dye',2 if flower.endswith('_tall_blossom') else 1)
 tag=RES/'data/c/tags/item/hides.json';old=json.loads(tag.read_text()) if tag.exists() else {'replace':False,'values':[]}
 old['values']=list(dict.fromkeys(old['values']+['zerog_tweaks:'+x for x in HIDES]));write(tag,old)
 lang=RES/'assets/zerog_tweaks/lang/en_us.json';words=json.loads(lang.read_text());words['itemGroup.zerog_tweaks.liquids']='ZeroG: Liquids';write(lang,words)
 print(f'{len(COOKING)*3} cooking recipes, {len(HIDES)} leather conversions, {len(FLOWERS)} dye conversions, liquids tab label')
if __name__=='__main__':main()
