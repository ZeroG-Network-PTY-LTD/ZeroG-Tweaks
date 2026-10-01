"""Extract block coordinates from authored assemblies, without changing their art."""
from pathlib import Path
import json, re, hashlib, argparse
root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--code-root', type=Path, required=True, help='Separate checked-out 1.21.x code branch')
args = parser.parse_args()
source = root/'docs/asset-collection-1.21.1/bees/blockbench_by_use/multiblocks'
assert (args.code_root/'build.gradle').is_file(), 'Expected code checkout'
target = args.code_root/'src/main/resources/assets/zerog_tweaks/guides/multiblocks.json'
layouts = []
for path in sorted(source.glob('*.bbmodel')):
    raw = path.read_bytes(); data = json.loads(raw)
    cells = []; seen = set()
    for element in data['elements']:
        match = re.fullmatch(r'(.+)_(-?\d+)_(-?\d+)_(-?\d+)', element['name'])
        if not match: continue  # overlays/detail cubes are not additional blocks
        part, *numbers = match.groups(); x, y, z = map(int, numbers)
        assert element['from'] == [x*16, y*16, z*16]
        assert element['to'] == [(x+1)*16, (y+1)*16, (z+1)*16]
        assert (x,y,z) not in seen
        seen.add((x,y,z)); cells.append({'x':x,'y':y,'z':z,'part':part})
    assert cells and min(c['y'] for c in cells)==0
    assert sum(c['part']=='controller' for c in cells)==1
    layouts.append({'id':path.stem, 'source_sha256':hashlib.sha256(raw).hexdigest(),
                    'cells':cells, 'external_modules':['genetics','cryo']})
assert len(layouts)==8
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({'version':1,'layouts':layouts},indent=2)+'\n')
print(json.dumps({'layouts':len(layouts),'cells':sum(len(x['cells']) for x in layouts),
                  'origin':'authored integer coordinates, lowest layer Y=0',
                  'external_modules':'Separate; no invented socket substitutions'}))
