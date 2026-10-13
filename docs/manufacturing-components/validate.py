"""Read-only native PNG, material palette, alpha, overlay and uniqueness audit."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--code',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parent;res=a.code/'src/main/resources'
rows=json.loads((root/'manifest.json').read_text());seen={'cog':set(),'plate':set()}
for row in rows:
    payload=(root/'textures'/f'{row["id"]}.png').read_bytes()
    assert hashlib.sha256(payload).hexdigest()==row['sha256'],row['id']
    assert hashlib.sha256((a.code/row['ingot_source']).read_bytes()).hexdigest()==row['ingot_sha256'],f'Ingot changed: {row["metal"]}'
    for layer in row['layers']:assert (res/layer).read_bytes()==payload,f'Stale layer: {layer}'
    im=Image.open(root/'textures'/f'{row["id"]}.png').convert('RGBA')
    assert im.size==(32,32) and im.getextrema()[3]==(0,255),row['id']
    bounds=im.getbbox();assert bounds[0]>0 and bounds[1]>0 and bounds[2]<32 and bounds[3]<32,row['id']
    palette={tuple(c) for c in row['palette']}
    metal_pixels=sum(1 for c in im.getdata() if c[3]>0 and c[:3] in palette)
    visible=sum(1 for c in im.getdata() if c[3]>0)
    assert metal_pixels/visible>.97,f'Material hue lost: {row["id"]}'
    kind=row['id'].rsplit('_',1)[1]
    assert row['sha256'] not in seen[kind],f'Shared material pixels: {row["id"]}'
    seen[kind].add(row['sha256'])
    if kind=='cog':assert im.getpixel((16,14))[3]==0,f'Bore filled: {row["id"]}'
print(f'{len(rows)} native32 sprites: ingot-matched palettes, unique bytes, transparent padding/bore, all layers synchronized.')
