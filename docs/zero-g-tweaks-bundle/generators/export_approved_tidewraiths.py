"""Export approved local projects, preserving authored geometry and texels.

The source snapshots/receipts are immutable inputs. This is a project-specific
Bedrock->GeckoLib export, not GLB/canonical game-dev certification. Coordinate
conversions follow Blockbench's Bedrock codec (X reflection, XY rotation signs,
and both UV directions reversed on up/down faces). No provider calls.
"""
import argparse
import base64
import hashlib
import io
import json
import zipfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'docs/shattered-skies'
OUT = ROOT / 'docs/tidewraith-approved'
ASSETS = ROOT / 'src/main/resources/assets/zerog_tweaks'
SOURCES = {
    'tidewraith': SOURCE/'abyssal-face-repair/tidewraith_abyssal_concept_face.bbmodel',
    'tidewraith_boss': SOURCE/'tidewraith-concept/tidewraith_concept.bbmodel',
}
STYLES = ('', '_abyssal', '_pearl', '_storm')


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')


def verify_sources():
    for folder in ('abyssal-face-repair', 'tidewraith-concept'):
        base = SOURCE/folder
        receipt = json.loads((base/'manifest.json').read_text())
        actual = {p.relative_to(base).as_posix() for p in base.rglob('*')
                  if p.is_file() and p.name != 'manifest.json'}
        assert actual == set(receipt['files']), 'Source roster changed: '+folder
        for name, expected in receipt['files'].items():
            assert digest(base/name) == expected, 'Source hash mismatch: '+name


def point(p): return [-p[0], p[1], p[2]]
def angles(p): return [-p[0], -p[1], p[2]]


def export_geo(model, key):
    elements = {e['uuid']: e for e in model['elements']}
    bones = []
    assigned = set()
    def walk(items, parent=None):
        for node in items:
            assert isinstance(node, dict), 'Ungrouped cube must be rigged before export'
            bone = {'name': node['name'], 'pivot': point(node['origin']), 'cubes': []}
            if parent: bone['parent'] = parent
            if any(node.get('rotation', [0, 0, 0])): bone['rotation'] = angles(node['rotation'])
            for child in node['children']:
                if isinstance(child, dict): continue
                assert child not in assigned, 'Cube belongs to multiple bones'
                assigned.add(child)
                e = elements[child]
                lo, hi = e['from'], e['to']
                cube = {'origin': [-hi[0], lo[1], lo[2]],
                        'size': [b-a for a,b in zip(lo,hi)], 'uv': {}}
                if any(e.get('rotation', [0, 0, 0])):
                    cube.update(pivot=point(e['origin']), rotation=angles(e['rotation']))
                if e.get('inflate'): cube['inflate'] = e['inflate']
                for face, data in e['faces'].items():
                    if data.get('texture') is None: continue
                    assert str(data['texture']) == '0', 'Single atlas required'
                    assert not data.get('rotation', 0), 'Rotated UV export requires a newer format'
                    u0,v0,u1,v1 = data['uv']
                    uv = {'uv': [u0,v0], 'uv_size': [u1-u0,v1-v0]}
                    if face in ('up','down'):
                        uv = {'uv': [u1,v1], 'uv_size': [u0-u1,v0-v1]}
                    cube['uv'][face] = uv
                bone['cubes'].append(cube)
            bones.append(bone)
            walk([c for c in node['children'] if isinstance(c,dict)], node['name'])
    walk(model['outliner'])
    assert assigned == set(elements), 'Unexported or unknown cube'
    assert len({b['name'] for b in bones}) == len(bones), 'Duplicate bone name'
    return {'format_version': '1.12.0', 'minecraft:geometry': [{
        'description': {'identifier': 'geometry.zerog_tweaks.'+key,
            'texture_width': model['resolution']['width'],
            'texture_height': model['resolution']['height'],
            # Includes wings, tail and drooping tendrils throughout animation.
            'visible_bounds_width': 12, 'visible_bounds_height': 10,
            'visible_bounds_offset': [0,1.5,0]}, 'bones': bones}]}


def negate(value):
    if isinstance(value,(int,float)): return -value
    try: return -float(value)
    except ValueError: return '-('+value+')'


def vector(data, channel):
    values = [data[a] for a in ('x','y','z')]
    if channel in ('position','rotation'): values[0] = negate(values[0])
    if channel == 'rotation': values[1] = negate(values[1])
    return values


def export_animations(model, key):
    clips = {}
    for clip in model['animations']:
        name = 'animation.zerog_tweaks.'+key+'.'+clip['name'].rsplit('.',1)[1]
        entry = {'loop': clip['loop']=='loop', 'animation_length': clip['length'], 'bones': {}}
        for animator in clip['animators'].values():
            assert animator['type']=='bone', 'Effect tracks require explicit runtime wiring'
            channels = {}
            for frame in sorted(animator['keyframes'], key=lambda f: f['time']):
                assert frame['interpolation'] in ('linear','catmullrom')
                channel = frame['channel']
                points = frame['data_points']
                value = vector(points[0], channel)
                if len(points)>1:
                    value = {'pre':value, 'post':vector(points[-1],channel)}
                if frame['interpolation']=='catmullrom':
                    value = {'post':value, 'lerp_mode':'catmullrom'}
                channels.setdefault(channel,{})[str(frame['time'])] = value
            entry['bones'][animator['name']] = channels
        clips[name] = entry
    return {'format_version':'1.8.0', 'animations':clips}


