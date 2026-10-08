# Generated-output comparison tools

`treecheck.py` is a small, dependency-free, read-only directory comparator. It addresses a lesson from Cases 002 and 003: Git's tracking and whitespace policies are not the same as comparing the files a compiler produces.

## Use

```text
python treecheck.py path/to/expected-output path/to/freshly-built-output
```

Exit status: **0** for equality under the selected policy, **1** for differences, **2** for an inspection error. Output is JSON. Do not treat an inspection error as equality.

The tool never runs a build, executes inspected code, edits either tree, stages Git files, contacts a service, or reads credentials intentionally. It examines all directory entries, including Git-ignored files, so point it only at the intended output directories. The caller must produce the rebuilt tree in a clean location first.

## Comparison policy

- Regular files: size and SHA-256, with all bytes significant, including binary content, trailing whitespace, and line endings.
- Directories: names and presence, including empty directories.
- Symlinks: target text, without following links encountered in the tree. A root that is itself a symlink is rejected. Root ancestor paths remain subject to normal OS path resolution.
- Windows junctions and other unsupported reparse points: rejected.
- Special files such as FIFOs: rejected rather than read.
- Modification timestamps, ownership, ACLs, extended attributes, hard-link relationships, alternate data streams, and directory permissions: not compared.
- Optional `--check-executable` compares whether any POSIX executable bit is set on regular files. It is rejected on Windows; it is not a comparison of every permission bit.

This is file-tree equivalence under a stated policy, not a general filesystem forensic tool. SHA-256 equality is a practical content check, not a mathematical proof of identical bytes.

## Boundaries

Use frozen, quiescent directories or filesystem snapshots. The tool detects some file replacement/modification races, but its traversal is **not** an atomic snapshot or a race-proof security boundary. It cannot safely confine an attacker concurrently mutating path ancestors. A passing result does not establish that source code is safe, that the build is trustworthy, or that no secrets were embedded.

The Windows tests exposed different `ctime` values through descriptor and pathname queries in the available Python runtime. The tool therefore uses identity, size, and modification time for Windows mutation checks, additionally checking `ctime` on POSIX. It does not equate differing timestamps between two otherwise identical frozen files with different content.

## Verification

Run `python test_treecheck.py`. All 18 tests pass on Linux. On Windows, 13 pass and five POSIX-specific tests are skipped explicitly; Windows junction rejection is implemented but not independently fixture-tested. The suite covers ordinary and binary equality, new output, stale-file deletion, whitespace, same-size modifications, ignored files, empty directories, type changes, missing roots, timestamp policy, symlinks, FIFO rejection, executable mode, and command exit codes.

Recorded test reports: [Windows](./windows-tests.json), [Linux](./linux-tests.json). Test fixtures are temporary generated files; the test runner removes only its own temporary directories.

`validate_saved_builds.py` is a workspace-specific integration test against the existing Case 002 lab. It checks artifact hashes against the prior build record before comparing a stale-output tree with a clean tree, then compares outputs from two separate clean builds. It is not portable unless those recorded lab paths exist. The general comparator itself has no dependency on that lab.

These tools are experimental local review aids, not a deployed CI service or an audited security product. Nothing has been published or submitted upstream.
