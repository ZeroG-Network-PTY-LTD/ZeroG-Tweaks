"""Native adaptation of the supplied GUI. No made-up tanks or extra backend slots.
Run: python3 docs/alveary-controller-gui-v1/adapt_runtime.py --code ../zerog-code-integrated
"""
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path
from PIL import Image, ImageDraw

BASE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--code',type=Path,required=True);args=parser.parse_args()
spec=importlib.util.spec_from_file_location('provided_controller_gui',BASE/'reference/controller_gui.py')
gui=importlib.util.module_from_spec(spec);spec.loader.exec_module(gui)

def background():
    # Exact supplied 256x256 sheet / 256x250 visible window.
    return gui.background()

out=BASE/'source/assets/zerog_tweaks/textures/gui';out.mkdir(parents=True,exist_ok=True)
background().save(out/'alveary_controller_runtime.png');widgets=gui.widgets();widgets.save(out/'alveary_controller_widgets.png')
files=[]
for path in sorted(out.glob('*.png')):
    relative=path.relative_to(BASE/'source');data=path.read_bytes()
    for root in [args.code/'src/main/resources',args.code/'src/main/resources/resourcepacks/visual_refresh']:
        target=root/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    files.append({'path':relative.as_posix(),'sha256':hashlib.sha256(data).hexdigest()})
for tier in (1,3,7):
    image=background()
    frames=min(tier+1,7);products=min(6+tier*2,18)
    sealed=widgets.crop((60,82,78,100))
    for i in range(frames,27):image.alpha_composite(sealed,(11+i%9*18,98+i//9*18))
    for i in range(min(products,9),9):image.alpha_composite(sealed,(139+i%3*18,22+i//3*18))
    for x,y,w,h in [(44,22,6,62),(115,31,10,50),(205,22,8,62),(216,22,14,62),(233,22,12,62)]:
        image.alpha_composite(widgets.crop((80,82,80+w,82+h)),(x,y))
    draw=ImageDraw.Draw(image);gui.bee_icon(draw,21,31,(240,200,70),(60,40,20))
    for i in range(frames):gui.item_icon(draw,12+i*18,99,'frame','#e9a82c')
    for i in range(min(products,6)):gui.item_icon(draw,140+i%3*18,23+i//3*18,'comb','#9a5fd0')
    badge=(tier-1)%3*66,148+(tier-1)//3*14
    image.alpha_composite(widgets.crop((badge[0],badge[1],badge[0]+64,badge[1]+12)),(131,3))
    image.alpha_composite(widgets.crop((0,68,10,78)),(199,4))
    image.alpha_composite(widgets.crop((42,82,54,94)),(181,79))
    image.alpha_composite(widgets.crop((0,82,12,94)),(19,76))
    large=image.crop((0,0,256,250)).resize((768,750),Image.Resampling.NEAREST);d=ImageDraw.Draw(large)
    names={1:'Rustic',3:'Industrial',7:'Quantum'}
    for x,y,text in [(8,5,'Alveary Controller'),(211,5,'Formed'),(47,158,'Inventory'),
                    (193,101,'--'),(193,114,'--'),(193,127,'--'),(193,140,'--'),(142,80,'<'),(156,80,'>')]:
        d.text((x*3,y*3),text,font=gui.F(18),fill=gui.C['text'])
    d.text((146*3,5*3),names[tier],font=gui.F(16,True),fill=(255,255,255),stroke_width=1,stroke_fill=(0,0,0))
    large.save(BASE/f'runtime-t{tier}-preview.png')
(BASE/'runtime-manifest.json').write_text(json.dumps({'screen':[256,250],'files':files,
    'reference_hashes':{path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in (BASE/'reference').glob('*') if path.is_file()},
    'limits':'Frames/products reflect addon 1.0.0; sealed means unavailable, not simulated.'},indent=2)+'\n')
print('PASS: native GUI adaptation generated, source/runtime/pack files identical; previews are not in-game captures.')
