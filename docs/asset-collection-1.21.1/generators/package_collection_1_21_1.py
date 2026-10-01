"""Publishable design snapshot only: no runtime installation or third-party reference copying."""
from pathlib import Path
import base64, copy, hashlib, io, json, shutil, subprocess, tarfile, uuid
from collections import Counter
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/ZeroG_Full_Collection_1_21_1_06'
REPO = Path('/mnt/c/Users/jakem/Desktop/ZeroG_Mods/ZeroG_Tweaks_Assets')
RELEASE = ROOT / 'tidewraith-release-IqBNBf'
MOB_REV = '00d4013ba5863fd369e1ae581f295eedc645d7d2'
TIDE_REV = '6f16f6450eabdf07cf3984ee638ee64fe9588c28'
PS = '/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe'
WIN_GIT = '/mnt/c/Program Files/Git/cmd/git.exe'

def windows(path):
    value=str(path.resolve())
    assert value.lower().startswith('/mnt/c/')
    return 'C:\\'+value[7:].replace('/', '\\')

def ps_quote(path):
    return "'"+windows(path).replace("'", "''")+"'"

def native_ps(command):
    subprocess.run([PS,'-NoProfile','-NonInteractive','-Command',
                    "$ErrorActionPreference='Stop'; "+command],check=True)

def export_tree(repo, rev, paths, destination):
    snapshot = ROOT / 'work' / ('collection_snapshot_'+rev[:12]+'.zip')
    # Both immutable commits share the original repository's object store.
    subprocess.run([WIN_GIT, '-c', 'safe.directory='+windows(REPO).replace('\\','/'), '-C', windows(REPO),
                    'archive', '--format=zip', '-o', windows(snapshot), rev, *paths],check=True)
    native_ps('Expand-Archive -LiteralPath '+ps_quote(snapshot)+' -DestinationPath '+ps_quote(destination)+' -Force')

def copy_folder(src, dst):
    native_ps('New-Item -ItemType Directory -Force -Path '+ps_quote(dst)+' | Out-Null; '+
              'Get-ChildItem -LiteralPath '+ps_quote(src)+' | Copy-Item -Destination '+ps_quote(dst)+' -Recurse -Force')

def prepare():
    OUT.mkdir(parents=True, exist_ok=True)
    armor = ROOT / 'outputs/ZeroG_Vanilla_Fit_Armour_06'
    copy_folder(armor, OUT / 'armour')
    bee = ROOT / 'work/zerog_bees_complete_stack_1_21_1'
    copy_folder(bee / 'blockbench_by_use', OUT / 'bees/blockbench_by_use')
    for path in bee.iterdir():
        if path.is_file() and path.suffix in ['.md','.json']:
            shutil.copy2(path, OUT / 'bees' / path.name)
    material = ROOT / 'work/zerog_tweaks_materials_blockbench_1_21_1'
    copy_folder(material / 'blockbench', OUT / 'materials/blockbench')
    copy_folder(material / 'previews', OUT / 'materials/previews')
    for path in material.iterdir():
        if path.is_file() and path.suffix in ['.md','.json']:
            shutil.copy2(path, OUT / 'materials' / path.name)
    export_tree(REPO, MOB_REV, ['docs/zero-g-tweaks-bundle/blockbench',
                'docs/shattered-skies/blockbench', 'docs/shattered-skies/models',
                'docs/shattered-skies/sheets'], OUT / 'mobs')
    export_tree(RELEASE, TIDE_REV, ['docs/shattered-skies/abyssal-face-repair',
                'docs/shattered-skies/tidewraith-concept', 'docs/tidewraith-approved'],
                OUT / 'approved-tidewraith')

