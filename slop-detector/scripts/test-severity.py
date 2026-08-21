#!/usr/bin/env python3
"""Regression tests for the slop-detector severity contract.

Run after editing slop-detector.json:

    python3 slop-detector/scripts/test-severity.py

The test protects three boundaries:

1. only exact high-confidence pattern groups are hard fails;
2. broad lexical matches remain contextual review; and
3. rhetorical scaffolds warn only after their repeat threshold.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


DETECTOR_PATH = Path(__file__).resolve().parents[1] / "slop-detector.json"
ALLOWED_SEVERITIES = {
    "hard_fail",
    "warn_if_repeated",
    "contextual_review",
    "structural_diagnostic",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def compile_patterns(raw: list[str]) -> list[re.Pattern[str]]:
    return [re.compile(pattern, re.IGNORECASE | re.MULTILINE) for pattern in raw]


def first_hit(text: str, patterns: list[re.Pattern[str]]) -> str | None:
    return next((pattern.pattern for pattern in patterns if pattern.search(text)), None)


def check_patterns(check: dict[str, Any]) -> list[re.Pattern[str]]:
    raw = check.get("patterns")
    if raw is None:
        raw = [check["pattern"]]
    return compile_patterns(raw)


def occurrence_count(text: str, check: dict[str, Any]) -> int:
    return sum(len(pattern.findall(text)) for pattern in check_patterns(check))


def main() -> int:
    detector = load_json(DETECTOR_PATH)
    errors: list[str] = []

    detector_severities = set(detector["severity_model"])
    if detector_severities != ALLOWED_SEVERITIES:
        errors.append(
            f"detector severity keys {sorted(detector_severities)!r} do not match "
            f"{sorted(ALLOWED_SEVERITIES)!r}"
        )
    for severity, contract in detector["severity_model"].items():
        if severity == "hard_fail" and not (contract.get("blocking") is True and contract.get("scored") is False):
            errors.append("hard_fail must be blocking and unscored")
        if severity != "hard_fail" and not (contract.get("blocking") is False and contract.get("scored") is True):
            errors.append(f"{severity} must be non-blocking and scored")

    hard_fail_categories: list[str] = []
    for name, category in detector["categories"].items():
        severity = category.get("severity")
        grouped = category.get("severity_by_pattern_group")
        if severity is None and grouped is None:
            errors.append(f"category {name!r} has no severity classification")
            continue
        if severity is not None:
            if severity not in ALLOWED_SEVERITIES:
                errors.append(f"category {name!r} has unknown severity {severity!r}")
            if severity == "hard_fail":
                hard_fail_categories.append(name)
        if grouped is not None:
            for group, group_severity in grouped.items():
                if group_severity not in ALLOWED_SEVERITIES:
                    errors.append(
                        f"category {name!r} group {group!r} has unknown severity "
                        f"{group_severity!r}"
                    )

    if hard_fail_categories != ["production_commentary"]:
        errors.append(
            "only production_commentary may be a whole-category hard fail; got "
            f"{hard_fail_categories!r}"
        )

    process = detector["categories"]["process_leakage"]
    expected_process = {
        "always_fail": "hard_fail",
        "limit_one": "warn_if_repeated",
        "contextual_review": "contextual_review",
    }
    if process["severity_by_pattern_group"] != expected_process:
        errors.append(
            f"process leakage severities {process['severity_by_pattern_group']!r} do not match "
            f"{expected_process!r}"
        )
    if process.get("patterns") != process.get("always_fail"):
        errors.append("process_leakage.patterns alias drifted from always_fail")

    if detector["categories"]["broad_lexical_tells"]["severity"] != "contextual_review":
        errors.append("broad lexical tells must stay contextual_review")

    expected_thresholds = {
        "clean": {"min": 0, "max": 5},
        "needs_editing": {"min": 6, "max": 15},
        "rewrite_required": {"min": 16, "max": None},
    }
    detector_thresholds = detector["scoring"]["thresholds"]
    if detector_thresholds != expected_thresholds:
        errors.append(f"advisory thresholds changed unexpectedly: {detector_thresholds!r}")

    production_category = detector["categories"]["production_commentary"]
    production_patterns = compile_patterns(
        production_category["patterns"] + production_category.get("asset_only_patterns", [])
    )
    if "\\b(?:captured|taken|shot" not in "".join(production_category.get("asset_only_patterns", [])):
        errors.append("the tool-construction pattern must stay asset-only (hard fail in captions, review in prose)")
    process_hard_patterns = compile_patterns(process["always_fail"])
    process_repeat_patterns = compile_patterns(process["limit_one"])
    process_contextual_patterns = compile_patterns(process["contextual_review"])

    must_hard_fail = [
        ("production", "Dashboard captured with Playwright", production_patterns),
        (
            "process",
            "Weak spot: I didn't test its accuracy against the other tools.",
            process_hard_patterns,
        ),
        ("process", "Status in this study", process_hard_patterns),
        (
            "process",
            "The text browser used for this update could not open the page.",
            process_hard_patterns,
        ),
    ]
    for label, text, patterns in must_hard_fail:
        if not first_hit(text, patterns):
            errors.append(f"{label} hard-fail pattern missed {text!r}")

    must_not_hard_fail = [
        "Playwright test results showing 12 passing specs",
        "The crawler checks canonical tags and redirect chains.",
        "The text browser strips CSS and JavaScript before rendering the page.",
        "No independently verified result was available for that configuration.",
        "Access reviewed by the permissions team.",
        "Multisite behavior remains unverified, so this recommendation stays single-site.",
        "I did not test multisite, so this recommendation stays single-site.",
        "The detector flags the phrase 'here's the thing' for contextual review.",
        "The protocol needs a robust nonce implementation.",
    ]
    for text in must_not_hard_fail:
        if first_hit(text, production_patterns) or first_hit(text, process_hard_patterns):
            errors.append(f"legitimate/contextual text was classified hard-fail: {text!r}")

    boundary = "I did not test multisite, so this recommendation stays single-site."
    if not first_hit(boundary, process_repeat_patterns):
        errors.append("compact first-person claim boundary should enter repeat tracking")

    contextual_process_cases = [
        "The text browser strips CSS and JavaScript.",
        "No independently verified result was available.",
        "Access reviewed by the permissions team.",
    ]
    for text in contextual_process_cases:
        if not first_hit(text, process_contextual_patterns):
            errors.append(f"contextual process pattern missed {text!r}")

    template_threshold = detector["categories"]["templated_filler"]["repeat_threshold"]
    if template_threshold != 3:
        errors.append(f"templated filler repeat threshold changed to {template_threshold!r}")

    retired_patterns = compile_patterns(
        detector["categories"]["retired_and_secret_reveal_constructions"]["patterns"]
    )
    must_contextually_review = [
        "Here's the thing: the renewal price doubles.",
        "Here's what nobody tells you about annual plans.",
        "What no one tells you about the free tier is its export limit.",
        "The thing nobody talks about is the recovery path.",
        "This is the fee that nobody talks about.",
    ]
    for text in must_contextually_review:
        if not first_hit(text, retired_patterns):
            errors.append(f"retired/secret-reveal pattern missed {text!r}")

    contextual_must_pass = [
        "The thing most buyers miss is the renewal jump.",
        "Nobody talks during the timed section.",
        "Here is the item you ordered.",
    ]
    for text in contextual_must_pass:
        if first_hit(text, retired_patterns):
            errors.append(f"retired/secret-reveal false positive: {text!r}")

    scaffold_checks = {
        check["name"]: check
        for check in detector["categories"]["repeated_scaffolds"]["checks"]
    }
    repeated_cases = [
        (
            "mirrored_contrast",
            "It's not just faster. It's cheaper. It's not just smaller. It's easier to recover.",
            True,
        ),
        ("mirrored_contrast", "It's not just faster. It's cheaper.", False),
        (
            "rhetorical_no_triad",
            "No export. No backup. No rollback. No audit log. No owner. No recovery.",
            True,
        ),
        ("rhetorical_no_triad", "No export. No backup. No rollback.", False),
        (
            "repetitive_no_just",
            "No setup. Just use it. No export. Just copy it. No delay. Just ship it.",
            True,
        ),
        ("repetitive_no_just", "No setup. Just use it.", False),
    ]
    for name, text, should_warn in repeated_cases:
        check = scaffold_checks[name]
        count = occurrence_count(text, check)
        warned = count >= check["repeat_threshold"]
        if warned != should_warn:
            errors.append(
                f"{name} counted {count}, threshold {check['repeat_threshold']}, "
                f"warned={warned}; expected {should_warn} for {text!r}"
            )

    mirrored = scaffold_checks["mirrored_contrast"]
    if occurrence_count("The problem isn't binary. Cache invalidation has two causes.", mirrored):
        errors.append("ordinary non-mirrored contrast triggered mirrored scaffold")

    print(f"severity categories: {len(detector['categories'])}")
    print(f"hard-fail whole categories: {hard_fail_categories}")
    print(f"score thresholds: {detector_thresholds}")
    print(
        "hard-fail corpus: "
        f"{len(must_hard_fail)} must-fail, {len(must_not_hard_fail)} must-pass"
    )
    print(
        "contextual corpus: "
        f"{len(contextual_process_cases) + len(must_contextually_review)} must-review, "
        f"{len(contextual_must_pass)} must-pass"
    )
    print(f"repeat-threshold corpus: {len(repeated_cases)} cases")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: severity contract and phrase-family regressions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
