"""Read-only startup timing/inventory report; never prints authentication arguments.

Compare selected loading stages across plain/gzip logs. A missing completion marker
does not establish a deadlock or identify which mod is responsible.
"""
import argparse, gzip, json, re, tomllib
from pathlib import Path
from zipfile import ZipFile

STAGES={
    'launcher': 'ModLauncher running:',
    'graphics': 'OpenGL Renderer:',
    'shader_selected': 'Using shaderpack:',
    'mod_setup': 'Sending ConfigManager took',
    'registry_setup': 'NeoForge mod loading, version',
    'resources_started': 'Reloading ResourceManager:',
    'sound_ready': 'Sound engine started',
    'block_atlas_ready': 'minecraft:textures/atlas/blocks.png-atlas',
    'world_start': 'Preparing start region for dimension',
    'world_join': 'logged in with entity id',
}

def timing(path):
    opener=gzip.open if path.suffix=='.gz' else open
    stages={}; errors=0; last=None; rollover=0
    with opener(path,'rt',encoding='utf-8',errors='replace') as stream:
        for line in stream:
            match=re.search(r'\[(?:\d{2}\w{3}\d{4} )?(\d\d):(\d\d):(\d\d)(?:\.(\d+))?\]',line)
            if not match: continue
            hh,mm,ss,decimal=match.groups();t=int(hh)*3600+int(mm)*60+int(ss)+float('0.'+(decimal or '0'))
            if last is not None and t+rollover<last-43200: rollover+=86400
            last=t+rollover
            for name,text in STAGES.items():
                if text in line and name not in stages: stages[name]=last
            if re.search(r'Loaded \d+ recipes',line) and 'recipes_ready' not in stages:stages['recipes_ready']=last
            if re.search(r'/(?:ERROR|FATAL)\]',line): errors+=1
    gaps=[]; ordered=sorted(stages.items(),key=lambda v:v[1])
    for (before,start),(after,end) in zip(ordered,ordered[1:]):
        gaps.append({'from':before,'to':after,'seconds':round(end-start,3)})
    return {'file':path.name,'observed_stages':list(stages),'stage_gaps':gaps,
            'error_or_fatal_lines':errors,'reached_block_atlas': 'block_atlas_ready' in stages,
            'diagnosis':'Timing evidence only; obtain live thread samples to attribute stalls.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--instance',required=True,type=Path)
    p.add_argument('--log',action='append',required=True,type=Path);p.add_argument('--report',required=True,type=Path);a=p.parse_args()
    ids={};invalid=[]
    for path in sorted((a.instance/'mods').glob('*.jar')):
        try:
            with ZipFile(path) as jar:
                name=next((n for n in ['META-INF/neoforge.mods.toml','META-INF/mods.toml'] if n in jar.namelist()),None)
                if name:
                    for mod in tomllib.loads(jar.read(name).decode()).get('mods',[]):ids.setdefault(mod['modId'],[]).append(path.name)
        except Exception as exc:invalid.append({'jar':path.name,'error_type':type(exc).__name__})
    settings={}
    for path,allowed in [(a.instance/'options.txt',{'renderDistance','simulationDistance','mipmapLevels'}),
                         (a.instance/'config/iris.properties',{'enableShaders','shaderPack'})]:
        if path.exists():
            for line in path.read_text().splitlines():
                key,_,value=line.replace('=',':',1).partition(':')
                if key in allowed:settings[key]=value
    report={'schema':1,'scope':'Local client startup, no saves modified or client launched',
            'logs':[timing(path) for path in a.log],
            'duplicate_top_level_mod_ids':{k:v for k,v in ids.items() if len(v)>1},
            'invalid_jars':invalid,'settings':settings,'root_cause_confirmed':False}
    a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
