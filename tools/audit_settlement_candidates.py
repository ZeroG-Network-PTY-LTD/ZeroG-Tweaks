"""Read-only village candidate audit. Never generates chunks or edits a save.

Replicates PlanetSettlementFeature's LegacyRandomSource candidate selection;
reports explored candidate chunks, not a claim that every rejected site is a bug.
No player records, account data or inventory contents are read.
"""
import argparse
import gzip
import json
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'dev'))
import worldscan


def candidate(seed, dimension, rx, rz):
    h = 0
    for c in dimension:
        h = (31*h + ord(c)) & 0xffffffff
    if h >= 1 << 31:
        h -= 1 << 32
    state = (seed ^ (rx*341873128712) ^ (rz*132897987541) ^ h ^ 25214903917) & ((1 << 48)-1)
    def next_int(bound):
        nonlocal state
        while True:
            state = (state*25214903917+11) & ((1 << 48)-1)
            bits = state >> 17
            value = bits % bound
            if bits-value+bound-1 < 1 << 31:
                return value
    return rx*50+16+next_int(18), rz*50+16+next_int(18)


def saved_chunks(folder):
    result = set()
    for path in sorted((folder/'region').glob('r.*.*.mca')):
        _, rx, rz, _ = path.name.split('.')
        with path.open('rb') as stream:
            header = stream.read(4096)
        if len(header) != 4096:
            raise ValueError('Incomplete region header: '+path.name)
        for i in range(1024):
            if struct.unpack_from('>I', header, i*4)[0]:
                result.add((int(rx)*32+i%32, int(rz)*32+i//32))
    return result


def audit(world, dimension):
    if not dimension.replace('_','').isalnum():
        raise ValueError('Expected a simple ZeroG dimension path')
    raw = gzip.decompress((world/'level.dat').read_bytes())
    data = worldscan._read(raw, 3+struct.unpack_from('>H',raw,1)[0], 10)[0]['Data']
    settings = data['WorldGenSettings']
    folder = world/'dimensions/zerog_tweaks'/dimension
    chunks = saved_chunks(folder)
    regions = sorted({(x//50,z//50) for x,z in chunks})
    if len(regions) > 256:
        raise ValueError('Bounded audit supports at most 256 explored candidate regions')
    rows = []
    for rx,rz in regions:
        cx,cz = candidate(settings['seed'], dimension, rx,rz)
        row = {'region':[rx,rz], 'candidate_chunk':[cx,cz], 'candidate_saved':(cx,cz) in chunks}
        if row['candidate_saved']:
            c = worldscan.chunk(str(folder),cx,cz)
            row['status'] = c.get('Status')
            row['settlement_anchors'] = [
                {k:be.get(k) for k in ('x','y','z','residents','speciesResidents')}
                for be in c.get('block_entities',[]) if be.get('id')=='zerog_tweaks:settlement_anchor']
        rows.append(row)
    return {'scope':'Read-only explored village candidates; no terrain rejection cause or global density proof',
            'seed':settings['seed'], 'structures_enabled':settings.get('generate_features'),
            'dimension':'zerog_tweaks:'+dimension, 'saved_chunk_records':len(chunks),
            'candidate_regions':len(rows), 'saved_candidates':sum(r['candidate_saved'] for r in rows),
            'candidates_with_anchor':sum(bool(r.get('settlement_anchors')) for r in rows), 'candidates':rows}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--world', required=True, type=Path)
    p.add_argument('--dimension', required=True)
    p.add_argument('--require-settlement', action='store_true',
                   help='Fail when explored FULL candidate chunks contain no settlement anchor')
    a = p.parse_args()
    result = audit(a.world.resolve(),a.dimension)
    print(json.dumps(result,indent=2))
    if a.require_settlement:
        full = [r for r in result['candidates'] if r.get('status') in ('full','minecraft:full')]
        if not full:
            raise SystemExit('INCONCLUSIVE: no FULL village candidate chunks saved')
        if not any(r.get('settlement_anchors') for r in full):
            raise SystemExit('FAIL: no village anchor at any saved FULL candidate')
