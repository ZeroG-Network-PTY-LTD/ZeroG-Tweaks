"""Machine-readable hub shell reference; no image/model generation or registry changes."""
import argparse, hashlib, json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--check',action='store_true');a=p.parse_args()
old=json.loads(a.output.read_text());layouts=[]
for layout in old['layouts']:
    cells=[]
    for y in range(5):
        for x in range(5):
            for z in range(5):
                if y in (1,2) and 0<x<4 and 0<z<4:continue
                part='roof' if y==4 else 'controller' if y==1 and x==2 and z==4 else 'casing'
                if y==0 and z==4:part=['input_item_port','output_item_port','energy_port','input_fluid_port','output_fluid_port'][x]
                cells.append({'x':x,'y':y,'z':z,'part':part})
    source=json.dumps(cells,sort_keys=True,separators=(',',':')).encode()
    layouts.append({'id':layout['id'],'source':'HubExhibits.serviceShellState','source_sha256':hashlib.sha256(source).hexdigest(),
                    'cells':cells,'external_modules':layout['external_modules']})
payload=json.dumps({'version':2,'layouts':layouts},indent=2)+'\n'
if a.check:assert a.output.read_text()==payload,'Hub guide differs from canonical generator'
else:a.output.write_text(payload)
print(f'{len(layouts)} hub reference layouts;107 blocks,18 air,5 service ports each. No image or visual approval claimed.')
