"""Project-specific Blockbench -> GeckoLib export, preserving approved source bytes.

Not a canonical GLB vendor certificate. The human accepted the Blockbench-format
exception and unverified concept-reference artwork licence in this chat.
Default invocation plans only; --import-approved writes the resolved resources.
Coordinate/UV conventions match Blockbench v5.2.1's Bedrock codec.
"""
from pathlib import Path
import argparse, json, hashlib, shutil, math, datetime

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT
COLLECTION = ROOT / 'docs/asset-collection-1.21.1'
SOURCE = COLLECTION / 'approved-tidewraith/docs/shattered-skies'
DEST = PROJECT / 'src/main/resources/assets/zerog_tweaks'
MODELS = {
    'tidewraith': SOURCE / 'abyssal-face-repair/tidewraith_abyssal_concept_face.bbmodel',
    'tidewraith_boss': SOURCE / 'tidewraith-concept/tidewraith_concept.bbmodel',
}
TEXTURES = {
    'tidewraith': SOURCE / 'abyssal-face-repair/tidewraith_abyssal_concept_face',
    'tidewraith_boss': SOURCE / 'tidewraith-concept/tidewraith_concept',
    **{'tidewraith_boss_' + style: SOURCE / ('tidewraith-concept/tidewraith_concept_' + style)
       for style in ('abyssal', 'pearl', 'storm')},
}

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def vector(value, signs=(1, 1, 1)):
    assert len(value) == 3
    result = [float(v) * signs[i] for i, v in enumerate(value)]
    assert all(math.isfinite(v) for v in result)
    return result

def compile_model(data, identifier):
    elements = {e['uuid']: e for e in data['elements']}
    bones, seen, group_names = [], set(), {}
    def cube(e):
        assert e.get('type') == 'cube' and not e.get('box_uv'), 'Unsupported model element'
        size = [e['to'][i] - e['from'][i] for i in range(3)]
        assert all(v >= 0 for v in size)
        result = {'origin': [-e['to'][0], e['from'][1], e['from'][2]], 'size': size}
        if e.get('inflate'): result['inflate'] = e['inflate']
        if any(e.get('rotation', [0, 0, 0])):
            result['pivot'] = vector(e['origin'], (-1, 1, 1))
            result['rotation'] = vector(e['rotation'], (-1, -1, 1))
        result['uv'] = {}
        for direction, face in e.get('faces', {}).items():
            if face.get('texture') is None: continue
            assert face.get('texture') == 0 and not face.get('rotation'), 'Unsupported face texture/rotation'
            u, v, u2, v2 = face['uv']
            du, dv = u2-u, v2-v
            if direction in ('up', 'down'): u, v, du, dv = u2, v2, -du, -dv
            result['uv'][direction] = {'uv': [u, v], 'uv_size': [du, dv]}
        return result
    def group(g, parent=None):
        assert isinstance(g, dict) and g.get('export', True), 'Unsupported hidden group'
        assert g['name'] not in group_names.values(), 'Duplicate bone name'
        group_names[g['uuid']] = g['name']
        bone = {'name': g['name'], 'pivot': vector(g.get('origin', [0,0,0]), (-1,1,1))}
        if parent: bone['parent'] = parent
        if any(g.get('rotation', [0,0,0])): bone['rotation'] = vector(g['rotation'], (-1,-1,1))
        cubes = []
        bones.append(bone)
        for child in g.get('children', []):
            if isinstance(child, dict): group(child, g['name'])
            else:
                assert child not in seen, 'Element appears twice in outliner'
                e = elements[child]
                if e.get('export', True): cubes.append(cube(e)); seen.add(child)
        if cubes: bone['cubes'] = cubes
    for g in data['outliner']: group(g)
    assert seen == {e['uuid'] for e in elements.values() if e.get('export', True)}, 'Missing elements'
    resolution = data['resolution']
    geometry = {'format_version': '1.12.0', 'minecraft:geometry': [{
        'description': {'identifier': 'geometry.zerog_tweaks.' + identifier,
                        'texture_width': resolution['width'], 'texture_height': resolution['height'],
                        'visible_bounds_width': 16, 'visible_bounds_height': 16, 'visible_bounds_offset': [0,2,0]},
        'bones': bones}]}
    return geometry, group_names, len(seen)

