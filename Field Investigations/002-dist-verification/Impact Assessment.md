# Impact assessment: keep the claim narrow

September 21, 2026. Pinned revision `c5895f04a64254068ee4ce85086baae80a363b9c`.

## New evidence

The stale `184.index.js` is exactly equal to the current `606.index.js` after changing three identity fields: exported `id`, exported `ids`, and the bundled module key (`91184` to `606`). No function-body, string, or other code changes are required. This is evidence of duplicated implementation under old bundler identifiers, not of an older vulnerable implementation being retained.

A syntax-tree audit of all four JavaScript files found seven direct calls to the bundle's `__nccwpck_require__.e` chunk loader:

| Requested chunk | Calls | Context |
|---|---:|---|
| 606 | 6 | Imports the current `pMap` implementation |
| 50 | 1 | Optional dependency path |
| 184 | 0 | No direct request found |

All seven request arguments are numeric literals. The filename function maps a chunk ID to `<id>.index.js`; the loader dynamically imports that relative filename. The old module key `91184` occurs as a numeric syntax node only in the stale chunk's own module definition. These observations are consistent with an orphaned generated chunk.

## What this changes

Do not escalate stale-output retention into an allegation that a known vulnerable dependency executes. The retained implementation matches the current one after identifier normalization, and the reviewed direct chunk-loading sites do not request it.

The two build-verification correctness findings remain supported: omitted generated files can escape comparison, and rebuilding over old files is not equivalent to a clean build. The first finding's intentionally omitted `606.index.js` is referenced by six direct loading sites, so the missing file is not merely a license or documentation artifact. However, whether those paths run in any particular action invocation was not tested. No runtime failure or remote exploit is asserted.

## Scope and limits

The audit uses TypeScript's parser to inspect generated JavaScript; it never imports or executes the action. It examines direct syntax, not alias analysis, computed property access, `eval`, arbitrary external callers, or all possible dynamic behavior. Therefore zero direct requests is not a general proof of unreachability or security. No third-party system was tested.

[Audit script](./static_chunk_audit.cjs) and [recorded result](./build-evidence/static-chunk-audit.json) include filenames, source lines, extracted loader code, file hashes, and exact identity substitutions. All audited hashes match the earlier baseline build. Execution used the same pinned container image, disabled networking, a non-root user, dropped capabilities, read-only root, and only the disposable lab mount.

The report remains a build-correctness report with a tested local patch. It is not a vulnerability severity assessment, bounty claim, or full action security audit.
