"""Check original gas sources against the production JAR; not a GPU visual test."""
import argparse,json,hashlib
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

p=argparse.ArgumentParser();p.add_argument('--design',type=Path,required=True);p.add_argument('--jar',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
errors=[];checked=0
with ZipFile(a.jar) as jar:
    for path in (a.design/'source').rglob('*'):
        if not path.is_file():continue
        relative=path.relative_to(a.design/'source').as_posix();checked+=1
        if relative not in jar.namelist() or jar.read(relative)!=path.read_bytes():errors.append('Source/JAR mismatch: '+relative)
        if path.suffix=='.png':
            image=Image.open(path);animated=path.with_suffix('.png.mcmeta')
            expected=(32,256) if animated.exists() else (32,32)
            if image.size!=expected or image.mode!='RGBA':errors.append('Raster contract: '+relative)
            if animated.exists():
                animation=json.loads(animated.read_text())['animation']
                if animation['width']!=32 or animation['height']!=32 or animation['frametime']!=3:errors.append('Animation contract: '+relative)
        if '/models/block/' in relative and path.suffix=='.json':
            for cube in json.loads(path.read_text()).get('elements',[]):
                for face in cube['faces'].values():
                    if not all(0<=v<=16 for v in face['uv']):errors.append('UV bounds: '+relative)
    if any('/gametest/' in name or name.startswith('data/zerog_transport_visual/') for name in jar.namelist()):errors.append('Test classes/fixtures shipped')
report={'checked':checked,'error_count':len(errors),'errors':errors,'jar_sha256':hashlib.sha256(a.jar.read_bytes()).hexdigest(),'client_visual_approval':False}
a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(bool(errors))
