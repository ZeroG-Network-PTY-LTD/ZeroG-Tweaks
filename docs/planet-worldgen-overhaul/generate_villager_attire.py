"""Original native-UV space clothing only; all vanilla head/face/hat UVs transparent.

No Minecraft source pixels copied. Export source PNGs plus runtime overlays.
"""
import argparse
import hashlib
import json
import random
from pathlib import Path
from PIL import Image, ImageDraw

PALETTES={"moon":(163,166,204),"mars":(200,97,64),"cerulon":(59,169,188),
          "skarn":(181,80,67),"eidolon":(156,204,225),"solvane":(233,172,66)}
ROOT=Path(__file__).resolve().parent
def build(runtime):
    records=[]
    for theme,accent in PALETTES.items():
        for variant in range(4):
            name=f"{theme}_space_{variant}"
            image=Image.new("RGBA",(64,64),(0,0,0,0)); pixels=image.load()
            rng=random.Random(name)
            base=((45,52,69),(191,193,197),(71,88,105),(104,99,116))[variant]
            # Original suit overlay islands: body, legs, sleeves, tunic and folded
            # arms. Stay below the nose/head and left of the 30,47 hat-rim island.
            for left,top,right,bottom in ((16,20,40,38),(0,22,16,38),(40,22,64,38),
                                          (0,38,28,64),(40,38,64,46)):
                for y in range(top,bottom):
                    for x in range(left,right):
                        edge=min(x-left,right-x-1);shade=(.68 if edge==0 else .92)+.13*(1-(y-top)/(bottom-top))
                        grain=rng.randint(-4,4)
                        pixels[x,y]=tuple(max(0,min(255,int(v*shade)+grain)) for v in base)+(255,)
            draw=ImageDraw.Draw(image)
            # Narrow panel piping, belts, knee seams and a small chest status light.
            draw.rectangle((6,41,13,60),outline=accent+(255,),width=1)
            draw.line((0,52,27,52),fill=tuple(int(v*.7) for v in accent)+(255,),width=2)
            draw.rectangle((24,27,30,32),fill=accent+(255,))
            draw.point((27,29),fill=(215,247,255,255))
            draw.line((40,28,63,28),fill=accent+(255,),width=1)
            draw.line((0,32,15,32),fill=accent+(255,),width=1)
            # Regression guard: every actual head/nose/hat/rim pixel is untouched.
            assert all(pixels[x,y][3]==0 for y in range(20) for x in range(64))
            assert all(pixels[x,y][3]==0 for y in range(47,64) for x in range(30,64))
            source=ROOT/"source/villagers"/(name+".png");source.parent.mkdir(parents=True,exist_ok=True);image.save(source)
            target=runtime/"assets/zerog_tweaks/textures/entity/villager/type"/(name+".png")
            target.parent.mkdir(parents=True,exist_ok=True);image.save(target)
            records.append({"id":"zerog_tweaks:"+name,"resolution":[64,64],"sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"face_alpha":0})
    (ROOT/"source/villagers/manifest.json").write_text(json.dumps({"provenance":"Original code-authored clothing, no vanilla pixels redistributed","textures":records},indent=2)+"\n")
    print(f"{len(records)} original clothes-only palettes; face/nose/hat alpha tests passed")
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--runtime-resources",type=Path,required=True)
    build(parser.parse_args().runtime_resources)
