"""Keep earlier projects intact; create single-atlas Bedrock inspection copies."""
import base64, copy, io, json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'outputs/ZeroG_Armour_Vanilla_Reference_05'

def fix(name, side):
    original = FOLDER / name
    model = json.loads(original.read_text())
    atlas = Image.new('RGBA', (side, side))
    slots = []
    for i, texture in enumerate(model['textures']):
        image = Image.open(io.BytesIO(base64.b64decode(texture['source'].split(',', 1)[1]))).convert('RGBA')
        x, y = (i % (side//256))*256, (i//(side//256))*256
        assert image.size == (256,256)
        atlas.paste(image, (x,y))
        slots.append((x,y))
    for element in model['elements']:
        for face in element['faces'].values():
            if face.get('texture') is None:
                continue
            x,y = slots[int(face['texture'])]
            face['uv'] = [v+(x if i%2==0 else y) for i,v in enumerate(face['uv'])]
            face['texture'] = 0
    raw = io.BytesIO()
    atlas.save(raw, format='PNG')
    texture = copy.deepcopy(model['textures'][0])
    texture.update(source='data:image/png;base64,'+base64.b64encode(raw.getvalue()).decode(),
                   id='0', name=original.stem+'_single_atlas.png', path='', width=side,
                   height=side, uv_width=side, uv_height=side)
    model['textures'] = [texture]
    model['resolution'] = {'width':side, 'height':side}
    model['name'] += ' — single-atlas binding repaired'
    model.setdefault('design_notes', {})['texture_binding_repair'] = 'One atlas for Bedrock single_texture format; geometry, bones and alpha preserved.'
    output = original.with_name(original.stem+'_single_atlas.bbmodel')
    output.write_text(json.dumps(model, separators=(',',':')))
    atlas.save(output.with_suffix('.png'))
    assert len(model['textures']) == 1
    assert all(f.get('texture') in (0,None) for e in model['elements'] for f in e['faces'].values())
    print(output)

if __name__ == '__main__':
    fix('vanilla_netherite_vs_nullifite.bbmodel', 512)
    fix('all_20_armour_showcase.bbmodel', 2048)
