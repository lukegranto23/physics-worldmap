# Reproduced: generated-dist checks silently miss real changes

Date: September 18, 2026; real-build validation September 20. Status: **isolated upstream build reproduction with a tested patch; not submitted upstream**.

## Result

September 21 follow-up: [clean-build testing](./Clean%20Build%20Follow-up.md) confirms a second, independent gap: the normal build retains `184.index.js`, which a clean build does not produce. The original comparison-only patch does not fix output preparation. See the follow-up before treating it as a complete fresh-build consistency fix.

Three pinned `actions/attest` workflow predicates miss newly created, Git-visible files under `dist/`. The project's actual compiler regenerated an intentionally omitted JavaScript chunk, and all three predicates reported no change. Two also ignore changes consisting only of end-of-line whitespace. A separate harmless JavaScript template-literal fixture demonstrates that such whitespace can change program output while those checks report no change.

This is a concrete correctness gap in generated-artifact verification. It is **not** a demonstrated remote exploit, an attestation forgery, a bypass of the recently repaired repository-origin guard, or evidence that a published version is compromised. The real-build test intentionally omits an output from a local commit; it does not demonstrate a naturally occurring dependency update that produces only new files.

## Exact code examined

Repository revision: `c5895f04a64254068ee4ce85086baae80a363b9c`, resolved from the public `main` reference during this investigation.

