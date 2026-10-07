"""Check shipped machine profiles against the loader's actual slot bounds; not a GPU test."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
loader = (root / 'src/main/java/net/zerog/tweaks/client/MachineGuiProfile.java').read_text()
limit = int(re.search(r'xy\[1\]\+16>(\d+)', loader).group(1))
profiles = json.loads((root / 'src/main/resources/assets/zerog_tweaks/gui/machine_profiles.json').read_text())
opening=(root/'src/main/java/net/zerog/tweaks/client/AlvearyControllerScreen.java').read_text()
if re.search(r'menu\.slots\.size\(\)==profile\.roles\(\)\.size\(\)\+36\)',opening):
    raise AssertionError('Centrifuge/Smelter with appended two card slots fall back to broken addon screens: 7+36+2 != 7+36; 4+36+2 != 4+36')
assert 'LegacyMachineCards.supports(sides.sideMachine())?2:0' in opening, 'Missing verified card-slot allowance'
for name, profile in profiles.items():
    positions, roles = profile['positions'], profile['slots']
    assert len(positions) == len(roles) <= 9, name
    assert 0 <= profile['outputStart'] <= len(roles), name
    for index, (x, y) in enumerate(positions):
        assert 1 <= x and x + 16 <= 255 and 19 <= y and y + 16 <= limit, (name, index, x, y)
        for other_x, other_y in positions[:index]:
            assert x + 16 <= other_x or other_x + 16 <= x or y + 16 <= other_y or other_y + 16 <= y, (name, 'overlapping slots')
for name in ('silk_weaver', 'starmetal_smelter'):
    profile = profiles['aeroapiary:' + name]
    assert not profile['designOnly'] and len(profile['slots']) == 4, name
print(json.dumps({'profiles_checked': len(profiles), 'errors': 0, 'client_render_verified': False}))
