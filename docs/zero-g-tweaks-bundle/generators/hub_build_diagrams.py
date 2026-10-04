"""Exact source diagrams: build layers and authored 3D cell views, not gameplay captures."""
import argparse
import hashlib
import json
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--guide',type=Path,required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]/'structures/hub-exhibit-guides'
root.mkdir(parents=True,exist_ok=True)
layouts=json.loads(args.guide.read_text())['layouts']
assert len(layouts)==8

def svg(width,height,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="#0e1827"/><g font-family="sans-serif" fill="#e6effa">{body}</g></svg>'

colours={'casing':'#60798e','controller':'#ab87e2','energy_port':'#e5b746','frame_housing':'#64c3a0','roof':'#aab9c8','air':'#172839'}
body='<text x="28" y="36" font-size="25">5×5×5 formation reference • layers counted from Y=0</text>'
for y in range(5):
    ox=28+y*220
    body+=f'<text x="{ox}" y="77" font-size="19">Y={y}</text>'
    for z in range(5):
        for x in range(5):
            part='roof' if y==4 else 'casing'
            if y in (1,2) and 0<x<4 and 0<z<4:part='air'
            if y==0 and x==4 and z==4:part='controller'
            elif y==0 and x==0 and z==0:part='energy_port'
            elif y==1 and x==2 and z==4:part='frame_housing'
            px=ox+x*35;py=95+z*35;letter={'casing':'C','roof':'R','air':'·','controller':'G','energy_port':'E','frame_housing':'F'}[part]
            body+=f'<rect x="{px}" y="{py}" width="33" height="33" fill="{colours[part]}"/><text x="{px+11}" y="{py+22}" font-size="17">{letter}</text>'
body+='''<text x="28" y="306" font-size="17">Top view: north at top; controller is the southeast base corner. 107 blocks, 18 interior air cells.</text>
<text x="28" y="338" font-size="16">G controller • E energy • F frame housing • C same-tier casing • R same-tier roof • · air</text>
<text x="28" y="370" font-size="15">T3/T5/T6/T7. Alternate reference: energy at NE base; frame housing at west wall (Y=1, Z=2).</text>
<text x="28" y="397" font-size="14">Roof Y=4 must remain roof blocks. Y=3 is solid in the installed validator. Schematic, not a game capture.</text>'''
(root/'validated-build-layers.svg').write_text(svg(1140,425,body))

body='<text x="28" y="36" font-size="24">Eight authored apiary designs • exact cell geometry</text>'
parts=sorted({c['part'] for layout in layouts for c in layout['cells']})
for index,layout in enumerate(layouts):
    ox=165+(index%4)*300;oy=135+(index//4)*310
    def point(x,y,z):return ox+(x-z)*12,oy+(x+z)*6-y*17
    for c in sorted(layout['cells'],key=lambda c:(c['x']+c['z'],c['y'])):
        x,y,z=c['x'],c['y'],c['z'];part=c['part'];colour=colours.get(part,'#be8275')
        faces=[([point(x,y,z),point(x,y,z+1),point(x,y+1,z+1),point(x,y+1,z)],'.72'),
               ([point(x,y,z+1),point(x+1,y,z+1),point(x+1,y+1,z+1),point(x,y+1,z+1)],'.88'),
               ([point(x,y+1,z),point(x+1,y+1,z),point(x+1,y+1,z+1),point(x,y+1,z+1)],'1')]
        for points,opacity in faces:
            body+=f'<polygon points="{" ".join(f"{a},{b}" for a,b in points)}" fill="{colour}" opacity="{opacity}" stroke="#162233" stroke-width=".6"/>'
    label=layout['id'].replace('_',' ')
    body+=f'<text x="{ox-140}" y="{oy+146}" font-size="15">{label}</text><text x="{ox-140}" y="{oy+170}" font-size="13" fill="#9fb6cc">{len(layout["cells"])} cells • authored design</text>'
body+='''<text x="28" y="676" font-size="16">These are authored visual layouts, not the installed fixed-size validator recipe.</text>
<text x="28" y="704" font-size="14" fill="#9fb6cc">Use the separate formation layer sheet for accepted 5×5×5 references. Colours indicate part roles, not actual textures.</text>'''
(root/'eight-authored-apiaries.svg').write_text(svg(1220,735,body))
(root/'provenance.json').write_text(json.dumps({'input':'assets/zerog_tweaks/guides/multiblocks.json','sha256':hashlib.sha256(args.guide.read_bytes()).hexdigest(),
    'authored_layouts':len(layouts),'validated_tiers':['tier3','tier5','tier6','tier7'],'evidence':'source schematic, not GPU capture'},indent=2)+'\n')
print('Two exact schematic sheets and source hash written')
