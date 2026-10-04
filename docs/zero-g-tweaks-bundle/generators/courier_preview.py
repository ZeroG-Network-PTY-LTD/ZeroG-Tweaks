"""Render an original isometric schematic, not an in-game screenshot."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / 'structures/concord_courier'
cells = json.loads((root / 'cells.json').read_text())['cells']
palette = {'meteorite_fragment': ('#685276','#473353','#8d799d'),
           'corroded_hull': ('#455763','#293642','#657e88'),
           'hull_plating': ('#758b9c','#405564','#acbdc9'),
           'hull_plating_slab': ('#758b9c','#405564','#acbdc9'),
           'chest': ('#bb812f','#80521e','#e0af55'),
           'broken_console': ('#665596','#362d51','#ad91e4'),
           'selenite_lamp': ('#9adce6','#5999a9','#e7ffff')}

def point(x,y,z):
    return (480+(x-z)*30, 150+(x+z)*15-y*36)

def polygon(points, colour):
    coords=' '.join(f'{x},{y}' for x,y in points)
    return f'<polygon points="{coords}" fill="{colour}" stroke="#142334" stroke-width="1"/>'

body=[]
for cell in sorted(cells, key=lambda c:(sum((c['pos'][0],c['pos'][2])), c['pos'][1])):
    x,y,z=cell['pos']; name=cell['block'].split(':')[1]
    height=.5 if name.endswith('_slab') else 1
    left,right,top=palette[name]
    body.append(polygon([point(x,y,z),point(x,y,z+1),point(x,y+height,z+1),point(x,y+height,z)],left))
    body.append(polygon([point(x,y,z+1),point(x+1,y,z+1),point(x+1,y+height,z+1),point(x,y+height,z+1)],right))
    body.append(polygon([point(x,y+height,z),point(x+1,y+height,z),point(x+1,y+height,z+1),point(x,y+height,z+1)],top))
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="500" viewBox="0 0 960 500">
<rect width="960" height="500" rx="18" fill="#0e1827"/>
<g font-family="sans-serif" fill="#e6effa">
<text x="36" y="44" font-size="27">CONCORD COURIER • The Signal</text>
<text x="36" y="73" font-size="15" fill="#9fb6cc">73-block original schematic • 7 × 5 × 7 • isometric construction view</text>
''' + '\n'.join(body) + '''
<text x="36" y="430" font-size="16">Fractured hull • meteorite crater • accessible cargo chest • Broken Console</text>
<text x="36" y="459" font-size="14" fill="#9fb6cc">Cargo: Dormant Wisp + Concord Codex. Existing ZeroG blocks; diagram is not a game screenshot.</text>
</g></svg>'''
(root/'courier-isometric.svg').write_text(svg)
print(root/'courier-isometric.svg')
