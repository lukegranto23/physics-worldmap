# Reproducible build-verification review packet

Start with `Maintainer Report.md`. Supporting explanations are in `Finding.md` and `Clean Build Follow-up.md`; point-in-time upstream and duplicate-report checks are in `Upstream Review.md`.

Read `Impact Assessment.md` before making security claims: the stale chunk duplicates the current implementation apart from bundler identity, and the reviewed direct loading sites do not request it. Static audit source and results are included.

## What is established

1. Actual pinned workflow comparisons miss Git-visible new files. The real compiler restores an intentionally omitted chunk without those checks detecting it.
2. The ordinary build preserves an existing chunk that a clean build does not produce. The five shared output files are byte-identical.
3. A broader patch both prepares a clean output directory and compares staged Git-visible differences. Its build steps expose the stale file and accept an identical repeat build.

The semantic trailing-whitespace result is a separate harmless language fixture, not an observed dependency-update behavior. No full hosted workflow, attestation runtime, remote exploit, or external submission is claimed.

## Patch selection

Preferred candidate for both observed issues: `build-evidence/clean-iy_fho70/proposed-complete-fix.patch`.

`proposed-fix.patch` is retained as the narrower comparison-only patch. Do not apply both patches sequentially: both are based on the original pinned workflow files. The broader patch includes the narrow comparison changes.

The patch does not itself remove the stale tracked chunk from the upstream repository. A maintainer adopting it must regenerate and commit clean `dist/` output as well; otherwise the corrected checker should fail on that known discrepancy. Review temporary-output storage, Git ignore/filter policy, and hosted workflow behavior before merging.

## Reproduction

- `python reproduce.py`: original seven fixture cases; needs Python, Git, Bash, and Node. No network or automatic install. Creates new local fixture directories.
- `python3 container_build.py`: run from Linux/WSL with Docker. Downloads the specified image and pinned source, installs locked dependencies with lifecycle scripts disabled, compiles offline, and runs omitted-chunk checks. Records a new `build-evidence/run-.../run.json`.
- `python3 clean_build_probe.py build-evidence/run-.../run.json`: use the metadata from that run. Reuses its lab and image, copies dependencies into a fresh checkout, and performs offline overlay/clean/repeat-build tests of the broader patch. Creates a new `build-evidence/clean-.../` folder.

Container builds are non-root, network-disabled during compilation, resource-limited, and mount only the disposable lab directory. They do not mount personal folders, credentials, or the Docker socket. Download/install uses network access. The historical JSON files contain original machine-specific lab paths; rerun the container runner to generate usable metadata on another machine.

Dependencies, full source clones, container images, and fixture repositories are intentionally excluded from this packet. The selected upstream snapshot includes its MIT license. `SHA256SUMS.json` inventories packet contents for transfer checking; it is not a digital signature or independent attestation.

**Draft only. No issue, PR, security report, or message has been submitted.**