def selections():
    groups = {}
    groups['Armour — 20 fitted sets'] = sorted((OUT / 'armour').glob('*/*_player_fitted.bbmodel'))
    bee = OUT / 'bees/blockbench_by_use'
    for label, folder in [('Apiary blocks', 'blocks'), ('Apiary items and frames', 'items'),
                          ('Apiary multiblocks', 'multiblocks'), ('Apiarist wearables', 'wearables')]:
        groups[label] = sorted((bee / folder).rglob('*.bbmodel'))
    mat = OUT / 'materials/blockbench'
    groups['Material blocks'] = sorted((mat / 'blocks').rglob('*.bbmodel'))
    groups['Material items'] = sorted((mat / 'items').rglob('*.bbmodel'))
    mobs = OUT / 'mobs/docs/zero-g-tweaks-bundle/blockbench'
    groups['Mobs — existing committed designs'] = [p for p in sorted((mobs / 'mobs').glob('*.bbmodel'))
                                                   if 'tidewraith' not in p.stem]
    groups['Shattered Skies — style variants'] = [p for p in sorted((OUT / 'mobs/docs/shattered-skies/blockbench').glob('*.bbmodel'))
                                                   if 'tidewraith' not in p.stem]
    groups['Mob drops'] = sorted((mobs / 'mob_drops').glob('*.bbmodel'))
    groups['Spawn eggs'] = sorted((mobs / 'spawn_eggs').glob('*.bbmodel'))
    tide = OUT / 'approved-tidewraith/docs/shattered-skies'
    groups['Approved Tidewraith — regular and boss palettes'] = [tide / 'abyssal-face-repair/tidewraith_abyssal_concept_face.bbmodel']
    groups['Approved Tidewraith — regular and boss palettes'] += [tide / 'tidewraith-concept' / name for name in
        ['tidewraith_concept.bbmodel', 'tidewraith_concept_abyssal.bbmodel',
         'tidewraith_concept_pearl.bbmodel', 'tidewraith_concept_storm.bbmodel']]
    return {label: files for label, files in groups.items() if files}

def image_data(texture):
    source = texture.get('source', '')
    if not source.startswith('data:image/'):
        raise ValueError('Texture is not embedded: ' + texture.get('name', '?'))
    raw = base64.b64decode(source.split(',', 1)[1])
    return raw, Image.open(io.BytesIO(raw)).convert('RGBA')

