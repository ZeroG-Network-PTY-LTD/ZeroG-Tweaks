"""Record the actual local input digests and authority for this generated stack."""
import csv,hashlib,json,subprocess,zipfile
from pathlib import Path
from build_mob_models import ROOT,write_json

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    source=ROOT/'docs/zero-g-tweaks-bundle/sheets/mobs/data/mob_eye_styles.csv'
    rows=list(csv.DictReader(source.read_text().splitlines()))
    refs=[]
    for name in ('codex-clipboard-a00f6f55-1b30-4799-8a3a-a1f35e36aed9.png',
                 'codex-clipboard-2e1a4ef6-f29a-4cc7-894c-f408a9f9dd32.png',
                 'codex-clipboard-8ce7b9ae-65c2-4c0f-9806-e7a229b7b379.png'):
        p=Path('/mnt/c/Users/jakem/AppData/Local/Temp')/name
        if p.exists():refs.append({'file':name,'sha256':digest(p),'use':'Visual reference only; body retained, repository gameplay unchanged'})
    jar=Path('/mnt/c/Users/jakem/Desktop/ZeroG_Mods/ZeroG_Tweaks/build/moddev/artifacts/neoforge-21.1.252-sources.jar')
    phantom=None
    if jar.exists():
        with zipfile.ZipFile(jar) as z:
            phantom={'source':'Minecraft 1.21.1 PhantomModel.java (local NeoForge mapped sources)',
                     'sha256':hashlib.sha256(z.read('net/minecraft/client/model/PhantomModel.java')).hexdigest(),
                     'transforms':'Y-up conversion and X +0.5 recenter; original scale textures and paired manta gills; original textures/jars not distributed'}
    write_json(ROOT/'docs/zero-g-tweaks-bundle/blockbench/references/art_requirements.json',
        {'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
         'eye_table_sha256':digest(source),'eye_placements':rows,'visual_references':refs,'phantom':phantom,
         'guardian_ids':['prism_sentinel','rift_tyrant','eidolon_captain','dying_star'],
         'guardian_height_blocks':10.8,'guardian_hitbox_blocks':[3.6,10.8],
         'other_bosses':'Authored dimensions retained, per repository and user confirmation',
         'single_eye_body_rule':'One central eye on existing body, not replacement orb mobs',
         'texture_art':'Original local procedural pixel art, discrete five-tone material ramps; no paid provider invoked',
         'native_import_verified':False,'minecraft_runtime_verified':False})
    print('Recorded repository and visual-reference input digests.')

if __name__=='__main__':main()
