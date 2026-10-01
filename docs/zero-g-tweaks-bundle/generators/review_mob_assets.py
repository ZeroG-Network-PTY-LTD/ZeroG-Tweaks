"""Validate generated assets and render their actual UV-mapped cube geometry."""

from __future__ import annotations

import base64
import hashlib
import html
import io
import json
import math
import subprocess
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
BUNDLE = ROOT / "docs/zero-g-tweaks-bundle"
MODELS = BUNDLE / "blockbench/mobs"
ITEMS = BUNDLE / "blockbench/mob_drops"
ASSETS = ROOT / "src/main/resources/assets/zerog_tweaks"
PREVIEWS = BUNDLE / "blockbench/previews"


def image_from_model(model: dict, index=0) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(model["textures"][index]["source"].split(",", 1)[1]))).convert("RGBA")


def project(p: list[float], view='threequarter') -> tuple[float, float, float]:
    x,y,z = p
    if view=='front':return (x,-y,-z)
    if view=='right':return (z,-y,x)
    if view=='left':return (-z,-y,-x)
    a,e = math.radians(35), math.radians(22)
    return (math.cos(a)*x + math.sin(a)*z,
            math.sin(e)*math.sin(a)*x - math.cos(e)*y - math.sin(e)*math.cos(a)*z,
            math.sin(a)*math.cos(e)*x + math.sin(e)*y - math.cos(a)*math.cos(e)*z)


def render(model: dict, size: tuple[int, int] = (384, 384), vertex_transform=None, debug=None, view='threequarter') -> Image.Image:
    if vertex_transform is None:
        vertex_transform=rest_transform(model)
    tex = image_from_model(model)
    faces = []
    points = []
    for cube in model["elements"]:
        x0,y0,z0 = cube["from"]
        x1,y1,z1 = cube["to"]
        corners = {
            "north": [(x0,y1,z0),(x1,y1,z0),(x1,y0,z0),(x0,y0,z0)],
            "east": [(x1,y1,z0),(x1,y1,z1),(x1,y0,z1),(x1,y0,z0)],
            "up": [(x0,y1,z1),(x1,y1,z1),(x1,y1,z0),(x0,y1,z0)]}
        corners.update({
                "south":[(x1,y1,z1),(x0,y1,z1),(x0,y0,z1),(x1,y0,z1)],
                "west":[(x0,y1,z1),(x0,y1,z0),(x0,y0,z0),(x0,y0,z1)],
                "down":[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)]})
        for face, vertices in corners.items():
            if face not in cube["faces"]:
                continue
            if vertex_transform:
                vertices=[vertex_transform(cube,v) for v in vertices]
            a=[vertices[1][i]-vertices[0][i] for i in range(3)]
            b=[vertices[3][i]-vertices[0][i] for i in range(3)]
            normal=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
            if project(normal,view)[2]<=0:continue
            p = [project(v,view) for v in vertices]
            points.extend(p)
            faces.append((sum(v[2] for v in p)/4, p, cube["faces"][face]["uv"],cube["faces"][face].get("texture",0),cube["name"]))
    xmin,xmax = min(p[0] for p in points),max(p[0] for p in points)
    ymin,ymax = min(p[1] for p in points),max(p[1] for p in points)
    zoom = min((size[0]-50)/max(1,xmax-xmin),(size[1]-70)/max(1,ymax-ymin))
    ox = (size[0]-(xmax-xmin)*zoom)/2 - xmin*zoom
    oy = (size[1]-(ymax-ymin)*zoom)/2 - ymin*zoom
    # Actual per-pixel depth test. Average face sorting hides a near eye whenever
    # its face centre happens to sort behind the centre of the much larger head.
    result=np.empty((size[1],size[0],4),dtype=np.uint8);result[:]=[29,34,44,255]
    depth=np.full((size[1],size[0]),-np.inf)
    owner=np.full((size[1],size[0]),-1,dtype=int)
    names=list(dict.fromkeys(f[4] for f in faces));part_ids={name:i for i,name in enumerate(names)}
    textures=[np.asarray(image_from_model(model,i)) for i in range(len(model["textures"]))]
    fragments=[]
    for _,p,uv,texture_index,name in sorted(faces,key=lambda f:f[0]):
        polygon=np.array([(v[0]*zoom+ox,v[1]*zoom+oy) for v in p])
        lo=np.maximum(np.floor(polygon.min(axis=0)).astype(int),[0,0])
        hi=np.minimum(np.ceil(polygon.max(axis=0)).astype(int),size)
        if np.any(hi<=lo):continue
        a=polygon[1]-polygon[0];b=polygon[3]-polygon[0]
        matrix=np.column_stack((a,b));det=np.linalg.det(matrix)
        if abs(det)<1e-8:continue
        yy,xx=np.mgrid[lo[1]:hi[1],lo[0]:hi[0]]
        st=np.linalg.inv(matrix)@np.vstack(((xx+.5-polygon[0,0]).ravel(),(yy+.5-polygon[0,1]).ravel()))
        s,t=(v.reshape(xx.shape) for v in st)
        inside=(s>=0)&(s<1)&(t>=0)&(t<1)
        texture=textures[texture_index];u0,v0,u1,v1=uv
        u=np.clip(np.floor(u0+s*(u1-u0)).astype(int),0,texture.shape[1]-1)
        v=np.clip(np.floor(v0+t*(v1-v0)).astype(int),0,texture.shape[0]-1)
        pixels=texture[v,u]
        z=p[0][2]+s*(p[1][2]-p[0][2])+t*(p[3][2]-p[0][2])
        region=np.s_[lo[1]:hi[1],lo[0]:hi[0]]
        mask=inside&(pixels[:,:,3]==255)&(z>depth[region])
        result[region][mask]=pixels[mask];depth[region][mask]=z[mask];owner[region][mask]=part_ids[name]
        if np.any((pixels[:,:,3]>0)&(pixels[:,:,3]<255)&inside):
            fragments.append((region,inside,pixels,z))
    # Translucent aura/gel faces blend after opaque geometry, without overwriting
    # its depth. Their ordering remains an approximation, not a GPU capture.
    for region,inside,pixels,z in fragments:
        mask=inside&(pixels[:,:,3]>0)&(pixels[:,:,3]<255)&(z>depth[region])
        alpha=pixels[:,:,3:4]/255
        rgb=np.round(pixels[:,:,:3]*alpha+result[region][:,:,:3]*(1-alpha)).astype(np.uint8)
        result[region][:,:,:3][mask]=rgb[mask]
    if debug is not None:
        debug['visible_pixels']={name:int((owner==i).sum()) for name,i in part_ids.items()}
    return Image.fromarray(result)


