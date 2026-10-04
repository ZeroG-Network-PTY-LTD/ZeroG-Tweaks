"""Read-only audit of shipped Prologue data, template identity and production packaging."""
import argparse
import json
import zipfile
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--jar',type=Path,required=True)
parser.add_argument('--design-root',type=Path,required=True)
args=parser.parse_args()
with zipfile.ZipFile(args.jar) as jar:
    names=set(jar.namelist())
    assert not any('/gametest/' in name and name.endswith('.class') for name in names), 'Test classes leaked into production'
    def data(path):return json.loads(jar.read(path))
    recipe=data('data/zerog_tweaks/recipe/gate_controller.json')
    assert recipe['result']['id']=='zerog_tweaks:gate_controller'
    assert recipe['key']['W']['item']=='zerog_tweaks:dormant_wisp'
    assert recipe['pattern']==['NGN','RFR','NWN']
    for name,parent in [('falling_star','root'),('builders_template','falling_star'),('first_gate','builders_template')]:
        advancement=data(f'data/zerog_tweaks/advancement/codex/{name}.json')
        assert advancement['parent']==f'zerog_tweaks:codex/{parent}'
    lang=data('assets/zerog_tweaks/lang/en_us.json')
    assert lang['advancements.zerog_tweaks.root.description']=='It hums. Pick up a piece of Nullifite.'
    for name in ['concord_codex','dormant_wisp']:
        assert f'item.zerog_tweaks.{name}' in lang
        model=data(f'assets/zerog_tweaks/models/item/{name}.json')
        assert model['parent']=='minecraft:item/generated'
        texture=model['textures']['layer0']
        if texture.startswith('zerog_tweaks:'):
            assert f'assets/zerog_tweaks/textures/{texture.split(":",1)[1]}.png' in names
    source=args.design_root/'docs/zero-g-tweaks-bundle/structures/concord_courier'
    assert jar.read('data/zerog_tweaks/structure/concord_courier.nbt')==(source/'concord_courier.nbt').read_bytes()
    cells=data_from_source=json.loads((source/'cells.json').read_text())
    assert cells['size']==[7,5,7] and len(cells['cells'])==73
    locations={tuple(c['pos']):c['block'] for c in cells['cells']}
    assert locations[3,1,3]=='minecraft:chest' and locations[3,1,1]=='zerog_tweaks:broken_console'
    for name in ['net/zerog/tweaks/lore/ConcordPrologue.class','net/zerog/tweaks/item/ConcordCodexItem.class','net/zerog/tweaks/travel/HubExhibits.class']:
        assert name in names
    vault=data('data/zerog_tweaks/worldgen/structure/concord_vault.json')
    assert vault['min_rooms']==10 and vault['key_rooms']==4
print('PASS Prologue recipe/advancement/icons/lang, 73-cell template identity, latest Vault config, no test-class leakage')
