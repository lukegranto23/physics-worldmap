"""Audit this Obsidian vault without modifying knowledge notes.

The script reads the vault rooted two directories above this file. Its only
writes are the human-readable and JSON reports in ``95 Resources``.
"""

from __future__ import annotations

import collections
import json
import re
from datetime import datetime
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
RESOURCE_DIR = SCRIPT_PATH.parents[1]
ROOT = SCRIPT_PATH.parents[2]
HEALTH_PATH = RESOURCE_DIR / "Vault Health Report.md"
JSON_PATH = RESOURCE_DIR / "vault-audit.json"

WIKILINK = re.compile(r"!?\[\[([^\]]+)\]\]")
PROPERTY = re.compile(r"(?m)^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
MOJIBAKE_MARKERS = ("\u00c3", "\u00e2\u20ac", "\u00c2")
ALLOWED_EPISTEMIC_STATUSES = {
    "established",
    "effective",
    "active",
    "open",
    "conjectural",
    "speculative",
    "mixed",
    "reference",
}
METADATA_REQUIRED_TYPES = {"concept", "derivation", "experiment", "observation"}


def norm(value: str) -> str:
    return value.replace("\\", "/").strip().casefold()


def parse_properties(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    return {match.group(1): match.group(2).strip() for match in PROPERTY.finditer(text[4:end])}


def scalar_value(raw: str | None) -> str:
    """Return the simple YAML scalar representation used by this vault."""
    if raw is None:
        return ""
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1].strip()
    return "" if value.casefold() in {"null", "~"} else value


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def link_target(raw: str) -> str:
    return raw.split("|", 1)[0].split("#", 1)[0].split("^", 1)[0].strip()


def validate_layout() -> None:
    if (
        SCRIPT_PATH.parent.name != "Tools"
        or RESOURCE_DIR.name != "95 Resources"
        or not (ROOT / "Physics Worldmap.md").is_file()
    ):
        raise SystemExit(
            "Expected this script at <vault>/95 Resources/Tools/audit_vault.py "
            "with Physics Worldmap.md at the vault root. No files were changed."
        )


def audit() -> dict:
    md_files = sorted(ROOT.rglob("*.md"))
    all_files = sorted(path for path in ROOT.rglob("*") if path.is_file())
    by_stem: dict[str, list[Path]] = collections.defaultdict(list)
    by_name: dict[str, list[Path]] = collections.defaultdict(list)
    by_rel: dict[str, Path] = {}
    texts: dict[Path, str] = {}
    properties: dict[Path, dict[str, str]] = {}

    for path in md_files:
        rel_without_suffix = path.relative_to(ROOT).with_suffix("")
        by_stem[norm(path.stem)].append(path)
        by_rel[norm(str(rel_without_suffix))] = path
        text = path.read_text(encoding="utf-8")
        texts[path] = text
        properties[path] = parse_properties(text)

    for path in all_files:
        rel = path.relative_to(ROOT)
        by_name[norm(path.name)].append(path)
        by_rel[norm(str(rel))] = path
        by_rel[norm(str(rel.with_suffix("")))] = path

    unresolved: list[dict[str, str]] = []
    ambiguous: list[dict[str, str]] = []
    inbound: collections.Counter[Path] = collections.Counter()
    outbound: collections.Counter[Path] = collections.Counter()
    link_count = 0

    for source, text in texts.items():
        for raw in WIKILINK.findall(text):
            target = link_target(raw)
            if not target:
                continue
            link_count += 1
            resolved: Path | None = None
            target_path = Path(target)
            ambiguity: dict[str, str] | None = None

            if target_path.suffix and target_path.suffix.casefold() != ".md":
                matches = by_name.get(norm(target_path.name), [])
                if len(matches) == 1:
                    resolved = matches[0]
                elif len(matches) > 1:
                    ambiguity = {
                        "source": str(source.relative_to(ROOT)),
                        "target": target,
                        "matches": "; ".join(str(path.relative_to(ROOT)) for path in matches),
                    }
            elif "/" in target or "\\" in target:
                resolved = by_rel.get(norm(target)) or by_rel.get(
                    norm(str(target_path.with_suffix("")))
                )
            else:
                matches = by_stem.get(norm(target_path.stem), [])
                if len(matches) == 1:
                    resolved = matches[0]
                elif len(matches) > 1:
                    ambiguity = {
                        "source": str(source.relative_to(ROOT)),
                        "target": target,
                        "matches": "; ".join(str(path.relative_to(ROOT)) for path in matches),
                    }

            if ambiguity is not None:
                ambiguous.append(ambiguity)
            elif resolved is None:
                unresolved.append(
                    {"source": str(source.relative_to(ROOT)), "target": target}
                )
            else:
                outbound[source] += 1
                inbound[resolved] += 1

    duplicate_stems = {
        stem: [str(path.relative_to(ROOT)) for path in paths]
        for stem, paths in by_stem.items()
        if len(paths) > 1
    }
    no_frontmatter = [
        str(path.relative_to(ROOT))
        for path in md_files
        if not properties[path] and path.name != "README.md"
    ]
    control_character_files = []
    mojibake_files = []
    for path, text in texts.items():
        bad = sorted({ord(char) for char in text if ord(char) < 32 and char not in "\n\t"})
        if bad:
            control_character_files.append(
                {"path": str(path.relative_to(ROOT)), "codepoints": bad}
            )
        markers = [marker for marker in MOJIBAKE_MARKERS if marker in text]
        if markers:
            mojibake_files.append(
                {"path": str(path.relative_to(ROOT)), "markers": markers}
            )

    status_counts: collections.Counter[str] = collections.Counter()
    type_counts: collections.Counter[str] = collections.Counter()
    field_counts: collections.Counter[str] = collections.Counter()
    maturity_counts: collections.Counter[str] = collections.Counter()
    source_audit_counts: collections.Counter[str] = collections.Counter()
    unknown_statuses: dict[str, list[str]] = collections.defaultdict(list)
    note_maturity_missing: list[dict[str, str]] = []
    source_audit_missing: list[dict[str, str]] = []

    for path, metadata in properties.items():
        relative_path = path.relative_to(ROOT)
        relative = str(relative_path)
        status = scalar_value(metadata.get("epistemic_status"))
        note_type = scalar_value(metadata.get("type"))
        field = scalar_value(metadata.get("field"))

        if status:
            status_counts[status] += 1
            if status not in ALLOWED_EPISTEMIC_STATUSES:
                unknown_statuses[status].append(relative)
        if note_type:
            type_counts[note_type] += 1
        if field:
            field_counts[field] += 1

        is_template = "99 Templates" in relative_path.parts or note_type.casefold() == "template"
        if is_template:
            continue

        note_maturity = scalar_value(metadata.get("note_maturity"))
        source_audit = scalar_value(metadata.get("source_audit"))
        if note_maturity:
            maturity_counts[note_maturity] += 1
        if source_audit:
            source_audit_counts[source_audit] += 1

        normalized_type = note_type.casefold()
        if normalized_type in METADATA_REQUIRED_TYPES:
            if not note_maturity:
                note_maturity_missing.append({"path": relative, "type": note_type})
            if not source_audit:
                source_audit_missing.append({"path": relative, "type": note_type})

    orphans = [
        str(path.relative_to(ROOT))
        for path in md_files
        if inbound[path] == 0
        and outbound[path] == 0
        and "99 Templates" not in str(path)
        and path.name != "README.md"
    ]
    no_inbound = [
        str(path.relative_to(ROOT))
        for path in md_files
        if inbound[path] == 0
        and "99 Templates" not in str(path)
        and path.name != "README.md"
    ]
    equations = sum(
        text.count("$$") // 2
        + len(re.findall(r"(?<!\$)\$(?!\$)", text)) // 2
        for text in texts.values()
    )
    words = sum(len(re.findall(r"\b[\w'-]+\b", text)) for text in texts.values())

    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "root": ROOT.name,
        "markdown_notes": len(md_files),
        "python_labs": len(list((ROOT / "62 Computational Labs").glob("*.py"))),
        "total_words_approx": words,
        "equation_blocks_or_inline_pairs_approx": equations,
        "wikilinks": link_count,
        "resolved_wikilinks": link_count - len(unresolved) - len(ambiguous),
        "unresolved_count": len(unresolved),
        "ambiguous_count": len(ambiguous),
        "duplicate_stem_count": len(duplicate_stems),
        "frontmatter_missing_count": len(no_frontmatter),
        "orphan_count": len(orphans),
        "no_inbound_count": len(no_inbound),
        "control_character_files": control_character_files,
        "mojibake_files": mojibake_files,
        "allowed_epistemic_statuses": sorted(ALLOWED_EPISTEMIC_STATUSES),
        "status_counts": dict(status_counts.most_common()),
        "unknown_epistemic_status_count": sum(len(paths) for paths in unknown_statuses.values()),
        "unknown_epistemic_status_value_count": len(unknown_statuses),
        "unknown_epistemic_statuses": {
            value: paths for value, paths in sorted(unknown_statuses.items())
        },
        "type_counts": dict(type_counts.most_common()),
        "field_counts": dict(field_counts.most_common()),
        "note_maturity_counts": dict(maturity_counts.most_common()),
        "source_audit_counts": dict(source_audit_counts.most_common()),
        "note_maturity_missing_count": len(note_maturity_missing),
        "source_audit_missing_count": len(source_audit_missing),
        "note_maturity_missing": note_maturity_missing,
        "source_audit_missing": source_audit_missing,
        "unresolved": unresolved,
        "ambiguous": ambiguous,
        "duplicate_stems": duplicate_stems,
        "frontmatter_missing": no_frontmatter,
        "orphans": orphans,
        "no_inbound": no_inbound,
    }


