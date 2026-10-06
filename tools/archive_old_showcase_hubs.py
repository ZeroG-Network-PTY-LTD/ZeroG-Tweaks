"""Recoverably archive the four explicitly approved old hub worlds after new-world verification."""
import argparse
import json
from pathlib import Path
import shutil

NAMES = (
    'ZeroG_Planet_Showcase_1_0_8_Seed0',
    'ZeroG_Planet_Showcase_1_0_9_Seed0',
    'ZeroG_Planet_Showcase_1_0_12_ServicePorts_Seed0',
    'ZeroG_Planet_Showcase_1_0_12_Supplied_Workshop_Seed0',
)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--instance', type=Path, required=True)
    p.add_argument('--new-world', required=True)
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--move', action='store_true')
    a = p.parse_args()
    instance, archive = a.instance.resolve(), a.archive.resolve()
    saves = instance / 'saves'
    assert instance.name == 'ZeroG' and saves.is_dir()
    assert Path(a.new_world).name == a.new_world and a.new_world not in NAMES
    new = saves / a.new_world
    assert (new / 'level.dat').is_file() and (new / 'zerog-export-report.json').is_file()
    report = json.loads((new / 'zerog-export-report.json').read_text())
    assert report.get('exported') and report.get('gates') == 68
    assert not archive.is_relative_to(saves) and archive.parent == instance
    assert not archive.exists(), 'Use a new dedicated archive directory'
    sources = [saves / name for name in NAMES]
    assert all((world / 'level.dat').is_file() for world in sources)
    result = {'new_world': str(new), 'archive': str(archive), 'worlds': list(NAMES), 'moved': False}
    if a.move:
        archive.mkdir()
        moved = []
        try:
            for source in sources:
                target = archive / source.name
                shutil.move(str(source), str(target))
                moved.append((source, target))
            assert all((target / 'level.dat').is_file() for _, target in moved)
        except Exception:
            for source, target in reversed(moved):
                if target.exists() and not source.exists():
                    shutil.move(str(target), str(source))
            raise
        result['moved'] = True
        (archive / 'archive-receipt.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
