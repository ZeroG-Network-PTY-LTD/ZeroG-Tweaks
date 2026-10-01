"""Check bilateral anatomy, mirrored joint pivots and animation attachment chains."""
import json
import re
from pathlib import Path
from build_mob_models import ROOT, write_json

CORE=re.compile(r"(?:^|_)(?:head|body|neck|muzzle|mouth|jaw|legs?|thigh|shin|foot|feet|paw|hoof|hooves|eyes?|ears?|nostrils?)(?:_|$)")

def bounds(e):return tuple(round(v,4) for v in e["from"]+e["to"])
def mirror(b):return (-b[3],b[1],b[2],-b[0],b[4],b[5])
def paired(name):
    if "left" in name:return name.replace("left","right")
    if "right" in name:return name.replace("right","left")
    for a,b in (("_fl","_fr"),("_bl","_br"),("_l","_r")):
        if a in name:return name.replace(a,b)
        if b in name:return name.replace(b,a)
    return None

def audit(path):
    model=json.loads(path.read_text())
    elements=model["elements"]
    lookup={bounds(e) for e in elements}
    unmatched=[]
    for e in elements:
        b=bounds(e)
        decorative=any(s in e["name"] for s in ("vine","growth","ornament"))
        if CORE.search(e["name"]) and not decorative and mirror(b) not in lookup:
            unmatched.append({"part":e["name"],"bounds":b})
    bones={}
    memberships={}
    def walk(nodes,parent=None):
        for n in nodes:
            if isinstance(n,str):memberships[n]=parent
            else:
                bones[n["name"]]={"pivot":n["origin"],"parent":parent,"uuid":n["uuid"]}
                walk(n["children"],n["name"])
    walk(model["outliner"])
    pivot_errors=[]
    for name,bone in bones.items():
        other=paired(name)
        if other in bones:
            x,y,z=bone["pivot"];px,py,pz=bones[other]["pivot"]
            if max(abs(x+px),abs(y-py),abs(z-pz))>.005:
                pivot_errors.append({"bone":name,"paired":other,"pivot":bone["pivot"],"other_pivot":bones[other]["pivot"]})
    attachment_errors=[]
    for name,bone in bones.items():
        parent=bone["parent"] or ""
        torso_face=path.stem.startswith("meteor_maw")
        if name.startswith("eye_") and parent not in ("head","helm","stalk_l","stalk_r","body"):
            attachment_errors.append({"bone":name,"parent":parent,"reason":"eye must follow head/helm"})
        if name.endswith("_foot") and not parent.endswith("_shin") and not parent.startswith("leg_"):
            attachment_errors.append({"bone":name,"parent":parent,"reason":"foot must follow its own leg"})
        if name.endswith("_shin") and parent!=name.removesuffix("_shin"):
            attachment_errors.append({"bone":name,"parent":parent,"reason":"shin must follow its own upper leg"})
        if name=="jaw" and parent!="head" and not (torso_face and parent=="body"):
            attachment_errors.append({"bone":name,"parent":parent,"reason":"jaw must follow head"})
        if name.startswith("foot_"):
            suffix=name.removeprefix("foot_")
            if parent not in ("leg_"+suffix,"shin_"+suffix):attachment_errors.append({"bone":name,"parent":parent,"reason":"foot must follow its own leg chain"})
        if name.startswith("shin_") and parent!="leg_"+name.removeprefix("shin_"):
            attachment_errors.append({"bone":name,"parent":parent,"reason":"shin must follow its own thigh"})
        if name=="mouth" and parent not in ("head","body"):
            attachment_errors.append({"bone":name,"parent":parent,"reason":"mouth must follow its face"})
    return {"model":path.stem,"unmatched_anatomy":unmatched,"pivot_errors":pivot_errors,"attachment_errors":attachment_errors,"intentional_features":["Meteor Maw's jaw and eyes attach to its torso by design"] if torso_face else [],"bones":bones}

def main():
    paths=sorted((ROOT/"docs/zero-g-tweaks-bundle/blockbench/mobs").glob("*.bbmodel"))+sorted((ROOT/"docs/shattered-skies/blockbench").glob("*.bbmodel"))
    results=[audit(p) for p in paths]
    report={"models":len(results),"results":results,"status":"review_required" if any(r[k] for r in results for k in ("unmatched_anatomy","pivot_errors","attachment_errors")) else "passed"}
    write_json(ROOT/"docs/zero-g-tweaks-bundle/blockbench/rig_audit.json",report)
    for r in results:
        problems={k:r[k] for k in ("unmatched_anatomy","pivot_errors","attachment_errors") if r[k]}
        if problems:print(r["model"],json.dumps(problems))
    print(report["status"],len(results))
    if report['status']!='passed':raise SystemExit(1)

if __name__=="__main__":main()
