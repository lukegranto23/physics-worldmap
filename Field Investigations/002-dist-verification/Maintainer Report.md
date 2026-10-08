# Dist comparison misses untracked outputs and semantic trailing-whitespace changes

I reproduced a generated-artifact comparison issue in `actions/attest` at commit `c5895f04a64254068ee4ce85086baae80a363b9c`.

`check-dist.yml` and `rebuild-dist.yml` use `git diff --ignore-space-at-eol --text dist/`. This misses untracked additions and suppresses trailing-whitespace changes. `commit-dist.yml` checks `git diff --quiet -- dist/` before `git add`, so it also misses additions-only updates.

Real-build reproduction (September 20):

1. Fetch the pinned revision and run `npm ci --ignore-scripts`, then `npm run bundle`, using its specified Node 24.5.0. The baseline output matches the checked-in tree.
2. In a disposable local commit, omit `dist/606.index.js`, preserving it elsewhere. Change no source or dependencies.
3. Run `npm run bundle` again. The compiler restores `606.index.js`; all output hashes match the baseline. Git reports only `?? dist/606.index.js` under `dist/`.
4. All three original decision blocks report no change. Apply the attached patch: all three detect the regenerated file. Both original and patched checks accept the unchanged baseline.

This ran in a credential-free Docker container, with compilation and comparison tests disconnected from the network. Image digest, lockfile hash, logs, and result JSON are recorded. No action runtime or commit/push workflow steps were executed. Installation emitted transitive engine warnings, but both builds succeeded using the pinned Node version.

Two additional small reproductions:

1. Start with a committed `dist/index.js`, leave it unchanged, and create `dist/new-asset.txt`. All three original predicates report no changes.
2. In a committed JavaScript template literal containing an embedded newline, add a trailing space before that newline. Node produces a different string, but the comparison in `check-dist.yml` and `rebuild-dist.yml` reports no changes.

The attached original local harness executes the actual reviewed detection blocks, not a reimplementation of their logic. That harness does not install dependencies or build upstream; the separate container runner performs the real-build reproduction above. Seven small fixtures cover unchanged output, normal edits, additions, deletion, nested additions, meaningful whitespace, and staged changes.

The proposed patch stages `dist/` first and compares the cached diff without whitespace suppression, with explicit handling of Git errors. All fixtures behave as expected after the change, and the patch applies to the pinned revision. Existing origin/actor/revision and permission guards are unchanged.

I am reporting an incomplete comparison, not a bypass of the recent workflow-origin fix or a demonstrated malicious release. The build reproduction intentionally omits an output; it does not establish a naturally occurring dependency update with additions-only output. The semantic-whitespace example remains a separate language fixture, not a project-build result. The staging approach should be reviewed for compatibility with your preferred workflow policy and Git ignore/filter settings; it does not guarantee clean-build equivalence.

Available attachments: source-hashed reproduction, original fixture results, isolated real-build runner/cases/logs/results, and a three-workflow patch. Original fixture platform: Windows Git Bash, Git 2.53.0, Node 24.11.1, Python 3.14.3. Real-build platform: Debian Bookworm container on WSL, Node 24.5.0, npm 11.5.1, ncc 0.45.0.

Additional clean-build observation (September 21): the pinned checkout retains `dist/184.index.js` when rebuilt normally, but the same build starting without the old output directory does not emit that file. All five shared files are byte-identical. Both original and comparison-only patched checks accept the overlay build and detect the deletion after the clean build. This is stale output retention, not evidence of runtime exploitation. A complete fresh-build check also needs an empty output directory before compilation. Separate logs and hashes are in `Clean Build Follow-up.md`.

An optional broader patch now adds clean output preparation in both build jobs. It applied to the pinned files; its actual build blocks exposed the stale deletion and then produced an identical repeat build that passed all three comparisons. Logs, hashes, and the patch are linked from the follow-up. This does not execute or validate the full hosted workflow.

Impact refinement: static parsing found seven direct chunk-loader calls, requesting only chunks 606 and 50, not stale chunk 184. The stale chunk matches chunk 606 exactly after normalizing its three bundler identity fields. This supports treating the retained file as duplicate leftover output, not claiming that old vulnerable code executes. It does not prove general unreachability; the audit excludes alias/eval behavior and runtime execution. Details and hashes are in `Impact Assessment.md`.

**Draft only. Not submitted.**
