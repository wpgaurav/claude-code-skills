# Changelog

## 1.2.0 - 2026-10-24

### Fixed

- `stop-slop` is now credited to Hardik Pandya, whose [stop-slop](https://github.com/hardikpandya/stop-slop) it is based on. `NOTICE.md`, the README and the skill's frontmatter previously named Gaurav Tiwari as its sole author, while the folder's `LICENSE` was already Hardik's. The license now carries both copyright lines.

### Changed

- `stop-slop` 2.0.0: a four-tier severity model for reading matches, rules 6 to 9 (production narration, performed humanity, details with a job, leaving working prose alone), a "What I Keep" list of voice features it will not strip, extra quick checks and self-audit items, a scored pass that mirrors `slop-detector`, and "What It Won't Do." The phrase list gains retired openers, chatbot tells, listicle slop, wordy phrases and words that are not slop. The structure list gains mirrored contrasts, repeated punchlines, templated filler, production commentary, process leakage, performed humanity, template symmetry, explained implication, buried answers, over-hedging and dead table columns. Six new before/after examples, including one where the right edit is none.

## 1.1.1 - 2026-08-21

### Fixed

- `NOTICE.md` now states that the five impeccable-derived skills are near-verbatim copies of impeccable's January 2026 command files, frontmatter aside; the earlier wording credited this repository with additions that were Paul Bakaus's.
- The soft dependency line in `distill`, `quieter`, and `polish` named a `/design` command impeccable does not have; it now says `/impeccable`.

## 1.1.0 - 2026-08-21

### Added

- `slop-detector`: a new skill with a four-tier severity model (`hard_fail`, `warn_if_repeated`, `contextual_review`, `structural_diagnostic`), a 13-category `slop-detector.json`, reference files for 28 AI tells and the banned-phrase families, `scripts/scan.py` to score Markdown, HTML, or text files, `scripts/check-assets.py` for captions and alt text, and `scripts/test-severity.py` regression tests.
- `install.sh` for Claude Code, Codex, and Cursor, with per-skill selection.
- `scripts/validate.sh` and a GitHub workflow that runs it on every push and pull request.
- `NOTICE.md` and `LICENSE-APACHE-2.0` recording where each skill came from.

### Changed

- `stop-slop`: added a caption and alt-text check to the quick checks, pointed the scoring section at `slop-detector` for pass/fail, and added two before-and-after examples.
- `clarify`, `distill`, `quieter`, `polish`, `harden`: credited their origin in [impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus and relicensed the folders under Apache-2.0 to match. Replaced the hard "do not proceed until the frontend-design skill has executed" dependency with a soft "load it if installed" instruction so the skills run on their own.
- `red-pen`: credited Rich Tabor in the file and in `NOTICE.md`, and stopped claiming MIT over a folder whose upstream publishes no license.
- All skills: removed the undocumented `args` frontmatter block, added `argument-hint`, `license`, and `metadata`.
- README: corrected the article and documentation links, added origin and license columns, and documented the scanner.

## 1.0.0 - 2026-04-26

- Initial release: `stop-slop`, `red-pen`, `clarify`, `distill`, `quieter`, `polish`, `harden`.
