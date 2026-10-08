"""Download a bounded immutable public source snapshot; never execute it."""
from pathlib import Path
import hashlib
import json
import urllib.request
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
REV = 'd03f956b94ed239f47c936923ae7a4386c3db8e1'
REPO = 'sigstore/sigstore-python'
NAMES = ['LICENSE', 'COPYRIGHT.txt', 'pyproject.toml', 'sigstore/verify/verifier.py',
         'sigstore/verify/policy.py', 'sigstore/models.py', 'sigstore/_cli.py',
         'test/unit/verify/test_policy.py', 'test/unit/verify/test_verifier.py',
         'test/integration/cli/test_verify.py', 'sigstore/dsse/__init__.py', 'sigstore/_utils.py',
         'test/unit/test_dsse.py']

def get(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'local-verifier-boundary-review'})
    return urllib.request.urlopen(request, timeout=40).read()

tree = json.loads(get(f'https://api.github.com/repos/{REPO}/git/trees/{REV}?recursive=1'))
assert not tree.get('truncated')
blobs = {x['path']: x['sha'] for x in tree['tree'] if x['type'] == 'blob'}
record = {'repository': REPO, 'revision': REV, 'utc': datetime.now(timezone.utc).isoformat(), 'files': {}}
for name in NAMES:
    assert name in blobs
    raw = get(f'https://raw.githubusercontent.com/{REPO}/{REV}/{name}')
    actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    assert actual == blobs[name]
    target = ROOT / 'upstream' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        assert target.read_bytes() == raw
    else:
        with target.open('xb') as stream:
            stream.write(raw)
    record['files'][name] = {'git_blob': actual, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
(ROOT / 'source-record.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
