"""Operate a loopback-only disposable ordinary server; never touches client saves.

prepare copies an already accepted local EULA, not a new acceptance.
command uses RCON without displaying credentials. inspect reads saved natural
structure starts; it is not proof every chest/room or village has generated.
"""
import argparse,gzip,json,secrets,struct,sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('action',choices=['prepare','command','inspect'])
p.add_argument('--run',required=True,type=Path)
p.add_argument('--accepted-eula',type=Path)
p.add_argument('--command')
p.add_argument('--dimension',default='zerog_tweaks:cerulon')
p.add_argument('--chunk-x',type=int)
p.add_argument('--chunk-z',type=int)
p.add_argument('--radius',type=int,default=0)
p.add_argument('--report',type=Path)
p.add_argument('--require-vault-keys',action='store_true',help='Fail unless all four planned natural altars are actually present')
a=p.parse_args();run=a.run.resolve()
assert run.parent==ROOT and run.name.startswith('run-local-ordinary-'), 'Exact isolated project directory required'
if a.action=='prepare':
    assert not run.exists(),'Refuse to overwrite an existing audit world'
    assert a.accepted_eula and 'eula=true' in a.accepted_eula.read_text().splitlines(),'An already accepted local EULA is required'
    run.mkdir()
    (run/'eula.txt').write_bytes(a.accepted_eula.read_bytes())
    (run/'server.properties').write_text('\n'.join([
        'server-ip=127.0.0.1','server-port=25587','enable-rcon=true',
        'rcon.port=25588','rcon.password='+secrets.token_hex(24),
        'broadcast-rcon-to-ops=false','online-mode=true','level-name=world',
        'level-seed=0','generate-structures=true','view-distance=3',
        'simulation-distance=3','spawn-protection=0','max-players=1',
        'sync-chunk-writes=true','initial-enabled-packs=vanilla',
        'motd=Disposable ZeroG structure audit'])+'\n')
    print('Prepared disposable loopback server; no client files copied.')
elif a.action=='command':
    assert a.command
    sys.path.insert(0,str(ROOT/'tools/dev'))
    import rcon
    rcon.SERVER_DIR=str(run)
    r=rcon.Rcon();r.s.settimeout(120)
    try: print(r.cmd(a.command))
    finally:r.s.close()
else:
    assert a.chunk_x is not None and a.chunk_z is not None and a.report
    ns,dim=a.dimension.split(':')
    assert ns=='zerog_tweaks' and '/' not in dim and '..' not in dim
    sys.path.insert(0,str(ROOT/'tools/dev'))
    import worldscan
    raw=gzip.decompress((run/'world/level.dat').read_bytes())
    metadata=worldscan._read(raw,3+struct.unpack_from('>H',raw,1)[0],10)[0]['Data']['WorldGenSettings']
    assert int(metadata['seed'])==0 and metadata['generate_features'],'Wrong seed or structures disabled'
    data=worldscan.chunk(str(run/'world/dimensions'/ns/dim),a.chunk_x,a.chunk_z)
    assert data, 'Target chunk has not been saved'
    starts=data.get('structures',{}).get('starts',{})
    planned_altars=[]
    for start in starts.values():
        for piece in start.get('Children',[]):
            if piece.get('id')!='zerog_tweaks:vault_key_altar':continue
            bb=piece['BB'];x,y,z=bb[0],bb[4],bb[2]
            c=worldscan.chunk(str(run/'world/dimensions'/ns/dim),x>>4,z>>4)
            observed=None;properties={}
            if c:
                for section in c.get('sections',[]):
                    for index,name,yy in worldscan.section_blocks(section):
                        if yy==y and index&15==x&15 and (index>>4)&15==z&15:
                            observed=name
                            states=section['block_states'];palette=states['palette']
                            if len(palette)==1:selected=palette[0]
                            else:
                                bits=max(4,(len(palette)-1).bit_length());per=64//bits
                                selected=palette[((states['data'][index//per]&0xffffffffffffffff)>>((index%per)*bits))&((1<<bits)-1)]
                            properties=selected.get('Properties',{})
            planned_altars.append({'position':[x,y,z],'chunk':[x>>4,z>>4],
                'observed_block':observed,'observed_properties':properties,'references':sorted((c or {}).get('structures',{}).get('References',{}))})
    assert 0<=a.radius<=9,'Bounded saved-chunk inspection only'
    blocks=Counter();loot=Counter();anchors=[];saved=0
    for cx in range(a.chunk_x-a.radius,a.chunk_x+a.radius+1):
        for cz in range(a.chunk_z-a.radius,a.chunk_z+a.radius+1):
            c=worldscan.chunk(str(run/'world/dimensions'/ns/dim),cx,cz)
            if not c or c.get('Status') not in {'minecraft:full','full'}:continue
            saved+=1
            for section in c.get('sections',[]):
                for _,name,_ in worldscan.section_blocks(section):
                    if name in {'zerog_tweaks:vault_key_altar','zerog_tweaks:concord_lock','zerog_tweaks:settlement_anchor','zerog_tweaks:aresite_block'}:blocks[name]+=1
            for be in c.get('block_entities',[]):
                if be.get('LootTable','').startswith('zerog_tweaks:'):loot[be['LootTable']]+=1
                if be.get('id')=='zerog_tweaks:settlement_anchor':anchors.append({k:be.get(k) for k in ['x','y','z','residents','speciesResidents']})
    report={'seed':0,'dimension':a.dimension,'chunk':[a.chunk_x,a.chunk_z],
        'ordinary_server':True,'structure_generation_enabled':bool(metadata['generate_features']),
        'scope':'Saved natural structure starts; not complete room/chest or village coverage',
        'status':data.get('Status'),
        'saved_full_chunks':saved,'observed_blocks':dict(blocks),'unopened_chest_loot_tables':dict(loot),'settlement_anchors':anchors,'planned_key_altars':planned_altars,
        'starts':{key:{'id':value.get('id'),'pieces':len(value.get('Children',[])),
            'piece_types':sorted({piece.get('id','unknown') for piece in value.get('Children',[])})}
            for key,value in starts.items()}}
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
    if a.require_vault_keys:
        assert len(planned_altars)==4 and all(v['observed_block']=='zerog_tweaks:vault_key_altar' and v['observed_properties'].get('has_key')=='true' for v in planned_altars), 'Natural Vault does not supply all four planned key altars'
