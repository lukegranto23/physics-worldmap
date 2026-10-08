# Template comparison ignores some generated-output changes

September 21, 2026. Status: pinned-source comparison tests plus an isolated actual Rollup build; patch tested on Windows fixtures and Linux build output; not submitted.

## Result

The public `actions/javascript-action` template at revision `1fead38ed9c0cc1cee241ecea2e5b3e28772eab6` uses the same whitespace-suppressing, unstaged Git comparison examined in Case 002. Its actual comparison block accepts a newly generated untracked file and a meaningful trailing-space change in a harmless multiline string fixture. It also ignores an already-staged edit, included only as a robustness control.

This verifies the pattern in a reusable template, not its inheritance by particular downstream projects or the number of affected actions. It is not a remote exploit, a novelty claim, or evidence of a compromised release.

The actual template build now also reproduces the omitted-output case using its generated source map. The original comparison accepts the restored-but-untracked map; the corrected patch detects it. This is a debugging artifact, not evidence of broken action execution.

## Important difference from Case 002

The template already removes `dist/` before building. Its package script also removes `dist/` before invoking Rollup. Therefore the ncc stale-output finding from `actions/attest` must **not** be transferred to this template. The suggested patch changes only the comparison; it preserves the clean-build steps, the missing-directory guard, and permissions. [Pinned workflow](https://github.com/actions/javascript-action/blob/1fead38ed9c0cc1cee241ecea2e5b3e28772eab6/.github/workflows/check-dist.yml), [pinned package configuration](https://github.com/actions/javascript-action/blob/1fead38ed9c0cc1cee241ecea2e5b3e28772eab6/package.json).

## Tests actually run

For the initial fixture tests, three source files were fetched from the immutable revision and their Git blob identities matched the public repository tree. The saved comparison block was reviewed before execution. Only that block ran in those newly created local Git fixtures. The separate isolated build extension below subsequently ran the real template dependencies and build steps.

| Fixture | Original | Patched |
|---|---|---|
| Unchanged output | Accept | Accept |
| Tracked content edit | Reject | Reject |
| New Git-visible output | **Accept** | Reject |
| Meaningful trailing-space change | **Accept** | Reject |
| Already-staged edit | **Accept** | Reject |
| Entire output directory missing | Reject | Reject |
| Tracked output deleted | Reject | Reject |

The whitespace fixture changes the output of our own tiny Node program from `"left \nright"` to `"left  \nright"`. This is a language-semantics control, not evidence that the current Rollup build preserves that exact source spelling. The full-build reproduction below tests an omitted source map, not whitespace behavior.

The patch stages Git-visible changes in `dist/`, compares the index without whitespace suppression, and treats Git errors distinctly from differences. Real `git apply --check` and `git apply` succeeded, and the resulting file matched the tested proposal. It changes the checkout index and does not audit ignored files or Git filters. Existing missing-directory rejection is preserved.

## Evidence and reproduction

### Actual Rollup build

Using the pinned template's Node 24.4.0, npm 11.4.2, and unchanged package lock, the complete `npm run bundle` succeeded in a restricted Debian container with networking disabled. The baseline `dist/index.js` and `dist/index.js.map` hashes matched the checked-in files exactly.

The test preserved the map outside the checkout and omitted it from a disposable local commit. No source, build configuration, package declaration, or lockfile changed. Running the complete bundle command again restored exactly the same two output files. The only output-tree status was `?? dist/index.js.map`.

The original comparison returned success (0). The corrected patch applied with Git on Linux, and the patched comparison returned mismatch (1). After recording the complete generated output in a local fixture commit, the patched comparison correctly returned success (0). Neither the action runtime nor hosted workflow was executed. Omission was deliberate; no naturally occurring dependency-update failure is claimed.

[Build result](./build-evidence/run-757mhk3u/rollup-results.json), [run metadata](./build-evidence/run-757mhk3u/run.json), [baseline log](./build-evidence/run-757mhk3u/baseline-build.log), [regeneration log](./build-evidence/run-757mhk3u/regeneration.log), [installation log](./build-evidence/run-757mhk3u/fetch-install.log), [container runner](./rollup_build.py).

Container isolation: non-root user, no capabilities, no-new-privileges, read-only root, resource limits, and only a fresh task lab mounted. Downloads and `npm ci --ignore-scripts` used network access; compilation and decision tests did not. No credentials, personal folders, or Docker socket were mounted. The template's cleanup command affected only its disposable container checkout.

The first Linux run reproduced the omitted map but rejected the supplied patch because the Windows-generated patch used CRLF line endings. That attempt is retained as a failed validation, not counted as a passing patch test. Patch generation now writes LF explicitly. All seven Windows fixtures were rerun successfully, followed by the successful fresh Linux build test. [Failed attempt](./build-evidence/run-tw_rc7b_/offline-test.log). Current patch SHA-256: `236f781255b77b5af47cbc87c714dd55d7abde406c4e9e6499bb915f0b4f5d1d`.

### Original fixture evidence

- [Source hashes and fetch record](./source-record.json)
- [Recorded results](./results.json)
- [Comparison-only patch](./comparison.patch)
- [Local test script](./template_check.py)
- [Upstream MIT license](./upstream/LICENSE)

Run `python template_check.py` with Python, Git, Bash, and Node available. It uses the shared reviewed helper from sibling `002-dist-verification/reproduce.py`, makes no network requests, and preserves uniquely named fixture directories. `--fetch` is an explicit separate network phase for initially collecting the pinned snapshot; it refuses to overwrite existing source files.

Run `python3 rollup_build.py` from Linux/WSL with Docker for the full build extension. It downloads the pinned source and Node image, installs locked dependencies without lifecycle scripts, and executes tests offline. It creates new lab/evidence directories and does not reuse or reset a user's checkout. It also needs the sibling helper noted above.

GitHub's main-commit API returned this tested revision on September 21. Public issue/PR search for `repo:actions/javascript-action "ignore-space-at-eol"` returned zero results. That limited search cannot exclude differently worded, private, or unindexed reports. No external contact or submission was made.

## Maintainer draft

Separate reproducibility observation: [pre-install cleanup review](./Preinstall%20Cleanup%20Review.md) shows that the redundant `npx rimraf` step before `npm ci` needs uncached registry metadata in a fresh offline checkout, despite the lockfile. The same command resolves locally after dependencies exist. This is documented npm behavior and a cleanup opportunity, not a newly demonstrated security vulnerability.

The generated-output check compares only unstaged tracked changes and ignores end-of-line whitespace. I reproduced false-clean results using the exact pinned workflow block. The actual Rollup build restores an intentionally omitted `dist/index.js.map` with no change to the main bundle, but the original comparison accepts it. The patch stages `dist/` and compares the index without whitespace suppression, preserving existing missing-directory and clean-build guards. Seven fixture cases pass; Linux patch application and complete/incomplete real-build controls pass. The semantic-whitespace example remains a separate language fixture. This is a comparison-correctness report, not a demonstrated security exploit or action runtime failure.
