#!/usr/bin/env python3
"""Fail when captions or image alt text narrate the production process.

    python3 check-assets.py post.html another.html

Uses the production_commentary patterns from ../slop-detector.json. Exit 1 on any hit.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class AssetCopyParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: list[tuple[str, str]] = []
        self._caption_depth = 0
        self._caption_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attributes = dict(attrs)
        if tag == "img":
            alt = (attributes.get("alt") or "").strip()
            if alt:
                self.items.append(("img_alt", alt))
        if tag == "figcaption":
            self._caption_depth += 1
            if self._caption_depth == 1:
                self._caption_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "figcaption" or not self._caption_depth:
            return
        self._caption_depth -= 1
        if self._caption_depth == 0:
            caption = " ".join(" ".join(self._caption_parts).split())
            if caption:
                self.items.append(("figcaption", caption))
            self._caption_parts = []

    def handle_data(self, data: str) -> None:
        if self._caption_depth:
            self._caption_parts.append(data)


def load_patterns() -> list[re.Pattern[str]]:
    detector_path = Path(__file__).resolve().parents[1] / "slop-detector.json"
    detector = json.loads(detector_path.read_text(encoding="utf-8"))
    production = detector["categories"]["production_commentary"]
    if production.get("severity") != "hard_fail":
        raise ValueError("production_commentary must remain a hard-fail category")
    raw_patterns = production["patterns"] + production.get("asset_only_patterns", [])
    return [re.compile(pattern, re.IGNORECASE) for pattern in raw_patterns]


def scan(path: Path, patterns: list[re.Pattern[str]]) -> list[str]:
    parser = AssetCopyParser()
    parser.feed(path.read_text(encoding="utf-8"))
    violations = []
    for kind, text in parser.items:
        for pattern in patterns:
            found = pattern.search(text)
            if found:
                # Lead with the offending words. The raw pattern is long enough to
                # bury the actual problem, so it goes last and truncated.
                rule = pattern.pattern
                if len(rule) > 60:
                    rule = rule[:57] + "..."
                violations.append(
                    f"{path}:{kind}: {found.group(0).strip()!r}"
                    f" in {text!r}\n    rule: /{rule}/"
                )
                break  # one report per string; the first hit is the fix to make
    return violations


def main() -> int:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("files", nargs="+", type=Path)
    args = argument_parser.parse_args()
    patterns = load_patterns()
    violations = []
    for path in args.files:
        if not path.is_file():
            violations.append(f"{path}: file not found")
            continue
        violations.extend(scan(path, patterns))
    if violations:
        print("\n".join(violations), file=sys.stderr)
        return 1
    print(f"PASS: {len(args.files)} file(s), no production commentary in captions or alt text")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
