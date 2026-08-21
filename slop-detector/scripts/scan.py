#!/usr/bin/env python3
"""Score a Markdown, HTML, or plain-text file against slop-detector.json.

    python3 scan.py draft.md
    python3 scan.py post.html --json
    python3 scan.py a.md b.md c.md          # sibling-boilerplate check across files
    python3 scan.py draft.md --fail-on needs_editing

Severity model (see ../SKILL.md):

    hard_fail              exact production or process narration; blocks, unscored
    warn_if_repeated       rhetorical scaffolds past their repeat threshold; +2 each
    contextual_review      lexical prompts; +1 each ONLY after a human confirms them
    structural_diagnostic  document-level heuristics; +3 / +2 / +1 by priority

The script cannot confirm contextual findings, so it prints two numbers: the
score from automatic findings alone, and the ceiling if every contextual prompt
turns out to be real. Matches inside quotation marks, blockquotes, or code are
downgraded to contextual_review because a sentence that discusses a phrase is
not a sentence that uses it.

Standard library only. Python 3.9+.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DETECTOR_PATH = Path(__file__).resolve().parents[1] / "slop-detector.json"
ASSET_KINDS = {"figcaption", "img_alt", "image_caption", "image_description"}
REGEX_HINTS = ("\\b", "(?", "[", "\\s", "\\w", "|", "?", "*", "+", "^", "$", "{")
PASSIVE_RE = re.compile(
    r"\b(?:am|is|are|was|were|be|been|being)\s+(?:\w+ed|known|shown|seen|given|made|done|"
    r"taken|built|written|found|held|kept|left|lost|met|paid|put|read|said|sent|set|sold|"
    r"told|thought|understood|won|chosen|driven|drawn|eaten|fallen|forgotten|hidden|"
    r"ridden|risen|spoken|stolen|torn|worn|broken|frozen|woven)\b",
    re.IGNORECASE,
)
QUOTE_RE = re.compile(r"[\"“][^\"”]{3,}?[\"”]|'[^']{12,}?'")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"“(])")
LINK_CELL_RE = re.compile(r"^\s*\[[^\]]+\]\([^)]+\)\s*$|^\s*<a\b[^>]*>.*?</a>\s*$", re.IGNORECASE | re.DOTALL)


# --------------------------------------------------------------------------- input


class Block:
    __slots__ = ("kind", "text", "quoted")

    def __init__(self, kind: str, text: str, quoted: bool = False) -> None:
        self.kind = kind
        self.text = " ".join(text.split())
        self.quoted = quoted


class HTMLBlocks(HTMLParser):
    """Collect reader-facing text blocks and tables from HTML."""

    TEXT_TAGS = {"p": "body_prose", "li": "list_item", "h1": "heading", "h2": "heading",
                 "h3": "heading", "h4": "heading", "figcaption": "figcaption",
                 "td": "table_cell", "th": "table_header", "dd": "body_prose", "dt": "body_prose"}
    SKIP_TAGS = {"script", "style", "code", "pre", "noscript", "template"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: List[Block] = []
        self.tables: List[List[List[Tuple[str, bool]]]] = []
        self.title = ""
        self._stack: List[Tuple[str, List[str]]] = []
        self._skip = 0
        self._quote = 0
        self._row: Optional[List[Tuple[str, bool]]] = None
        self._cell_is_link = False
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        tag = tag.lower()
        a = dict(attrs)
        if tag in self.SKIP_TAGS:
            self._skip += 1
            return
        if tag == "blockquote":
            self._quote += 1
        if tag == "title":
            self._in_title = True
        if tag == "img" and (a.get("alt") or "").strip():
            self.blocks.append(Block("img_alt", a["alt"], bool(self._quote)))
        if tag == "table":
            self.tables.append([])
        if tag == "tr" and self.tables:
            self._row = []
        if tag in ("td", "th") and self._row is not None:
            self._cell_is_link = False
        if tag == "a" and self._stack and self._stack[-1][0] in ("td", "th"):
            self._cell_is_link = True
        if tag in self.TEXT_TAGS:
            self._stack.append((tag, []))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self._skip = max(0, self._skip - 1)
            return
        if tag == "blockquote":
            self._quote = max(0, self._quote - 1)
        if tag == "title":
            self._in_title = False
        if tag == "tr" and self._row is not None and self.tables:
            self.tables[-1].append(self._row)
            self._row = None
        if self._stack and self._stack[-1][0] == tag:
            _, parts = self._stack.pop()
            text = " ".join("".join(parts).split())
            if text:
                kind = self.TEXT_TAGS[tag]
                self.blocks.append(Block(kind, text, bool(self._quote)))
                if tag in ("td", "th") and self._row is not None:
                    self._row.append((text, self._cell_is_link))

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        if self._in_title:
            self.title += data
        if self._stack:
            self._stack[-1][1].append(data)


def parse_html(text: str) -> Tuple[List[Block], List[List[List[Tuple[str, bool]]]], str]:
    parser = HTMLBlocks()
    parser.feed(text)
    return parser.blocks, parser.tables, parser.title.strip()


def parse_markdown(text: str) -> Tuple[List[Block], List[List[List[Tuple[str, bool]]]], str]:
    blocks: List[Block] = []
    tables: List[List[List[Tuple[str, bool]]]] = []
    title = ""
    in_fence = False
    table: Optional[List[List[Tuple[str, bool]]]] = None
    para: List[str] = []
    para_quoted = False

    def flush() -> None:
        nonlocal para, para_quoted
        if para:
            blocks.append(Block("body_prose", " ".join(para), para_quoted))
        para, para_quoted = [], False

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.lstrip().startswith("```") or line.lstrip().startswith("~~~"):
            in_fence = not in_fence
            flush()
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if not stripped:
            flush()
            if table is not None:
                tables.append(table)
                table = None
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            flush()
            if re.fullmatch(r"\|(?:\s*:?-{2,}:?\s*\|)+", stripped):
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if table is None:
                table = []
            table.append([(c, bool(LINK_CELL_RE.match(c))) for c in cells])
            kind = "table_header" if len(table) == 1 else "table_cell"
            for c in cells:
                if c:
                    blocks.append(Block(kind, strip_inline(c)))
            continue
        if table is not None:
            tables.append(table)
            table = None
        for alt in re.findall(r"!\[([^\]]+)\]\([^)]*\)", stripped):
            blocks.append(Block("img_alt", alt))
        stripped = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", stripped).strip()
        if not stripped:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            flush()
            heading = strip_inline(m.group(2))
            blocks.append(Block("heading", heading))
            if len(m.group(1)) == 1 and not title:
                title = heading
            continue
        quoted = stripped.startswith(">")
        if quoted:
            stripped = stripped.lstrip("> ").strip()
        m = re.match(r"^(?:[-*+]|\d+[.)])\s+(.*)$", stripped)
        if m:
            flush()
            blocks.append(Block("list_item", strip_inline(m.group(1)), quoted))
            continue
        if quoted and not para:
            para_quoted = True
        para.append(strip_inline(stripped))
    flush()
    if table is not None:
        tables.append(table)
    return blocks, tables, title


def strip_inline(text: str) -> str:
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"[*_]{1,3}(\S.*?\S|\S)[*_]{1,3}", r"\1", text)


def load_document(path: Path) -> Tuple[List[Block], List[List[List[Tuple[str, bool]]]], str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in (".html", ".htm") or re.search(r"<(?:p|div|article|html)\b", text[:4000], re.I):
        return parse_html(text)
    return parse_markdown(text)


# --------------------------------------------------------------------------- patterns


def compile_any(pattern: str) -> re.Pattern:
    if any(h in pattern for h in REGEX_HINTS):
        return re.compile(pattern, re.IGNORECASE | re.MULTILINE)
    escaped = re.escape(pattern)
    lead = r"\b" if pattern[:1].isalnum() else ""
    tail = r"\b" if pattern[-1:].isalnum() else ""
    return re.compile(lead + escaped + tail, re.IGNORECASE)


def in_quotes(text: str, span: Tuple[int, int]) -> bool:
    return any(m.start() <= span[0] and span[1] <= m.end() for m in QUOTE_RE.finditer(text))


class Finding:
    def __init__(self, severity: str, category: str, match: str, block: Block, index: int,
                 note: str = "", points: int = 0) -> None:
        self.severity = severity
        self.category = category
        self.match = match
        self.block = block
        self.index = index
        self.note = note
        self.points = points

    def as_dict(self) -> Dict[str, Any]:
        return {"severity": self.severity, "category": self.category, "match": self.match,
                "block": self.index, "kind": self.block.kind, "note": self.note,
                "points": self.points, "context": clip(self.block.text, self.match)}


def clip(text: str, needle: str, width: int = 110) -> str:
    i = text.lower().find(needle.lower())
    if i < 0 or len(text) <= width:
        return text[:width]
    start = max(0, i - width // 3)
    return ("..." if start else "") + text[start:start + width] + ("..." if start + width < len(text) else "")


# --------------------------------------------------------------------------- scanning


def scan_blocks(detector: Dict[str, Any], blocks: List[Block]) -> List[Finding]:
    cats = detector["categories"]
    findings: List[Finding] = []

    seen: set = set()

    def add(severity: str, category: str, rx: re.Pattern, note: str = "", applies_to: Optional[List[str]] = None,
            asset_only: bool = False) -> None:
        for i, b in enumerate(blocks):
            if applies_to and b.kind not in applies_to and not (b.kind == "heading" and "body_prose" in applies_to):
                continue
            for m in rx.finditer(b.text):
                key = (i, category, m.start())
                if key in seen:
                    break
                seen.add(key)
                sev, why = severity, note
                if asset_only and b.kind not in ASSET_KINDS:
                    sev, why = "contextual_review", "hard-fails only in captions and alt text; in prose, confirm it narrates this page's own production"
                if b.quoted or in_quotes(b.text, m.span()):
                    if sev != "contextual_review":
                        sev, why = "contextual_review", "inside a quotation or blockquote; confirm it is not the author's own voice"
                findings.append(Finding(sev, category, m.group(0).strip()[:80], b, i, why))
                break  # one report per block per pattern

    for name, cat in cats.items():
        sev = cat.get("severity")
        if sev == "warn_if_repeated":
            continue  # counted across the document in scan_repeats
        if "patterns" in cat and name != "process_leakage":
            for p in cat["patterns"]:
                add(sev, name, compile_any(p), applies_to=cat.get("applies_to"))
            for p in cat.get("asset_only_patterns", []):
                add(sev, name, compile_any(p), applies_to=cat.get("applies_to"), asset_only=True)
        if "replacements" in cat:
            for phrase, repl in cat["replacements"].items():
                add(sev, name, compile_any(phrase), note=f"possible replacement: {repl}")

    pl = cats["process_leakage"]
    groups = pl["severity_by_pattern_group"]
    for p in pl["always_fail"]:
        add(groups["always_fail"], "process_leakage", compile_any(p), applies_to=pl.get("applies_to"))
    for p in pl["contextual_review"]:
        add(groups["contextual_review"], "process_leakage", compile_any(p), applies_to=pl.get("applies_to"))
    return findings


def scan_repeats(detector: Dict[str, Any], blocks: List[Block]) -> List[Finding]:
    """warn_if_repeated families are counted across the whole document."""
    cats = detector["categories"]
    doc = "\n\n".join(b.text for b in blocks if not b.quoted)
    anchor = blocks[0] if blocks else Block("body_prose", "")
    out: List[Finding] = []

    for check in cats["repeated_scaffolds"]["checks"]:
        patterns = check.get("patterns") or [check["pattern"]]
        hits = [m.group(0) for p in patterns for m in compile_any(p).finditer(doc)]
        if len(hits) >= check["repeat_threshold"]:
            out.append(Finding("warn_if_repeated", f"repeated_scaffolds/{check['name']}", hits[0][:80], anchor, -1,
                               f"{len(hits)} occurrences, threshold {check['repeat_threshold']}", 2))

    tf = cats["templated_filler"]
    for p in tf["patterns"]:
        hits = compile_any(p).findall(doc)
        if len(hits) >= tf["repeat_threshold"]:
            out.append(Finding("warn_if_repeated", "templated_filler", hits[0][:80], anchor, -1,
                               f"{len(hits)} occurrences, threshold {tf['repeat_threshold']}", 2))

    pl = cats["process_leakage"]
    limit = pl.get("limit_one_max", 2)
    hits = [m.group(0) for p in pl["limit_one"] for m in compile_any(p).finditer(doc)]
    if len(hits) > limit:
        out.append(Finding("warn_if_repeated", "process_leakage/limit_one", hits[0][:80], anchor, -1,
                           f"{len(hits)} claim-boundary disclaimers; more than {limit} reads as per-item apology", 2))
    return out


def scan_structure(detector: Dict[str, Any], blocks: List[Block],
                   tables: List[List[List[Tuple[str, bool]]]], title: str) -> Tuple[List[Finding], List[str]]:
    checks = {c["name"]: c for c in detector["categories"]["structural_patterns"]["checks"]}
    pts = detector["scoring"]["points"]
    out: List[Finding] = []
    manual: List[str] = []
    anchor = blocks[0] if blocks else Block("body_prose", "")

    def flag(name: str, detail: str) -> None:
        c = checks[name]
        pr = c.get("review_priority", "low")
        out.append(Finding("structural_diagnostic", name, detail, anchor, -1,
                           c.get("description", ""), pts[f"structural_diagnostic_{pr}"]))

    paras = [b.text for b in blocks if b.kind == "body_prose" and not b.quoted]
    words = [len(p.split()) for p in paras]
    total_words = sum(len(b.text.split()) for b in blocks)
    sentences = [s for p in paras for s in SENTENCE_RE.split(p) if len(s.split()) >= 3]

    if len(words) >= 5 and max(words) - min(words) <= 10:
        flag("identical_paragraph_length", f"{len(words)} paragraphs all within {max(words) - min(words)} words of each other")

    if total_words >= 2000 and len(sentences) >= 40:
        lens = [len(s.split()) for s in sentences]
        med = statistics.median(lens)
        share = sum(1 for n in lens if abs(n - med) <= 6) / len(lens)
        if share >= 0.85:
            flag("uniform_sentence_band", f"{share:.0%} of sentences sit within 6 words of the median ({med:.0f})")

    if len(sentences) >= 10:
        passive = sum(1 for s in sentences if PASSIVE_RE.search(s))
        ratio = passive / len(sentences)
        if ratio > 0.20:
            flag("passive_voice_heavy", f"{ratio:.0%} of sentences match a passive construction (heuristic)")

    for ti, table in enumerate(tables):
        body = table[1:] if len(table) > 1 else table
        if len(body) < 5:
            continue
        ncols = min(len(r) for r in body)
        for col in range(ncols):
            cells = [r[col] for r in body]
            if all(is_link for _, is_link in cells):
                continue  # action column: links or buttons are a legitimate affordance
            values = Counter(text for text, _ in cells)
            top, n = values.most_common(1)[0]
            if n == len(cells):
                flag("dead_table_column", f"table {ti + 1}, column {col + 1}: every row reads {top!r}")
            elif n / len(cells) >= 0.8:
                flag("near_dead_table_column", f"table {ti + 1}, column {col + 1}: {n}/{len(cells)} rows read {top!r}")

    closers = Counter(
        SENTENCE_RE.split(p)[-1].strip() for p in paras if len(SENTENCE_RE.split(p)[-1].split()) >= 6
    )
    for sentence, n in closers.items():
        if n >= 3:
            flag("repeated_per_item_sentence", f"closes {n} paragraphs: {sentence[:90]!r}")

    m = re.search(r"\b(\d{1,3})\s+(?:best\s+)?[a-z][a-z-]*s\b", title, re.IGNORECASE) if title else None
    if m:
        claimed = int(m.group(1))
        items = sum(1 for b in blocks if b.kind == "heading")
        if items and claimed > items:
            flag("count_claim_mismatch", f"title claims {claimed}, document has only {items} headings in total")

    manual.extend(name for name in ("symmetric_pros_cons", "faq_duplicates_own_h2", "sibling_article_boilerplate")
                  if name in checks)
    return out, manual


def scan_siblings(paths: List[Path], docs: Dict[Path, List[Block]]) -> List[Finding]:
    """Byte-identical paragraphs of 40+ words appearing in 3+ files."""
    owners: Dict[str, set] = {}
    for p in paths:
        for b in docs[p]:
            if b.kind == "body_prose" and len(b.text.split()) >= 40:
                owners.setdefault(b.text, set()).add(p)
    out = []
    for text, files in owners.items():
        if len(files) >= 3:
            out.append(Finding("structural_diagnostic", "sibling_article_boilerplate", text[:90],
                               Block("body_prose", text), -1, f"identical in {len(files)} files", 3))
    return out


# --------------------------------------------------------------------------- report


def band(score: int, thresholds: Dict[str, Dict[str, Optional[int]]]) -> str:
    for name, t in thresholds.items():
        lo, hi = t.get("min", 0), t.get("max")
        if score >= (lo or 0) and (hi is None or score <= hi):
            return name
    return "rewrite_required"


def report(path: Path, findings: List[Finding], manual: List[str], detector: Dict[str, Any],
           as_json: bool) -> Dict[str, Any]:
    order = ["hard_fail", "warn_if_repeated", "structural_diagnostic", "contextual_review"]
    by = {s: [f for f in findings if f.severity == s] for s in order}
    auto_score = sum(f.points for f in by["warn_if_repeated"] + by["structural_diagnostic"])
    ceiling = auto_score + detector["scoring"]["points"]["contextual_review_confirmed"] * len(by["contextual_review"])
    thresholds = detector["scoring"]["thresholds"]
    result = {
        "file": str(path),
        "hard_fail": len(by["hard_fail"]),
        "score_automatic": auto_score,
        "band_automatic": band(auto_score, thresholds),
        "score_if_all_contextual_confirmed": ceiling,
        "band_if_all_contextual_confirmed": band(ceiling, thresholds),
        "contextual_prompts": len(by["contextual_review"]),
        "manual_checks": manual,
        "findings": [f.as_dict() for f in findings],
    }
    if as_json:
        return result

    print(f"\n== {path}")
    for sev in order:
        items = by[sev]
        if not items:
            continue
        print(f"\n{sev} ({len(items)})")
        for f in items:
            where = f"block {f.index}, {f.block.kind}" if f.index >= 0 else "document"
            line = f"  - {f.category}: {f.match!r}  [{where}]"
            if f.points:
                line += f"  +{f.points}"
            print(line)
            if f.note:
                print(f"      {f.note}")
            if f.index >= 0:
                print(f"      > {clip(f.block.text, f.match)}")
    print()
    if by["hard_fail"]:
        print(f"HARD FAIL: {len(by['hard_fail'])} blocking construction(s). Rewrite before publishing; the score below cannot rescue them.")
    print(f"Advisory score from automatic findings: {auto_score} ({result['band_automatic'].replace('_', ' ')})")
    if by["contextual_review"]:
        print(f"Ceiling if every contextual prompt is confirmed: {ceiling} ({result['band_if_all_contextual_confirmed'].replace('_', ' ')}). "
              f"Review the {len(by['contextual_review'])} prompt(s) in context; quotations, code, proper names, and precise technical terms are not defects.")
    if manual:
        print(f"Not automated, check by hand: {', '.join(manual)}")
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--detector", type=Path, default=DETECTOR_PATH)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--fail-on", choices=["hard_fail", "needs_editing", "rewrite_required"], default="hard_fail",
                    help="exit 1 at this level or worse (band uses the automatic score)")
    args = ap.parse_args()

    detector = json.loads(args.detector.read_text(encoding="utf-8"))
    docs: Dict[Path, List[Block]] = {}
    tables_by: Dict[Path, Any] = {}
    titles: Dict[Path, str] = {}
    for p in args.files:
        if not p.is_file():
            print(f"{p}: file not found", file=sys.stderr)
            return 2
        docs[p], tables_by[p], titles[p] = load_document(p)

    sibling = scan_siblings(args.files, docs) if len(args.files) >= 3 else []
    results = []
    worst = 0
    rank = {"clean": 0, "needs_editing": 1, "rewrite_required": 2}
    for p in args.files:
        blocks = docs[p]
        findings = scan_blocks(detector, blocks) + scan_repeats(detector, blocks)
        structural, manual = scan_structure(detector, blocks, tables_by[p], titles[p])
        findings += structural + [f for f in sibling if f.block.text in {b.text for b in blocks}]
        if len(args.files) >= 3 and "sibling_article_boilerplate" in manual:
            manual.remove("sibling_article_boilerplate")
        r = report(p, findings, manual, detector, args.json)
        results.append(r)
        if r["hard_fail"]:
            worst = max(worst, 3)
        worst = max(worst, rank[r["band_automatic"]])

    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0], indent=2, ensure_ascii=False))

    threshold = {"hard_fail": 3, "needs_editing": 1, "rewrite_required": 2}[args.fail_on]
    return 1 if worst >= threshold else 0


if __name__ == "__main__":
    raise SystemExit(main())