def rest_transform(model):
    """Honor authored rest rotations in the software review, including Phantom.

    Model coordinates are absolute; every child is rotated around its own
    absolute hinge then composed through ancestors, just like animation review.
    """
    from preview_mob_animation import rotation,translate
    bones={};members={};matrices={}
    def walk(nodes,parent=None):
        for n in nodes:
            if isinstance(n,str):members[n]=parent
            else:bones[n['uuid']]={**n,'parent':parent};walk(n['children'],n['uuid'])
    walk(model['outliner'])
    def matrix(key):
        if key is None:return np.eye(4)
        if key not in matrices:
            b=bones[key];p=np.array(b['origin'])
            matrices[key]=matrix(b['parent'])@translate(p)@rotation(b.get('rotation',[0,0,0]))@translate(-p)
        return matrices[key]
    return lambda cube,p:(matrix(members[cube['uuid']])@np.array([*p,1]))[:3].tolist()


def check(path: Path) -> dict:
    model = json.loads(path.read_text(encoding="utf-8"))
    tex = image_from_model(model)
    textures=[image_from_model(model,i) for i in range(len(model["textures"]))]
    assert tex.size == (model["resolution"]["width"],model["resolution"]["height"]), path
    ids = [e["uuid"] for e in model["elements"]]
    assert len(ids)==len(set(ids)), path
    members = []
    bones = {}
    def walk(nodes: list) -> None:
        for node in nodes:
            if isinstance(node,str):
                members.append(node)
            else:
                assert node["uuid"] not in bones, path
                bones[node["uuid"]]=node["name"]
                walk(node["children"])
    walk(model["outliner"])
    assert sorted(ids)==sorted(members), f"{path}: missing or duplicate bone membership"
    for cube in model["elements"]:
        sizes=[b-a for a,b in zip(cube["from"],cube["to"])]
        assert all(s>=0 for s in sizes) and sum(s>0 for s in sizes)>=2, (path,cube["name"])
        if 0 in sizes:
            axis=sizes.index(0)
            assert set(cube["faces"])==set((("east","west"),("up","down"),("north","south"))[axis]), (path,cube["name"])
        for face in cube["faces"].values():
            tex=textures[face.get("texture",0)]
            u0,v0,u1,v1=face["uv"]
            assert 0<=min(u0,u1)<max(u0,u1)<=tex.width, path
            assert 0<=min(v0,v1)<max(v0,v1)<=tex.height, path
            region=tex.crop((min(u0,u1),min(v0,v1),max(u0,u1),max(v0,v1)))
            assert region.getbbox(), f"{path}: empty UV face"
    for anim in model.get("animations",[]):
        for bone_id, animator in anim["animators"].items():
            assert bone_id in bones, (path,anim["name"],bone_id)
            assert all(0<=k["time"]<=anim["length"] for k in animator["keyframes"]), path
    return {"file":path.name,"cubes":len(ids),"planes":sum(any(a==b for a,b in zip(e["from"],e["to"])) for e in model["elements"]),"bones":len(bones),"animations":len(model.get("animations",[])),
            "texture":list(tex.size),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}


