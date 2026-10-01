"""Resolve the 41 authored Shattered Skies looks into editable entity assets."""

from __future__ import annotations

import copy
import json
import math
import re
from pathlib import Path

from build_mob_models import ROOT, build, keyframe, uid, write_json

SOURCE = ROOT / "docs/shattered-skies/models"


def resolve(key: str, trail: tuple[str, ...] = ()) -> dict:
    if key in trail:
        raise ValueError(f"Inheritance cycle: {trail} -> {key}")
    raw = json.loads((SOURCE / f"{key}.json").read_text(encoding="utf-8"))
    if "extends" not in raw:
        result = copy.deepcopy(raw)
        result["base_rig"] = key
        return result
    base = resolve(raw["extends"], (*trail, key))
    result = copy.deepcopy(base)
    for field in ("id", "name", "role", "notes", "callouts"):
        if field in raw:
            result[field] = copy.deepcopy(raw[field])
    for field in ("palette", "materials"):
        result[field] = {**base.get(field, {}), **raw.get(field, {})}
    result["unshaded"] = sorted(set(base.get("unshaded", [])) | set(raw.get("unshaded", [])))
    removes = set(raw.get("remove_boxes", []))
    missing = removes - {box["name"] for box in base["boxes"]}
    if missing:
        raise ValueError(f"{key}: unknown removed boxes {missing}")
    result["boxes"] = [box for box in base["boxes"] if box["name"] not in removes] + raw.get("add_boxes", [])
    return result


def rig_parents(rig: str, names: set[str]) -> dict[str, str]:
    parents = {n: "body" for n in names if n != "body"}
    parents["body"] = "root"
    for n in names:
        if n.startswith("shin_"):parents[n]="leg_"+n.removeprefix("shin_")
        if n.startswith("foot_"):
            suffix=n.removeprefix("foot_")
            parents[n]="shin_"+suffix if "shin_"+suffix in names else "leg_"+suffix
    if "mouth" in names:parents["mouth"]="head" if "head" in names else "body"
    if rig == "splinter_wisp":
        return {"core": "root", "orbit": "core", "chip_1": "orbit", "chip_2": "orbit", "chip_3": "orbit"}
    for side in ("l", "r"):
        for child,parent in ((f"forearm_{side}", f"arm_{side}"), (f"fist_{side}", f"forearm_{side}"),
                             (f"shin_{side}", f"leg_{side}"), (f"foot_{side}", f"shin_{side}"),
                             (f"wing_{side}_outer", f"wing_{side}"), (f"wing_{side}_tip", f"wing_{side}_outer")):
            if child in names:
                parents[child] = parent
        for child in (f"ear_{side}", f"horn_{side}", f"mandible_{side}", f"fin_{side}"):
            if child in names: parents[child] = "head"
        for n in range(1,4):
            child = f"leg_{side}{n}_lower"
            if child in names: parents[child] = f"leg_{side}{n}"
    for child,parent in (("tail_tip","tail"),("tail2","tail"),("tail3","tail2"),("jaw","head"),
                         ("tusks","head"),("beard","head"),("horns","head")):
        if child in names and parent in names: parents[child]=parent
    if rig == "amethyst_stalker":
        parents.update({"neck":"chest","head":"neck"})
    elif rig == "hollow_sentinel":
        parents.update({"crest":"helm","lantern":"forearm_l","glaive":"forearm_r"})
    elif rig == "shardmother":
        parents.update({"arm_l":"head","arm_r":"head","claw_l":"arm_l","claw_r":"arm_r",
                        "splinter":"abdomen","sacs":"abdomen","crystals":"abdomen"})
    elif rig == "stormbitten_wyvern":
        parents.update({"neck":"body","neck2":"neck","head":"neck2","splinter":"neck2"})
    elif rig == "tidewraith":
        parents["splinter"]="head"
    elif rig == "slagjaw":
        parents["brow"]="head"
    return parents


