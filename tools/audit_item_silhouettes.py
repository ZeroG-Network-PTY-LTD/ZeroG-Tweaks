"""Read-only regression for item textures accidentally replaced by white glow masks."""
import argparse, io, json
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--jar',required=True)
p.add_argument('--namespace',default='aeroapiary')
p.add_argument('--overlay-dir',type=Path)
a=p.parse_args();bad=[];checked=0
with ZipFile(a.jar) as jar:
    names=set(jar.namelist())
    overlay={str(path.relative_to(a.overlay_dir)).replace('\\','/'):path.read_bytes()
             for path in a.overlay_dir.rglob('*') if path.is_file()} if a.overlay_dir else {}
    names.update(overlay)
    def read(name):return overlay[name] if name in overlay else jar.read(name)
    for name in sorted(names):
        if not name.startswith(f'assets/{a.namespace}/models/item/') or not name.endswith('.json'):continue
        model=json.loads(read(name))
        for layer,ref in model.get('textures',{}).items():
            if not layer.startswith('layer') or ref.startswith('#'):continue
            ns,path=ref.split(':',1) if ':' in ref else ('minecraft',ref)
            file=f'assets/{ns}/textures/{path}.png'
            if ns=='minecraft':continue
            if file not in names:
                bad.append((name,'missing',file));continue
            im=Image.open(io.BytesIO(read(file))).convert('RGBA')
            colors={pixel[:3] for pixel in im.get_flattened_data() if pixel[3]>0}
            checked+=1
            if not colors or all(min(color)>245 for color in colors):
                bad.append((name,'empty or white-only visible layer',file))
print(json.dumps({'checked_visible_layers':checked,'bad_count':len(bad),'first_failures':bad[:8]},indent=2))
raise SystemExit(bool(bad))