def main() -> None:
    PREVIEWS.mkdir(parents=True,exist_ok=True)
    paths = sorted(MODELS.glob("*.bbmodel"))
    shattered = sorted((ROOT/"docs/shattered-skies/blockbench").glob("*.bbmodel"))
    item_paths = sorted(ITEMS.glob("*.bbmodel"))
    auras=sorted((BUNDLE/"blockbench/auras").glob("*.bbmodel"))
    eggs=sorted((BUNDLE/"blockbench/spawn_eggs").glob("*.bbmodel"))
    assert len(eggs)==38, 'Expected one egg for each of the 38 base mobs'
    results = [check(p) for p in paths+shattered+item_paths+auras+eggs]
    for p in eggs:
        item=json.loads((ASSETS/"models/item"/(p.stem+".json")).read_text())
        assert item["textures"]["layer0"]=="minecraft:item/spawn_egg"
        assert item["textures"]["layer1"]=="minecraft:item/spawn_egg_overlay"
        assert (ASSETS/"textures/item"/(p.stem+"_accent.png")).exists()
    export_checks=[]
    for namespace in ("zerog_tweaks","shatteredskies"):
        assets=ROOT/"src/main/resources/assets"/namespace
        for geo_path in sorted((assets/"geo").glob("*.geo.json")):
            document=json.loads(geo_path.read_text())["minecraft:geometry"][0]
            bones={b["name"]:b for b in document["bones"]}
            assert len(bones)==len(document["bones"]),geo_path
            width,height=document["description"]["texture_width"],document["description"]["texture_height"]
            for name,bone in bones.items():
                seen=set()
                current=name
                while current:
                    assert current in bones and current not in seen,(geo_path,current)
                    seen.add(current)
                    current=bones[current].get("parent")
                for cube in bone.get("cubes",[]):
                    assert all(s>=0 for s in cube["size"]),geo_path
                    for face in cube["uv"].values():
                        u,v=face["uv"];w,h=face["uv_size"]
                        assert 0<=u<=u+w<=width and 0<=v<=v+h<=height,geo_path
            stem=geo_path.name.removesuffix(".geo.json")
            animation=assets/"animations"/f"{stem}.animation.json"
            clips=json.loads(animation.read_text())["animations"]
            assert all(set(a.get("bones",{}))<=set(bones) for a in clips.values()),animation
            texture_key=stem.removesuffix(".aura")+("_aura" if stem.endswith(".aura") else "")
            texture=Image.open(assets/"textures/entity"/f"{texture_key}.png")
            assert texture.size==(width,height),geo_path
            glow=assets/"textures/entity"/f"{texture_key}_glowmask.png"
            if glow.exists():assert Image.open(glow).size==texture.size,glow
            export_checks.append({"geometry":str(geo_path.relative_to(ROOT)),"bones":len(bones),"clips":len(clips)})
    try:
        font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",15)
    except OSError:
        font=ImageFont.load_default()
    contact=Image.new("RGB",(384*4,424*math.ceil(len(paths)/4)),(20,24,31))
    for index,path in enumerate(paths):
        model=json.loads(path.read_text(encoding="utf-8"))
        preview=render(model)
        preview.save(PREVIEWS/f"{path.stem}.png")
        x,y=index%4*384,index//4*424
        contact.paste(preview,(x,y))
        ImageDraw.Draw(contact).text((x+14,y+391),path.stem.replace("_"," ").title(),font=font,fill=(232,235,242))
    contact.save(PREVIEWS/"all_mobs.png")
    shattered_contact=Image.new("RGB",(384*4,424*math.ceil(len(shattered)/4)),(20,24,31))
    for index,path in enumerate(shattered):
        model=json.loads(path.read_text(encoding="utf-8"))
        preview=render(model)
        preview.save(PREVIEWS/f"{path.stem}.png")
        x,y=index%4*384,index//4*424
        shattered_contact.paste(preview,(x,y))
        ImageDraw.Draw(shattered_contact).text((x+10,y+391),path.stem.replace("_"," ").title(),font=font,fill=(215,194,248))
    shattered_contact.save(PREVIEWS/"all_shattered_skies.png")
    drops=Image.new("RGB",(224*6,144*math.ceil(len(item_paths)/6)),(29,34,44))
    for index,path in enumerate(item_paths):
        model=json.loads(path.read_text(encoding="utf-8"))
        icon=image_from_model(model).resize((96,96),Image.Resampling.NEAREST)
        x,y=index%6*224,index//6*144
        drops.paste(icon,(x+64,y+5),icon)
        ImageDraw.Draw(drops).text((x+8,y+112),path.stem.replace("_"," ").title(),font=font,fill=(232,235,242))
    drops.save(PREVIEWS/"all_drops.png")
    sections=[]
    for title, collection in (("ZeroG mobs",paths),("Shattered Skies creatures and styles",shattered),("Spawn eggs — vanilla shape",eggs),("Mob drops and rewards",item_paths),("Optional aura previews",auras)):
        cards=[]
        for path in collection:
            label=html.escape(path.stem.replace("_"," ").title())
            link=Path(__import__('os').path.relpath(path,BUNDLE/"blockbench")).as_posix()
            if path in eggs:
                preview=f"spawn_eggs/{path.stem}.png"
            elif path in item_paths:
                icon=image_from_model(json.loads(path.read_text(encoding="utf-8")))
                icon.resize((256,256),Image.Resampling.NEAREST).save(PREVIEWS/f"drop_{path.stem}.png")
                preview=f"previews/drop_{path.stem}.png"
            else:
                if path in auras:
                    render(json.loads(path.read_text())).save(PREVIEWS/f"aura_{path.stem}.png")
                    preview=f"previews/aura_{path.stem}.png"
                else:preview=f"previews/{path.stem}.png"
            cards.append(f'<article><img loading="lazy" src="{preview}" alt="{label}"><h3>{label}</h3><a href="{html.escape(link)}" download>Download Blockbench model</a></article>')
            if path in paths+shattered:
                cards[-1]=cards[-1].replace('</article>',f'<p><a href="previews/{path.stem}_face_review.png">Front and side eye review</a></p></article>')
                demos=sorted(PREVIEWS.glob(path.stem+"_*.gif"))
                if demos:
                    links=' '.join(f'<a href="previews/{p.name}">Animation preview</a>' for p in demos)
                    cards[-1]=cards[-1].replace('</article>',f'<p>{links}</p></article>')
        sections.append(f'<section><h2>{title}</h2><div class="grid">'+''.join(cards)+'</div></section>')
    gallery='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ZeroG Blockbench asset gallery</title><style>body{background:#14181f;color:#e8ebf2;font:16px system-ui;margin:32px auto;max-width:1400px;padding:0 20px}a{color:#a6dbff}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px}article{background:#1d222c;border-radius:12px;padding:16px}img{width:100%;aspect-ratio:1;object-fit:contain;image-rendering:pixelated}h3{font-size:18px}section{margin:40px 0}input{padding:12px;width:min(90%,500px);font:inherit}article[hidden]{display:none}</style><h1>ZeroG Minecraft 1.21.1 — current designs</h1><p>28 ZeroG mobs, 41 Shattered Skies looks, 38 spawn eggs, 65 drops and 52 optional aura previews. Only current generated designs are shown. Open downloaded .bbmodel files in Blockbench. Creature animations require the GeckoLib plugin.</p><p>These are software-rendered geometry previews. Animation, emissive layers and appearance still need inspection in Blockbench and Minecraft. Egg projects are baked colour previews; runtime eggs retain vanilla layers and registered tints.</p><p><a href="references/vanilla_animation_reference.md">1.21.1 animation research and ID mappings</a> · <a href="README.md">Asset and runtime notes</a> · <a href="spawn_eggs/spawn_eggs_preview.png">All spawn eggs</a></p><label>Find a model <input id="search" type="search" placeholder="Mob, egg or drop name…"></label>'''+''.join(sections)+'''<script>document.getElementById('search').addEventListener('input',e=>{let q=e.target.value.toLowerCase();document.querySelectorAll('article').forEach(a=>a.hidden=!a.querySelector('h3').textContent.toLowerCase().includes(q))});</script></html>'''
    (BUNDLE/"blockbench/index.html").write_text(gallery,encoding="utf-8")
    report={"minecraft":"1.21.1","source_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
            "models":len(paths),"shattered_styles":len(shattered),"spawn_eggs":len(eggs),"drop_models":len(item_paths),"aura_previews":len(auras),"validation":"passed",
            "runtime_tested":False,"native_blockbench_tested":False,"files":results,"export_checks":export_checks}
    (BUNDLE/"blockbench/validation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    references={"minecraft":"1.21.1","current_only":True,"models":[{"id":json.loads(p.read_text())["model_identifier"],
                "project":Path(__import__('os').path.relpath(p,BUNDLE/"blockbench")).as_posix(),
                "reference":f"previews/{p.stem}.png"} for p in paths+shattered],
                "spawn_eggs":len(eggs),"drops":len(item_paths),"software_animation_previews":[p.name for p in PREVIEWS.glob('*.gif')]}
    (BUNDLE/"blockbench/references/current_assets.json").write_text(json.dumps(references,indent=2)+"\n")
    if "--previews-only" in __import__('sys').argv:
        print(f"Validated {len(paths)+len(shattered)} creature looks; refreshed gallery without repackaging ZIP.")
        return
    archive=BUNDLE/"ZeroG_Mob_Blockbench_1.21.1.zip"
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted((BUNDLE/"blockbench").rglob("*")):
            if p.is_file(): z.write(p,Path("zero-g-tweaks-bundle")/p.relative_to(BUNDLE))
        for p in sorted((ROOT/"docs/shattered-skies/blockbench").rglob("*")):
            if p.is_file(): z.write(p,Path("shattered-skies")/p.relative_to(ROOT/"docs/shattered-skies"))
        for key in [p.stem for p in paths]:
            for folder,filename in (("geo",f"{key}.geo.json"),("animations",f"{key}.animation.json"),("textures/entity",f"{key}.png"),("textures/entity",f"{key}_glowmask.png")):
                p=ASSETS/folder/filename
                if p.exists():z.write(p,p.relative_to(ROOT/"src/main/resources"))
        for p in item_paths:
            texture=ASSETS/"textures/item"/f"{p.stem}.png"
            if texture.exists():z.write(texture,texture.relative_to(ROOT/"src/main/resources"))
            item_model=ASSETS/"models/item"/(p.stem+".json")
            if item_model.exists():z.write(item_model,item_model.relative_to(ROOT/"src/main/resources"))
        for p in eggs:
            for asset in (ASSETS/"models/item"/(p.stem+".json"),ASSETS/"textures/item"/(p.stem+"_accent.png")):
                z.write(asset,asset.relative_to(ROOT/"src/main/resources"))
        for p in shattered:
            namespace_assets=ROOT/"src/main/resources/assets/shatteredskies"
            for folder,filename in (("geo",f"{p.stem}.geo.json"),("animations",f"{p.stem}.animation.json"),("textures/entity",f"{p.stem}.png"),("textures/entity",f"{p.stem}_glowmask.png")):
                asset=namespace_assets/folder/filename
                if asset.exists():z.write(asset,asset.relative_to(ROOT/"src/main/resources"))
        for model in auras:
            ns=json.loads(model.read_text())["model_identifier"].split(":")[0]
            for folder,name in (("geo",f"{model.stem}.aura.geo.json"),("animations",f"{model.stem}.aura.animation.json"),("textures/entity",f"{model.stem}_aura.png")):
                asset=ROOT/"src/main/resources/assets"/ns/folder/name
                z.write(asset,asset.relative_to(ROOT/"src/main/resources"))
    print(f"Validated {len(paths)} ZeroG mobs, {len(shattered)} Shattered Skies looks and {len(item_paths)} drops; previews and ZIP saved.")


if __name__=="__main__":
    main()
