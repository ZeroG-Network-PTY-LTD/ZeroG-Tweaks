"""Pinned NeoForge 1.21.1 Iris/Sodium installation, shaders off; dry-run by default."""
import argparse, hashlib, json, re, shutil, tempfile, tomllib, urllib.request, zipfile
from datetime import datetime, timezone
from pathlib import Path

VERSIONS = {'iris':'t3ruzodq','sodium':'Pb3OXVqC'}
CONFLICTS = {'iris','sodium','oculus','embeddium','rubidium','optifine','vulkanmod'}

def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def metadata(version):
    request=urllib.request.Request('https://api.modrinth.com/v2/version/'+version,
                headers={'User-Agent':'ZeroG-Tweaks-compatible-graphics-install/1.0'})
    with urllib.request.urlopen(request,timeout=30) as response:return json.load(response)

def modids(path):
    with zipfile.ZipFile(path) as jar:
        result=set()
        for n in ['META-INF/neoforge.mods.toml','META-INF/mods.toml']:
            if n in jar.namelist():
                result.update(m['modId'] for m in tomllib.loads(jar.read(n).decode()).get('mods',[]))
        if 'fabric.mod.json' in jar.namelist():result.add(json.loads(jar.read('fabric.mod.json'))['id'])
        return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--instance',type=Path,required=True)
    parser.add_argument('--install',action='store_true')
    args=parser.parse_args();instance=args.instance.resolve();mods=instance/'mods'
    assert instance.name=='ZeroG' and mods.is_dir(),'Use the existing exact ZeroG instance'
    installed={p.name:digest(p) for p in mods.glob('*.jar')}
    conflicts=[p.name for p in mods.glob('*.jar') if modids(p)&CONFLICTS]
    assert not conflicts,f'Existing graphics mods require a separate reviewed update: {conflicts}'
    versions={mod:metadata(id) for mod,id in VERSIONS.items()}
    assert any(d['version_id']==VERSIONS['sodium'] and d['dependency_type']=='required'
               for d in versions['iris']['dependencies']),'Pinned dependency mismatch'
    plan=[]
    for mod,v in versions.items():
        assert v['version_type']=='release' and '1.21.1' in v['game_versions'] and 'neoforge' in v['loaders']
        f=next(f for f in v['files'] if f['primary'])
        assert f['url'].startswith('https://cdn.modrinth.com/')
        assert Path(f['filename']).name==f['filename'] and not (mods/f['filename']).exists()
        plan.append({'id':mod,'version':v['version_number'],'file':f['filename'],
                     'sha512':f['hashes']['sha512'],'url':f['url'],'size':f['size']})
    report={'installed':False,'instance':str(instance),'files':plan,'shaders_enabled':False,
            'client_launched':False,'preserved_existing_jars':len(installed)}
    if not args.install:print(json.dumps(report,indent=2));return
    receipt=instance/'zerog-mod-backups'/('graphics-'+datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-UTC'))
    receipt.mkdir(parents=True,exist_ok=False)
    with tempfile.TemporaryDirectory(prefix='zerog-iris-') as staging:
        for row in plan:
            request=urllib.request.Request(row['url'],headers={'User-Agent':'ZeroG-Tweaks-local-install/1.0'})
            with urllib.request.urlopen(request,timeout=60) as response:data=response.read()
            assert len(data)==row['size'] and hashlib.sha512(data).hexdigest()==row['sha512'],'Publisher hash mismatch'
            path=Path(staging)/row['file'];path.write_bytes(data)
            assert row['id'] in modids(path),'Wrong mod/loader binary'
            with zipfile.ZipFile(path) as jar:
                assert 'META-INF/neoforge.mods.toml' in jar.namelist()
                assert jar.testzip() is None
            row['sha256']=digest(path)
        config=instance/'config'/'iris.properties'
        original=config.read_text() if config.exists() else None
        if config.exists():shutil.copyfile(config,receipt/'iris.properties.before')
        text=original or ''
        if re.search(r'^enableShaders\s*=',text,re.M):
            text=re.sub(r'^enableShaders\s*=.*$', 'enableShaders=false',text,flags=re.M)
        else:text+='\nenableShaders=false\n'
        created=[]
        try:
            for row in plan:
                target=mods/row['file']
                assert not target.exists();shutil.copyfile(Path(staging)/row['file'],target);created.append(target)
                assert digest(target)==row['sha256']
            config.parent.mkdir(parents=True,exist_ok=True);config.write_text(text)
            for name,sha in installed.items():assert digest(mods/name)==sha,'Existing JAR changed'
        except Exception:
            for p in created:
                if p.exists():p.rename(receipt/('failed-install-'+p.name))
            if original is not None:config.write_text(original)
            raise
    report.update(installed=True,receipt=str(receipt))
    (receipt/'installation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
