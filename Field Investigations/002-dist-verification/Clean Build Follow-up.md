# A fresh build must start without old outputs

September 21, 2026. Local, isolated reproduction; no external submission.

## Result

The pinned `actions/attest` checkout (`c5895f04a64254068ee4ce85086baae80a363b9c`) contains six files under `dist/`. Its ordinary build preserves all six unchanged. Starting the same build with that directory moved aside produces five files: `184.index.js` is absent. Every shared file has exactly the same SHA-256 in both builds. Source, package declarations, and lockfile are unchanged.

This is a discrepancy already present in the pinned tree, not an artificially inserted extra file. Rebuilding over old output retains a file that the current compiler does not emit.

| Build preparation | Existing checks | Comparison-only patch |
|---|---|---|
| Build over existing `dist/` | All report unchanged | All report unchanged |
| Preserve old `dist/` elsewhere, then build | All detect the deletion | All detect the deletion |

The original patch fixes an incomplete comparison but cannot expose differences hidden by the build process itself. A complete repair of these two observed failure modes requires both clean output preparation and a complete Git-visible comparison.

## Evidence and controls

- [Successful comparison results](./build-evidence/clean-gua4skq6/clean-results.json) record all hashes and decisions.
- [Overlay-build log](./build-evidence/clean-gua4skq6/overlay-build.log) and [clean-build log](./build-evidence/clean-gua4skq6/clean-build.log) record real `npm run bundle` executions.
- [Runner](./clean_build_probe.py) clones the pinned local source into a separate disposable checkout, copies the installed locked dependencies, and builds offline in the recorded restricted container image. No credentials, personal folders, or Docker socket are mounted.
- The first probe used a directory symlink to share dependencies. It emitted different chunk names and a changed main bundle, failing the required byte-identical baseline. That run was rejected. Its [failure log](./build-evidence/clean-f440qmvg/execution.log) is preserved. Copying dependencies into the ordinary project-relative layout restored the exact baseline.

The original output directory is preserved in the lab; no user checkout was cleaned or reset. Builds run in a non-root container with networking disabled, a read-only root filesystem, dropped capabilities, resource bounds, and only the task's disposable lab mounted.

## Interpretation and limits

`184.index.js` contains a bundled `pMap` implementation. Stale presence alone does not establish maliciousness, runtime reachability, or an exploitable path. The action runtime and privileged workflow steps were not executed. The test concerns the pinned revision, not every release or the current default branch.

The workflow's own comment promises comparison with a fresh build. Retaining pre-existing output is weaker than that property. It also means a pure comparison patch should not be presented as a full source-to-artifact consistency fix.

## Broader patch tested

The [broader patch](./build-evidence/clean-iy_fho70/proposed-complete-fix.patch) moves existing output to a fresh temporary directory before each producer/checker build, then uses the previously tested indexed comparison. It preserves old output for the lifetime of the job and avoids recursive deletion. The consumer's origin/actor/revision guards are unchanged.

The patch applied to the exact pinned workflow files. The test executed its actual checker build block, detected the stale-file deletion, recorded the clean output in a disposable local commit, then executed the actual producer build block. All five output hashes remained identical and all three patched checks correctly reported no change. The two build blocks are identical and were checked for equality. No commit/push workflow step was run; the local fixture commit only establishes the repeat-build control.

[Broader-patch results](./build-evidence/clean-iy_fho70/clean-results.json), [clean build log](./build-evidence/clean-iy_fho70/clean-build.log), [repeat-build log](./build-evidence/clean-iy_fho70/repeat-build.log), and [run metadata](./build-evidence/clean-iy_fho70/run.json) are preserved. Patch SHA-256: `a16b2e42c7c6a579c52f4d3cf57263bc98d563425ee93a629535f6419f8aa824`.

This validates output preparation and the recorded decision blocks, not the complete hosted workflow or every Git ignore/filter policy. Maintainer review is still needed. The original comparison-only patch and its seven regression fixtures remain unchanged for independent review.
