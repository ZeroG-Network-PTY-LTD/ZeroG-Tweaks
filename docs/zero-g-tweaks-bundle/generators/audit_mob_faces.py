"""Check each optical part's visibility in its anatomical view, and render reviews.

This catches occlusion and incorrect orientation. It does NOT certify artistic
matching or native Blockbench/Minecraft behaviour.
"""
import copy, json, math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from build_mob_models import ROOT,write_json
from mob_faces import PROFILES
from review_mob_assets import render,project

OUT=ROOT/'docs/zero-g-tweaks-bundle/blockbench/previews'

def inspect(path,base):
    model=json.loads(path.read_text());eyes=[e for e in model['elements'] if e['name'].startswith('eyes_')]
    orientation=PROFILES[base][0] if base in PROFILES else 'front'
    expected=1 if orientation=='ender_eye' else 2
    assert len(eyes)==expected,(path,len(eyes),expected)
    views={}
    for view in ('front','left','right'):
        debug={};render(model,view=view,debug=debug)
        views[view]={e['name']:debug['visible_pixels'].get(e['name'],0) for e in eyes}
    issues=[]
    for e in eyes:
        view='left' if orientation=='side' and e['from'][0]<0 else 'right' if orientation=='side' else 'front'
        if views[view][e['name']]==0:issues.append({'part':e['name'],'view':view,'reason':'Fully hidden in the intended anatomical view'})
    # Isolate the face assembly for clear visual comparison, without claiming
    # isolation proves visibility in the full model (full-model checks are above).
    members={}
    def walk(nodes,parent=None):
        for n in nodes:
            if isinstance(n,str):members[n]=parent
            else:walk(n['children'],n['name'])
    walk(model['outliner'])
    selected=[e for e in model['elements'] if members.get(e['uuid']) in ('head','helm','jaw','mouth','stalk_l','stalk_r') or e in eyes
              or any(s in e['name'] for s in ('muzzle','nose','nostril','beak','eye_socket','optical_mount'))]
    host={'meteor_maw':'torso_','splinter_wisp':'core_01','ice_leech':'translucent_gel_body_00','glimmerfish':'body_'}
    if base in host:
        selected += [e for e in model['elements'] if e['name'].startswith(host[base]) and e not in selected]
    if not any(e not in eyes for e in selected):
        candidates=[e for e in model['elements'] if any(s in e['name'] for s in ('stone_body','meteorite_shell','prism_core','core','translucent_gel_body'))]
        if candidates:selected+=candidates[:1]
    face=copy.copy(model);face['elements']=selected
    panels=[]
    for view in ('front','right'):
        picture=render(face,size=(256,256),view=view)
        ImageDraw.Draw(picture).text((8,8),view.title(),fill='white')
        panels.append(picture)
    review=Image.new('RGB',(512,288),(20,24,31));review.paste(panels[0],(0,20));review.paste(panels[1],(256,20))
    ImageDraw.Draw(review).text((12,276),path.stem.replace('_',' ').title(),fill='white')
    review.save(OUT/(path.stem+'_face_review.png'))
    return {'model':path.stem,'base':base,'orientation':orientation,'eyes':len(eyes),'visibility':views,'issues':issues},review

def main():
    zg=ROOT/'docs/zero-g-tweaks-bundle/blockbench/mobs'
    ss=ROOT/'docs/shattered-skies/blockbench'
    variants={r['model']:r['base_rig'] for r in json.loads((ss/'manifest.json').read_text())['models']}
    paths=sorted(zg.glob('*.bbmodel'))+sorted(ss.glob('*.bbmodel'))
    records=[];family_reviews=[]
    for path in paths:
        base=variants.get(path.stem,path.stem);record,review=inspect(path,base);records.append(record)
        if base==path.stem:family_reviews.append(review)
    for page in range(math.ceil(len(family_reviews)/8)):
        sheet=Image.new('RGB',(1024,288*4),(20,24,31))
        for i,picture in enumerate(family_reviews[page*8:(page+1)*8]):sheet.paste(picture,(i%2*512,i//2*288))
        sheet.save(OUT/f'face_review_page_{page+1}.png')
    failures=[r for r in records if r['issues']]
    report={'status':'review_required' if failures else 'visibility_checks_passed','models':len(records),
            'evidence':'Depth-tested software front/left/right views plus isolated face review panels; not native or artistic certification',
            'results':records}
    write_json(ROOT/'docs/zero-g-tweaks-bundle/blockbench/face_audit.json',report)
    print(report['status'],len(records))
    for r in failures:print(r['model'],r['issues'])
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
