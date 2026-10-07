"""Publish a verified same-version JAR and compact evidence, without private logs/art.

Run only after install_dev_jar has installed the audited candidate. This does not
modify the Minecraft instance or saves; it updates the separate Docs checkout.
"""
import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar', required=True, type=Path)
    parser.add_argument('--docs', required=True, type=Path)
    parser.add_argument('--installation', required=True, type=Path)
    parser.add_argument('--build-log', required=True, type=Path)
    parser.add_argument('--test-log', required=True, action='append', type=Path)
    parser.add_argument('--asset-report', required=True, action='append', type=Path)
    parser.add_argument('--receipt-name', default='storage-machinery-delivery-2026-10-05.json')
    parser.add_argument('--jar-name', help='Optional same-version archive name; preserves earlier published JAR bytes')
    parser.add_argument('--remaining-file', type=Path, help='Current TODO ledger instead of the historical delivery list')
    parser.add_argument('--red-test-log', type=Path, help='Observed failing regression before the repaired pass')
    parser.add_argument('--hub-installation', type=Path, help='Verified scoped hub migration receipt')
    parser.add_argument('--hub-rebuild', type=Path, help='Verified fresh compact hub export receipt')
    args = parser.parse_args()
    sha = digest(args.jar)
    installation = json.loads(args.installation.read_text())
    assert installation['installed'] and installation['sha256'] == sha
    assert digest(Path(installation['target'])) == sha, 'Installed JAR no longer matches'
    assert 'BUILD SUCCESSFUL' in args.build_log.read_text(errors='replace')
    tests = []
    for path in args.test_log:
        text = path.read_text(errors='replace')
        matches = re.findall(r'All (\d+) required tests passed', text)
        assert matches and 'BUILD SUCCESSFUL' in text, f'Tests did not pass: {path.name}'
        tests.append({'log': path.name, 'sha256': digest(path),
                      'required_passes': int(matches[-1]), 'client_visual_approval': False})
    assets = []
    for path in args.asset_report:
        report = json.loads(path.read_text())
        assert report['error_count'] == 0, f'Asset errors in {path.name}'
        assets.append({'report': path.name, 'sha256': digest(path),
                       'checked': report['checked'], 'errors': 0})
    with ZipFile(args.jar) as jar:
        assert not any('/gametest/' in name for name in jar.namelist())
        metadata = jar.read('META-INF/neoforge.mods.toml').decode()
        manifest = jar.read('META-INF/MANIFEST.MF').decode()
        assert ('version="${file.jarVersion}"' in metadata and
                re.search(r'^Implementation-Version: 1\.0\.12-dev\s*$', manifest, re.M)) or \
               'version="1.0.12-dev"' in metadata, 'Keep the approved same version'
    archive_name=args.jar_name or args.jar.name
    assert Path(archive_name).name==archive_name and archive_name.endswith('.jar')
    assert Path(args.receipt_name).name==args.receipt_name and args.receipt_name.endswith('.json')
    destination = args.docs / 'docs' / 'jars' / archive_name
    assert destination.parent.is_dir(), 'Existing Docs jar directory required'
    shutil.copyfile(args.jar, destination)
    assert digest(destination) == sha
    jars = sorted(destination.parent.glob('*.jar'), key=lambda path: path.name)
    sums = ''.join(f'{digest(path)}  {path.name}\n' for path in jars)
    (destination.parent / 'SHA256SUMS.txt').write_text(sums, encoding='utf-8')
    receipt = {
        'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'version': '1.0.12-dev', 'minecraft': '1.21.1', 'loader': 'NeoForge',
        'jar': archive_name, 'sha256': sha, 'bytes': args.jar.stat().st_size,
        'installed_before_publication': True,
        'old_jar_backup': Path(installation['backup']).name if installation['backup'] else None,
        'backed_up': installation.get('backed_up', []),
        'preserved_dependencies': installation['preserved_dependencies'],
        'save_changes': False, 'world_regeneration': False, 'client_launched': False,
        'tests': tests, 'asset_audits': assets,
        'build': {'log': args.build_log.name, 'sha256': digest(args.build_log), 'clean_production': True},
        'remaining': ['Client visual/gameplay approval', 'Transport family-specific GUI/recovery',
                      'Legacy addon centrifuge dispatch and other machine input contracts',
                      'Advanced alveary biology', 'Dynamic tank-fluid renderer and chest-lid animation'],
        'guide': 'storage-and-machinery-workflow.md', 'todo': 'storage-and-machinery-todo.json',
        'ownership': {'runtime': '1.21.x', 'source_art': 'Design', 'guides_images_jars': 'Docs'},
        'jar_checksums_preserved': len(jars)
    }
    if args.remaining_file:
        ledger=json.loads(args.remaining_file.read_text())
        # Preserve specification, deferred and installed-but-client-pending states too.
        # A selective status whitelist used to silently omit unfinished roadmap items.
        receipt['remaining']=[row['id'] for row in ledger['tasks'] if row['status'] not in {'complete','completed','done','closed'}]
        receipt['todo_sha256']=digest(args.remaining_file)
    if args.hub_installation:
        hub=json.loads(args.hub_installation.read_text())
        assert hub['installed'] and hub['files'], 'Hub installation did not complete'
        receipt['save_changes']=True
        receipt['hub_migration']={'save':Path(hub['save']).name,'backup':Path(hub['backup']).name,
            'files':hub['files'],'scope':'north gate exhibits and six prepared return regions; player data unchanged'}
    if args.hub_rebuild:
        hub=json.loads(args.hub_rebuild.read_text())
        assert hub['installed'] and hub['files'] and not hub['planetary_terrain_copied']
        receipt['save_changes']=True
        receipt['world_regeneration']=True
        receipt['guide']='compact-hub-2026-10-07.md'
        receipt['gate_building_guide']='gate-building-tiers-1.21.1.md'
        receipt['hub_rebuild']={'save':Path(hub['destination']).name,
            'archived_save':Path(hub.get('archived_compact') or hub.get('archived_cardinal')).name if hub.get('archived_compact') or hub.get('archived_cardinal') else None,
            'files':hub['files'],'planetary_generation':'fresh terrain on first visit',
            'forced_chunks_copied':False,'scope':'new compact Overworld hub; unrelated saves untouched'}
    if args.red_test_log:
        red=args.red_test_log.read_text(errors='replace')
        assert 'unused_machine_input_slots_are_not_misleading_inputs failed' in red
        assert 'energy_and_fluid_buffers_recover_old_items_but_refuse_new_storage failed' in red
        receipt['regression_red']={'log':args.red_test_log.name,'sha256':digest(args.red_test_log),
            'observed_failures':['unused legacy machine insertion','non-item transport incidental storage'],
            'centrifuge_dispatch_suspicion_disproved':True}
    target = args.docs / 'docs' / args.receipt_name
    assert not target.exists() or target.name=='storage-machinery-delivery-2026-10-05.json','Use a new receipt name to preserve historical evidence'
    target.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'receipt': str(target), 'jar': archive_name, 'sha256': sha,
                      'tests': sum(row['required_passes'] for row in tests),
                      'checksums': len(jars)}, indent=2))


if __name__ == '__main__':
    main()
