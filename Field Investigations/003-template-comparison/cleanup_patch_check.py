"""Generate and apply-check the small cleanup proposal; no workflow execution."""
from pathlib import Path
import difflib
import hashlib
import json
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / '002-dist-verification'))
import reproduce as h

name = '.github/workflows/check-dist.yml'
source = (ROOT / 'upstream' / name).read_text()
block = ('      - name: Remove dist/ Directory\n'
         '        id: remove-dist\n'
         '        run: npx rimraf ./dist\n\n')
assert source.count(block) == 1
changed = source.replace(block, '')
patch = ''.join(difflib.unified_diff(source.splitlines(keepends=True),
    changed.splitlines(keepends=True), fromfile='a/' + name, tofile='b/' + name))
proposal = ROOT / 'remove-preinstall-cleanup.patch'
proposal.write_text(patch, encoding='utf-8', newline='\n')
base = ROOT / 'fixtures'
base.mkdir(exist_ok=True)
lab = Path(tempfile.mkdtemp(prefix='cleanup-proposal-', dir=base))
workflow = lab / name
workflow.parent.mkdir(parents=True)
workflow.write_text(source, encoding='utf-8', newline='\n')
h.git(lab, 'init', '-q')
h.git(lab, 'apply', '--check', str(proposal))
h.git(lab, 'apply', str(proposal))
assert workflow.read_text() == changed
h.git(lab, 'apply', '--check', str(ROOT / 'comparison.patch'))
h.git(lab, 'apply', str(ROOT / 'comparison.patch'))
combined = workflow.read_text()
assert block not in combined
assert 'git diff --cached --quiet -- dist/' in combined
assert combined.index('run: npm ci') < combined.index('run: npm run bundle')
report = {'cleanup_patch_applied_exactly': True, 'comparison_patch_composes': True,
          'install_still_precedes_bundle': True,
          'patch_sha256': hashlib.sha256(proposal.read_bytes()).hexdigest(),
          'limit': 'Patch application and step-order checks only; no hosted workflow execution'}
(ROOT / 'cleanup-patch-results.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
