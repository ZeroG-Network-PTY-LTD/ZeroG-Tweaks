"""Deterministic Mars wreck/shrine templates using only approved existing blocks.

No new textures, registry IDs, external NBT packages or reused proprietary art.
Run with --resources pointing to the code branch resources; output copies remain
on Design under generated/. Sparse ruin geometry includes explicit air so the
surface jigsaw clears intruding terrain, with beard-box foundation blending.
"""
import argparse
import gzip
import json
import struct
from pathlib import Path

Z="zerog_tweaks:"

def string(value):
    data=value.encode("utf-8")
    return struct.pack(">H",len(data))+data

def payload(kind,value):
    if kind==3:return struct.pack(">i",value)
    if kind==8:return string(value)
    if kind==9:
        child,items=value
        return bytes([child])+struct.pack(">i",len(items))+b"".join(payload(child,item) for item in items)
    if kind==10:return b"".join(bytes([k])+string(name)+payload(k,v) for name,(k,v) in value.items())+b"\0"
    raise ValueError(kind)

def template(size,blocks):
    palette=[]
    lookup={}
    packed=[]
    sx,sy,sz=size
    for y in range(sy):
        for z in range(sz):
            for x in range(sx):
                state,nbt=blocks.get((x,y,z),("minecraft:air",None))
                if state not in lookup:
                    lookup[state]=len(palette)
                    parts=state.split("[",1)
                    entry={"Name":(8,parts[0])}
                    if len(parts)>1:entry["Properties"]=(10,{k:(8,v) for k,v in (a.split("=") for a in parts[1][:-1].split(","))})
                    palette.append(entry)
                entry={"pos":(9,(3,[x,y,z])),"state":(3,lookup[state])}
                if nbt:entry["nbt"]=(10,{k:(8,v) for k,v in nbt.items()})
                packed.append(entry)
    root={"DataVersion":(3,3955),"size":(9,(3,list(size))),"palette":(9,(10,palette)),"blocks":(9,(10,packed)),"entities":(9,(10,[]))}
    return gzip.compress(b"\x0a\x00\x00"+payload(10,root),mtime=0)

def wreck(variant):
    b={}
    def put(x,y,z,state):b[x,y,z]=(Z+state,None)
    for x in range(21):
        for z in range(15):
            if ((x-10)/10)**2+((z-7)/7)**2<=1:put(x,0,z,"martian_stone")
    # Half-buried hull, collapsed ribs, asymmetric broken tail and scattered panels.
    for x in range(5,16):
        for z in range(4,11):put(x,1,z,"corroded_hull")
    for x in range(6,15):
        for z in (4,10):
            for y in range(2,5 if (x+variant)%3 else 3):put(x,y,z,"hull_plating" if (x+y)%4 else "corroded_hull")
    for x in (6,10,14):
        for z in range(5,10):
            if (z+x+variant)%4:put(x,5,z,"hull_plating")
    for x,y,z in ((3,1,3),(17,1,11),(18,1,6),(4,1,12),(2,1,7),(19,1,4)):
        put(x,y,z,"corroded_hull")
    for x in range(1,6):put(x,1,7+variant,"olympium_plating")
    put(9,2,5,"broken_console")
    b[11,2,8]=("minecraft:chest[facing=north,type=single,waterlogged=false]",{"id":"minecraft:chest","LootTable":Z+"chests/mars_crash_site"})
    return template((21,9,15),b)

def shrine():
    b={}
    def put(x,y,z,state):b[x,y,z]=(Z+state,None)
    for x in range(13):
        for z in range(13):
            if 1<=x<=11 and 1<=z<=11:put(x,0,z,"martian_stone")
            if 3<=x<=9 and 3<=z<=9:put(x,1,z,"martian_stone_bricks")
    for x,z in ((3,3),(9,3),(3,9),(9,9)):
        for y in range(2,6):put(x,y,z,"martian_stone_bricks")
        put(x,6,z,"olympium_plating")
    for x in range(3,10):
        put(x,6,9,"martian_stone_bricks")
    put(6,2,6,"chiseled_martian_stone")
    put(6,3,6,"broken_console")
    b[6,2,5]=("minecraft:chest[facing=north,type=single,waterlogged=false]",{"id":"minecraft:chest","LootTable":Z+"chests/mars_aresite_shrine"})
    return template((13,8,13),b)

def resources():
    result={}
    for name,biomes,spacing,salt,templates in (
        ("mars_crash_site",["rust_plains","oxide_badlands","polar_caps"],40,19477391,["mars_crash_site/wreck_a","mars_crash_site/wreck_b"]),
        ("mars_aresite_shrine",["rust_plains","oxide_badlands"],56,19477392,["mars_aresite_shrine/shrine"]),
    ):
        result[f"worldgen/structure/{name}.json"]={"type":Z+"dry_land_jigsaw","biomes":"#"+Z+"has_structure/"+name,"step":"surface_structures","spawn_overrides":{},"terrain_adaptation":"beard_box","start_pool":Z+name+"/start","size":1,"start_height":-1,"max_distance_from_center":48,"max_height_difference":6,"search_radius":32,"always_place":False}
        result[f"worldgen/structure_set/{name}.json"]={"structures":[{"structure":Z+name,"weight":1}],"placement":{"type":"minecraft:random_spread","spacing":spacing,"separation":spacing//2,"salt":salt}}
        result[f"worldgen/template_pool/{name}/start.json"]={"fallback":"minecraft:empty","elements":[{"weight":1,"element":{"element_type":"minecraft:single_pool_element","location":Z+t,"projection":"rigid","processors":"minecraft:empty"}} for t in templates]}
        result[f"tags/worldgen/biome/has_structure/{name}.json"]={"replace":False,"values":[Z+b for b in biomes]}
    result["loot_table/chests/mars_aresite_shrine.json"]={"type":"minecraft:chest","pools":[{"rolls":1,"entries":[{"type":"minecraft:item","name":Z+"aresite"}]},{"rolls":1,"entries":[{"type":"minecraft:item","name":Z+"concord_codex"}]},{"rolls":1,"entries":[{"type":"minecraft:loot_table","value":Z+"chests/mars_crash_site"}]}],"random_sequence":Z+"chests/mars_aresite_shrine"}
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--resources",type=Path,required=True)
    args=parser.parse_args()
    destinations=[args.resources/"data/zerog_tweaks",Path(__file__).parent/"generated/data/zerog_tweaks"]
    binaries={"structure/mars_crash_site/wreck_a.nbt":wreck(0),"structure/mars_crash_site/wreck_b.nbt":wreck(1),"structure/mars_aresite_shrine/shrine.nbt":shrine()}
    for destination in destinations:
        for relative,data in resources().items():
            path=destination/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
        for relative,data in binaries.items():
            path=destination/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print("Generated 3 Mars templates, 2 structure sets, 2 pools, biome tags and shrine loot.")

if __name__=="__main__":main()
