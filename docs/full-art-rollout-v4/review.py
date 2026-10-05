"""Revalidate an existing rollout and refresh paginated proof without repainting."""
import ast, json, runpy
from pathlib import Path
from PIL import Image, ImageDraw
base=Path(__file__).resolve().parent
manifest=json.loads((base/'manifest.json').read_text())
ns=runpy.run_path(str(base/'generate.py'),run_name='asset_review')
ns['ROWS'].extend(manifest['files'])
ns['REUSED'].extend(manifest['reused_native_sources'])
ns['MODEL_ROWS'].extend(manifest['models'])
for row in manifest['files']:
    image=Image.open(base/'source'/row['path']).convert('RGBA')
    key=row['path'].split('/textures/')[1].removesuffix('.png')
    ns['TILES'].append((key,image.crop((0,0,image.width,min(image.width,image.height)))))
ns['validate_and_report']()
# Source generator and runtime material cells must agree after future reruns.
toolsource=base.parent/'zero-g-tweaks-bundle/generators/tools3d.py'
tree=ast.parse(toolsource.read_text())
tools={'Image':Image,'ImageDraw':ImageDraw}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='swatch'],type_ignores=[]),str(toolsource),'exec'),tools)
names=['light','mid','dark','edge','grip','wrap','glow','gem','plate','trim','socket','core']
expected=Image.new('RGBA',(64,64))
for i,name in enumerate(names):expected.paste(tools['swatch'](name,None),((i%4)*16,(i//4)*16))
actual=Image.open(ns['TEXTURES']/'item/3d/moonsteel_tools.png').convert('RGBA')
assert actual.tobytes()==expected.tobytes(),'Moonsteel atlas/source mismatch'
display=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DISPLAY' for t in n.targets))
for kind in ['sword','pickaxe','axe','shovel','hoe']:
    model=json.loads((ns['RES']/f'assets/zerog_tweaks/models/item/moonsteel_{kind}.json').read_text())
    for hand in ['firstperson_righthand','firstperson_lefthand','thirdperson_righthand','thirdperson_lefthand']:
        assert model['display'][hand]==display[hand],f'Moonsteel display/source mismatch: {kind}/{hand}'
print('Moonsteel atlas and all twenty handheld display entries match the generator.')
