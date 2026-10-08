"""Package only explicit public-source evidence and our review artifacts."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
names = ['Review Packet.md', 'Maintainer Report.md', 'Finding.md',
         'Clean Build Follow-up.md', 'Upstream Review.md', 'reproduce.py',
         'results.json', 'proposed-fix.patch', 'container_build.py',
         'actual_build_cases.py', 'clean_build_probe.py', 'package_review.py',
         'Impact Assessment.md', 'static_chunk_audit.cjs', 'build-evidence/static-chunk-audit.json',
         'upstream/LICENSE', 'upstream/package.json']
names += ['upstream/.github/workflows/' + n for n in
          ('check-dist.yml', 'rebuild-dist.yml', 'commit-dist.yml')]
for run, files in {
    'run-qryqclvl': ['run.json', 'fetch-and-install.log', 'offline-build.log',
                     'offline-regression.log', 'actual-build-results.json', 'regeneration.log'],
    'clean-f440qmvg': ['execution.log', 'run.json'],
    'clean-gua4skq6': ['run.json', 'clean-results.json', 'overlay-build.log', 'clean-build.log'],
    'clean-iy_fho70': ['run.json', 'clean-results.json', 'overlay-build.log',
                      'clean-build.log', 'repeat-build.log', 'proposed-complete-fix.patch'],
}.items():
    names += [f'build-evidence/{run}/{name}' for name in files]

payload = {n: (ROOT / n).read_bytes() for n in sorted(names)}
manifest = {n: {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
            for n, b in payload.items()}
payload['SHA256SUMS.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
destination = ROOT / 'review-packets'
destination.mkdir(exist_ok=True)
fingerprint = hashlib.sha256(payload['SHA256SUMS.json']).hexdigest()[:16]
archive = destination / f'attest-dist-review-{fingerprint}.zip'
if archive.exists():
    raise SystemExit(f'Packet already exists: {archive}')
with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as out:
    for name, data in payload.items():
        info = zipfile.ZipInfo(name, date_time=(2026, 9, 21, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        out.writestr(info, data)
with zipfile.ZipFile(archive) as verify:
    assert verify.testzip() is None
    assert set(verify.namelist()) == set(payload)
    assert all(verify.read(n) == b for n, b in payload.items())
print(json.dumps({'archive': str(archive), 'files': len(payload),
                  'bytes': archive.stat().st_size,
                  'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                  'roundtrip_verified': True}, indent=2))
