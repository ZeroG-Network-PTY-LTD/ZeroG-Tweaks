"""Verify portable gallery links, current ZIP bytes and retirement boundaries."""
import hashlib, json, zipfile
from html.parser import HTMLParser
from pathlib import Path
from review_mob_assets import ROOT, BUNDLE, ASSETS

class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.cards=0
    def handle_starttag(self,tag,attrs):
        if tag=='article':self.cards+=1
        for key,value in attrs:
            if key in ('href','src'):self.links.append(value)

def main():
    base=BUNDLE/'blockbench';parser=Links();parser.feed((base/'index.html').read_text())
    assert parser.cards==224,parser.cards
    for link in parser.links:
        if '://' not in link and not link.startswith('#'):assert (base/link).is_file(),link
    report=json.loads((base/'validation.json').read_text())
    assert (report['models'],report['shattered_styles'],report['spawn_eggs'],report['drop_models'],report['aura_previews'])==(28,41,38,65,52)
    assert json.loads((base/'rig_audit.json').read_text())['status']=='passed'
    keys=[p.stem for p in (base/'mobs').glob('*.bbmodel')]
    assert len(keys)==28
    for key in keys:
        for folder,suffix in [('geckolib/models/entity','.geo.json'),('geckolib/animations/entity','.animation.json')]:
            assert not (ASSETS/folder/(key+suffix)).exists()
    assert len(json.loads((base/'references/vanilla_animation_inventory.json').read_text())['mobs'])==82
    archive=BUNDLE/'ZeroG_Mob_Blockbench_1.21.1.zip'
    with zipfile.ZipFile(archive) as jar:
        assert jar.testzip() is None
        assert sum(p.endswith('.bbmodel') for p in jar.namelist())==224
        for p in base.rglob('*'):
            if not p.is_file():continue
            entry=(Path('zero-g-tweaks-bundle')/p.relative_to(BUNDLE)).as_posix()
            assert jar.read(entry)==p.read_bytes(),f'Stale ZIP file: {entry}'
        for entry in jar.namelist():
            if entry.startswith('assets/'):
                assert jar.read(entry)==(ROOT/'src/main/resources'/entry).read_bytes(),entry
    print('PASS: 224 gallery projects, all local links, current ZIP bytes, 82-mob reference inventory, and 56-export retirement boundaries')
    print('ZIP SHA256:',hashlib.sha256(archive.read_bytes()).hexdigest())

if __name__=='__main__':main()