def compile_animations(data, identifier, names):
    animations = {}
    for source in data.get('animations', []):
        clip = source['name'].split('.')[-1]
        name = 'animation.zerog_tweaks.' + identifier + '.' + clip
        assert name not in animations
        out = {'animation_length': source['length'], 'bones': {}}
        if source.get('loop') == 'loop': out['loop'] = True
        elif source.get('loop') == 'hold': out['loop'] = 'hold_on_last_frame'
        if source.get('override'): out['override_previous_animation'] = True
        for uuid, animator in source.get('animators', {}).items():
            assert animator.get('type') == 'bone' and uuid in names, 'Unsupported animation target'
            channels = {}
            for k in sorted(animator.get('keyframes', []), key=lambda k:k['time']):
                channel = k['channel']
                assert channel in ('rotation','position','scale') and k.get('interpolation') == 'linear'
                signs = (-1,-1,1) if channel == 'rotation' else (-1,1,1) if channel == 'position' else (1,1,1)
                values = [vector([p['x'],p['y'],p['z']], signs) for p in k['data_points']]
                assert len(values) in (1,2)
                value = values[0] if len(values)==1 else {'pre':values[0], 'post':values[1]}
                time = str(round(k['time'], 4))
                assert time not in channels.setdefault(channel,{})
                channels[channel][time] = value
            if channels: out['bones'][names[uuid]] = channels
        animations[name] = out
    for required in ('fly','blink','mouth_open'):
        assert 'animation.zerog_tweaks.' + identifier + '.' + required in animations
    return {'format_version':'1.8.0', 'animations':animations}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--import-approved', action='store_true')
    parser.add_argument('--code-root', type=Path, required=True, help='Separate 1.21.x checkout')
    parser.add_argument('--receipt', type=Path, help='Receipt path inside the separate Docs checkout')
    args = parser.parse_args()
    global PROJECT, DEST
    PROJECT = args.code_root.resolve()
    assert (PROJECT/'build.gradle').is_file(), 'Expected code checkout'
    DEST = PROJECT/'src/main/resources/assets/zerog_tweaks'
    if args.import_approved:
        assert args.receipt, '--receipt is required when importing; never write docs into code'
    manifest = json.loads((COLLECTION/'catalog.json').read_text())
    roster = {r['path']:r for r in manifest['files']}
    files, source_records, summaries = {}, {}, {}
    def verify(path):
        rel = path.relative_to(COLLECTION).as_posix()
        expected = roster[rel]
        assert path.stat().st_size == expected['bytes'] and digest(path) == expected['sha256'], 'Source integrity mismatch: '+rel
        source_records[rel] = {'bytes':path.stat().st_size, 'sha256':digest(path)}
    for identifier, path in MODELS.items():
        verify(path)
        data = json.loads(path.read_text())
        geometry, names, count = compile_model(data, identifier)
        animations = compile_animations(data, identifier, names)
        files[DEST/'geo'/(identifier+'.geo.json')] = (json.dumps(geometry, separators=(',',':'))+'\n').encode()
        files[DEST/'animations'/(identifier+'.animation.json')] = (json.dumps(animations, separators=(',',':'))+'\n').encode()
        summaries[identifier] = {'cubes':count, 'bones':len(names), 'texture':data['resolution'],
                                'animations':list(animations['animations'])}
    for identifier, stem in TEXTURES.items():
        for suffix in ('.png','_glowmask.png'):
            path = Path(str(stem)+suffix); verify(path)
            files[DEST/'textures/entity'/(identifier+suffix)] = path.read_bytes()
        # Explicit _glowmask wins over glowsections in GeckoLib 4.9.3. Keep nearest
        # sampling; do not write invalid empty glowsections metadata.
        files[DEST/'textures/entity'/(identifier+'.png.mcmeta')] = b'{"texture":{"blur":false,"clamp":false}}\n'
    # Branch migration may retain CRLF/pretty JSON. Preserve existing bytes when
    # parsed JSON is identical; geometry/animation changes still fail closed.
    retained_json_formatting = []
    for path, raw in list(files.items()):
        if path.exists() and path.read_bytes() != raw and path.suffix in ('.json', '.mcmeta'):
            if json.loads(path.read_bytes()) == json.loads(raw):
                files[path] = path.read_bytes()
                retained_json_formatting.append(path.relative_to(PROJECT).as_posix())
    collisions = [str(p) for p,raw in files.items() if p.exists() and p.read_bytes()!=raw]
    assert not collisions, 'Refusing to overwrite different runtime artwork: '+str(collisions)
    receipt = {'format':'zerog.project-specific-blockbench-import.v1', 'project':str(PROJECT),
               'source_collection':str(COLLECTION), 'canonical_glb_admission':False,
               'accepted_exceptions':['noncanonical Minecraft Blockbench/GeckoLib format', 'unverified concept-reference artwork licence'],
               'approval':'Human replied continue to import/test request, then yes restore and continue',
               'sources':source_records, 'models':summaries,
               'outputs':[{ 'path':p.relative_to(PROJECT).as_posix(), 'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()} for p,raw in files.items()],
               'imported':args.import_approved, 'runtime_tested':False, 'gpu_render_verified':False}
    if args.import_approved:
        assert PROJECT.is_dir()
        for path, raw in files.items():
            path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(raw)
            assert digest(path)==hashlib.sha256(raw).hexdigest()
        out = args.receipt
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'project':str(PROJECT), 'models':summaries, 'resources':len(files),
                      'imported':args.import_approved, 'collisions':collisions,
                      'retained_json_formatting':retained_json_formatting},indent=2))

if __name__=='__main__':main()