def make_showcase(groups, filename, packed=False):
    models = []
    unique = {}
    metadata = {}
    for label, files in groups.items():
        for path in files:
            model = json.loads(path.read_text())
            tex = []
            for texture in model['textures']:
                raw, img = image_data(texture)
                uw=texture.get('uv_width',model['resolution']['width'])
                uh=texture.get('uv_height',model['resolution']['height'])
                key = hashlib.sha256(raw).hexdigest()+f':{uw}:{uh}'
                if key not in unique:
                    unique[key] = img
                    metadata[key] = {**texture,'width':img.width,'height':img.height,'uv_width':uw,'uv_height':uh}
                tex.append(key)
            models.append((label, path, model, tex))
    # One atlas avoids Bedrock's single-texture format dropping per-model textures.
    side = 2048 if packed else 256
    atlas = Image.new('RGBA', (side, side)) if packed else None
    offsets = {}
    x = y = shelf = 0
    for key, img in (sorted(unique.items(), key=lambda pair: -pair[1].height) if packed else []):
        if x + img.width + 2 > side:
            x = 0
            y += shelf
            shelf = 0
        if y + img.height + 2 > side:
            raise ValueError('Atlas overflow; never silently reduce texture resolution')
        offsets[key] = (x+1, y+1)
        atlas.paste(img, (x+1, y+1))
        x += img.width + 2
        shelf = max(shelf, img.height+2)
    (OUT / 'showcases').mkdir(parents=True,exist_ok=True)
    texture_indexes = {key:i for i,key in enumerate(unique)}
    if packed:
        png = io.BytesIO()
        atlas.save(png, format='PNG', optimize=True)
        png_data = png.getvalue()
        atlas_path = OUT / 'showcases' / (filename + '_atlas.png')
        atlas_path.write_bytes(png_data)
        textures=[{'name':atlas_path.name, 'id':'0', 'uuid':str(uuid.uuid4()),
                  'source':'data:image/png;base64,'+base64.b64encode(png_data).decode(),
                  'internal':True, 'saved':True, 'visible':True, 'render_mode':'default',
                  'width':side, 'height':side, 'uv_width':side, 'uv_height':side}]
    else:
        textures=[]
        for key,t in metadata.items():
            t={**t,'id':str(texture_indexes[key]),'uuid':str(uuid.uuid4()),'path':'','internal':True,'saved':True}
            textures.append(t)
    result = {'meta': {'format_version':'4.10', 'model_format':'bedrock' if packed else 'free', 'box_uv':False},
              'name':filename, 'model_identifier':filename.lower(),
              'resolution': {'width':side, 'height':side}, 'elements':[], 'outliner':[],
              'textures':textures,
              'animations':[], 'design_notes':{'purpose':'Static catalogue, not an entity export',
                  'geometry':'Authored scale preserved; catalogue translation only',
                  'animation':'Use each individual project for its original animation clips',
                  'emissive':'Glow colours visible; engine emissive behaviour not verified'}}
    last_label = None
    group_y = 0
    row_z = row_depth = cursor_x = 0
    group = None
    for label, path, model, tex in models:
        if label != last_label:
            if last_label is not None:
                group_y += row_z + row_depth + 64
            row_z = row_depth = cursor_x = 0
            group = {'name':label, 'uuid':str(uuid.uuid4()), 'origin':[0,0,0],
                     'children':[], 'isOpen':False, 'visibility':True}
            result['outliner'].append(group)
            last_label = label
        cubes = model.get('elements', [])
        if any(e.get('type', 'cube') != 'cube' for e in cubes):
            raise ValueError(f'Unsupported non-cube model: {path}')
        lo = [min(min(e['from'][i], e['to'][i]) for e in cubes) for i in range(3)]
        hi = [max(max(e['from'][i], e['to'][i]) for e in cubes) for i in range(3)]
        width, depth = hi[0]-lo[0]+24, hi[2]-lo[2]+24
        if cursor_x + width > 640 and cursor_x:
            row_z += row_depth
            row_depth = cursor_x = 0
        shift = [cursor_x-lo[0], -lo[1], group_y+row_z-lo[2]]
        cursor_x += width
        row_depth = max(row_depth, depth)
        ids = {}
        def rekey(old):
            if old not in ids:
                ids[old] = str(uuid.uuid5(uuid.NAMESPACE_URL, str(path.relative_to(OUT)) + '/' + old))
            return ids[old]
        for original in cubes:
            e = copy.deepcopy(original)
            e['uuid'] = rekey(e['uuid'])
            e['name'] = path.stem + '/' + e.get('name', 'cube')
            for key in ['from', 'to', 'origin']:
                if key in e:
                    e[key] = [v+shift[i] for i,v in enumerate(e[key])]
            e['box_uv'] = False
            for face in e.get('faces', {}).values():
                index = face.get('texture')
                if index is None:
                    continue
                if isinstance(index, str):
                    index = next((i for i,t in enumerate(model['textures']) if t.get('uuid') == index or t.get('id') == index), int(index) if index.isdigit() else -1)
                if not 0 <= index < len(tex):
                    raise ValueError(f'Invalid texture reference: {path}')
                img = unique[tex[index]]
                texture = model['textures'][index]
                uw = texture.get('uv_width', model['resolution']['width'])
                uh = texture.get('uv_height', model['resolution']['height'])
                if packed:
                    ox, oy = offsets[tex[index]]
                    face['uv'] = [ox+v*img.width/uw if i%2==0 else oy+v*img.height/uh for i,v in enumerate(face['uv'])]
                    face['texture'] = 0
                    assert all(0 <= v <= side for v in face['uv'])
                else:
                    face['texture'] = texture_indexes[tex[index]]
                    assert all(0 <= v <= (uw if i%2==0 else uh) for i,v in enumerate(face['uv'])),path
            result['elements'].append(e)
        def node(n):
            if isinstance(n, str):
                return rekey(n)
            n = copy.deepcopy(n)
            n['uuid'] = rekey(n['uuid'])
            if 'origin' in n:
                n['origin'] = [v+shift[i] for i,v in enumerate(n['origin'])]
            n['children'] = [node(c) for c in n.get('children', [])]
            return n
        group['children'].append({'name':path.stem, 'uuid':str(uuid.uuid4()),
            'origin':shift, 'children':[node(n) for n in model.get('outliner', [])],
            'isOpen':False, 'visibility':True})
    model_path = OUT / 'showcases' / (filename + '.bbmodel')
    model_path.write_text(json.dumps(result, separators=(',',':')))
    return {'file':str(model_path.relative_to(OUT)), 'models':len(models),
            'cubes':len(result['elements']), 'atlas_size':side if packed else None,
            'format':'bedrock' if packed else 'free', 'unique_textures':len(unique)}

