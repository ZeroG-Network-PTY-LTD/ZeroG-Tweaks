"""Additive 1.21.1 material, crop and rare-Blaze data. Never alters world saves."""
import copy, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/'src/main/resources'
DATA=RES/'data/zerog_tweaks'
ASSET=RES/'assets/zerog_tweaks'
FAMILIES={
 'moon':('lunarium','eclipse_opal','moon_millet','#ada5cc','#785fc5'),
 'mars':('aresium','redshift_garnet','rustgrain','#ba6e49','#d03e5d'),
 'cerulon':('azurium','tidal_sapphire','azure_rice','#59aec2','#408ad7'),
 'skarn':('basaltine','ember_spinel','ember_wheat','#86766b','#ef8849'),
 'eidolon':('rime_nickel','wraith_quartz','frost_barley','#98bec7','#b5dbed'),
 'solvane':('helion','corona_topaz','sunspike','#ddaf58','#f5cd59')}
THEMES={'barren':'moon','desert':'mars','ocean':'cerulon','volcanic':'skarn','toxic':'skarn','frozen':'eidolon','crystal':'solvane'}
BLAZES={'moon':'void','mars':'pulsar','cerulon':'nebula','skarn':'void_c','eidolon':'comet','solvane':'nova'}
def read(p): return json.loads(p.read_text())
def write(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def merge_tag(p,values):
 obj=read(p) if p.exists() else {'replace':False,'values':[]}
 obj['values']=list(dict.fromkeys(obj['values']+values));write(p,obj)
def rl(id): return 'zerog_tweaks:'+id
def tag(kind,name,values,namespace='minecraft'):
 merge_tag(RES/f'data/{namespace}/tags/{kind}/{name}.json',values)
def recipe(id,obj): write(DATA/f'recipe/{id}.json',obj)
def item_model(id,block=False): write(ASSET/f'models/item/{id}.json',{'parent':rl('block/'+id)} if block else {'parent':'minecraft:item/generated','textures':{'layer0':rl('item/'+id)}})
def self_loot(id):return {'type':'minecraft:block','pools':[{'rolls':1,'entries':[{'type':'minecraft:item','name':rl(id)}],'conditions':[{'condition':'minecraft:survives_explosion'}]}]}
def shapeless(id,ingredients,result,count=1):
 recipe(id,{'type':'minecraft:crafting_shapeless','category':'misc','ingredients':[{'item':rl(x) if ':' not in x else x} for x in ingredients],'result':{'id':rl(result),'count':count}})
def storage(base,block):
 recipe(block,{'type':'minecraft:crafting_shaped','category':'building','pattern':['###','###','###'],'key':{'#':{'item':rl(base)}},'result':{'id':rl(block),'count':1}})
 shapeless(base+'_from_'+block,[block],base,9)
def crop_loot(crop,seed,produce,max_age=3):
 mature={'condition':'minecraft:block_state_property','block':rl(crop),'properties':{'age':str(max_age)}}
 write(DATA/f'loot_table/blocks/{crop}.json',{'type':'minecraft:block','pools':[
  {'rolls':1,'entries':[{'type':'minecraft:alternatives','children':[
   {'type':'minecraft:item','name':rl(produce),'conditions':[mature]}, {'type':'minecraft:item','name':rl(seed)}]}]},
  {'rolls':1,'conditions':[mature],'entries':[{'type':'minecraft:item','name':rl(seed),'functions':[{'function':'minecraft:apply_bonus','enchantment':'minecraft:fortune','formula':'minecraft:binomial_with_bonus_count','parameters':{'extra':3,'probability':.5714286}}]}]}],
  'functions':[{'function':'minecraft:explosion_decay'}]})
def main():
 lang=read(ASSET/'lang/en_us.json');allblocks=[];oreblocks=[];cropblocks=[];art=[]
 biome_groups={p:set() for p in FAMILIES};hosts=set();coverage={}
 for path in sorted((DATA/'dimension').glob('*.json')):
  dim=read(path);settings=dim['generator']['settings'];theme=settings.split(':')[-1].removeprefix('wasteland_')
  planet=theme if theme in FAMILIES else THEMES[theme]
  coverage[path.stem]=planet
  biomes={x['biome'] for x in dim['generator']['biome_source'].get('biomes',[])}
  biome_groups[planet]|=biomes
  noise=read(DATA/('worldgen/noise_settings/'+settings.split(':')[-1]+'.json'))
  hosts.add(noise['default_block']['Name'])
 write(ROOT/'tools/planet_materials.json',{'families':{p:{'metal':v[0],'gem':v[1],'crop':v[2],'metal_colour':v[3],'gem_colour':v[4]} for p,v in FAMILIES.items()},'dimension_themes':coverage})
 tag('block','planet_ore_replaceables',sorted(hosts),'zerog_tweaks')
 # Low-density water-only kelp in planet lakes, avoiding the already-populated ocean-slot biomes.
 kelp=read(DATA/'worldgen/placed_feature/glowkelp.json');kelp['placement'][0]['count']=8
 write(DATA/'worldgen/placed_feature/glowkelp_lakes.json',kelp)
 ocean_biomes={rl(x) for x in ['wasteland_deep_trenches','wasteland_kelp_jungles','wasteland_island_chains']}
 write(DATA/'neoforge/biome_modifier/planet_lake_glowkelp.json',{'type':'neoforge:add_features','biomes':sorted(set.union(*biome_groups.values())-ocean_biomes),'features':rl('glowkelp_lakes'),'step':'vegetal_decoration'})
 ore_template=read(DATA/'loot_table/blocks/cobaltium_ore.json')
 for planet,(metal,gem,crop,metal_colour,gem_colour) in FAMILIES.items():
  for material,is_gem,colour in [(metal,False,metal_colour),(gem,True,gem_colour)]:
   blocks=[material+'_ore',material+'_block']+([] if is_gem else ['raw_'+material+'_block'])
   items=[material,material+'_dust'] if is_gem else ['raw_'+material,material+'_ingot',material+'_nugget',material+'_dust']
   drop=material if is_gem else 'raw_'+material
   for id in blocks:
    write(ASSET/f'blockstates/{id}.json',{'variants':{'':{'model':rl('block/'+id)}}});write(ASSET/f'models/block/{id}.json',{'parent':'minecraft:block/cube_all','textures':{'all':rl('block/'+id)}});item_model(id,True)
    table=copy.deepcopy(ore_template) if id.endswith('_ore') else self_loot(id)
    if id.endswith('_ore'):
     table=json.loads(json.dumps(table).replace('zerog_tweaks:cobaltium_ore',rl(id)).replace('zerog_tweaks:raw_cobaltium',rl(drop)))
    write(DATA/f'loot_table/blocks/{id}.json',table);lang['block.zerog_tweaks.'+id]=id.replace('_',' ').title()
   for id in items:item_model(id);lang['item.zerog_tweaks.'+id]=id.replace('_',' ').title()
   allblocks+=blocks;oreblocks.append(material+'_ore');art.append({'id':material,'planet':planet,'gem':is_gem,'colour':colour,'blocks':blocks,'items':items})
   storage(material if is_gem else material+'_ingot',material+'_block')
   if not is_gem:
    storage('raw_'+material,'raw_'+material+'_block');storage(material+'_nugget',material+'_ingot')
    for source in ['raw_'+material,material+'_ore',material+'_dust']:
     for kind,time in [('smelting',200),('blasting',100)]:recipe(source+'_'+kind,{'type':'minecraft:'+kind,'category':'misc','ingredient':{'item':rl(source)},'result':{'id':rl(material+'_ingot'),'count':1},'experience':.7,'cookingtime':time})
   shapeless(material+'_dust_crushing',[material if is_gem else material+'_ingot','minecraft:flint'],material+'_dust')
   for category,ids in [('ores',[material+'_ore']),('storage_blocks',blocks[1:]),('gems',[material] if is_gem else []),('raw_materials',[] if is_gem else ['raw_'+material]),('ingots',[] if is_gem else [material+'_ingot']),('nuggets',[] if is_gem else [material+'_nugget']),('dusts',[material+'_dust'])]:
    if ids:
     tag('item',category+'/'+material,[rl(x) for x in ids],'c');tag('item',category,['#c:'+category+'/'+material],'c')
   feature='ore_'+material
   write(DATA/f'worldgen/configured_feature/{feature}.json',{'type':'minecraft:ore','config':{'size':3 if is_gem else 8,'discard_chance_on_air_exposure':.5 if is_gem else .15,'targets':[{'target':{'predicate_type':'minecraft:tag_match','tag':'zerog_tweaks:planet_ore_replaceables'},'state':{'Name':rl(material+'_ore')}}]}})
   frequency={'type':'minecraft:rarity_filter','chance':16} if is_gem else {'type':'minecraft:count','count':8}
   write(DATA/f'worldgen/placed_feature/{feature}.json',{'feature':rl(feature),'placement':[frequency,{'type':'minecraft:in_square'},{'type':'minecraft:height_range','height':{'type':'minecraft:uniform','min_inclusive':{'absolute':-48},'max_inclusive':{'absolute':48 if is_gem else 112}}},{'type':'minecraft:biome'}]})
  write(DATA/f'neoforge/biome_modifier/planet_minerals_{planet}.json',{'type':'neoforge:add_features','biomes':sorted(biome_groups[planet]),'features':[rl('ore_'+metal),rl('ore_'+gem)],'step':'underground_ores'})
  path=DATA/f'neoforge/biome_modifier/spawns_{BLAZES[planet]}_blaze.json'
  if not path.exists():
   candidates=list((DATA/'neoforge/biome_modifier').glob('*'+BLAZES[planet]+'_blaze*.json'))
   if len(candidates)!=1:raise RuntimeError((planet,candidates))
   path=candidates[0]
  obj=read(path);obj['biomes']=sorted(biome_groups[planet])
  for spawn in obj['spawners']:spawn.update(weight=1,minCount=1,maxCount=1)
  write(path,obj)
  for id in [crop+'_seeds',crop]:item_model(id);lang['item.zerog_tweaks.'+id]=id.replace('_',' ').title()
  cropblocks.append(crop+'_crop')
  for age in range(4):write(ASSET/f'models/block/{crop}_crop_stage{age}.json',{'parent':'minecraft:block/crop','render_type':'minecraft:cutout','textures':{'crop':rl(f'block/{crop}_crop_stage{age}')}})
  write(ASSET/f'blockstates/{crop}_crop.json',{'variants':{f'age={age}':{'model':rl(f'block/{crop}_crop_stage{age}')} for age in range(4)}})
  crop_loot(crop+'_crop',crop+'_seeds',crop);shapeless(crop+'_seeds_from_harvest',[crop],crop+'_seeds',2)
  blossom=planet+'_tall_blossom'
  write(ASSET/f'blockstates/{blossom}.json',{'variants':{f'half={half}':{'model':rl('block/'+blossom+'_'+half)} for half in ['lower','upper']}})
  for half in ['lower','upper']:write(ASSET/f'models/block/{blossom}_{half}.json',{'parent':'minecraft:block/cross','render_type':'minecraft:cutout','textures':{'cross':rl('block/'+blossom+'_'+half)}})
  write(ASSET/f'models/item/{blossom}.json',{'parent':'minecraft:item/generated','textures':{'layer0':rl('block/'+blossom+'_upper')}})
  table=self_loot(blossom);table['pools'][0]['conditions'].append({'condition':'minecraft:block_state_property','block':rl(blossom),'properties':{'half':'lower'}});write(DATA/f'loot_table/blocks/{blossom}.json',table)
  lang['block.zerog_tweaks.'+blossom]=planet.title()+' Torch Blossom'
  tag('block','flowers',[rl(blossom)]);tag('block','tall_flowers',[rl(blossom)]);tag('item','flowers',[rl(blossom)]);tag('item','tall_flowers',[rl(blossom)])
  # A low-chance bonus seed drop; preserves existing shears, silk-touch and wheat-seed drops.
  for dim in [d for d,p in coverage.items() if p==planet]:
   for height in ['short','tall']:
    path=DATA/f'loot_table/blocks/{dim}_{height}_grass.json';table=read(path)
    condition=[{'condition':'minecraft:random_chance','chance':.08},{'condition':'minecraft:survives_explosion'}]
    if height=='tall':condition.append({'condition':'minecraft:block_state_property','block':rl(dim+'_tall_grass'),'properties':{'half':'lower'}})
    marker={'rolls':1,'conditions':condition,'entries':[{'type':'minecraft:item','name':rl(crop+'_seeds')}]}
    # Idempotent; do not add duplicate seed pools on rerun.
    table['pools']=[p for p in table['pools'] if rl(crop+'_seeds') not in json.dumps(p)]+[marker];write(path,table)
 chestmap={'moon':'buried_observatory','mars':'mars_crash_site','cerulon':'sunken_lab','skarn':'collapsed_forge','eidolon':'frozen_outpost','solvane':'solar_shrine'}
 for planet,chest in chestmap.items():
  metal,gem,crop,*_=FAMILIES[planet];path=DATA/f'loot_table/chests/{chest}.json';obj=read(path)
  pool={'rolls':1,'entries':[{'type':'minecraft:item','name':rl('raw_'+metal),'weight':5,'functions':[{'function':'minecraft:set_count','count':{'type':'minecraft:uniform','min':1,'max':3}}]},{'type':'minecraft:item','name':rl(gem),'weight':1},{'type':'minecraft:item','name':rl(crop+'_seeds'),'weight':4},{'type':'minecraft:empty','weight':10}]}
  obj['pools']=[p for p in obj['pools'] if rl('raw_'+metal) not in json.dumps(p)]+[pool];write(path,obj)
 for crop,seed,produce in [('rust_tuber','rust_tuber_seeds','rust_tuber'),('solflower','solflower_seeds','solflower')]:
  crop_loot(crop+'_crop',seed,produce);shapeless(seed+'_from_harvest',[produce],seed,2);item_model(seed)
  lang['item.zerog_tweaks.'+seed]=seed.replace('_',' ').title()
  if crop=='solflower':
   cropblocks.append(crop+'_crop')
   for age in range(4):write(ASSET/f'models/block/{crop}_crop_stage{age}.json',{'parent':'minecraft:block/crop','render_type':'minecraft:cutout','textures':{'crop':rl(f'block/{crop}_crop_stage{age}')}})
   write(ASSET/f'blockstates/{crop}_crop.json',{'variants':{f'age={age}':{'model':rl(f'block/{crop}_crop_stage{age}')} for age in range(4)}})
 tag('block','mineable/pickaxe',[rl(x) for x in allblocks]);tag('block','needs_iron_tool',[rl(x) for x in allblocks if not any(x.startswith(g[1]) for g in FAMILIES.values())]);tag('block','needs_diamond_tool',[rl(g[1]+'_ore') for g in FAMILIES.values()])
 tag('block','maintains_farmland',[rl(x) for x in cropblocks]);tag('block','crops',[rl(x) for x in cropblocks]);tag('item','villager_plantable_seeds',[rl(v[2]+'_seeds') for v in FAMILIES.values()]+[rl('rust_tuber_seeds'),rl('solflower_seeds')])
 write(ASSET/'lang/en_us.json',lang);write(ROOT/'tools/planet_material_art_manifest.json',art)
 print(f'{len(art)} material families, {len(allblocks)} blocks, 6 grain crops, seed recipes, 34-dimension coverage')
if __name__=='__main__':main()
