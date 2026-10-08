"""Container-only experiments on the disposable pinned upstream checkout."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
from datetime import datetime, timezone
import reproduce as harness

REPO = Path('/work/repo')
OUT = Path('/work/cases')
OUT.mkdir(exist_ok=False)

def run(*args):
    return subprocess.run(args, cwd=REPO, check=True, text=True,
                          capture_output=True, timeout=300).stdout

def hashes():
    return {p.relative_to(REPO).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((REPO / 'dist').rglob('*')) if p.is_file()}

paths = {'check': '.github/workflows/check-dist.yml',
         'producer': '.github/workflows/rebuild-dist.yml',
         'consumer': '.github/workflows/commit-dist.yml'}
source = {name: (REPO / name).read_text() for name in harness.BLOBS}
for name, expected in harness.BLOBS.items():
    raw = (REPO / name).read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == expected
fixed = harness.revised_sources(source)
assert run('git', 'rev-parse', 'HEAD').strip() == harness.REVISION
assert not run('git', 'status', '--porcelain', '--', 'dist/')

def decisions(mapping, label):
    check = harness.shell(REPO, harness.block(mapping[paths['check']], 'Compare Directories'))
    producer = harness.shell(REPO, harness.block(mapping[paths['producer']], 'Detect dist/ changes'),
                             output_name=label + '-output.txt')
    consumer = harness.shell(REPO, harness.consumer_decision(mapping[paths['consumer']]))
    assert check.returncode in (0, 1)
    assert producer.returncode == consumer.returncode == 0
    return [check.returncode == 1,
            'changed=true' in (REPO / (label + '-output.txt')).read_text(),
            'WOULD_COMMIT' in consumer.stdout]

report = {'time_utc': datetime.now(timezone.utc).isoformat(), 'revision': harness.REVISION,
          'node': run('node', '--version').strip(), 'git': run('git', '--version').strip(),
          'baseline_hashes': hashes(), 'baseline_original': decisions(source, 'baseline'),
          'baseline_patched': decisions(fixed, 'baseline-patched')}
assert report['baseline_original'] == report['baseline_patched'] == [False] * 3

# Preserve the generated file outside dist rather than deleting it. Change only
# this disposable checkout's local index/commit, simulating an omitted output.
target = 'dist/606.index.js'
assert target in report['baseline_hashes']
run('git', 'config', 'user.name', 'Local build regression')
run('git', 'config', 'user.email', 'regression@example.invalid')
run('git', 'config', 'core.hooksPath', '/dev/null')
run('git', 'config', 'commit.gpgsign', 'false')
run('git', 'update-index', '--force-remove', '--', target)
(REPO / target).rename(OUT / '606.index.js.saved')
run('git', 'commit', '-m', 'Local fixture only: omit generated chunk')
assert not run('git', 'status', '--porcelain', '--', 'dist/')
build = run('npm', 'run', 'bundle')
(OUT / 'regeneration.log').write_text(build)
report['regenerated_hashes'] = hashes()
report['status_after_rebuild'] = run('git', 'status', '--porcelain', '--', 'dist/')
report['tracked_diff_after_rebuild'] = run('git', 'diff', '--stat', '--', 'dist/')
assert report['baseline_hashes'] == report['regenerated_hashes']
assert report['status_after_rebuild'].strip() == '?? dist/606.index.js'
report['missing_chunk_original'] = decisions(source, 'missing-original')
assert report['missing_chunk_original'] == [False] * 3
run('git', 'apply', '--check', '/work/proposed-fix.patch')
run('git', 'apply', '/work/proposed-fix.patch')
applied = {name: (REPO / name).read_text() for name in source}
assert applied == fixed
report['missing_chunk_patched'] = decisions(applied, 'missing-patched')
assert report['missing_chunk_patched'] == [True] * 3
report['patch_applied_exactly'] = True
report['source_delta'] = run('git', 'diff', harness.REVISION, '--', 'src/', 'package.json', 'package-lock.json')
assert report['source_delta'] == ''
report['limits'] = ['Intentional omitted-output fixture, not naturally occurring dependency update',
                    'Compiled the real project; did not execute the attestation action',
                    'Executed comparison blocks only, never commit/push workflow steps',
                    'No remote exploit, hosted CI run, or external submission']
(OUT / 'actual-build-results.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