def texture(model):
    assert len(model['textures'])==1
    return base64.b64decode(model['textures'][0]['source'].split(',',1)[1])


def backup():
    verify_sources()
    OUT.mkdir(parents=True, exist_ok=True)
    # Fixed archive metadata makes the snapshot reproducible. No sources removed.
    target = OUT/'approved-models-backup.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for folder in ('abyssal-face-repair','tidewraith-concept'):
            for path in sorted((SOURCE/folder).rglob('*')):
                if path.is_file():
                    info = zipfile.ZipInfo(path.relative_to(SOURCE).as_posix(), (2026,10,1,0,0,0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info,path.read_bytes())
    write(OUT/'backup-receipt.json', {'archive':target.name,'sha256':digest(target),
          'regular_model': str(SOURCES['tidewraith'].relative_to(ROOT)),
          'regular_sha256': digest(SOURCES['tidewraith']),
          'boss_model': str(SOURCES['tidewraith_boss'].relative_to(ROOT)),
          'boss_sha256': digest(SOURCES['tidewraith_boss']),
          'boss_scale':'authored; multiplier 1.0; half-block studies excluded from runtime',
          'source_snapshots_preserved':True})


def build_runtime():
    verify_sources()
    paths = []
    def record(path, data=None, raw=None):
        if raw is None: write(path,data)
        else: path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(raw)
        paths.append(path)
    records = []
    for key, source in SOURCES.items():
        model = json.loads(source.read_text())
        record(ASSETS/'geo'/f'{key}.geo.json',export_geo(model,key))
        record(ASSETS/'animations'/f'{key}.animation.json',export_animations(model,key))
        for style in (STYLES if key=='tidewraith_boss' else ('',)):
            current = source if not style else source.with_name('tidewraith_concept'+style+'.bbmodel')
            current_model = json.loads(current.read_text())
            image = texture(current_model)
            record(ASSETS/'textures/entity'/f'{key}{style}.png',raw=image)
            glow = current.with_name(current.stem+'_glowmask.png')
            record(ASSETS/'textures/entity'/f'{key}{style}_glowmask.png',raw=glow.read_bytes())
            # Verified against 4.9.3 GeoGlowingTextureMeta.fromExistingImage:
            # RGBA-zero pixels are skipped and selected pixels preserve alpha.
            # A separate PNG mask needs no glowsections metadata.
        record(ASSETS/'models/item'/f'{key}_spawn_egg.json',{'parent':'minecraft:item/template_spawn_egg'})
        records.append({'id':'zerog_tweaks:'+key,'boss':key=='tidewraith_boss',
            'model':str(source.relative_to(ROOT)), 'model_sha256':digest(source),
            'elements':len(model['elements']),'eyes':8 if key.endswith('_boss') else 2,
            'texture':list(model['resolution'].values()),'authored_scale_multiplier':1,
            'spawn_egg':'zerog_tweaks:'+key+'_spawn_egg',
            'natural_spawns_enabled':False,'campaign_abilities_implemented':False})
    # Merge only owned names; unrelated translations remain intact.
    lang_path=ASSETS/'lang/en_us.json'
    lang=json.loads(lang_path.read_text())
    lang.update({'entity.zerog_tweaks.tidewraith':'Tidewraith',
        'entity.zerog_tweaks.tidewraith_boss':'Tidewraith Boss',
        'item.zerog_tweaks.tidewraith_spawn_egg':'Tidewraith Spawn Egg',
        'item.zerog_tweaks.tidewraith_boss_spawn_egg':'Tidewraith Boss Spawn Egg',
        'itemGroup.zerog_tweaks.spawn_eggs':'ZeroG: Spawn Eggs'})
    write(lang_path,lang)
    write(OUT/'catalogue.json', {'minecraft':'1.21.1','loader':'NeoForge 21.1.252',
        'animation_library':'GeckoLib 4.9.3','mobs':records,
        'runtime_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},
        'admission':'Project-specific export; not game-dev canonical package certification',
        'source_art_rights':'User-supplied reference; licence not independently verified',
        'rendering_verified_in_game':False})
    print(json.dumps({'mobs':2,'runtime_assets':len(paths),'boss_scale':1,'output':str(OUT)}))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--backup-only',action='store_true')
    parser.add_argument('--plan',action='store_true',help='Validate export in memory; write nothing')
    args=parser.parse_args()
    if args.plan:
        verify_sources()
        for key,path in SOURCES.items():
            model=json.loads(path.read_text())
            geo=export_geo(model,key);clips=export_animations(model,key)
            print(json.dumps({'id':'zerog_tweaks:'+key,'source':str(path.relative_to(ROOT)),
                'destination':str(ASSETS.relative_to(ROOT)), 'elements':len(model['elements']),
                'bones':len(geo['minecraft:geometry'][0]['bones']),
                'clips':len(clips['animations']),'scale':1,
                'blocker':'Requires acceptance of project-specific import and unverified reference licence'}))
        return
    backup()
    if not args.backup_only: build_runtime()


if __name__=='__main__': main()