def pivot_for(name: str, boxes: list[dict]) -> list[float]:
    if not boxes:
        return [0, 0, 0]
    # Decorative crystals, trim and toe tips must not move the anatomical hinge.
    preferred=[]
    if name.startswith("arm_"):
        preferred=[b for b in boxes if b["name"].lower().startswith(("shoulder ","pauldron ")) and len(b["name"].split())==2]
    elif name.startswith("leg_"):
        preferred=[b for b in boxes if b["name"].lower().startswith(("haunch ","thigh ")) and len(b["name"].split())==2]
        if not preferred:preferred=[b for b in boxes if b["name"].lower().startswith(("leg ","upper leg ","greave "))]
    elif name=="jaw":
        preferred=[b for b in boxes if b["name"].lower()=="jaw"]
    if preferred:boxes=preferred
    lo = [min(b["from"][i] for b in boxes) for i in range(3)]
    hi = [max(b["to"][i] for b in boxes) for i in range(3)]
    p = [(a+b)/2 for a,b in zip(lo,hi)]
    if any(name.startswith(s) for s in ("leg", "shin", "foot", "arm", "forearm", "fist", "claw", "mandible")):
        p[1] = hi[1]
    if name.startswith("wing"):
        p[0] = hi[0] if p[0] < 0 else lo[0]
    if name in ("head", "neck", "neck2", "jaw", "mouth"):
        p[2] = hi[2]
    if name in ("jaw","mouth"):p[1]=hi[1]
    if name.startswith("tail"):
        p[2] = lo[2]
    if name.startswith(("horn", "ear")) or name == "splinter":
        p[1] = lo[1]
    return [round(v,3) for v in p]


def convert(raw: dict) -> dict:
    raw=copy.deepcopy(raw)
    phantom_pivots={};phantom_rotations={}
    if raw["base_rig"]=="tidewraith":
        from phantom_tidewraith import geometry
        raw['boxes'],phantom_pivots,phantom_rotations=geometry(raw['palette'])
        raw.setdefault('materials',{})['skin']='scales';raw['materials']['skin_dark']='scales'
    # Complete the authored left-side eye decals with matching right-side decals.
    original=list(raw["boxes"])
    signatures={tuple(b["from"]+b["to"]) for b in original}
    for b in original:
        if "eye" not in b["name"].lower() and "visor side" not in b["name"].lower():continue
        lo,hi=b["from"],b["to"]
        reflected=[-hi[0],lo[1],lo[2],-lo[0],hi[1],hi[2]]
        if tuple(reflected) in signatures:continue
        other=copy.deepcopy(b)
        other["name"]=b["name"]+" mirrored"
        other["from"],other["to"]=reflected[:3],reflected[3:]
        if other.get("decal")=="left":other["decal"]="right"
        raw["boxes"].append(other)
        signatures.add(tuple(reflected))
    original_names={b["bone"] for b in raw["boxes"]}
    articulated=[]
    for b in raw["boxes"]:
        name=b["name"].lower();bone=b["bone"]
        if bone.startswith("leg_") and "lower" not in bone:
            suffix=bone.removeprefix("leg_")
            if name.startswith(("paw ","foot ","hoof ","sabaton ")):
                b["bone"]="foot_"+suffix
            elif name.startswith(("leg ","greave ")) and b["to"][1]-b["from"][1]>=6 and "shin_"+suffix not in original_names and bone+"_lower" not in original_names:
                knee=round((b["from"][1]+(b["to"][1]-b["from"][1])*.46)*4)/4
                lower=copy.deepcopy(b);lower["name"]=b["name"]+" lower"
                lower["to"][1]=knee;lower["bone"]="shin_"+suffix
                b["from"][1]=knee
                articulated.append(lower)
        if name=="mouth" and bone=="head":b["bone"]="mouth"
        articulated.append(b)
    raw["boxes"]=articulated
    names = {b["bone"] for b in raw["boxes"]}
    parents = rig_parents(raw["base_rig"], names)
    boxes=[]
    glow=set(raw.get("unshaded", [])) | {"glow", "splinter", "splinter_dim"}
    for box in raw["boxes"]:
        material=box["color"]
        if material not in raw["palette"]:
            raise ValueError(f"{raw['id']}: undefined palette color {material}")
        pattern=raw.get("materials",{}).get(material,box.get("texture","noise"))
        if material in glow: pattern="glow"
        if pattern in ("splinter", "splinter_dim", "amethyst", "prism", "ice"):
            pattern="crystal"
        boxes.append((box["name"],*box["from"],*box["to"],material,pattern))
    pivots={n:pivot_for(n,[b for b in raw["boxes"] if b["bone"]==n]) for n in parents}
    if raw["base_rig"]=="splinter_wisp":
        pivots["orbit"]=[0,13,0]
    pivots.update(phantom_pivots)
    return {"name":raw["name"],"pal":raw["palette"],"boxes":boxes,
            "namespace":"shatteredskies","authored_bones":[b["bone"] for b in raw["boxes"]],
            "parents":parents,"pivots":pivots,'rotations':phantom_rotations,"base_rig":raw["base_rig"]}


