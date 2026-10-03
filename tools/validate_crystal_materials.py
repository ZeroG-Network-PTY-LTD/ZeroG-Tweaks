"""Read-only validation of the local crystal/material revision and built jar."""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--design-root', type=Path, required=True)
parser.add_argument('--jar', type=Path, required=True)
args = parser.parse_args()
CODE = Path(__file__).resolve().parents[1]
PACK = args.design_root / 'docs/asset-collection-1.21.1/crystals-amethyst-style-v2'
RES = CODE / 'src/main/resources'
manifest = json.loads((PACK / 'manifest.json').read_text())
digest = lambda data: hashlib.sha256(data).hexdigest()

with ZipFile(args.jar) as jar:
    assert not any('/gametest/' in n or 'AssetReview' in n or '/tidewraithgametest/' in n for n in jar.namelist()), 'Test classes leaked into production jar'
    for entry in manifest['textures']:
        relative = 'assets/zerog_tweaks/textures/' + entry['path']
        source = (PACK / 'textures' / entry['path']).read_bytes()
        assert digest(source) == entry['sha256']
        assert source == (RES / relative).read_bytes() == jar.read(relative), relative
        with Image.open(io.BytesIO(source)) as png:
            assert list(png.size) == entry['size']
            assert png.size in [(32, 32), (64, 1024)]
    for name in ['star_glass', 'star_glass_blue', 'star_glass_teal']:
        relative = f'assets/zerog_tweaks/textures/block/{name}.png.mcmeta'
        meta = json.loads((RES / relative).read_text())['animation']
        assert meta['frametime'] == 3 and meta['interpolate'] is True
        assert meta['width'] == meta['height'] == 64
        assert jar.read(relative) == (RES / relative).read_bytes()

projects = list((PACK / 'blockbench').glob('*.bbmodel'))
assert len(projects) == manifest['editable_projects'] == 80
for path in projects:
    model = json.loads(path.read_text())
    width, height = model['resolution']['width'], model['resolution']['height']
    for texture in model['textures']:
        with Image.open(io.BytesIO(base64.b64decode(texture['source'].split(',', 1)[1]))) as png:
            assert png.size == (width, height), path.name
    for element in model['elements']:
        for face in element['faces'].values():
            u1, v1, u2, v2 = face['uv']
            assert all(0 <= u <= width for u in [u1, u2]), path.name
            assert all(0 <= v <= height for v in [v1, v2]), path.name

for metal in manifest['metal_families']:
    for item in [metal + '_ingot', 'raw_' + metal]:
        model = json.loads((RES / f'assets/zerog_tweaks/models/item/{item}.json').read_text())
        assert model['parent'] == 'minecraft:item/generated', item

for planet in ['moon', 'mars', 'cerulon', 'skarn', 'eidolon', 'solvane']:
    recipe = json.loads((RES / f'data/zerog_tweaks/recipe/{planet}_star_sand_to_star_glass.json').read_text())
    assert recipe['type'] == 'minecraft:smelting'
    assert recipe['result'] == {'id': 'zerog_tweaks:star_glass', 'count': 1}
    assert recipe['cookingtime'] == 200

for path in (PACK / 'textures/block').glob('*.png'):
    if any(key in path.stem for key in ['brine', 'frost', 'prism']):
        with Image.open(path) as png:
            assert all(r == g == b for r, g, b, a in (list(png.convert('RGBA').get_flattened_data()) if hasattr(png, 'get_flattened_data') else list(png.convert('RGBA').getdata()))), path.name

with Image.open(PACK / 'animated_updates.gif') as gif:
    assert gif.n_frames == 16 and gif.info['loop'] == 0

print('PASS: 96 texture hashes and jar entries; 80 embedded projects and UV bounds;')
print('32 generated item models; 6 Star Glass furnace recipes; grayscale tint assets;')
print('3 animated strips; 16-frame GIF; no GameTest classes in production jar.')
print('Static checks only: no Minecraft client or GameTests were run.')
