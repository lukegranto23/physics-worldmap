"""Actual pinned template build, isolated Docker download/build phases.

Run from WSL/Linux. Builds offline; never executes the action or pushes commits.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

REV = '1fead38ed9c0cc1cee241ecea2e5b3e28772eab6'
IMAGE = 'node:24.4.0-bookworm'

def inside():
    import reproduce as h
    repo = Path('/work/repo')
    wf = repo / '.github/workflows/check-dist.yml'
    source = wf.read_text()
    raw = wf.read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == '125ade30c29c9b9e74dd229351765c968ce4ed24'
    def run(*args):
        result = subprocess.run(args, cwd=repo, capture_output=True, text=True, timeout=300)
        if result.returncode:
            Path('/work/last-command-error.txt').write_text(result.stdout + '\n' + result.stderr)
            result.check_returncode()
        return result.stdout
    def hashes():
        return {p.relative_to(repo).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted((repo / 'dist').rglob('*')) if p.is_file()}
    def decision(text):
        answer = h.shell(repo, h.block(text, 'Compare Directories')).returncode
        assert answer in (0, 1)
        return answer
    assert run('git', 'rev-parse', 'HEAD').strip() == REV
    report = {'revision': REV, 'utc': datetime.now(timezone.utc).isoformat(),
              'node': run('node', '--version').strip(), 'npm': run('npm', '--version').strip(),
              'lock_sha256': hashlib.sha256((repo / 'package-lock.json').read_bytes()).hexdigest(),
              'committed_hashes': hashes()}
    Path('/work/baseline-build.log').write_text(run('npm', 'run', 'bundle'))
    report['baseline_hashes'] = hashes()
    report['baseline_status'] = run('git', 'status', '--porcelain', '--', 'dist/')
    Path('/work/baseline-check.json').write_text(json.dumps(report, indent=2) + '\n')
    assert report['committed_hashes'] == report['baseline_hashes']
    assert report['baseline_status'] == '' and decision(source) == 0
    target = 'dist/index.js.map'
    assert target in report['baseline_hashes']
    for key, value in [('user.name','Local template build test'), ('user.email','test@example.invalid'),
                       ('core.hooksPath','/dev/null'), ('commit.gpgsign','false')]:
        run('git', 'config', key, value)
    run('git', 'update-index', '--force-remove', '--', target)
    (repo / target).rename('/work/preserved-index.js.map')
    run('git', 'commit', '-m', 'Local fixture only: omit generated source map')
    Path('/work/regeneration.log').write_text(run('npm', 'run', 'bundle'))
    report['regenerated_hashes'] = hashes()
    report['status_after_rebuild'] = run('git', 'status', '--porcelain', '--', 'dist/')
    assert report['regenerated_hashes'] == report['baseline_hashes']
    assert report['status_after_rebuild'].strip() == '?? dist/index.js.map'
    report['original_exit'] = decision(source)
    assert report['original_exit'] == 0
    run('git', 'apply', '--check', '/work/comparison.patch')
    run('git', 'apply', '/work/comparison.patch')
    report['patched_exit'] = decision(wf.read_text())
    assert report['patched_exit'] == 1
    run('git', 'commit', '-m', 'Local fixture only: record regenerated source map')
    report['patched_unchanged_exit'] = decision(wf.read_text())
    assert report['patched_unchanged_exit'] == 0
    report['source_delta'] = run('git', 'diff', REV, '--', 'src/', 'package.json', 'package-lock.json', 'rollup.config.js')
    assert report['source_delta'] == ''
    report['patch_sha256'] = hashlib.sha256(Path('/work/comparison.patch').read_bytes()).hexdigest()
    report['limits'] = ['Deliberately omitted map, not a naturally occurring update',
        'Source map affects debugging; no action runtime failure demonstrated',
        'No action runtime, hosted workflow, or external submission']
    Path('/work/rollup-results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))

def outside():
    root = Path(__file__).resolve().parent
    evidence = root / 'build-evidence'
    evidence.mkdir(exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix='run-', dir=evidence))
    lab = Path(tempfile.mkdtemp(prefix='template-build-', dir='/var/tmp'))
    shutil.copyfile(__file__, lab / 'rollup_build.py')
    shutil.copyfile(root.parent / '002-dist-verification/reproduce.py', lab / 'reproduce.py')
    shutil.copyfile(root / 'comparison.patch', lab / 'comparison.patch')
    report = {'utc': datetime.now(timezone.utc).isoformat(), 'lab': str(lab), 'revision': REV,
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'steps': []}
    def invoke(label, args):
        print(label, flush=True)
        with (output / (label + '.log')).open('w') as stream:
            result = subprocess.run(args, stdout=stream, stderr=subprocess.STDOUT, timeout=900)
        report['steps'].append({'name': label, 'exit': result.returncode})
        (output / 'run.json').write_text(json.dumps(report, indent=2) + '\n')
        if result.returncode:
            raise RuntimeError(f'{label} failed; see {output}')
    invoke('image-pull', ['docker', 'pull', IMAGE])
    report['image_id'] = subprocess.check_output(['docker','image','inspect',IMAGE,'--format','{{.Id}}'], text=True).strip()
    common = ['docker','run','--rm','--init','--user','1000:1000','--read-only','--cap-drop=ALL',
        '--security-opt=no-new-privileges','--pids-limit=256','--memory=4g','--cpus=2',
        '--tmpfs','/tmp:rw,nosuid,nodev,size=512m','--mount',f'type=bind,src={lab},dst=/work',
        '-w','/work','-e','HOME=/tmp','-e','GIT_CONFIG_NOSYSTEM=1','-e','GIT_CONFIG_GLOBAL=/dev/null',
        '-e','GIT_TERMINAL_PROMPT=0']
    invoke('fetch-install', common + [report['image_id'],'sh','-ec',
        'git init -q repo && cd repo && '
        f'git -c core.hooksPath=/dev/null fetch --depth=1 https://github.com/actions/javascript-action.git {REV} && '
        'git -c core.hooksPath=/dev/null checkout --detach FETCH_HEAD && '
        'npm ci --ignore-scripts --no-audit --no-fund'])
    invoke('offline-test', common + ['--network=none',report['image_id'],'python3','/work/rollup_build.py','--inside'])
    for name in ('rollup-results.json','baseline-build.log','regeneration.log','baseline-check.json'):
        shutil.copyfile(lab / name, output / name)
    print(json.dumps({'evidence': str(output), **report}, indent=2))

if __name__ == '__main__':
    inside() if '--inside' in sys.argv else outside()
