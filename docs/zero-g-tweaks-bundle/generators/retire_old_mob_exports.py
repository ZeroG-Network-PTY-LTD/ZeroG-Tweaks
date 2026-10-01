"""Retire only the 56 superseded ZeroG creature exports, with recoverable backups."""
import hashlib, json, shutil
from pathlib import Path
from build_mob_models import ROOT, write_json

def main():
    base=ROOT/'src/main/resources/assets/zerog_tweaks'
    keys=[r['model'] for r in json.loads((ROOT/'docs/zero-g-tweaks-bundle/blockbench/mobs/manifest.json').read_text())['models']]
    assert len(keys)==28 and len(set(keys))==28
    backup=Path('/mnt/c/users/jakem/documents/codex/2026-09-29/blo/retired-mob-exports-2026-09-30')
    rows=[]
    for key in keys:
        for old_dir,new_dir,suffix in (('geckolib/models/entity','geo','.geo.json'),('geckolib/animations/entity','animations','.animation.json')):
            old=base/old_dir/(key+suffix);current=base/new_dir/(key+suffix)
            assert current.is_file(),current
            if not old.exists():continue
            digest=hashlib.sha256(old.read_bytes()).hexdigest()
            target=backup/old_dir/(key+suffix)
            target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():
                assert hashlib.sha256(target.read_bytes()).hexdigest()==digest,'Backup collision; stop before removal'
            else:shutil.copy2(old,target)
            assert hashlib.sha256(target.read_bytes()).hexdigest()==digest
            old.unlink()
            rows.append({'removed':str(old.relative_to(ROOT)),'backup':str(target),'sha256':digest})
    report=ROOT/'docs/zero-g-tweaks-bundle/blockbench/references/retired_exports.json'
    if rows:write_json(report,{'count':len(rows),'recoverable':True,'scope':'Only superseded ZeroG creature geometry and animation exports; armour/source specs retained','files':rows})
    print('Retired',len(rows),'old exports; verified backups at',backup)

if __name__=='__main__':main()
