# Cleanup before the locked install has a separate resolution dependency

Tested September 21, 2026; documented September 22. Status: local offline differential test, not a vulnerability finding or external submission.

## Observation

In the pinned template revision `1fead38ed9c0cc1cee241ecea2e5b3e28772eab6`, the workflow runs `npx rimraf ./dist` before `npm ci`. The build script later performs cleanup again before Rollup. `rimraf` is not a direct dependency but appears in the package lock as version 3.0.2. [Pinned workflow](https://github.com/actions/javascript-action/blob/1fead38ed9c0cc1cee241ecea2e5b3e28772eab6/.github/workflows/check-dist.yml), [package configuration](https://github.com/actions/javascript-action/blob/1fead38ed9c0cc1cee241ecea2e5b3e28772eab6/package.json).

Using the recorded Node 24.4.0 / npm 11.4.2 container, a fresh local checkout, an empty npm cache, and no external network:

| State | Same `npx rimraf ./dist` command with npm offline mode | Output directory |
|---|---|---|
| Lockfile present, dependencies not installed | Exit 1, `ENOTCACHED` while looking up the registry's `rimraf` metadata | Remains |
| Locked dependencies made available | Exit 0, local `node_modules/rimraf/bin.js` resolved | Removed |

The lockfile hash remained unchanged. The after-install control reused the already installed dependency tree through a directory symlink; it tests executable resolution, not a new install or Rollup build. The command ran only in a newly created disposable checkout. Its generated `dist/` was copied aside first and remains recoverable in that lab. No user's source tree or other container was cleaned.

## Interpretation

Having a lockfile does not make this pre-install command self-contained. In the tested fresh state, npm needed metadata absent from its cache. npm documents that `exec`/`npx` may install unavailable tools into its cache and use local executables when available. This is documented command behavior, not itself a security vulnerability. [npm exec documentation](https://docs.npmjs.com/cli/v11/commands/npm-exec/).

The test did **not** contact the registry, observe which live version would be selected, install a substituted package, or demonstrate attacker influence. It must not be described as a proven malicious-package execution or bypass of the lockfile installer. Registry/cache availability is distinct from compromise.

## Smallest corrective option

Remove the redundant pre-install cleanup step and retain the package script's existing cleanup after `npm ci`. The earlier real-build tests already showed that the complete package script cleans and rebuilds output without that separate workflow step. This avoids the unnecessary early package lookup. It does not eliminate all dependency or lifecycle-script risk.

The [small cleanup patch](./remove-preinstall-cleanup.patch) applies exactly to the pinned workflow and composes with the earlier comparison patch. The installation step still precedes the bundle step. [Patch checks](./cleanup-patch-results.json) validate application and ordering only, not a hosted workflow run; [check script](./cleanup_patch_check.py).

For longer-term clarity, a tool used directly by project scripts can be declared as a direct locked development dependency instead of relying on a transitive executable. That would require a separate lockfile update and review; none was made here.

## Evidence

- [Recorded offline results](./build-evidence/preinstall-results.json)
- [Reproduction source](./preinstall_probe.py)
- [Prior complete-build evidence](./build-evidence/run-757mhk3u/rollup-results.json)

The probe requires the existing lab mounted as `/work` in its recorded container; it is not a standalone host command. It never enables external networking. All source and configuration changes remain local proposals. No report, issue, pull request, or message has been sent.