ABILITIES = {
    "mossback": ("ability_leap_slam", "ability_frenzy"),
    "slagjaw": ("ability_leap_slam", "ability_call_adds"),
    "amethyst_stalker": ("ability_blink", "ability_splinter_volley", "ability_frenzy"),
    "meteor_maw": ("ability_leap_slam", "ability_effect_pulse", "ability_call_adds"),
    "hollow_sentinel": ("ability_call_adds", "ability_shield_phase", "ability_targeted_aoe"),
    "shardmother": ("ability_call_adds", "ability_shield_phase", "ability_splinter_volley"),
    "stormbitten_wyvern": ("ability_lightning", "ability_line_aoe", "ability_void_pull"),
    "tidewraith": ("ability_void_pull", "ability_splinter_volley", "ability_telegraph_aoe"),
    "splinter_mite": (), "splinter_wisp": (),
}


def animate_rig(key: str, rig: str, groups: dict) -> tuple[list,dict]:
    actions=["spawn","idle","walk","run","attack","hurt","death",*ABILITIES[rig]]
    if rig in ("hollow_sentinel","shardmother","splinter_mite"):
        actions.remove("run")
    if rig=="tidewraith":
        actions.remove("walk")
        actions.remove("run")
    if rig in ("stormbitten_wyvern","tidewraith"):
        actions += ["fly","glide"]
    if rig=="splinter_wisp": actions=["spawn","idle","attack","hurt","death"]
    bb=[]
    export={}
    for action in actions:
        looping=action in ("idle","walk","run","fly","glide","ability_frenzy","ability_shield_phase")
        length=4.0 if action=="idle" else 0.55 if action=="run" else 0.9 if action=="walk" else 1.2
        animators={}
        bones={}
        for name,g in groups.items():
            channel="rotation"
            axis=0
            amount=0
            side=-1 if name.endswith(("_l","_fl","_bl")) or "_l" in name else 1
            if action=="idle":
                if name in ("body","core"): channel,axis,amount="position",1,0.45
                elif name=="orbit": axis,amount=1,360
                elif name.startswith("tail"): axis,amount=1,4
                elif name.startswith("ear"): axis,amount=2,4*side
                elif name in ("jaw","head","helm"): amount=2
                elif name.startswith("tendril"): axis,amount=2,4*side
                elif name.startswith('stalk_'):axis,amount=1,6*side
                elif name in ("mantle","sacs"):channel,amount="scale",1.015
            elif action in ("walk","run","ability_frenzy"):
                speed=1.4 if action!="walk" else 1.0
                leg_index=re.search(r"leg_[lr](\d)",name)
                number=int(leg_index.group(1)) if leg_index else (1 if name.endswith(("_bl","_br")) else 0)
                phase=side*((-1)**number)
                if name.startswith("leg"):
                    amount=20*phase*speed
                    if "lower" in name: amount*=-0.4
                elif name.startswith("shin"): amount=-10*phase*speed
                elif name.startswith("foot"): amount=5*phase*speed
                elif name.startswith("arm") and rig in ("slagjaw","meteor_maw","hollow_sentinel"): amount=-18*side*speed
                elif name=="body": channel,axis,amount="position",1,0.5*speed
                elif name.startswith("tail"): axis,amount=1,6*speed
            elif action in ("fly","glide","ability_void_pull"):
                if name.startswith("wing"):
                    axis,amount=2,side*(7 if action=="glide" else 16 if rig=='tidewraith' else 22)
                    if rig!='tidewraith' and ("outer" in name or "tip" in name): amount*=0.6
                elif name=="body" and rig!='tidewraith': channel,axis,amount="position",1,1.0
                elif rig=="tidewraith" and name.startswith("tail"):
                    amount=-5
            elif action=="attack":
                if name=="jaw": amount=18
                elif name in ("head","helm","neck"): amount=-12
                elif name.startswith(("arm","forearm")): amount=-35
                elif name.startswith("tail"): axis,amount=1,18
                elif name=="core": channel,amount="scale",1.18
                elif name.startswith("mandible"):axis,amount=1,20*side
                elif name.startswith("claw"):axis,amount=1,18*side
            elif action=="spawn":
                if name=="root": channel,axis,amount="position",1,-5
            elif action=="death":
                if name=="root": axis,amount=2,80
                elif rig=="shardmother" and name.startswith("leg"):axis,amount=2,-45*side
                elif rig=="stormbitten_wyvern" and name.startswith("wing"):axis,amount=2,55*side
                elif rig=="splinter_wisp" and name=="core":channel,amount="scale",0.01
            elif action=="hurt":
                if name=="root": axis,amount=2,5
            elif action in ("ability_leap_slam","ability_pounce"):
                if name=="root": channel,axis,amount="position",1,8
                elif name=="head": amount=18
                elif name.startswith("arm"): amount=-70
            elif action in ("ability_lightning","ability_line_aoe"):
                if name in ("head","neck","neck2"): amount=-15
                elif name=="jaw": amount=22
            elif action in ("ability_effect_pulse","ability_shield_phase","ability_call_adds"):
                if name in ("splinter","core","sacs"): channel,amount="scale",1.12
                elif name.startswith("arm"): amount=-28
                elif name=="jaw" and action=="ability_effect_pulse":amount=30
            elif action=="ability_blink" and name=="root":
                channel,amount="scale",0.01
            elif action=="ability_splinter_volley":
                if name in ("body","abdomen"):amount=-10
                elif name in ("splinter","ridge","crystals"):channel,amount="scale",1.1
            elif action=="ability_targeted_aoe" and name.startswith(("arm","forearm")):
                amount=-70
            elif action=="ability_telegraph_aoe" and name.startswith("wing"):
                axis,amount=2,45*side
            if amount==0: continue
            if name=="orbit": values=[(0,0),(length,360)]
            elif action=="death": values=[(0,1 if channel=="scale" else 0),(length,amount)]
            elif action=="spawn": values=[(0,amount),(length,0)]
            elif channel=="scale": values=[(0,1),(length/2,amount),(length,1)]
            elif looping: values=[(0,0),(length/4,amount),(length*3/4,-amount),(length,0)]
            else: values=[(0,0),(length/2,amount),(length,0)]
            if rig=="tidewraith" and action=='fly' and name.startswith('wing'):
                # Sample the actual 1.21.1 cosine at 16 phases; vanilla period
                # is 360 / 7.448451 ticks, converted to seconds (20 TPS).
                length=round(360/7.448451/20,3)
                values=[(length*i/16,16*side*math.cos(2*math.pi*i/16)) for i in range(17)]
            if rig=="tidewraith" and action in ("fly","glide") and name.startswith("tail"):
                # Phantom reference: two tail cycles for every one wing cycle.
                if action=='fly':length=round(360/7.448451/20,3)
                values=[(length*i/16,5+5*math.cos(4*math.pi*i/16)) for i in range(17)]
            bbf=[]
            gf={}
            for t,v in values:
                xyz=[v,v,v] if channel=="scale" else [0,0,0]
                if channel!="scale":xyz[axis]=v
                bbf.append(keyframe(round(t,3),channel,xyz,f"{key}/{action}/{name}"))
                gf[str(round(t,3))]=xyz
            animators[g["uuid"]]={"name":name,"type":"bone","keyframes":bbf}
            bones[name]={channel:gf}
        anim_name=f"animation.shatteredskies.{key}.{action}"
        bb.append({"uuid":uid(key,action),"name":anim_name,"loop":"loop" if looping else "once",
                   "override":False,"length":length,"snapping":20,"animators":animators})
        export[anim_name]={"loop":looping,"animation_length":length,"bones":bones}
    return bb,{"format_version":"1.8.0","animations":export}


