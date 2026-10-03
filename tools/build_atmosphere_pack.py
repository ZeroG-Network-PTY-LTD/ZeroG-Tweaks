"""Package original Iris shaders; optional GLSL syntax/link checking, no game launch."""
import argparse, hashlib, itertools, json, re, subprocess, tempfile, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'graphics' / 'zero-g-atmosphere'

def expand(path, stack=()):
    path = path.resolve()
    if path in stack:
        raise ValueError('Recursive shader include')
    text = path.read_text()
    def include(match):
        child = (ROOT / 'shaders' / match[1].lstrip('/')).resolve()
        if not child.is_relative_to((ROOT / 'shaders').resolve()):
            raise ValueError('Include escapes shader root')
        return expand(child, stack + (path,))
    return re.sub(r'^#include "([^"]+)"\s*$', include, text, flags=re.M)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--validator', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Output already exists; use a new version/destination')
    checked = []
    shaders = sorted(p for p in (ROOT / 'shaders').rglob('*.fsh') if p.with_suffix('.vsh').exists())
    with tempfile.TemporaryDirectory(prefix='zerog-glsl-') as tmp:
        for source in shaders:
            vertex = expand(source.with_suffix('.vsh'))
            fragment = expand(source)
            # All shipped sample counts, with atmosphere on/off and cloud toggle.
            for steps, enabled in itertools.product((8,16,24),(0,1)):
                candidate = re.sub(r'#define CLOUD_STEPS \d+', f'#define CLOUD_STEPS {steps}', fragment)
                candidate = re.sub(r'#define CLOUDS_ENABLED \d+', f'#define CLOUDS_ENABLED {enabled}', candidate)
                for stage, text in [('vert',vertex),('frag',candidate)]:
                    target = Path(tmp) / ('composite.' + stage)
                    target.write_text(text)
                if args.validator:
                    result = subprocess.run([str(args.validator),'-l',str(Path(tmp)/'composite.vert'),
                                    str(Path(tmp)/'composite.frag')],capture_output=True,text=True)
                    if result.returncode:
                        raise SystemExit(result.stdout + result.stderr)
                checked.append({'shader':source.relative_to(ROOT).as_posix(), 'steps':steps,
                                'clouds':enabled,'glsl_linked':bool(args.validator)})
    files = sorted(p for p in ROOT.rglob('*') if p.is_file())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for p in files:
            archive.write(p,p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(args.output) as archive:
        assert archive.testzip() is None
        assert 'shaders/composite.fsh' in archive.namelist()
    report = {'pack':str(args.output),'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),
              'files':len(files),'checks':checked,'gpu_tested':False,'enabled_by_default':False}
    args.output.with_suffix('.validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
