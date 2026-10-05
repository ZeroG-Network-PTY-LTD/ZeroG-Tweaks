"""Normalize existing approved pending machine recipes into registered runtime data.

No art, source balance, registry IDs or saves are changed. Seed ingredients in
crystal growth are reusable; feed and FE are spent. All original output chances,
quantities, catalyst flags, costs and timing values are retained.
"""
import argparse
import json
from pathlib import Path


def counted(value, consumed=True):
    ingredient = {key: value[key] for key in ('item', 'tag') if key in value}
    assert len(ingredient) == 1
    return {'ingredient': ingredient, 'count': value.get('count', 1), 'consumed': consumed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resources', required=True, type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / 'zero-g-tweaks-bundle' / 'pending-data' / 'recipe'
    exported = []
    for family in ('refining', 'alloying', 'crystal_growth', 'salvaging'):
        for path in sorted((source / family).glob('*.json')):
            data = json.loads(path.read_text())
            inputs = ([counted(value) for value in data['ingredients']] if family == 'alloying'
                      else [counted(data['seed'], False), counted(data['feed'])] if family == 'crystal_growth'
                      else [counted(data['ingredient'])])
            outputs = ([{'stack': {key: result[key] for key in ('id', 'count')},
                         'chance': result.get('chance', 1)} for result in data['results']]
                       if 'results' in data else [{'stack': data['result'], 'chance': 1}])
            normalized = {'type': data['type'], 'inputs': inputs, 'outputs': outputs,
                          'energy': data['energy'], 'time': data['time']}
            if 'upgraded_result_count' in data:
                normalized['upgraded_result_count'] = data['upgraded_result_count']
            if 'catalyst' in data:
                normalized['catalyst'] = counted(data['catalyst'], data['catalyst'].get('consumed', True))
            destination = args.resources / 'data' / 'zerog_tweaks' / 'recipe' / family / path.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(json.dumps(normalized, indent=2) + '\n')
            exported.append(str(destination.relative_to(args.resources)))
    print(json.dumps({'activated_recipes': len(exported), 'files': exported}, indent=2))


if __name__ == '__main__':
    main()