def main() -> None:
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--only',help='Rebuild one base family; refresh metadata for all existing projects')
    args=parser.parse_args()
    manifest_path=ROOT/'docs/shattered-skies/blockbench/manifest.json'
    prior={r['model']:r for r in json.loads(manifest_path.read_text())['models']} if manifest_path.exists() else {}
    results=[]
    for path in sorted(SOURCE.glob("*.json")):
        raw=resolve(path.stem)
        if not args.only or raw['base_rig']==args.only:
            result=build(path.stem,convert(raw))
            print(path.stem,flush=True)
        else:
            project=manifest_path.parent/(path.stem+'.bbmodel')
            model=json.loads(project.read_text())
            result=dict(prior[path.stem]);result.update(boxes=len(model['elements']),atlas=model['resolution']['width'],
                eye_controls=sum(e['name'].startswith('eyes_') for e in model['elements']),
                planes=sum(any(a==b for a,b in zip(e['from'],e['to'])) for e in model['elements']))
        result.update({"base_rig":raw["base_rig"],"source":str(path.relative_to(ROOT))})
        results.append(result)
    write_json(manifest_path,{"minecraft":"1.21.1","models":results})
    print(f"Built {len(results)} Shattered Skies looks with authored geometry and bone names.")


if __name__=="__main__":
    main()
