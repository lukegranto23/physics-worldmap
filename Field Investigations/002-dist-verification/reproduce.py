"""Reproduce real Git predicates from pinned actions/attest workflow source.

No network, installs, upstream builds, credentials, or remote Git operations.
Executes only reviewed detection blocks, local Git, and our harmless JS fixture.
Keeps generated fixture repositories for inspection; deletes nothing.
"""
from __future__ import annotations
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT / "upstream"
REVISION = "c5895f04a64254068ee4ce85086baae80a363b9c"
BLOBS = {
    ".github/workflows/check-dist.yml": "22569bf8df918d82a4d30af1efb3024edf0f296e",
    ".github/workflows/commit-dist.yml": "b142a55b064eaaa86187020879701a1318708e93",
    ".github/workflows/rebuild-dist.yml": "77f3f0558a2c49d64d0de66f3283ab2c10f0185e",
    "LICENSE": "5f9e342dcc1e39277b96077541676ce6307de2c7",
    "package.json": "3df6ba2623d7feaa919157762cbcdbdbdc397d74",
}
GIT = shutil.which("git")
NODE = shutil.which("node")
BASH = ("C:/Program Files/Git/bin/bash.exe" if os.name == "nt"
        else shutil.which("bash"))
ENV = {k: v for k, v in os.environ.items()
       if not k.upper().startswith("GIT_") and k not in {"BASH_ENV", "ENV", "NODE_OPTIONS"}}
ENV.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
           GIT_TERMINAL_PROMPT="0")


def run(args, cwd, *, env=None, allowed=(0,)):
    result = subprocess.run(args, cwd=cwd, env=env or ENV, text=True,
                            capture_output=True, timeout=30)
    if result.returncode not in allowed:
        raise RuntimeError(f"Unexpected exit {result.returncode}: {args[0]}\n{result.stderr}")
    return result


def git(cwd, *args, allowed=(0,)):
    return run([GIT, *args], cwd, allowed=allowed)


def block(text, step):
    """Extract one reviewed literal run block; no arbitrary YAML evaluation."""
    after = text.split("      - name: " + step + "\n", 1)[1]
    body = after.split("        run: |\n", 1)[1]
    lines = []
    for line in body.splitlines():
        if not line.strip():
            lines.append("")
        elif line.startswith("          "):
            lines.append(line[10:])
        else:
            break
    return "\n".join(lines).rstrip() + "\n"


def shell(cwd, code, *, output_name="producer-output.txt"):
    env = dict(ENV, GITHUB_OUTPUT=(cwd / output_name).as_posix())
    return run([BASH, "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", code],
               cwd, env=env, allowed=(0, 1, 128))


def revised_sources(source):
    """Minimal mechanical edits; preserve origin, permissions and push guards."""
    result = dict(source)
    prefix = ("          git add -- dist/\n"
              "          diff_status=0\n"
              "          git diff --cached --quiet -- dist/ || diff_status=$?\n"
              "          if [ \"$diff_status\" -gt 1 ]; then\n"
              "            exit \"$diff_status\"\n"
              "          fi\n")
    old = '          if [ "$(git diff --ignore-space-at-eol --text dist/ | wc -l)" -gt "0" ]; then\n'
    for name in ("check-dist.yml", "rebuild-dist.yml"):
        key = ".github/workflows/" + name
        if result[key].count(old) != 1:
            raise RuntimeError("Upstream predicate changed: " + key)
        result[key] = result[key].replace(old, prefix + '          if [ "$diff_status" -eq 1 ]; then\n')
        result[key] = result[key].replace("            git diff --ignore-space-at-eol --text dist/\n",
                                          "            git diff --cached -- dist/\n")
    key = ".github/workflows/commit-dist.yml"
    old = "          if git diff --quiet -- dist/; then\n"
    if result[key].count(old) != 1:
        raise RuntimeError("Upstream consumer predicate changed")
    result[key] = result[key].replace(old, prefix + '          if [ "$diff_status" -eq 0 ]; then\n')
    result[key] = result[key].replace("          git add dist/\n", "")
    return result


