"""Keep vanilla egg layers/tints; add original, silhouette-clipped accent overlays."""
from pathlib import Path
import hashlib, io, json, re, zipfile
from PIL import Image, ImageDraw
from build_mob_drops_hd import bbmodel

ROOT = Path(__file__).resolve().parents[3]
ASSETS = ROOT / 'src/main/resources/assets/zerog_tweaks'
OUT = ROOT / 'docs/zero-g-tweaks-bundle/blockbench/spawn_eggs'
JAR = Path('/mnt/c/Users/jakem/.gradle/caches/neoformruntime/artifacts/minecraft_1.21.1_client.jar')

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(JAR) as archive:
        raw = [archive.read('assets/minecraft/textures/item/' + name + '.png')
               for name in ('spawn_egg', 'spawn_egg_overlay')]
    layers = [Image.open(io.BytesIO(data)).convert('RGBA') for data in raw]
    rows = re.findall(r'egg\("(\w+)", 0x([\dA-F]{6}), 0x([\dA-F]{6}), ([^;]+)\);',
                      (ROOT / 'src/main/java/net/zerog/tweaks/registry/ZGSpawnEggs.java').read_text())
    assert len(rows) == 38
    sheet = Image.new('RGB', (760, 560), '#1b202b')
    draw = ImageDraw.Draw(sheet)
    records = []
    for index, (key, base, spots, ids) in enumerate(rows):
        colours = [tuple(bytes.fromhex(base)), tuple(bytes.fromhex(spots))]
        preview = Image.new('RGBA', (16, 16))
        for layer, colour in zip(layers, colours):
            tinted = Image.new('RGBA', layer.size)
            tinted.putdata([(*(round(c * p[i] / 255) for i, c in enumerate(colour)), p[3])
                            for p in layer.getdata()])
            preview = Image.alpha_composite(preview, tinted)
        accent = Image.new('RGBA', (16, 16))
        ink = ImageDraw.Draw(accent)
        family = 'shatteredskies:' in ids
        colour = (201, 168, 255, 255) if family else (*colours[1], 255)
        # Small pixel diamond/star; no silhouette, shell or vanilla spot changes.
        for x, y in ((6, 5), (5, 6), (6, 6), (7, 6), (6, 7)):
            if layers[0].getpixel((x, y))[3]:
                ink.point((x, y), fill=colour)
        ink.point((6, 6), fill=(245, 239, 255, 255))
        texture = ASSETS / 'textures/item' / (key + '_spawn_egg_accent.png')
        accent.save(texture)
        model = {'parent': 'minecraft:item/generated', 'textures': {
            'layer0': 'minecraft:item/spawn_egg',
            'layer1': 'minecraft:item/spawn_egg_overlay',
            'layer2': 'zerog_tweaks:item/' + key + '_spawn_egg_accent'}}
        (ASSETS / 'models/item' / (key + '_spawn_egg.json')).write_text(json.dumps(model, indent=2) + '\n')
        preview = Image.alpha_composite(preview, accent)
        preview.save(OUT / (key + '_spawn_egg.png'))
        project=bbmodel({'k':key+'_spawn_egg'},preview.resize((64,64),Image.Resampling.NEAREST))
        project['name']=key+'_spawn_egg_preview'
        project['preview_note']='Baked colour preview only; runtime uses vanilla layers with registry tints and an original layer2 accent.'
        (OUT/(key+'_spawn_egg.bbmodel')).write_text(json.dumps(project,indent=2)+'\n')
        x, y = (index % 8) * 95, (index // 8) * 112
        enlarged = preview.resize((64, 64), Image.Resampling.NEAREST)
        sheet.paste(enlarged, (x + 15, y + 7), enlarged)
        label = key.replace('_', ' ')
        for line, word in enumerate([label[:15], label[15:]]):
            draw.text((x + 3, y + 77 + line * 12), word, fill='#c9a8ff' if family else '#e7edf5')
        records.append({'mob': key, 'base': '#' + base, 'spots': '#' + spots,
                        'entity_ids': re.findall(r'"([^"]+)"', ids)})
    sheet.save(OUT / 'spawn_eggs_preview.png')
    (OUT / 'manifest.json').write_text(json.dumps({
        'count': len(records), 'shape': 'Minecraft 1.21.1 vanilla egg, unmodified layer0/layer1',
        'source': 'Mojang Minecraft client resources; referenced at runtime, not bundled copies',
        'source_sha256': [hashlib.sha256(data).hexdigest() for data in raw],
        'accents': 'Original 16px coordinated star / violet splinter on untinted layer2',
        'eggs': records}, indent=2) + '\n')
    print('Validated and generated', len(records), 'vanilla-shape egg accents and previews')

if __name__ == '__main__':
    main()
