"""Check the approved X half-turn in runtime, design and generator displays."""
import argparse
import ast
import json
from pathlib import Path
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--design-root', type=Path, required=True)
parser.add_argument('--jar', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
expected = {
    'thirdperson_righthand': [180, -90, 55],
    'thirdperson_lefthand': [-180, 90, -55],
    'firstperson_righthand': [180, -90, 25],
    'firstperson_lefthand': [-180, 90, -25],
}
generator = args.design_root / 'docs/zero-g-tweaks-bundle/generators/tools3d.py'
tree = ast.parse(generator.read_text())
display = next(ast.literal_eval(node.value) for node in tree.body
               if isinstance(node, ast.Assign) and any(
                   isinstance(target, ast.Name) and target.id == 'DISPLAY'
                   for target in node.targets))
for context, rotation in expected.items():
    assert display[context]['rotation'] == rotation, context
archive = zipfile.ZipFile(args.jar) if args.jar else None
try:
    for tool in ['sword', 'pickaxe', 'axe', 'shovel', 'hoe']:
        name = f'moonsteel_{tool}.json'
        relative = f'assets/zerog_tweaks/models/item/{name}'
        runtime = json.loads((root / 'src/main/resources' / relative).read_text())
        source = json.loads((args.design_root /
            'docs/zero-g-tweaks-bundle/blockbench/tools/moonsteel/models/item' / name).read_text())
        assert runtime == source, f'Runtime/design mismatch: {name}'
        assert runtime['display'] == display, f'Generator mismatch: {name}'
        for context, rotation in expected.items():
            assert runtime['display'][context]['rotation'] == rotation, (name, context)
        if archive:
            assert json.loads(archive.read(relative)) == runtime, f'Stale JAR model: {name}'
finally:
    if archive:
        archive.close()
print('PASS: five Moonsteel tools; mirrored X half-turn; runtime/design/generator/JAR consistency.')
