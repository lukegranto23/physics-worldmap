"""Offline educational influence graph, not an exploit or repository scanner.

No network, shell calls, credential reads, third-party imports, or target inputs.
Edges are explicit hypothetical assumptions, not evidence of a live vulnerability.
Run with Python 3.10+; writes one JSON result next to this file.
"""
from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path


def find_path(edges: set[tuple[str, str]], start: str, goal: str):
    """Return a shortest directed influence path, or None."""
    queue = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        if path[-1] == goal:
            return path
        for source, target in sorted(edges):
            if source == path[-1] and target not in seen:
                seen.add(target)
                queue.append(path + [target])
    return None


def exhaustive_reachable(edges, start, goal):
    """Small independent reference: enumerate simple paths recursively."""
    def visit(node, visited):
        if node == goal:
            return True
        return any(visit(b, visited | {b}) for a, b in edges
                   if a == node and b not in visited)
    return visit(start, {start})


def main():
    base = {
        ("untrusted_pr_execution", "shared_cache"),
        ("shared_cache", "dependency_install_execution"),
        ("dependency_install_execution", "release_execution"),
        ("shared_cache", "build_tool_execution"),
        ("build_tool_execution", "release_execution"),
        ("release_execution", "publishing_authority"),
        ("release_execution", "built_artifact"),
        ("built_artifact", "published_bytes"),
    }
    authority_edge = ("release_execution", "publishing_authority")
    cache_edge = ("untrusted_pr_execution", "shared_cache")
    artifact_edge = ("built_artifact", "published_bytes")
    cases = [
        ("shared_cache_and_privileged_release", base,
         "untrusted_pr_execution", (True, True),
         "Untrusted cache contents are executed in a publisher-capable job."),
        ("short_lived_credentials_only", base,
         "untrusted_pr_execution", (True, True),
         "Credential lifetime changes, but authority is available during execution."),
        ("fresh_runner_with_same_shared_cache", base,
         "untrusted_pr_execution", (True, True),
         "A new machine still restores the same untrusted persistent state."),
        ("dependency_install_scripts_disabled", base - {
            ("shared_cache", "dependency_install_execution")},
         "untrusted_pr_execution", (True, True),
         "Build-tool execution remains; blocking one execution phase is not all phases."),
        ("separate_nonexecuting_publisher", base - {authority_edge},
         "untrusted_pr_execution", (False, True),
         "Publisher does not execute artifact code, but accepts its bytes without an integrity gate."),
        ("untrusted_pr_cache_path_removed", base - {cache_edge},
         "untrusted_pr_execution", (False, False),
         "Only the modeled PR-to-cache route is considered in this row."),
        ("cache_cut_but_different_dependency_entry", (base - {cache_edge}) | {
            ("unreviewed_dependency", "build_tool_execution")},
         "unreviewed_dependency", (True, True),
         "A separate unreviewed code input survives the cache-specific control."),
        ("isolated_authority_and_effective_artifact_gate",
         base - {authority_edge, artifact_edge},
         "untrusted_pr_execution", (False, False),
         "Assumes the gate actually rejects these influenced bytes; no detector is implemented."),
    ]
    results = []
    checks = []
    goals = ("publishing_authority", "published_bytes")
    for name, edges, start, expected, assumption in cases:
        paths = {goal: find_path(edges, start, goal) for goal in goals}
        observed = tuple(paths[g] is not None for g in goals)
        passed = observed == expected and all(
            (paths[g] is not None) == exhaustive_reachable(edges, start, g)
            for g in goals)
        checks.append({"name": name, "passed": passed})
        results.append({"scenario": name, "assumption": assumption,
                        "entry": start, "edges": sorted(edges),
                        "influence_paths": paths})
    # Algorithm controls: directedness, cycles, disconnected targets, identity.
    controls = [
        ("directed_not_reversible", {( "a", "b")}, "b", "a", False),
        ("cycle_terminates", {("a", "b"), ("b", "a")}, "a", "c", False),
        ("identity_path", set(), "a", "a", True),
        ("disconnected", {("a", "b"), ("c", "d")}, "a", "d", False),
    ]
    for name, edges, start, goal, expected in controls:
        checks.append({"name": name,
                       "passed": (find_path(edges, start, goal) is not None) == expected})
    report = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Deterministic reachability under declared toy-graph assumptions only",
        "not_demonstrated": ["live exploitation", "real repository configuration",
                             "credential theft", "malware detection", "security certification"],
        "scenarios": results,
        "checks": checks,
        "all_checks_passed": all(c["passed"] for c in checks),
    }
    destination = Path(__file__).with_name("trust_boundary_lab_results.json")
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if not report["all_checks_passed"]:
        raise RuntimeError("Offline model regression failed; inspect result JSON")
    print(f"PASS: {len(cases)} declared scenarios, {len(checks)} checks; no network activity.")
    for scenario in results:
        paths = scenario["influence_paths"]
        print(scenario["scenario"],
              "authority=" + str(paths[goals[0]] is not None),
              "artifact=" + str(paths[goals[1]] is not None))


if __name__ == "__main__":
    main()