- [check-dist.yml, comparison at line 55](https://github.com/actions/attest/blob/c5895f04a64254068ee4ce85086baae80a363b9c/.github/workflows/check-dist.yml#L55)
- [rebuild-dist.yml, detection at line 65](https://github.com/actions/attest/blob/c5895f04a64254068ee4ce85086baae80a363b9c/.github/workflows/rebuild-dist.yml#L65)
- [commit-dist.yml, early-exit check at line 104](https://github.com/actions/attest/blob/c5895f04a64254068ee4ce85086baae80a363b9c/.github/workflows/commit-dist.yml#L104)

The first two determine changes from `git diff --ignore-space-at-eol --text dist/`. The consumer checks `git diff --quiet -- dist/` **before** staging files. Ordinary unstaged diff does not include new untracked files or already-staged changes; the explicit whitespace option additionally suppresses end-of-line whitespace differences. [Git's diff documentation](https://git-scm.com/docs/git-diff).

The saved five-file source snapshot includes upstream MIT licensing. Each file's Git blob hash is checked against the pinned repository tree before tests execute. The original fixture tests installed nothing; the September 20 extension installed locked dependencies in a container with lifecycle scripts disabled and ran the actual upstream build offline. No full workflow was executed.

## Actual upstream build validation — September 20

The pinned checkout's `.node-version` specifies Node 24.5.0. Using that version, npm 11.5.1, its unchanged package lock, ncc 0.45.0 and TypeScript 6.0.3, `npm run bundle` succeeded. Git reported no changes under `dist/` after the baseline build.

In the disposable local checkout, the test then preserved `dist/606.index.js` outside the output directory and omitted it from a new local commit. It changed no source, dependency declaration, or lockfile. Running the same complete build restored the chunk. Every output-file SHA-256 matched the first build; the only output-tree status was `?? dist/606.index.js`.

| Actual build case | Original check / producer / consumer | Applied patch |
|---|---|---|
| Unchanged compiled output | No / No / No | No / No / No |
| Compiler restores omitted `606.index.js` | **No / No / No** | **Yes / Yes / Yes** |

The patch was applied with real Git, its resulting workflow files matched the proposed edits exactly, and their reviewed decision blocks ran against this actual compiled tree. Consumer commit/push steps were excluded. The action itself was not executed.

Isolation: Docker on WSL, non-root UID, read-only container root, dropped capabilities, no-new-privileges, bounded CPU/memory/processes, and only a fresh lab directory mounted. Downloads and `npm ci --ignore-scripts` used networking; both compilation passes and comparison tests used `--network=none`. No personal directory, credentials, or Docker socket was mounted. Image digest and run metadata are recorded. This is not a hosted GitHub Actions run.

Installation emitted engine warnings for some locked transitive dependencies requiring a newer Node version. Both builds nevertheless completed under the repository's specified version. That does not establish runtime compatibility of the action. Output cleanup was not tested in this September 20 run; the September 21 follow-up above tests it separately. The original patch should not be construed as a clean-build guarantee.

Evidence: [actual-build results](./build-evidence/run-qryqclvl/actual-build-results.json), [run metadata](./build-evidence/run-qryqclvl/run.json), [baseline build log](./build-evidence/run-qryqclvl/offline-build.log), [regeneration log](./build-evidence/run-qryqclvl/regeneration.log), [installation log](./build-evidence/run-qryqclvl/fetch-and-install.log). The earlier Windows fixture results remain separate and unchanged.

## What actually ran

The test extracts and executes the reviewed Bash comparison blocks from the saved upstream files, using real Git in newly created local fixture repositories. It evaluates the consumer's early-exit guard only: its push and commit commands are excluded. Node executes only our own harmless string-output fixture.

| Fixture | Existing check-dist / rebuild / consumer detects change | Patched checks |
|---|---|---|
| Unchanged tree | No / No / No | All correctly report unchanged |
| Tracked content edit | Yes / Yes / Yes | All detect |
| New file only | **No / No / No** | All detect |
| Tracked file deleted | Yes / Yes / Yes | All detect |
| Meaningful trailing space in template literal | **No / No / Yes** | All detect |
| New nested file only | **No / No / No** | All detect |
| Already-staged edit | **No / No / No** | All detect |

The staged case is a robustness control, not evidence that the examined build currently stages files. The unchanged and normal-change cases prevent a trivial “always fail” fix from passing.

For the semantic example, the fixture prints a JSON-encoded template literal. Adding one space before its embedded newline changes output from `"left \nright"` to `"left  \nright"`. The first two original checks still report no change. No malicious JavaScript is involved.

Environment: Python 3.14.3, Git 2.53.0.windows.2, Node 24.11.1, Git Bash on Windows. Git system/global configuration and inherited Git overrides are excluded; hooks and signing are disabled in fixture repositories. This is not a GitHub-hosted Ubuntu run, and Node here is used for the tiny language-semantics control, not the upstream package's full dependency stack.

## Fix supplied

[proposed-fix.patch](./proposed-fix.patch) stages `dist/` before deciding whether it changed, then compares the index against HEAD without suppressing whitespace. It preserves the existing origin, actor, revision, permission, and push guards. It also distinguishes normal diff status 1 from a Git error greater than 1.

All seven behavior cases pass after the patch. A non-repository control fails explicitly rather than reporting unchanged. Real `git apply --check` and `git apply` succeed against the pinned files, and the applied files match the tested proposal exactly.

This deliberately changes the ephemeral checkout's index. It does not commit in the verification/producer jobs. Review this design against any future additional steps that depend on a pristine index. The patch covers Git-visible files according to repository policy; it is not a general byte-for-byte directory comparator and does not audit ignored files or Git filters.

## Why it matters, without exaggeration

The check advertises agreement between generated and checked-in output, but its comparison is incomplete. A build that only adds an output can get a false-clean result; the producer can omit an artifact, and the consumer can skip an additions-only update. The repository's package script uses ncc, whose public interface supports emitted assets in addition to code. That makes the output-tree question relevant, but does **not** establish that the current dependency graph has triggered this particular failure. [Pinned package configuration](https://github.com/actions/attest/blob/c5895f04a64254068ee4ce85086baae80a363b9c/package.json), [ncc documentation](https://github.com/vercel/ncc#programmatically-from-nodejs).

The recent artifact-origin security fix is a different issue. Its source/actor checks remain present and are not bypassed in this reproduction. An integrity check with a false negative deserves repair without inflating it into a critical vulnerability.

## Prior-report check

Public GitHub issue searches on September 18 returned no results for `repo:actions/attest is:issue dist untracked` or `repo:actions/attest is:issue "ignore-space-at-eol"`. A corresponding template-repository issue search also returned none. A broad `repo:actions/attest is:pr "git diff"` query returned PR #466, titled “Support single-subject attestations.” These limited searches do not prove novelty or exclude private reports.

The `actions/javascript-action` template also surfaced with the whitespace-suppressing comparison in public search. It has not been pinned and independently regression-tested here; this report's verified scope is the `actions/attest` revision above.

## Reproduce and review

Run `python reproduce.py` from this directory with Git, Bash, and Node available. Nothing is installed automatically. The script makes no network requests and preserves generated fixture repositories under `local-fixtures/`. Each run creates a new folder; it does not reset or clean an existing checkout.

- [Reproduction harness](./reproduce.py)
- [Recorded results and source/patch hashes](./results.json)
- [Proposed patch](./proposed-fix.patch)
- [Maintainer-ready draft](./Maintainer%20Report.md)

To repeat the real-build extension, run `python3 container_build.py` from WSL with Docker available. It downloads the specified image and pinned project, installs locked dependencies without lifecycle scripts, and compiles offline in isolated containers. It preserves uniquely named evidence runs and disposable Linux lab directories; it does not modify another checkout. See [container runner](./container_build.py) and [actual-build cases](./actual_build_cases.py).

Remaining gates: maintainer review, hosted-workflow validation, and agreement on whether indexed comparison is the preferred policy. No issue, pull request, security report, or message has been sent.
