---
name: slop-detector
description: Score a draft, page, or caption set for AI slop with a four-tier severity model instead of a flat banned-words list. Exact production narration fails outright, rhetorical scaffolds warn only when repeated, lexical tells become review prompts, and document-level patterns are diagnosed. Use when the user asks to score, audit, grade, or check text for AI tells, runs /slop-detector, or wants a pass/fail gate before publishing.
argument-hint: "[file]"
license: MIT
metadata:
  version: 1.0.0
  author: Gaurav Tiwari
---

# Slop Detector

Audit prose for AI slop and report findings by severity. Stop Slop tells a model what not to write; this skill checks what was written and says how bad it is.

A banned-words list fails in both directions. It flags "robust" in a sentence about a nonce implementation, and it passes a caption that says "a fresh capture, not a generic mockup." The severity model below separates the two.

## Severity model

`slop-detector.json` in this folder is the authority. Four tiers:

| Severity | Meaning | What to do |
|---|---|---|
| `hard_fail` | Exact, high-confidence production or process narration in reader-facing copy ("captured with Playwright", "Status in this study", "Weak spot: I didn't test") | Block publication and rewrite. A low score never rescues a hard fail. |
| `warn_if_repeated` | Rhetorical scaffolds that can carry one real turn: mirrored "not X, it's Y" contrasts, "No X. No Y. No Z." triads, per-item disclaimers, templated roundup filler | Count across the piece. Warn only at the family's repeat threshold. |
| `contextual_review` | Broad lexical signals: "leverage", "seamless", "here's the thing", academic connectors, empty intensifiers | Read the sentence. Quotations, code, proper names, and precise technical terms are not defects. Never auto-replace. |
| `structural_diagnostic` | Document-level patterns: identical paragraph lengths, a dead table column, the same sentence closing every item, passive-voice density | Diagnose the cause. Never add fragments, emotion, or asymmetry to make a metric pass. |

Advisory score, counted only after context review: `warn_if_repeated` +2, confirmed `contextual_review` +1, `structural_diagnostic` +3, +2, or +1 by priority.

- **0 to 5:** clean
- **6 to 15:** needs editing
- **16+:** rewrite the affected passages or structure

Truth, source fidelity, and authorial intention sit above this model. An unsupported claim or invented first-person experience blocks publication even when the score is 0.

## Workflow

1. **If the text is a file on disk, run the scanner first.**

   ```bash
   python3 scripts/scan.py draft.md
   python3 scripts/scan.py post.html --json
   python3 scripts/scan.py a.md b.md c.md     # adds the sibling-boilerplate check
   ```

   It prints hard fails, warnings, structural findings, and contextual prompts, then two numbers: the score from automatic findings and the ceiling if every contextual prompt is confirmed. Matches inside quotation marks, blockquotes, and code are downgraded to `contextual_review` automatically.

2. **Review every contextual prompt in context.** Keep the word when it is quoted, a product name, a technical term, or the precise word. Confirm it only when the sentence would be better without it. Recompute the score from confirmed findings.

3. **Run the structural checks the scanner cannot.** Symmetric pros and cons, an FAQ entry that restates an H2, and boilerplate shared across sibling articles need a reader. The scanner names these as manual checks.

4. **If there is no file, do the pass by hand.** Load [references/banned-phrases.md](references/banned-phrases.md) for the phrase families and [references/ai-tells.md](references/ai-tells.md) for the 28 structural, language, rhythm, content, and teaching tells. Apply the same four tiers.

5. **Report, then fix the cause.** For each confirmed finding give the severity, the quoted evidence, why it hurts this reader, and the smallest durable fix. Fix rhythm by following the thought, not by inserting one-word sentences. Fix a dead column by deleting it and stating the fact once. Fix a hard fail by naming what the image or result shows and nothing about how it was made.

For captions and alt text alone, `scripts/check-assets.py post.html` runs only the hard-fail production-commentary patterns and exits 1 on any hit. It is built for CI.

## Output format

```text
HARD FAIL (1)
  production_commentary: "captured with Playwright" [block 14, figcaption]
  Fix: "Semrush's affiliate program page inside Impact."

warn_if_repeated (1)  +2
  repeated_scaffolds/mirrored_contrast: 3 occurrences, threshold 2

contextual_review (4)  review before counting
  broad_lexical_tells: "robust" [block 9] -> technical term, keep
  ...

Advisory score: 2 (clean) from automatic findings; ceiling 6 (needs editing) if every prompt is confirmed.
```

Lead with the verdict. If nothing actionable is present, say so in one line.

## What this skill does not do

- It does not fact-check. A clean score says nothing about whether a price, version, or quote is true.
- It does not detect authorship. Humans write slop too, and the tells are evidence to inspect, not proof a model wrote the text.
- It does not rewrite. Pair it with `stop-slop` for drafting rules and `red-pen` for a line edit.
- It does not reward roughness. Fragments, typos, and performed asides are tells of their own (see ai-tells.md, Authorial Intention Tells).

## Regression tests

```bash
python3 scripts/test-severity.py
```

The test locks the contract: only `production_commentary` and the `always_fail` group of `process_leakage` may hard-fail, broad lexical matches stay contextual, scaffolds warn only past their thresholds, and the score bands do not drift. Run it after any edit to `slop-detector.json`.
