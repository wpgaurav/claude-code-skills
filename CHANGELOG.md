# Changelog

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
