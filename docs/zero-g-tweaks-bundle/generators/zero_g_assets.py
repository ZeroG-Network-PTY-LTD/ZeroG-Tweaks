#!/usr/bin/env python3
"""Local ZeroG asset CLI. Does not impersonate Blockbench's desktop API.

Builds editable .bbmodel projects with embedded textures through the existing
generators. No API account, paid service, global installation or credentials.
"""
import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OUT=ROOT/'docs/zero-g-tweaks-bundle/blockbench'
BLOCKBENCH=Path('/mnt/c/Users/jakem/AppData/Local/Programs/Blockbench/Blockbench.exe')

def run(name,*args):
    print(f'Running {name}',flush=True)
    subprocess.run([sys.executable,str(HERE/name),*args],cwd=ROOT,check=True)

def projects():
    return sorted((OUT/'mobs').glob('*.bbmodel'))+sorted((ROOT/'docs/shattered-skies/blockbench').glob('*.bbmodel'))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor',help='Read-only capability check')
    sub.add_parser('list',help='List existing creature projects')
    for name in ('build','review'):
        s=sub.add_parser(name,help='Rebuild generated assets' if name=='build' else 'Refresh audit reports, previews and HTML')
        s.add_argument('--overwrite',action='store_true',help='Allow replacement of generated output, never authored source specs')
        s.add_argument('--zip',action='store_true',help='Also replace the downloadable ZIP')
    sub.add_parser('validate',help='Read-only per-project UV/bone/animation checks')
    s=sub.add_parser('open',help='Launch one existing project in installed Blockbench')
    s.add_argument('model',help='Stable mob/style id, e.g. tidewraith')
    args=p.parse_args()
    if args.command=='doctor':
        print(json.dumps({'python':sys.executable,'pillow':importlib.util.find_spec('PIL') is not None,
              'numpy':importlib.util.find_spec('numpy') is not None,'blockbench':str(BLOCKBENCH) if BLOCKBENCH.exists() else shutil.which('blockbench'),
              'game_dev':shutil.which('game-dev'),'creature_projects':len(projects()),
              'native_import_verified':False},indent=2));return
    if args.command=='list':
        for f in projects():print(f.stem)
        return
    if args.command=='validate':
        from review_mob_assets import check
        records=[check(f) for f in projects()]
        print(json.dumps({'static_validation':'passed','projects':len(records),'native_import_verified':False}));return
    if args.command=='open':
        found=[f for f in projects() if f.stem==args.model]
        if len(found)!=1:p.error('Choose one existing mob/style id from the list command')
        executable=str(BLOCKBENCH) if BLOCKBENCH.exists() else shutil.which('blockbench')
        if not executable:p.error('Blockbench executable not found')
        path=str(found[0])
        if executable.endswith('.exe') and sys.platform=='linux':path=subprocess.check_output(['wslpath','-w',path],text=True).strip()
        subprocess.Popen([executable,path],cwd=ROOT)
        print('Launch requested; verify the opened model in Blockbench.');return
    if not args.overwrite:p.error('This replaces generated output. Add --overwrite to authorize it.')
    if args.command=='build':
        for script in ('build_mob_models.py','build_shattered_models.py','build_mob_drops_hd.py','build_spawn_egg_accents.py','build_mob_auras.py'):
            run(script)
    for script in ('record_asset_requirements.py','audit_mob_rigs.py','audit_mob_faces.py','test_mob_asset_regressions.py','preview_mob_animation.py'):
        run(script)
    run('review_mob_assets.py',*(() if args.zip else ('--previews-only',)))
    if args.zip:run('verify_current_gallery.py')

if __name__=='__main__':main()
