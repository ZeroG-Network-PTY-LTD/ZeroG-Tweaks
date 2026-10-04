"""Verified explicit art overrides, in generator rollout order; read-only."""
import hashlib
import json

def effective_art_sources(design):
    latest = {}
    recovered = design / 'docs/asset-collection-1.21.1/inventory-texture-refresh-v1'
    if (recovered / 'manifest.json').exists():
        for row in json.loads((recovered / 'manifest.json').read_text()).get('files', []):
            data = (recovered / 'resourcepack' / row['path']).read_bytes()
            assert hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
            latest[row['path']] = data
    for folder in ['planet-botany-v2', 'wood-dust-art-v2']:
        base = design / 'docs' / folder
        if not (base / 'manifest.json').exists():
            continue
        for row in json.loads((base / 'manifest.json').read_text())['textures']:
            data = (base / 'source' / row['path']).read_bytes()
            assert hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
            latest['assets/zerog_tweaks/textures/' + row['path']] = data
    rollout = design / 'docs/art-rollout-v3'
    if (rollout / 'manifest.json').exists():
        for row in json.loads((rollout / 'manifest.json').read_text())['files']:
            data = (rollout / 'source' / row['path']).read_bytes()
            assert hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
            latest[row['path']] = data
    single=design/'docs/single-block-machines-v1'
    if (single/'manifest.json').exists():
        for row in json.loads((single/'manifest.json').read_text())['files']:
            data=(single/'source'/row['path']).read_bytes()
            assert hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
            latest[row['path']]=data
    return latest
