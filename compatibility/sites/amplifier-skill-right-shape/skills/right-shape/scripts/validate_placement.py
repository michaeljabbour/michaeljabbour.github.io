#!/usr/bin/env python3
"""Compute and validate placement arithmetic from the adjacent canonical rubric.

No gate truth or security claim is inferred. JSON input on stdin or --input.
The site builder imports this same parser and validator.
"""
import argparse
import json
from pathlib import Path
import re
import sys

def section(markdown, heading):
    """Return the body of one '## heading' section."""
    match = re.search(rf'^## {re.escape(heading)}\n(.*?)(?=^## |\Z)', markdown, re.M | re.S)
    if not match:
        raise ValueError(f'Missing section: {heading}')
    return match.group(1)


def table_rows(block):
    rows = [line for line in block.splitlines() if line.startswith('|')]
    return [[cell.strip() for cell in row.strip('|').split('|')] for row in rows[2:]]


def bullets(block):
    return [line[2:].split(' | ') for line in block.splitlines() if line.startswith('- ')]


def read_rubric(rubric, benchmark=None):
    # The site presents the canonical method, never a second copy of it.
    r = {
        'questions': re.findall(r'^\d\. (.+)$', section(rubric, 'Sorting questions'), re.M),
        'shapes': bullets(section(rubric, 'Shapes')),
        'need': bullets(section(rubric, 'Need dimensions')),
        'need_map': table_rows(section(rubric, 'Need to rung')),
        'ladder': bullets(section(rubric, 'Ladder')),
        'gates': table_rows(section(rubric, 'Gates')),
        'checks': bullets(section(rubric, 'Shape checks')),
        'engines': table_rows(section(rubric, 'Engines')),
        'replace': bullets(section(rubric, 'Replaceability')),
        'evals': table_rows(section(rubric, 'Evaluation ladder')),
        'contract': re.search(r'```\n(.*?)```', section(rubric, 'Capability contract'), re.S).group(1),
        'dispositions': table_rows(section(rubric, 'Dispositions')),
        'diagnosis': table_rows(section(rubric, 'Diagnosis')),
    }
    expect = {'questions': (4, None), 'shapes': (6, 2), 'need': (4, 5), 'need_map': (6, 2), 'ladder': (10, 4),
              'gates': (6, 3), 'checks': (4, 2), 'engines': (4, 3), 'replace': (5, 2), 'evals': (5, 3),
              'dispositions': (11, 2), 'diagnosis': (8, 3)}
    if benchmark is not None:
        r['tests'] = table_rows(section(benchmark, 'Tests'))
        expect['tests'] = (12, 3)
    for key, (count, width) in expect.items():
        rows = r[key]
        if len(rows) != count or (width and any(len(row) != width for row in rows)):
            raise ValueError(f'Rubric section {key}: expected {count} rows of {width} fields')
    if [int(row[0]) for row in r['ladder']] != list(range(10)):
        raise ValueError('The ladder must run from rung 0 to rung 9')
    # Need score bands, for example "0 to 1" -> rung 1, must cover 0 to 12 exactly once.
    bands = []
    for span, rung in r['need_map']:
        low, high = (int(x) for x in span.split(' to '))
        bands.append((low, high, int(rung)))
    covered = [s for low, high, _ in bands for s in range(low, high + 1)]
    if covered != list(range(13)):
        raise ValueError('Need-to-rung bands must cover scores 0 to 12 exactly once')
    r['bands'] = bands
    r['caps'] = {row[0].split()[0]: int(row[2]) for row in r['gates']}
    return r


def need_rung(score, bands):
    return next(rung for low, high, rung in bands if low <= score <= high)


def place(example, r):
    """Recompute a fictional placement from the rubric and refuse one that does not follow it."""
    eid = example['id']
    need = example['need']
    if not isinstance(need, list) or len(need) != 4 or any(type(v) is not int or v not in (0, 1, 2, 3) for v in need):
        raise ValueError(f'{eid}: need is four scores from 0 to 3')
    score = sum(need)
    wanted = need_rung(score, r['bands'])
    for field in ('failed', 'checks'):
        values = example[field]
        if not isinstance(values, list) or any(not isinstance(v, str) for v in values) or len(set(values)) != len(values):
            raise ValueError(f'{eid}: {field} must be a list of unique IDs')
    unknown = set(example['failed']) - set(r['caps'])
    if unknown:
        raise ValueError(f'{eid}: unknown gates {sorted(unknown)}')
    ceiling = min([r['caps'][g] for g in example['failed']] or [9])
    expected = min(wanted, ceiling)
    rung = example.get('rung', expected)
    if type(rung) is not int or not 0 <= rung <= 9:
        raise ValueError(f'{eid}: rung must be an integer from 0 to 9')
    for name, actual in [('need_score', score), ('need_rung', wanted), ('ceiling', ceiling)]:
        if name in example and (type(example[name]) is not int or example[name] != actual):
            raise ValueError(f'{eid}: claimed {name} {example[name]} differs from computed {actual}')
    if rung > expected:
        raise ValueError(f'{eid}: rung {rung} is above min(need {wanted}, ceiling {ceiling})')
    if rung < expected and not example.get('tiebreak'):
        raise ValueError(f'{eid}: a rung below {expected} needs a stated tiebreak')
    if (wanted > ceiling) != bool(example.get('honest_move')):
        raise ValueError(f'{eid}: an honest move is required exactly when need exceeds the ceiling')
    check_ids = {row[0].split()[0] for row in r['checks']}
    if not set(example['checks']) <= check_ids:
        raise ValueError(f'{eid}: unknown shape checks')
    shape = 'Outer harness behind an agent interface' if len(example['checks']) >= 2 else 'Single worker'
    if example['engine'] not in {row[0] for row in r['engines']}:
        raise ValueError(f'{eid}: unknown engine')
    return score, wanted, ceiling, shape


def validate(payload, rubric_path=None):
    rubric_path = rubric_path or Path(__file__).resolve().parents[1] / 'references/rubric.md'
    rules = read_rubric(Path(rubric_path).read_text(encoding='utf-8'))
    if not isinstance(payload, dict):
        raise ValueError('Input must be one placement object')
    example = dict(payload)
    example.setdefault('id', 'placement')
    score, wanted, ceiling, composition = place(example, rules)
    return {'valid': True, 'need_score': score, 'need_rung': wanted,
            'ceiling': ceiling, 'maximum_rung': min(wanted, ceiling),
            'placement_rung': example.get('rung', min(wanted, ceiling)),
            'composition': composition,
            'decompose_first': example['checks'] == ['H4'],
            'scope': 'Arithmetic and recognized labels only; gate truth, audience, utility and safety are not established.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='JSON file; otherwise reads stdin')
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text() if args.input else sys.stdin.read())
        result = validate(payload)
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(json.dumps({'valid': False, 'error': str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