def report(data: dict) -> str:
    status_rows = "\n".join(f"| {key} | {value} |" for key, value in data["status_counts"].items())
    type_rows = "\n".join(f"| {key} | {value} |" for key, value in data["type_counts"].items())
    maturity_rows = "\n".join(
        f"| {markdown_cell(key)} | {value} |"
        for key, value in data["note_maturity_counts"].items()
    ) or "| — | 0 |"
    source_audit_rows = "\n".join(
        f"| {markdown_cell(key)} | {value} |"
        for key, value in data["source_audit_counts"].items()
    ) or "| — | 0 |"
    unknown_status_rows = "\n".join(
        f"| `{markdown_cell(value)}` | {len(paths)} | "
        f"{'<br>'.join(f'`{path}`' for path in paths)} |"
        for value, paths in data["unknown_epistemic_statuses"].items()
    ) or "| — | 0 | — |"
    note_maturity_missing_rows = "\n".join(
        f"| `{item['path']}` | `{item['type']}` |"
        for item in data["note_maturity_missing"]
    ) or "| — | — |"
    source_audit_missing_rows = "\n".join(
        f"| `{item['path']}` | `{item['type']}` |"
        for item in data["source_audit_missing"]
    ) or "| — | — |"
    unresolved_rows = "\n".join(
        f"| `{item['source']}` | `{item['target']}` |"
        for item in data["unresolved"][:200]
    ) or "| — | — |"
    ambiguous_rows = "\n".join(
        f"| `{item['source']}` | `{item['target']}` | {item['matches']} |"
        for item in data["ambiguous"][:100]
    ) or "| — | — | — |"
    duplicate_rows = "\n".join(
        f"| `{stem}` | {'; '.join(paths)} |"
        for stem, paths in data["duplicate_stems"].items()
    ) or "| — | — |"
    health = "PASS" if not (
        data["unresolved_count"]
        or data["ambiguous_count"]
        or data["duplicate_stem_count"]
        or data["control_character_files"]
        or data["mojibake_files"]
        or data["unknown_epistemic_status_count"]
        or data["note_maturity_missing_count"]
        or data["source_audit_missing_count"]
    ) else "NEEDS ATTENTION"
    today = data["generated_at"][:10]

    return f'''---
type: vault-health-report
field: Physics
epistemic_status: reference
level: all
tags: [physics, maintenance, validation]
created: 2026-07-30
updated: {today}
---

# Vault Health Report

**Structural health: {health}**

Generated by the bundled local link, metadata, encoding, and graph audit at `{data['generated_at']}`.

| Metric | Value |
|---|---:|
| Markdown notes | {data['markdown_notes']:,} |
| Runnable Python files | {data['python_labs']:,} |
| Approximate words | {data['total_words_approx']:,} |
| Approximate equation pairs | {data['equation_blocks_or_inline_pairs_approx']:,} |
| Wikilinks | {data['wikilinks']:,} |
| Resolved Wikilinks | {data['resolved_wikilinks']:,} |
| Unresolved links | {data['unresolved_count']:,} |
| Ambiguous links | {data['ambiguous_count']:,} |
| Duplicate basenames | {data['duplicate_stem_count']:,} |
| Notes missing frontmatter | {data['frontmatter_missing_count']:,} |
| Fully disconnected notes | {data['orphan_count']:,} |
| Notes with no inbound link | {data['no_inbound_count']:,} |
| Files with control characters | {len(data['control_character_files']):,} |
| Files with mojibake markers | {len(data['mojibake_files']):,} |
| Notes with unknown epistemic status | {data['unknown_epistemic_status_count']:,} |
| Required notes missing `note_maturity` | {data['note_maturity_missing_count']:,} |
| Required notes missing `source_audit` | {data['source_audit_missing_count']:,} |

## Epistemic status counts

| Status | Notes |
|---|---:|
{status_rows}

Allowed values: {', '.join(f'`{value}`' for value in data['allowed_epistemic_statuses'])}.

### Unknown epistemic status values

| Value | Notes | Paths |
|---|---:|---|
{unknown_status_rows}

## Note type counts

| Type | Notes |
|---|---:|
{type_rows}

## Note maturity counts

Counts include all non-template notes that declare `note_maturity`.

| Maturity | Notes |
|---|---:|
{maturity_rows}

## Source-audit counts

Counts include all non-template notes that declare `source_audit`.

| Source audit | Notes |
|---|---:|
{source_audit_rows}

## Required metadata gaps

Non-template notes of type `concept`, `derivation`, `experiment`, or `observation` must declare both metadata properties.

### Missing `note_maturity`

| Note | Type |
|---|---|
{note_maturity_missing_rows}

### Missing `source_audit`

| Note | Type |
|---|---|
{source_audit_missing_rows}

## Unresolved links

| Source | Target |
|---|---|
{unresolved_rows}

## Ambiguous links

| Source | Target | Matches |
|---|---|---|
{ambiguous_rows}

## Duplicate basenames

| Basename | Paths |
|---|---|
{duplicate_rows}

## Maintenance rule

Re-run the audit after renaming, bulk generation, or frontier updates. A structurally clean vault can still contain scientific errors; evidence and derivation audits are separate layers.

## Refresh this report on Windows

1. Open PowerShell in the vault folder.
2. Run `python ".\\95 Resources\\Tools\\audit_vault.py"`.
3. Reopen this note to see the refreshed report. The machine-readable result is saved beside it as `vault-audit.json`.

The checker reads the vault and only replaces this report and `95 Resources/vault-audit.json`.

## Navigation

- [[Physics Worldmap|Home]]
- [[Architecture and Completeness Audit|Architecture and completeness audit]]
'''


def main() -> None:
    validate_layout()
    data = audit()
    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    HEALTH_PATH.write_text(report(data).rstrip() + "\n", encoding="utf-8")
    summary_keys = (
        "markdown_notes",
        "python_labs",
        "total_words_approx",
        "wikilinks",
        "unresolved_count",
        "ambiguous_count",
        "duplicate_stem_count",
        "frontmatter_missing_count",
        "orphan_count",
        "unknown_epistemic_status_count",
        "unknown_epistemic_status_value_count",
        "note_maturity_missing_count",
        "source_audit_missing_count",
        "control_character_files",
        "mojibake_files",
    )
    print(json.dumps({key: data[key] for key in summary_keys}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
