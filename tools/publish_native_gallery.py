"""Copy only original approved ZeroG native galleries/manifests to the Docs branch.

No concept cropping, third-party artwork, runtime code, private logs or saves.
This is an explicit bulk artifact copy; prior galleries are retained.
"""
import argparse,hashlib,json,shutil
from pathlib import Path

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--design',type=Path,required=True);p.add_argument('--docs',type=Path,required=True)
a=p.parse_args();count=0
for group in ['full-art-rollout-v4','storage-joinery-v1']:
    source=a.design/'docs'/group;dest=a.docs/'docs/images'/group
    assert source.is_dir() and dest.is_dir()
    manifest=json.loads((source/'manifest.json').read_text())
    assert not manifest.get('validation_errors',[]),'Source validation failed'
    files=[source/'manifest.json',source/'README.md']
    files+=sorted(source.glob('*native-*.png'))
    files+=sorted(source.glob('native-gallery-*.png'))
    if group=='full-art-rollout-v4':files.append(source/'worn-front-fit-preview.png')
    for item in files:
        assert item.is_file()
        target=dest/item.name;shutil.copyfile(item,target)
        assert hashlib.sha256(item.read_bytes()).digest()==hashlib.sha256(target.read_bytes()).digest()
        count+=1
print(json.dumps({'copied_original_artifacts':count,'third_party_assets_copied':False}))
