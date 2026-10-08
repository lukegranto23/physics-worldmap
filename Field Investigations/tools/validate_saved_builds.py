"""Read saved lab artifacts and compare against independently recorded hashes."""
from pathlib import Path
import hashlib
import json
import treecheck

ROOT = Path(__file__).resolve().parent
case = ROOT.parent / '002-dist-verification/build-evidence'
metadata = json.loads((case / 'run-qryqclvl/run.json').read_text())
lab = Path(metadata['lab'])
old = lab / 'clean-iy_fho70/preserved-overlay-dist'
clean = lab / 'clean-iy_fho70/checkout/dist'
other_clean = lab / 'clean-gua4skq6/checkout/dist'
oracle = json.loads((case / 'clean-iy_fho70/clean-results.json').read_text())

def digests(root):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir() if p.is_file()}

assert digests(old) == oracle['overlay_hashes']
assert digests(clean) == oracle['clean_hashes']
assert digests(other_clean) == oracle['clean_hashes']
changed = treecheck.compare(old, clean)
equal = treecheck.compare(other_clean, clean)
assert [(d['path'], d['change']) for d in changed['differences']] == [('184.index.js', 'removed')]
assert equal['equal']
assert digests(old) == oracle['overlay_hashes'] and digests(clean) == oracle['clean_hashes']
report = {'changed_build_comparison': changed, 'independent_clean_build_comparison': equal,
          'matched_prior_build_hashes': True, 'source_artifacts_unchanged': True,
          'tool_sha256': hashlib.sha256((ROOT / 'treecheck.py').read_bytes()).hexdigest(),
          'scope': 'Saved actual-build outputs, not a newly executed build or security audit'}
(ROOT / 'saved-build-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