def consumer_decision(text):
    full = block(text, "Commit and push")
    # Never run the upstream commit/push part: evaluate only its early-exit guard.
    return full.split('git config user.name', 1)[0] + "printf 'WOULD_COMMIT\\n'\n"


def main():
    if not all((GIT, NODE, BASH)):
        raise RuntimeError("Git, Node and Bash are required; nothing is installed automatically")
    source = {}
    for name, expected in BLOBS.items():
        data = (UPSTREAM / name).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if actual != expected:
            raise RuntimeError("Source snapshot differs from pinned GitHub blob: " + name)
        source[name] = data.decode("utf-8")
    fixed = revised_sources(source)
    patch = "".join("".join(difflib.unified_diff(
        source[name].splitlines(keepends=True), fixed[name].splitlines(keepends=True),
        fromfile="a/" + name, tofile="b/" + name))
        for name in sorted(source) if source[name] != fixed[name])
    (ROOT / "proposed-fix.patch").write_text(patch, encoding="utf-8", newline="\n")
    fixtures = ROOT / "local-fixtures"
    fixtures.mkdir(exist_ok=True)
    run_root = Path(tempfile.mkdtemp(prefix="run-", dir=fixtures)).resolve()
    if not run_root.is_relative_to(fixtures.resolve()):
        raise RuntimeError("Unexpected fixture location")
    baseline = 'process.stdout.write(JSON.stringify(`left \nright`));\n'
    paths = {"check": ".github/workflows/check-dist.yml",
             "producer": ".github/workflows/rebuild-dist.yml",
             "consumer": ".github/workflows/commit-dist.yml"}
    cases = ["unchanged", "tracked_content", "new_file_only", "tracked_delete",
             "semantic_trailing_space", "nested_new_file", "already_staged"]
    rows = []
    for case in cases:
        repo = run_root / case
        repo.mkdir()
        (repo / "dist").mkdir()
        (repo / "empty-hooks").mkdir()
        (repo / "dist/index.js").write_text(baseline, encoding="utf-8", newline="\n")
        (repo / "dist/legacy.txt").write_text("baseline\n", encoding="utf-8", newline="\n")
        git(repo, "init", "-q")
        for key, value in (("user.name", "Local regression test"),
                           ("user.email", "regression@example.invalid"),
                           ("core.autocrlf", "false"),
                           ("core.hooksPath", (repo / "empty-hooks").as_posix()),
                           ("commit.gpgsign", "false")):
            git(repo, "config", key, value)
        git(repo, "add", "--", "dist/")
        git(repo, "commit", "-qm", "Harmless fixture baseline")
        before = run([NODE, "dist/index.js"], repo).stdout
        if case == "tracked_content":
            (repo / "dist/legacy.txt").write_text("changed\n", encoding="utf-8")
        elif case == "new_file_only":
            (repo / "dist/new-asset.txt").write_text("new harmless asset\n", encoding="utf-8")
        elif case == "tracked_delete":
            # Only a generated, explicitly named fixture file is removed.
            (repo / "dist/legacy.txt").unlink()
        elif case == "semantic_trailing_space":
            (repo / "dist/index.js").write_text(baseline.replace("left ", "left  "),
                                                encoding="utf-8", newline="\n")
        elif case == "nested_new_file":
            (repo / "dist/assets").mkdir()
            (repo / "dist/assets/notice.txt").write_text("new notice\n", encoding="utf-8")
        elif case == "already_staged":
            (repo / "dist/legacy.txt").write_text("staged\n", encoding="utf-8")
            git(repo, "add", "--", "dist/")
        after = run([NODE, "dist/index.js"], repo).stdout
        old_check = shell(repo, block(source[paths["check"]], "Compare Directories"))
        old_producer = shell(repo, block(source[paths["producer"]], "Detect dist/ changes"))
        old_consumer = shell(repo, consumer_decision(source[paths["consumer"]]))
        new_check = shell(repo, block(fixed[paths["check"]], "Compare Directories"))
        new_producer = shell(repo, block(fixed[paths["producer"]], "Detect dist/ changes"),
                             output_name="fixed-producer-output.txt")
        new_consumer = shell(repo, consumer_decision(fixed[paths["consumer"]]))
        intended = case != "unchanged"
        fixed_detected = (new_check.returncode == 1,
                          "changed=true" in (repo / "fixed-producer-output.txt").read_text(),
                          "WOULD_COMMIT" in new_consumer.stdout)
        original_detected = (old_check.returncode == 1,
                             "changed=true" in (repo / "producer-output.txt").read_text(),
                             "WOULD_COMMIT" in old_consumer.stdout)
        expected_original = {
            "unchanged": (False, False, False),
            "tracked_content": (True, True, True),
            "new_file_only": (False, False, False),
            "tracked_delete": (True, True, True),
            "semantic_trailing_space": (False, False, True),
            "nested_new_file": (False, False, False),
            "already_staged": (False, False, False),
        }[case]
        if original_detected != expected_original:
            raise RuntimeError(f"Original behavior changed: {case}: {original_detected}")
        if old_check.returncode not in (0, 1) or new_check.returncode not in (0, 1):
            raise RuntimeError("A Git error must not be mistaken for a successful check")
        if (before != after) != (case == "semantic_trailing_space"):
            raise RuntimeError("Harmless JavaScript semantic control failed")
        if fixed_detected != (intended,) * 3:
            raise RuntimeError(f"Regression: {case}: {fixed_detected}")
        if any(r.returncode != 0 for r in (old_producer, old_consumer, new_producer, new_consumer)):
            raise RuntimeError("Unexpected decision-block execution failure")
        rows.append({"case": case, "change_expected": intended,
                     "original_detected_check_producer_consumer": original_detected,
                     "patched_detected_check_producer_consumer": fixed_detected,
                     "node_output_before": before, "node_output_after": after,
                     "fixture": repo.relative_to(ROOT).as_posix()})
    # Validate the patch with real Git, and ensure applying it yields intended files.
    apply_repo = run_root / "patch-application"
    apply_repo.mkdir()
    for name, content in source.items():
        path = apply_repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    git(apply_repo, "init", "-q")
    git(apply_repo, "apply", "--check", str(ROOT / "proposed-fix.patch"))
    git(apply_repo, "apply", str(ROOT / "proposed-fix.patch"))
    if any((apply_repo / n).read_text(encoding="utf-8") != s for n, s in fixed.items()):
        raise RuntimeError("Applied patch differs from tested proposal")
    # Error control: index staging fails outside a repository; do not report unchanged.
    nonrepo = run_root / "not-a-repository"
    (nonrepo / "dist").mkdir(parents=True)
    (nonrepo / "dist/index.js").write_text(baseline, encoding="utf-8")
    error_control = shell(nonrepo, block(fixed[paths["check"]], "Compare Directories"))
    if error_control.returncode != 128:
        raise RuntimeError("Expected explicit failure outside Git repository")
    report = {"generated_utc": datetime.now(timezone.utc).isoformat(),
              "upstream_revision": REVISION, "verified_git_blobs": BLOBS,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "patch_sha256": hashlib.sha256((ROOT / "proposed-fix.patch").read_bytes()).hexdigest(),
              "git_version": git(ROOT, "--version").stdout.strip(),
              "node_version": run([NODE, "--version"], ROOT).stdout.strip(),
              "platform": os.name, "cases": rows,
              "patch_application_verified": True, "nonrepo_error_exit": 128,
              "all_regressions_passed": True,
              "limits": ["No upstream ncc build or GitHub hosted job executed",
                         "Harmless generated-tree fixtures, not demonstrated exploit",
                         "Git-visible files; ignored-file and hostile filter policies not audited",
                         "No external disclosure or pull request submitted"]}
    (ROOT / "results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
