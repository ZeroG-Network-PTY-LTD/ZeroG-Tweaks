"""Replay the observed resource-pack precedence and inspect the bound item pixels.

This checks the white-silhouette asset symptom, not shader/GPU correctness.
The observed reload log loads aeroapiary before zerog_tweaks in mod_resources.
"""
import argparse
import io
import json
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

p = argparse.ArgumentParser()
p.add_argument('--instance', type=Path, required=True)
p.add_argument('--jar', type=Path)
a = p.parse_args()
root = Path(__file__).resolve().parents[1] / 'src/main/resources'
addon_path = a.instance / 'mods/zerog-binnie-expansion-1.21.1-1.0.0.jar'
options = (a.instance / 'options.txt').read_text()
selected = json.loads(next(line.split(':', 1)[1] for line in options.splitlines()
                          if line.startswith('resourcePacks:')))
addon = ZipFile(addon_path)
candidate = ZipFile(a.jar) if a.jar else None

def own(path):
    if candidate:
        return candidate.read(path) if path in candidate.namelist() else None
    file = root / path
    return file.read_bytes() if file.is_file() else None

def resolve(path):
    result = None
    for pack in selected:
        if pack == 'mod/zerog_tweaks:resourcepacks/visual_refresh':
            result = own('resourcepacks/visual_refresh/' + path) or result
        elif pack == 'mod_resources':
            if path in addon.namelist():
                result = addon.read(path)
            result = own(path) or result
    return result

failures = []
checked = 0
try:
    for file in addon.namelist():
        if not file.startswith('assets/aeroapiary/models/item/') or not file.endswith('.json'):
            continue
        model = json.loads(resolve(file))
        texture = model.get('textures', {}).get('layer0')
        if not texture or texture.startswith('#'):
            continue
        ns, key = texture.split(':')
        payload = resolve(f'assets/{ns}/textures/{key}.png')
        if payload is None:
            failures.append(file + ': missing bound PNG')
            continue
        with Image.open(io.BytesIO(payload)) as image:
            pixels = [v for v in image.convert('RGBA').get_flattened_data() if v[3]]
        checked += 1
        fraction = sum(min(v[:3]) > 230 for v in pixels) / max(1, len(pixels))
        if not pixels or fraction > .60:
            failures.append(file.rsplit('/', 1)[-1] + f': white fraction {fraction:.3f}')
finally:
    addon.close()
    if candidate:
        candidate.close()
assert checked >= 60, f'Unexpectedly shallow item coverage: {checked}'
assert not failures, 'Visible item art failures under saved pack order:\n' + '\n'.join(failures)
print(f'PASS: {checked} bound apiary item PNGs retain coloured artwork under the saved pack order. GPU review remains separate.')
