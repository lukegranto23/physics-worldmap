"""Container-only offline comparison of npx before/after dependencies exist.

Run inside the previously recorded template lab with no external network.
Only a new disposable checkout's generated dist is removed by its rimraf tool.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import tempfile

ROOT = Path(tempfile.mkdtemp(prefix='preinstall-', dir='/work'))
REPO = ROOT / 'checkout'
REV = '1fead38ed9c0cc1cee241ecea2e5b3e28772eab6'

def command(args, *, env=None):
    return subprocess.run(args, cwd=REPO if REPO.exists() else ROOT,
                          env=env, text=True, capture_output=True, timeout=60)

command(['git','clone','--no-hardlinks','--no-checkout','/work/repo',str(REPO)]).check_returncode()
command(['git','-c','core.hooksPath=/dev/null','checkout','--detach',REV]).check_returncode()
lock_before = hashlib.sha256((REPO / 'package-lock.json').read_bytes()).hexdigest()
package = json.loads((REPO / 'package.json').read_text())
lock = json.loads((REPO / 'package-lock.json').read_text())
locked_rimraf = {k:v['version'] for k,v in lock['packages'].items() if k.endswith('/rimraf')}
assert not (REPO / 'node_modules').exists()
# Preserve the two generated output files before testing cleanup in this new clone.
shutil.copytree(REPO / 'dist', ROOT / 'preserved-dist')
assert (REPO / 'dist').resolve().is_relative_to(ROOT.resolve())

def trial(label):
    env = dict(os.environ, CI='true', npm_config_offline='true',
               npm_config_cache=f'/tmp/{ROOT.name}-{label}', npm_config_update_notifier='false')
    result = command(['npx','rimraf','./dist'], env=env)
    return {'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr,
            'dist_exists_after': (REPO / 'dist').exists()}

before = trial('before')
assert before['exit'] != 0 and before['dist_exists_after']
assert 'ENOTCACHED' in before['stderr']
(REPO / 'node_modules').symlink_to('/work/repo/node_modules', target_is_directory=True)
local_bin = (REPO / 'node_modules/.bin/rimraf').resolve()
assert local_bin.is_relative_to(Path('/work/repo/node_modules').resolve())
after = trial('after')
assert after['exit'] == 0 and not after['dist_exists_after']
assert hashlib.sha256((REPO / 'package-lock.json').read_bytes()).hexdigest() == lock_before
report = {'revision':REV, 'node':command(['node','--version']).stdout.strip(),
    'npm':command(['npm','--version']).stdout.strip(), 'lock_sha256':lock_before,
    'declared_direct_rimraf': any('rimraf' in package.get(k,{}) for k in ('dependencies','devDependencies','optionalDependencies')),
    'locked_rimraf':locked_rimraf,'resolved_local_binary':str(local_bin),
    'before_dependencies':before,'after_dependencies':after,
    'limits':['Offline cache-miss evidence, not observation of live registry version selection',
              'Existing locked dependencies reused via symlink for command resolution only',
              'No malicious package, registry modification, external execution, or exploit']}
(ROOT / 'results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'evidence_path':str(ROOT / 'results.json'),**report},indent=2))
