"""Artifact/provenance and client-source contracts; does not claim in-game rendering tests."""
import argparse, hashlib, json, re
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

p=argparse.ArgumentParser();p.add_argument('--design-root',type=Path,required=True);p.add_argument('--jar',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[1];design=a.design_root/'docs/alveary-controller-gui-v1'
manifest=json.loads((design/'runtime-manifest.json').read_text())
with ZipFile(a.jar) as jar:
    for item in manifest['files']:
        path=item['path'];data=(design/'source'/path).read_bytes()
        assert hashlib.sha256(data).hexdigest()==item['sha256']
        assert (root/'src/main/resources'/path).read_bytes()==jar.read(path)==data
        assert jar.read('resourcepacks/visual_refresh/'+path)==data
        with Image.open(design/'source'/path) as im:assert im.size==(256,256)
    for name in ['client/AlvearyControllerScreen','client/AlvearyControllerScreen$Opening','client/PlanetSpaceSky$StarOverlay',
                 'event/AlvearyMenuSync','event/AlvearyMenuSync$Networking','guide/ApiaryMachineAccess','guide/AlvearyLayout']:
        assert 'net/zerog/tweaks/'+name+'.class' in jar.namelist(),name
    lang=json.loads(jar.read('assets/zerog_tweaks/lang/en_us.json'))
    screen=(root/'src/main/java/net/zerog/tweaks/client/AlvearyControllerScreen.java').read_text()
    keys=re.findall(r'label\("([a-z_]+)"\s*[,)]',screen)
    keys += [f'ledger_{i}' for i in range(5)] + [f'ledger_details_{i}' for i in range(4)]
    keys += [f'tier_name_{i}' for i in range(1,8)]
    for key in keys:assert 'screen.zerog_tweaks.alveary.'+key in lang,key
for name,digest in manifest['reference_hashes'].items():assert hashlib.sha256((design/'reference'/name).read_bytes()).hexdigest()==digest
sky=(root/'src/main/java/net/zerog/tweaks/client/PlanetSpaceSky.java').read_text()
assert 'universe_v3' not in sky and 'getPositionTexShader' not in sky and 'MESH' not in sky
assert 'Stage.AFTER_SKY' in sky and 'new float[480][11]' in sky and 'float size=.35F+random.nextFloat()*.55F' in sky
assert 'return false;' in sky.split('public boolean renderSky',1)[1].split('@EventBusSubscriber',1)[0]
assert 'level.random' not in sky and 'getStarBrightness(partialTick)' in sky
sync=(root/'src/main/java/net/zerog/tweaks/event/AlvearyMenuSync.java').read_text()
assert 'menu.containerId!=id' in sync and 'menu.stillValid(player)' in sync and 'distanceToSqr' in sync
assert 'getItem().copy()' in sync and 'menu.broadcastChanges()' in sync
assert 'new PositionedSlot' in screen and 'original.mayPlace(stack)' in screen and 'original.mayPickup(player)' in screen
repair=(root/'src/main/java/net/zerog/tweaks/client/ApiaryRendererRepair.java').read_text()
assert 'RenderShape.ENTITYBLOCK_ANIMATED' in repair
print('PASS: two native GUI textures, provenance, packaged classes/lang; guarded sort, delegated slots, native sky fallback, 480 larger coloured stars. Visual review remains manual.')
