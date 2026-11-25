"""Replay the approved local research and compare it with committed evidence."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.cache'
REPORTS = ROOT / 'research/reports'
HARYANA = ROOT / 'data/private/zenodo-11392582/replication-package.zip'
GROUPS = ('fictional', 'haryana', 'sierra-leone', 'community', 'us', 'documents')


def compare(actual: Any, expected: Any, label: str) -> None:
    if isinstance(expected, dict) and isinstance(actual, dict) and actual.keys() == expected.keys():
        for key in expected:
            compare(actual[key], expected[key], f'{label}.{key}')
    elif isinstance(expected, list) and isinstance(actual, list) and len(actual) == len(expected):
        for index, (value, reference) in enumerate(zip(actual, expected, strict=True)):
            compare(value, reference, f'{label}[{index}]')
    elif isinstance(expected, float) and isinstance(actual, (int, float)) and not isinstance(actual, bool):
        if not math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-10):
            raise ValueError(f'Numeric reproduction differs at {label}')
    elif type(actual) is not type(expected) or actual != expected:
        raise ValueError(f'Reproduction differs at {label}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('groups', nargs='*', metavar='GROUP', help=', '.join(GROUPS) + ' (default: all)')
    parser.add_argument('--haryana-archive', type=Path, default=HARYANA)
    parser.add_argument('--sierra-cache', type=Path, default=CACHE / 'benchmark')
    parser.add_argument('--us-cache', type=Path, default=CACHE / 'us-evidence')
    parser.add_argument('--document-cache', type=Path, default=CACHE / 'document-holdout-v3')
    args = parser.parse_args()
    groups = args.groups or GROUPS
    if invalid := set(groups).difference(GROUPS):
        parser.error(f'Unknown groups: {", ".join(sorted(invalid))}')
    CACHE.mkdir(exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix='reproduction-', dir=CACHE))
    ledger: dict[str, Any] = {'python': sys.version.split()[0], 'relative_tolerance': 1e-9,
                              'absolute_tolerance': 1e-10, 'stages': {}}
    env = {**os.environ, 'OPENBLAS_NUM_THREADS': '1', 'PYTHONUTF8': '1'}
    print(f'Replay artifacts: {output}', flush=True)

    def run(name: str, command: list[str], *, report_flag: bool = False,
            exclude: tuple[str, ...] = (), document_scores: bool = False, verify_only: bool = False) -> None:
        target = output / f'{name}.json'
        if report_flag:
            command = [*command, '--report', str(target)]
        started = time.perf_counter()
        result = subprocess.run([sys.executable, *command], cwd=ROOT, env=env, check=True,
                                stdout=subprocess.PIPE)
        entry: dict[str, Any] = {'seconds': round(time.perf_counter() - started, 3)}
        if not verify_only:
            if not report_flag:
                target.write_bytes(result.stdout)
            data = target.read_bytes()
            actual = json.loads(data)
            reference = json.loads((REPORTS / target.name).read_bytes())
            if document_scores:
                for key in ('manifest_sha256', 'extractor_sha256', 'trial_count', 'pypdf'):
                    compare(actual[key], reference[key], key)
                for method, scores in actual['scores'].items():
                    stable = [key for key in reference['scores'][method] if not key.endswith('_seconds')]
                    compare({key: scores[key] for key in stable},
                            {key: reference['scores'][method][key] for key in stable}, method)
            else:
                compare({key: value for key, value in actual.items() if key not in exclude},
                        {key: value for key, value in reference.items() if key not in exclude}, name)
            entry.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        ledger['stages'][name] = entry
        (output / 'run.json').write_text(json.dumps(ledger, indent=2) + '\n', encoding='utf-8')
        print(f'{name}: verified in {entry["seconds"]} s', flush=True)

    archive = str(args.haryana_archive.resolve())
    sierra_cache = ['--cache', str(args.sierra_cache.resolve())]
    if 'fictional' in groups:
        run('fictional_validation', ['-m', 'patient_outreach.validate', '--reps', '1500'])
        run('fictional_policy_holdout', ['-m', 'patient_outreach.fictional'])
        run('pilot_validation', ['-m', 'patient_outreach.validate_pilot'])
    if 'haryana' in groups:
        historical = json.loads((REPORTS / 'haryana_empirical.json').read_bytes())
        for field, path in (('code_sha256', 'scripts/evaluate_haryana.py'),
                            ('protocol_sha256', 'research/HARYANA_PROTOCOL.md')):
            original = subprocess.check_output(['git', 'show', f'dad2575:{path}'], cwd=ROOT)
            compare(hashlib.sha256(original).hexdigest(), historical[field], f'historical Haryana {field}')
        run('haryana_figure4_replication', ['scripts/replicate_haryana.py', archive, '--check-reference'],
            exclude=('runtime',))
        run('haryana_empirical', ['scripts/evaluate_haryana.py', archive, '--check-reference'],
            report_flag=True, exclude=('runtime', 'code_sha256', 'protocol_sha256', 'ridge_model_sha256'))
        run('haryana_simulation', ['scripts/validate_haryana.py'])
        run('haryana_projection', ['scripts/export_haryana.py', '--check'], verify_only=True)
    if 'sierra-leone' in groups:
        run('sierra_leone_replication', ['scripts/replicate_sierra_leone.py', *sierra_cache, '--check-reference'])
        run('sierra_leone_policy', ['scripts/evaluate_sierra_leone.py', *sierra_cache],
            report_flag=True, exclude=('runtime',))
        run('sierra_leone_lottery_audit', ['scripts/audit_sierra_leone_lottery.py', *sierra_cache])
        run('sierra_leone_projection', ['scripts/export_sierra_leone.py', '--check'], verify_only=True)
    if 'community' in groups:
        run('community_inference', ['scripts/validate_community_inference.py', '--haryana-archive', archive],
            report_flag=True)
    if 'us' in groups:
        if not all((args.us_cache / name).is_file() for name in ('cms.zip', 'NCT05525494.json')):
            parser.error('US source replay requires both pinned source files in --us-cache')
        run('us_projection', ['scripts/export_us_evidence.py', '--check', '--cache', str(args.us_cache.resolve())],
            verify_only=True)
    if 'documents' in groups:
        run('document_holdout_v3', ['-m', 'patient_outreach.document_evaluation', '--final-cycle', '--holdout',
            '--manifest', 'research/manifests/document_holdout_v3.json', '--cache',
            str(args.document_cache.resolve())], document_scores=True)


if __name__ == '__main__':
    main()
