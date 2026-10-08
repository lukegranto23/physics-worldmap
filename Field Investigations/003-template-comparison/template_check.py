"""Pin public template sources; test only its reviewed comparison block locally.

--fetch downloads three public files and verifies their Git blob identities.
Default mode is offline and never installs or executes template dependencies.
"""
from pathlib import Path
import difflib
import hashlib
import json
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / '002-dist-verification'))
import reproduce as h

REV = '1fead38ed9c0cc1cee241ecea2e5b3e28772eab6'
REPO = 'actions/javascript-action'
WORKFLOW = '.github/workflows/check-dist.yml'

def fetch():
    def get(url):
        req = urllib.request.Request(url, headers={'User-Agent': 'local-build-comparison-review'})
        return urllib.request.urlopen(req, timeout=40).read()
    tree = json.loads(get(f'https://api.github.com/repos/{REPO}/git/trees/{REV}?recursive=1'))
    assert not tree.get('truncated')
    blobs = {x['path']: x['sha'] for x in tree['tree'] if x['type'] == 'blob'}
    record = {'revision': REV, 'repository': REPO, 'utc': datetime.now(timezone.utc).isoformat(), 'files': {}}
    for name in (WORKFLOW, 'package.json', 'LICENSE'):
        raw = get(f'https://raw.githubusercontent.com/{REPO}/{REV}/{name}')
        actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert actual == blobs[name]
        path = ROOT / 'upstream' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(raw)
        record['files'][name] = {'git_blob': actual, 'sha256': hashlib.sha256(raw).hexdigest()}
    (ROOT / 'source-record.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record, indent=2))

def test():
    record = json.loads((ROOT / 'source-record.json').read_text())
    for name, hashes in record['files'].items():
        assert hashlib.sha256((ROOT / 'upstream' / name).read_bytes()).hexdigest() == hashes['sha256']
    source = (ROOT / 'upstream' / WORKFLOW).read_text()
    old = '          if [ "$(git diff --ignore-space-at-eol --text dist/ | wc -l)" -gt "0" ]; then\n'
    assert source.count(old) == 1
    prefix = ('          git add -- dist/\n'
              '          diff_status=0\n'
              '          git diff --cached --quiet -- dist/ || diff_status=$?\n'
              '          if [ "$diff_status" -gt 1 ]; then\n'
              '            exit "$diff_status"\n'
              '          fi\n')
    fixed = source.replace(old, prefix + '          if [ "$diff_status" -eq 1 ]; then\n')
    fixed = fixed.replace('            git diff --ignore-space-at-eol --text dist/\n',
                          '            git diff --cached -- dist/\n')
    patch = ''.join(difflib.unified_diff(source.splitlines(keepends=True),
        fixed.splitlines(keepends=True), fromfile='a/' + WORKFLOW, tofile='b/' + WORKFLOW))
    (ROOT / 'comparison.patch').write_text(patch, encoding='utf-8', newline='\n')
    fixtures = ROOT / 'fixtures'
    fixtures.mkdir(exist_ok=True)
    lab = Path(tempfile.mkdtemp(prefix='run-', dir=fixtures))
    rows = []
    for case in ('unchanged', 'tracked_edit', 'new_output', 'semantic_whitespace',
                 'staged_edit', 'missing_dist', 'tracked_deletion'):
        repo = lab / case
        (repo / 'dist').mkdir(parents=True)
        path = repo / 'dist/index.js'
        path.write_text('process.stdout.write(JSON.stringify(`left \nright`));\n')
        h.git(repo, 'init', '-q')
        for k, v in [('user.name', 'Local template regression'), ('user.email', 'test@example.invalid'),
                     ('core.autocrlf', 'false'), ('core.hooksPath', '/dev/null'), ('commit.gpgsign', 'false')]:
            h.git(repo, 'config', k, v)
        h.git(repo, 'add', '--', 'dist/')
        h.git(repo, 'commit', '-qm', 'Harmless fixture')
        before = h.run([h.NODE, 'dist/index.js'], repo).stdout
        after = before
        if case == 'tracked_edit' or case == 'staged_edit':
            path.write_text('process.stdout.write("changed");\n')
            if case == 'staged_edit':
                h.git(repo, 'add', '--', 'dist/')
        elif case == 'new_output':
            (repo / 'dist/extra.txt').write_text('new harmless output\n')
        elif case == 'semantic_whitespace':
            path.write_text('process.stdout.write(JSON.stringify(`left  \nright`));\n')
            after = h.run([h.NODE, 'dist/index.js'], repo).stdout
            assert before != after
        elif case == 'missing_dist':
            (repo / 'dist').rename(repo / 'preserved-dist')
        elif case == 'tracked_deletion':
            path.rename(repo / 'preserved-index.js')
        original = h.shell(repo, h.block(source, 'Compare Directories')).returncode
        patched = h.shell(repo, h.block(fixed, 'Compare Directories')).returncode
        expected_old = int(case in ('tracked_edit', 'missing_dist', 'tracked_deletion'))
        assert original == expected_old and patched == int(case != 'unchanged')
        rows.append({'case': case, 'original_exit': original, 'patched_exit': patched,
                     'semantic_before': before if case == 'semantic_whitespace' else None,
                     'semantic_after': after if case == 'semantic_whitespace' else None})
    apply_repo = lab / 'patch-check'
    wf = apply_repo / WORKFLOW
    wf.parent.mkdir(parents=True)
    wf.write_text(source, encoding='utf-8', newline='\n')
    h.git(apply_repo, 'init', '-q')
    h.git(apply_repo, 'apply', '--check', str(ROOT / 'comparison.patch'))
    h.git(apply_repo, 'apply', str(ROOT / 'comparison.patch'))
    assert wf.read_text() == fixed
    result = {'revision': REV, 'utc': datetime.now(timezone.utc).isoformat(), 'cases': rows,
              'patch_applied_exactly': True, 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'patch_sha256': hashlib.sha256((ROOT / 'comparison.patch').read_bytes()).hexdigest(),
              'limitations': ['Comparison block only; no Rollup/project build executed',
                'Template already cleans dist; stale-output finding is not transferred',
                'No external submission, remote exploit, or novelty claim']}
    (ROOT / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    fetch() if '--fetch' in sys.argv else test()