def inventory(groups, showcases):
    names = {label:[p.stem.replace('_', ' ') for p in files] for label,files in groups.items()}
    guide = '''# ZeroG — complete design collection for Minecraft 1.21.1

Open `showcases/ZeroG_Full_Collection_1_21_1.bbmodel` in Blockbench. The Outliner groups the collection by use. Each individual model remains available in its source folder; use those projects to play their original animation clips. The combined catalogue intentionally has no animation clips: playing hundreds of entity animations together would not be a meaningful fit test.

This is an **asset and documentation snapshot**, not a new compiled release. Existing gameplay source and release jars on `1.21.1-update` are unchanged. Catalogue geometry keeps authored dimensions; only positions are translated to arrange rows. The complete catalogue uses Blockbench's generic Free format, which supports multiple textures and per-texture UV sizes without Bedrock's single-texture limitation. Individual source entity projects retain their authored formats. The twenty-armour catalogue uses one packed atlas. Both approaches preserve texels and alpha; neither catalogue is an entity intended for runtime export. For a lighter review, open one category showcase instead of the texture-heavy full scene.

## Armour

Twenty sets now use the **user-approved green-box vanilla-fitting silhouette**, replacing the orange-box custom armour geometry. Minecraft 1.21.1 humanoid joint positions are head/body Y24, arms X±5/Y22 and legs X±1.9/Y12. Neutral arm rotations are zero. Open faces, exposed forearms and hands, and independently painted family palettes follow the supplied twenty-material lineup. Hidden medial leg-shell walls are trimmed to X±0.05 to prevent neutral-pose leg z-fighting without changing the outside silhouette. Eight sets include 12-frame animated PNG studies: Nullifite, Moonsteel, Cerulite, Wraithsteel, Eidolite, Astrium, Radiantine and Solvanite. Each loop is 2.4 seconds. Java worn-armour animation/emissive rendering still needs runtime support; a tall PNG plus mcmeta alone does not prove it works on equipment. No detached halo/effect geometry has been added; animated fire/aura treatments remain future work.

The actual vanilla netherite/Sentry/amethyst study is kept locally only. No extracted Mojang source, Steve texture or netherite reference atlas is published in this snapshot. Armour uses an independently painted procedural player reference. Orange-box revisions remain local backups and are excluded from this active collection.

## Bees, apiaries and genetics

The supplied complete non-bee stack contains 85 block models, 65 standalone item models, 85 block-inventory item views, 8 multiblock assemblies, 8 Apiarist/Cosmic wearable projects and separate animation/held-item studies. Frames are inventory inserts, tools use held-item views, armour uses player rigs and multiblocks retain their individual controller/casing layout. Machines, frame housing, jelly, serums, combs, tools, confinement coils and tier assemblies are included as designs.

**Bee entity models are not included.** The earlier rejected bee designs have not been restored. Accepted vanilla Bedrock-style bees with recoloured space textures, original wings/eyes and suitable emissive details remain future work. The Binnie material is a concept translation, not a claim that Binnie's code or artwork was imported.

## Materials, blocks and inventory items

Thirty-nine material families provide 94 blocks (39 ores, 16 raw-storage blocks, 39 processed-storage blocks) and 71 item models. Blocks are full six-faced cubes; materials use transparent front/back inventory geometry. Original 16×16 art is preserved and nearest-neighbour enlarged to 64×64. That enlargement is not claimed as newly painted HD detail. Textures are embedded in the Blockbench projects. Duplicate loose runtime resources are not included or installed by this update.

## Mobs, drops and eggs

The committed mob snapshot retains existing creature designs, Shattered Skies style variants, drop items, coordinated spawn-egg studies, auras and reference sheets. These files are existing committed work, not a claim that every creature has been rebuilt or newly approved. Historical Tidewraith studies are retained for provenance but excluded from the main showcase in favour of the approved pair.

The approved non-boss Tidewraith has the repaired face and body/head connection. The manta-mouth Tidewraith is the boss design, retaining its authored size rather than applying the earlier six-player-height rule. Boss variants retain the shared silhouette, mouth, eight-eye design, articulated tendrils and wing animation studies. Individual source projects retain their clips and palettes. The approved branch's runtime draft is an archive, **not a spawnable-entity implementation installed here**. No fresh jar was built or placed into CurseForge by this asset update.

## Validation and provenance

`catalog.json` lists every packaged file with SHA-256, the immutable mob/approved-Tidewraith source commits, and the exact models selected for the catalogue. The showcase builder checks embedded textures, texture references, atlas packing where used and UV bounds; it preserves authored cube geometry and bone hierarchy. It does not certify every legacy model's animation, symmetry or in-game renderer. Software previews are not GPU captures. Separate emissive textures in individual models remain authoritative; catalogue previews do not demonstrate engine emissive behaviour. No canonical GLB asset-admission certificate is claimed. Generic-format capability was verified against the official Blockbench source at https://github.com/JannisX11/blockbench/blob/v5.2.1/js/formats/generic.ts .

## Future updates — not yet completed

- Accepted vanilla-based space bee entities and Productive Bees compatibility for Minecraft 1.21.1.
- Registration and renderers for mob designs; real spawn eggs, AI, attributes, drops and boss mechanics.
- Controller/hatchery/menu bindings, frame/bee/genetic/comb slots, production outputs and export automation.
- Multiblock formation and interaction tests against the running mod, plus missing renderer/emissive bindings.
- Java wearable integration, first/third-person fit checks, trim support, animated texture frames and synchronised glow masks.
- Fresh higher-detail material painting where requested, rather than only texture enlargement.
- Client launch, multiplayer checks, recipe validation, packaging and tested release jars.

The existing branch build/install instructions still apply to the unchanged code. This collection must not be described as a working implementation of the future features above.

## Catalogue by use

'''
    for label, files in groups.items():
        guide += f'### {label} — {len(files)} projects\n\n'
        guide += ', '.join(names[label]) + '.\n\n'
    guide += '## Showcase files\n\n'+''.join('- ['+s['file']+']('+s['file']+') — '+str(s['models'])+' projects\n' for s in showcases)
    (OUT / 'README.md').write_text(guide)
    import html
    cards = []
    for label, files in groups.items():
        links = ''.join('<li><a href="'+html.escape(str(p.relative_to(OUT)),quote=True)+'">'+html.escape(p.stem.replace('_',' '))+'</a></li>' for p in files)
        cards.append('<details><summary>'+html.escape(label)+f' ({len(files)})</summary><ul>'+links+'</ul></details>')
    armor_cards = ''.join('<article><h3>'+html.escape(p.parent.name.title())+'</h3><img src="armour/'+p.parent.name+'/threequarter.png"></article>' for p in groups['Armour — 20 fitted sets'])
    (OUT / 'review.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>ZeroG 1.21.1 collection</title><style>body{background:#111722;color:#eee;font:16px system-ui;margin:30px}a{color:#b7dcff}summary{cursor:pointer;padding:12px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}img{max-width:100%}article{background:#202b3b;padding:12px}</style><h1>ZeroG — Minecraft 1.21.1 design collection</h1><p>Design assets, not a new playable release. Individual projects retain animation clips.</p><p><a href="showcases/ZeroG_Full_Collection_1_21_1.bbmodel">Full Blockbench showcase</a> · <a href="showcases/ZeroG_All_20_Armour.bbmodel">20-set armour showcase</a> · <a href="README.md">Descriptions and future updates</a> · <a href="catalog.json">Hashed inventory</a></p>'+''.join(cards)+'<h2>Player-fitted armour</h2><main>'+armor_cards+'</main></html>')
    gen = OUT / 'generators'
    gen.mkdir(exist_ok=True)
    for name in ['package_collection_1_21_1.py', 'fix_armour_showcase_texture_binding.py',
                 'build_vanilla_fit_armour_collection_06.py', 'check_armour_clearance.py']:
        shutil.copy2(ROOT / 'work' / name, gen / name)
    records = []
    for path in sorted(OUT.rglob('*')):
        if path.is_file() and path.name != 'catalog.json':
            content = path.read_bytes()
            records.append({'path':str(path.relative_to(OUT)), 'bytes':len(content),
                            'sha256':hashlib.sha256(content).hexdigest()})
    catalogue = {'target':'Minecraft 1.21.1 / NeoForge', 'snapshot_only':True,
       'sources':{'mob_commit':MOB_REV, 'approved_tidewraith_commit':TIDE_REV,
                  'armour_revision':'06 green-box replacement', 'bee_entity_models_included':False,
                  'vanilla_reference_pixels_and_sources_published':False},
       'showcase_categories':{label:[str(p.relative_to(OUT)) for p in files] for label,files in groups.items()},
       'showcases':showcases, 'files':records,
       'limitations':['Not a compiled mod or runtime registration update',
          'Legacy mob snapshots are preserved, not newly approved or rebuilt',
          'Historical Tidewraith models are archived but excluded from the main showcase',
          'No bee entities included; previously rejected designs remain excluded',
          'Original materials art is nearest-neighbour enlarged, not newly detailed HD art',
          'Animated armour PNGs require explicit Java renderer support',
          'Catalogue layout has no animation clips; individual projects retain clips']}
    (OUT / 'catalog.json').write_text(json.dumps(catalogue, indent=2))
    print(json.dumps({'showcases':showcases, 'files':len(records),
                      'category_counts':{k:len(v) for k,v in groups.items()}}, indent=2))

if __name__ == '__main__':
    import sys
    if '--use-prepared' not in sys.argv:
        prepare()
    groups = selections()
    showcases = [make_showcase(groups, 'ZeroG_Full_Collection_1_21_1'),
                 make_showcase({'Armour — 20 fitted sets':groups['Armour — 20 fitted sets']}, 'ZeroG_All_20_Armour',packed=True)]
    for label,files in groups.items():
        if label!='Armour — 20 fitted sets':
            stem='Category_'+label.split(' — ')[0].replace(' ','_')
            showcases.append(make_showcase({label:files},stem))
    inventory(groups, showcases)
