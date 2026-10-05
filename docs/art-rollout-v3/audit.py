"""Audit all ZeroG item-model bindings; style flags require human review.

Do not equate a model-file count with registered items, or 16px with broken art.
Never class vanilla inherited/generated-atlas sprites as missing custom textures.
"""
import argparse, hashlib, html, json, re
from pathlib import Path
from PIL import Image

p=argparse.ArgumentParser();p.add_argument('--code',type=Path,required=True);a=p.parse_args()
base=Path(__file__).resolve().parent;res=a.code/'src/main/resources';records=[]
known={}
for relative in ['art-rollout-v3/manifest.json','asset-collection-1.21.1/inventory-texture-refresh-v1/manifest.json']:
    file=base.parent/relative
    for row in json.loads(file.read_text()).get('files',[]):known[row['path']]=row['sha256']
for folder in ['planet-botany-v2','wood-dust-art-v2']:
    for row in json.loads((base.parent/folder/'manifest.json').read_text())['textures']:
        known['assets/zerog_tweaks/textures/'+row['path']]=row['sha256']
for row in json.loads((base.parent/'asset-collection-1.21.1/planet-art-refresh-v1/manifest.json').read_text())['files']:
    known.setdefault(row['path'],row['sha256'])
# Final approved overlay takes precedence over historical source manifests.
for row in json.loads((base.parent/'full-art-rollout-v4/manifest.json').read_text())['files']:
    known[row['path']]=row['sha256']
model_cache={};texture_cache={}
def resolve(ref,seen=None):
    if ref in model_cache:return dict(model_cache[ref])
    seen=set() if seen is None else seen
    if ref in seen:return {}
    seen.add(ref);ns,key=ref.split(':',1) if ':' in ref else ('minecraft',ref)
    path=res/f'assets/{ns}/models/{key}.json'
    if not path.exists():return {}
    obj=json.loads(path.read_text());textures=resolve(obj['parent'],seen) if 'parent' in obj else {}
    textures.update(obj.get('textures',{}));model_cache[ref]=dict(textures);return textures
for file in sorted((res/'assets/zerog_tweaks/models/item').glob('*.json')):
    textures=resolve('zerog_tweaks:item/'+file.stem);bound=[];review=[]
    for slot,value in textures.items():
        visited=set()
        while value.startswith('#') and value[1:] in textures and value not in visited:
            visited.add(value);value=textures[value[1:]]
        if value.startswith('#') or ':' not in value:continue
        ns,key=value.split(':',1)
        if ns=='minecraft':continue
        relative=f'assets/{ns}/textures/{key}.png';path=res/relative
        if not path.exists():
            # Atlas palette permutations may legitimately have no standalone PNG.
            bound.append({'texture':relative,'status':'needs model-reference/atlas check'});continue
        if relative not in texture_cache:
            digest=hashlib.sha256(path.read_bytes()).hexdigest()
            with Image.open(path) as im:size=list(im.size)
            texture_cache[relative]=(digest,size)
        digest,size=texture_cache[relative]
        current=known.get(relative)==digest
        bound.append({'texture':relative,'resolution':size,'sha256':digest,'in_approved_rollout':current})
        if not current and min(size)<=16:review.append('Legacy-resolution custom artwork: '+relative)
        elif not current:review.append('Outside current approved-source audit: '+relative)
    records.append({'model':'zerog_tweaks:'+file.stem,'scope':'model file, not a registry assertion','bindings':bound,'review':list(dict.fromkeys(review))})
queue=[row for row in records if row['review']]
(base/'item-model-audit.json').write_text(json.dumps({'scope':'item model files; not registered-item count; resolution is not proof of style or breakage',
    'models_scanned':len(records),'models_flagged_for_review':len(queue),'items':records},indent=2)+'\n')
cards=[]
for row in queue:
    cards.append('<article><h3>'+html.escape(row['model'])+'</h3><p>'+'<br>'.join(html.escape(v) for v in row['review'])+'</p></article>')
(base/'review-queue.html').write_text('<!doctype html><meta charset="utf-8"><title>ZeroG art review queue</title><style>body{background:#131b27;color:#d9e5ee;font:15px system-ui;padding:24px}article{padding:12px;margin:8px 0;background:#202c40}h3{margin:0}p{overflow-wrap:anywhere}</style><h1>Remaining asset review queue</h1><p>Model-file audit, not an item registry or in-game visual proof. Older resolution does not by itself mean broken artwork. Existing IDs are preserved.</p>'+''.join(cards))
print(json.dumps({'model_files_scanned':len(records),'review_flags':len(queue),'output':str(base/'item-model-audit.json')}))
