"""Run from WSL: isolated pinned build, no credentials or other host mounts.

Only generated lab files are writable. Download/install has network; build does not.
Does not execute the attestation action, publish, push, or delete user files.
"""
import json
import pathlib
import subprocess
import tempfile
import shutil
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent
REV = 'c5895f04a64254068ee4ce85086baae80a363b9c'
IMAGE = 'node:24.5.0-bookworm'

def main():
    evidence = ROOT / 'build-evidence'
    evidence.mkdir(exist_ok=True)
    output = pathlib.Path(tempfile.mkdtemp(prefix='run-', dir=evidence))
    lab = pathlib.Path(tempfile.mkdtemp(prefix='attest-build-', dir='/var/tmp'))
    for name in ('actual_build_cases.py', 'reproduce.py', 'proposed-fix.patch'):
        shutil.copyfile(ROOT / name, lab / name)
    report = {'started_utc': datetime.now(timezone.utc).isoformat(),
              'revision': REV, 'image_tag': IMAGE, 'lab': str(lab), 'steps': []}

    def invoke(label, args, timeout=900):
        print(label, flush=True)
        with (output / (label + '.log')).open('w') as stream:
            result = subprocess.run(args, stdout=stream, stderr=subprocess.STDOUT,
                                    timeout=timeout)
        report['steps'].append({'name': label, 'exit': result.returncode})
        (output / 'run.json').write_text(json.dumps(report, indent=2) + '\n')
        if result.returncode:
            raise RuntimeError(f'{label} failed; see saved log')

    invoke('image-pull', ['docker', 'pull', IMAGE])
    image = subprocess.check_output(['docker', 'image', 'inspect', IMAGE,
                                    '--format', '{{.Id}}'], text=True).strip()
    report['image_id'] = image
    report['image_digests'] = json.loads(subprocess.check_output(
        ['docker', 'image', 'inspect', IMAGE, '--format', '{{json .RepoDigests}}'], text=True))
    common = ['docker', 'run', '--rm', '--init', '--user', '1000:1000',
              '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges',
              '--pids-limit=256', '--memory=4g', '--cpus=2',
              '--tmpfs', '/tmp:rw,nosuid,nodev,size=512m',
              '--mount', f'type=bind,src={lab},dst=/work', '-w', '/work',
              '-e', 'HOME=/tmp', '-e', 'GIT_CONFIG_NOSYSTEM=1',
              '-e', 'GIT_CONFIG_GLOBAL=/dev/null', '-e', 'GIT_TERMINAL_PROMPT=0']
    # The only mounted host directory is the fresh, empty lab above.
    invoke('fetch-and-install', common + [image, 'sh', '-ec',
        f'git init -q repo && cd repo && '
        f'git -c core.hooksPath=/dev/null fetch --depth=1 https://github.com/actions/attest.git {REV} && '
        f'git -c core.hooksPath=/dev/null checkout --detach FETCH_HEAD && '
        f'test "$(git rev-parse HEAD)" = "{REV}" && '
        'node --version && npm --version && cat .node-version && '
        'sha256sum package-lock.json && npm ci --ignore-scripts --no-audit --no-fund'])
    invoke('offline-build', common + ['--network=none', image, 'sh', '-ec',
        'cd repo && npm run bundle && git status --short && '
        'git diff --stat -- dist/ && find dist -type f -exec sha256sum {} +'])
    invoke('offline-regression', common + ['--network=none', image,
                                         'python3', '/work/actual_build_cases.py'])
    for name in ('actual-build-results.json', 'regeneration.log'):
        shutil.copyfile(lab / 'cases' / name, output / name)
    report['completed_utc'] = datetime.now(timezone.utc).isoformat()
    (output / 'run.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)

if __name__ == '__main__':
    main()
