"""Export an honest, exhaustive item-model art reference to a separate Docs checkout.

Thumbnails are flat texture references, not baked 3D inventory screenshots.
Model IDs do not imply item registration. Never deletes previous galleries.
"""
import argparse, html, json, shutil
from pathlib import Path
from PIL import Image, ImageDraw

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--docs',type=Path,required=True)
a=p.parse_args(); root=Path(__file__).resolve().parents[1]/'src/main/resources'
out=a.docs/'docs/images/runtime-item-catalog-1.0.6';out.mkdir(parents=True,exist_ok=True)
rows=[]
def resolve(ref,seen=None):
    seen=set() if seen is None else seen
    if ref in seen:return {}
    seen.add(ref);ns,key=ref.split(':',1) if ':' in ref else ('minecraft',ref)
    path=root/f'assets/{ns}/models/{key}.json'
    if not path.exists():return {}
    obj=json.loads(path.read_text()); textures=resolve(obj['parent'],seen) if 'parent' in obj else {}
    textures.update(obj.get('textures',{}));return textures
for path in sorted((root/'assets/zerog_tweaks/models/item').glob('*.json')):
    textures=resolve('zerog_tweaks:item/'+path.stem); chosen=None
    for value in textures.values():
        visited=set()
        while value.startswith('#') and value[1:] in textures and value not in visited:
            visited.add(value);value=textures[value[1:]]
        if value.startswith('#'):continue
        ns,key=value.split(':',1) if ':' in value else ('minecraft',value)
        png=root/f'assets/{ns}/textures/{key}.png'
        if png.is_file():chosen=png;break
    thumb=None
    if chosen:
        im=Image.open(chosen).convert('RGBA');im=im.crop((0,0,im.width,min(im.width,im.height)))
        im.thumbnail((48,48),Image.Resampling.NEAREST);thumb=path.stem+'.png';im.save(out/thumb)
    rows.append({'model':'zerog_tweaks:'+path.stem,'texture':str(chosen.relative_to(root)) if chosen else None,'thumbnail':thumb})
pages=[]
for offset in range(0,len(rows),100):
    canvas=Image.new('RGB',(1000,1000),(17,22,35));draw=ImageDraw.Draw(canvas)
    for index,row in enumerate(rows[offset:offset+100]):
        x=(index%10)*100;y=(index//10)*100
        if row['thumbnail']:
            im=Image.open(out/row['thumbnail']);canvas.paste(im,(x+25,y+5),im)
        label=row['model'].split(':',1)[1]
        draw.text((x+3,y+58),label[:16],fill=(190,220,240))
        draw.text((x+3,y+73),label[16:32],fill=(190,220,240))
    page=f'sheet-{offset//100+1:02}.png';canvas.save(out/page);pages.append(page)
(out/'catalog.json').write_text(json.dumps({'scope':'item-model files; NOT a registry count or 3D render','items':rows,'sheets':pages},indent=2)+'\n')
cards=''.join('<figure>'+('<img loading="lazy" src="'+r['thumbnail']+'">' if r['thumbnail'] else '<span>No local texture thumbnail</span>')+'<figcaption>'+html.escape(r['model'])+'</figcaption></figure>' for r in rows)
(out/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>ZeroG item art catalogue</title><style>body{background:#111623;color:#d9e8f7;font-family:system-ui}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr))}figure{margin:8px;padding:12px;background:#202b40}img{width:64px;image-rendering:pixelated}figcaption{overflow-wrap:anywhere}</style><h1>ZeroG 1.0.6 item-model artwork</h1><p>Exhaustive model-file index. Flat texture references, not 3D screenshots. Block faces and inherited vanilla sprites may not represent the actual inventory view. No local thumbnail is not proof of a missing in-game sprite.</p><main>'+cards+'</main>')
guide=a.docs/'docs/runtime-item-catalog-1.0.6.md'
guide.write_text('# ZeroG item artwork index — 1.0.6\n\n'+str(len(rows))+' item-model files, including block inventory models and variants. **Not a registered-item count.** These are flat first-frame texture references, not in-game/3D renders. Existing galleries are preserved.\n\n[Searchable HTML: download this folder and open locally](images/runtime-item-catalog-1.0.6/index.html) · [Full IDs and source texture paths](images/runtime-item-catalog-1.0.6/catalog.json).\n\n'+'\n\n'.join('![Item texture reference page '+str(i+1)+'](images/runtime-item-catalog-1.0.6/'+f+')' for i,f in enumerate(pages))+'\n')
print(json.dumps({'item_model_files':len(rows),'reference_sheets':len(pages),'output':str(out)},indent=2))
