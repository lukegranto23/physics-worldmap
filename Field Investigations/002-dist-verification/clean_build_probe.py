"""Check whether rebuilding atop committed dist masks stale compiler outputs.

Run under WSL after container_build.py. Reuses its credentials-free lab and
image ID, compiles offline, preserves original files, and never pushes.
"""
from pathlib import Path
import hashlib
import difflib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

REV = 'c5895f04a64254068ee4ce85086baae80a363b9c'

def inside(folder):
    sys.path.insert(0, '/work')
    import reproduce as h
    root = Path(folder)
    root.mkdir()
    repo = root / 'checkout'
    def run(*args, cwd=None):
        return subprocess.run(args, cwd=cwd or repo, text=True, capture_output=True,
                              check=True, timeout=300).stdout
    run('git', 'clone', '--no-hardlinks', '--no-checkout', '/work/repo', str(repo), cwd=root)
    run('git', '-c', 'core.hooksPath=/dev/null', 'checkout', '--detach', REV)
    # Preserve the normal project-relative dependency layout. A directory symlink
    # changed the emitted chunks in the first probe and failed its baseline.
    shutil.copytree('/work/repo/node_modules', repo / 'node_modules', symlinks=True)
    source = {name: (repo / name).read_text() for name in h.BLOBS}
    for name, expected in h.BLOBS.items():
        raw = (repo / name).read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == expected
    fixed = h.revised_sources(source)
    complete = dict(fixed)
    for name in ('.github/workflows/check-dist.yml', '.github/workflows/rebuild-dist.yml'):
        old = '        run: npm run bundle\n'
        assert complete[name].count(old) == 1
        complete[name] = complete[name].replace(old,
            '        run: |\n'
            '          previous_dist="$(mktemp -d)"\n'
            '          if [ -e dist ] || [ -L dist ]; then\n'
            '            mv -- dist "$previous_dist/dist"\n'
            '          fi\n'
            '          npm run bundle\n')
    patch = ''.join(''.join(difflib.unified_diff(source[n].splitlines(keepends=True),
        complete[n].splitlines(keepends=True), fromfile='a/' + n, tofile='b/' + n))
        for n in sorted(source) if source[n] != complete[n])
    patch_path = root / 'proposed-complete-fix.patch'
    patch_path.write_text(patch)
    def hashes():
        return {p.relative_to(repo / 'dist').as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted((repo / 'dist').rglob('*')) if p.is_file()}
    def decisions(mapping, label):
        check = h.shell(repo, h.block(mapping['.github/workflows/check-dist.yml'], 'Compare Directories'))
        prod = h.shell(repo, h.block(mapping['.github/workflows/rebuild-dist.yml'], 'Detect dist/ changes'),
                       output_name=label + '.txt')
        consume = h.shell(repo, h.consumer_decision(mapping['.github/workflows/commit-dist.yml']))
        assert check.returncode in (0, 1) and prod.returncode == consume.returncode == 0
        return [check.returncode == 1, 'changed=true' in (repo / (label + '.txt')).read_text(),
                'WOULD_COMMIT' in consume.stdout]
    report = {'utc': datetime.now(timezone.utc).isoformat(), 'revision': REV,
              'committed_hashes': hashes()}
    (root / 'overlay-build.log').write_text(run('npm', 'run', 'bundle'))
    report['overlay_hashes'] = hashes()
    report['overlay_status'] = run('git', 'status', '--porcelain', '--', 'dist/')
    report['overlay_original'] = decisions(source, 'overlay-original')
    report['overlay_patched'] = decisions(fixed, 'overlay-patched')
    (root / 'baseline-check.json').write_text(json.dumps(report, indent=2) + '\n')
    assert report['committed_hashes'] == report['overlay_hashes']
    assert report['overlay_original'] == report['overlay_patched'] == [False] * 3
    # Preserve evidence, then execute the patched build block itself.
    shutil.copytree(repo / 'dist', root / 'preserved-overlay-dist')
    run('git', 'apply', '--check', str(patch_path))
    run('git', 'apply', str(patch_path))
    assert all((repo / n).read_text() == complete[n] for n in source)
    checker_build = h.block(complete['.github/workflows/check-dist.yml'], 'Build dist/ Directory')
    producer_build = h.block(complete['.github/workflows/rebuild-dist.yml'], 'Build dist/ Directory')
    assert checker_build == producer_build
    (root / 'clean-build.log').write_text(run('bash', '-e', '-o', 'pipefail', '-c', checker_build))
    report['clean_hashes'] = hashes()
    report['absent_in_clean'] = sorted(set(report['overlay_hashes']) - set(report['clean_hashes']))
    report['added_in_clean'] = sorted(set(report['clean_hashes']) - set(report['overlay_hashes']))
    report['changed_shared_files'] = sorted(k for k in report['clean_hashes']
        if k in report['overlay_hashes'] and report['clean_hashes'][k] != report['overlay_hashes'][k])
    report['clean_status_before_staging'] = run('git', 'status', '--porcelain', '--', 'dist/')
    report['clean_original'] = decisions(source, 'clean-original')
    report['clean_patched'] = decisions(fixed, 'clean-patched')
    assert report['absent_in_clean'] == ['184.index.js']
    assert not report['added_in_clean'] and not report['changed_shared_files']
    assert report['clean_original'] == report['clean_patched'] == [True] * 3
    run('git', 'config', 'user.name', 'Local clean-build regression')
    run('git', 'config', 'user.email', 'regression@example.invalid')
    run('git', 'config', 'core.hooksPath', '/dev/null')
    run('git', 'config', 'commit.gpgsign', 'false')
    run('git', 'commit', '-m', 'Local fixture only: record clean generated output')
    (root / 'repeat-build.log').write_text(run('bash', '-e', '-o', 'pipefail', '-c', producer_build))
    report['repeat_hashes'] = hashes()
    report['repeat_complete_patch'] = decisions(complete, 'repeat-complete')
    assert report['repeat_hashes'] == report['clean_hashes']
    assert report['repeat_complete_patch'] == [False] * 3
    report['complete_patch_applied_exactly'] = True
    report['complete_patch_sha256'] = hashlib.sha256(patch_path.read_bytes()).hexdigest()
    report['source_delta'] = run('git', 'diff', REV, '--', 'src/', 'package.json', 'package-lock.json')
    assert not report['source_delta']
    report['limits'] = ['No action runtime, hosted workflow, remote exploit, or publication',
                        'Stale output presence alone does not establish reachability or execution']
    (root / 'clean-results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))

def outside(metadata):
    root = Path(__file__).resolve().parent
    prior = json.loads(Path(metadata).read_text())
    lab = Path(prior['lab']).resolve()
    assert lab.parent == Path('/var/tmp') and lab.name.startswith('attest-build-')
    assert (lab / 'repo/node_modules').is_dir()
    output = Path(tempfile.mkdtemp(prefix='clean-', dir=root / 'build-evidence'))
    script = lab / (output.name + '.py')
    assert not script.exists()
    shutil.copyfile(__file__, script)
    target = '/work/' + output.name
    command = ['docker', 'run', '--rm', '--init', '--network=none', '--user', '1000:1000',
        '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges',
        '--pids-limit=256', '--memory=4g', '--cpus=2',
        '--tmpfs', '/tmp:rw,nosuid,nodev,size=512m',
        '--mount', f'type=bind,src={lab},dst=/work', '-w', '/work', '-e', 'HOME=/tmp',
        '-e', 'GIT_CONFIG_NOSYSTEM=1', '-e', 'GIT_CONFIG_GLOBAL=/dev/null',
        '-e', 'GIT_TERMINAL_PROMPT=0', prior['image_id'], 'python3',
        '/work/' + script.name, '--inside', target]
    print(f'Offline clean-build comparison: {output}', flush=True)
    with (output / 'execution.log').open('w') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, timeout=750)
    (output / 'run.json').write_text(json.dumps({'exit': result.returncode,
        'image_id': prior['image_id'], 'prior_metadata': str(Path(metadata).resolve()),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}, indent=2) + '\n')
    if result.returncode:
        raise RuntimeError(f'Probe failed: see {output}/execution.log')
    for name in ('clean-results.json', 'overlay-build.log', 'clean-build.log',
                 'repeat-build.log', 'proposed-complete-fix.patch'):
        shutil.copyfile(lab / output.name / name, output / name)
    print((output / 'clean-results.json').read_text())

if __name__ == '__main__':
    if sys.argv[1] == '--inside':
        inside(sys.argv[2])
    else:
        outside(sys.argv[1])
