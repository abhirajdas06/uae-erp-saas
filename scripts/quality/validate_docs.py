"""Validate repository Markdown links and document-control identifiers."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

from common import emit_and_exit, evidence_envelope, finding, repository_root, safe_repo_path

LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
DOCUMENT_ID = re.compile(r"^\|\s*Document ID\s*\|\s*([^|]+?)\s*\|\s*$", re.MULTILINE)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
FENCE = re.compile(r"^```.*?^```\s*$", re.MULTILINE | re.DOTALL)


def _slug(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[`*_~]", "", value).strip().lower()
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    return re.sub(r"[\s-]+", "-", value).strip("-")


def _anchors(text: str) -> set[str]:
    counts: defaultdict[str, int] = defaultdict(int)
    anchors: set[str] = set()
    for match in HEADING.finditer(FENCE.sub("", text)):
        base = _slug(match.group(2))
        anchor = base if counts[base] == 0 else f"{base}-{counts[base]}"
        counts[base] += 1
        anchors.add(anchor)
    return anchors


def validate(root: Path, docs_root: Path) -> tuple[list[dict[str, object]], dict[str, object], list[Path]]:
    findings: list[dict[str, object]] = []
    markdown_files = sorted(docs_root.rglob("*.md"))
    for root_name in ("README.md", "AGENTS.md"):
        root_file = root / root_name
        if root_file.is_file():
            markdown_files.append(root_file)
    markdown_files = sorted(set(markdown_files))
    ids: defaultdict[str, list[str]] = defaultdict(list)
    anchor_cache: dict[Path, set[str]] = {}
    checked_links = 0

    for path in markdown_files:
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(finding("DOC_ENCODING", "Markdown file is not valid UTF-8", relative))
            continue
        for match in DOCUMENT_ID.finditer(text):
            ids[match.group(1).strip()].append(relative)
        scan_text = FENCE.sub("", text)
        for match in LINK.finditer(scan_text):
            raw = match.group(1).strip().strip("<>")
            if not raw or raw.startswith(("http://", "https://", "mailto:", "codex:")):
                continue
            checked_links += 1
            target_text, _, anchor = raw.partition("#")
            target_text = unquote(target_text)
            if target_text:
                target = (path.parent / target_text).resolve()
                try:
                    target.relative_to(root.resolve())
                except ValueError:
                    findings.append(finding("DOC_LINK_ESCAPE", f"Link leaves repository: {raw}", relative))
                    continue
            else:
                target = path.resolve()
            if not target.exists():
                line = text[: match.start()].count("\n") + 1
                findings.append(finding("DOC_LINK_MISSING", f"Missing internal link target: {raw}", relative, line))
                continue
            if anchor and target.is_file() and target.suffix.lower() == ".md":
                if target not in anchor_cache:
                    anchor_cache[target] = _anchors(target.read_text(encoding="utf-8"))
                normalized = unquote(anchor).lower()
                if normalized not in anchor_cache[target]:
                    line = text[: match.start()].count("\n") + 1
                    findings.append(finding("DOC_ANCHOR_MISSING", f"Missing heading anchor: {raw}", relative, line))

    for document_id, paths in ids.items():
        if len(paths) > 1:
            findings.append(finding("DOC_ID_DUPLICATE", f"Document ID {document_id!r} appears in: {', '.join(paths)}"))
    metrics: dict[str, object] = {
        "markdown_file_count": len(markdown_files),
        "internal_link_count": checked_links,
        "document_id_count": len(ids),
        "external_links_checked": False,
    }
    return findings, metrics, markdown_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Documentation directory relative to repository root")
    parser.add_argument("--format", choices=["json"], default="json")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repository_root()
    docs_root = safe_repo_path(root, args.root)
    if docs_root is None or not docs_root.is_dir():
        findings = [finding("DOC_ROOT", f"Documentation root does not exist: {args.root!r}")]
        metrics: dict[str, object] = {"markdown_file_count": 0, "internal_link_count": 0, "document_id_count": 0}
        files: list[Path] = []
    else:
        findings, metrics, files = validate(root, docs_root)
    evidence = evidence_envelope(
        gate_id="CI-GATE-002",
        command="python scripts/quality/validate_docs.py",
        root=root,
        input_files=files,
        findings=findings,
        metrics=metrics,
    )
    return emit_and_exit(evidence, Path(args.output))


if __name__ == "__main__":
    sys.exit(main())

