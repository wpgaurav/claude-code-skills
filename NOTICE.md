# Notices and attribution

This repository collects Agent Skills from four sources. Each folder's `SKILL.md` frontmatter names its license; this file explains the provenance so nothing here reads as more original than it is.

## Written here (MIT)

- `slop-detector` by Gaurav Tiwari. The severity model, `slop-detector.json`, the reference files, and the scripts were built for a private publishing system and released here after removing site-specific references.
- Repository scaffolding: `install.sh`, `scripts/`, the GitHub workflow, and this documentation.

Covered by [LICENSE](./LICENSE).

## Stop Slop, based on Hardik Pandya's original (MIT)

- `stop-slop`

`stop-slop` is based on [stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya (MIT, Copyright (c) 2025 Hardik Pandya), first published on 2026-01-11. Earlier versions of this repository credited it to Gaurav Tiwari alone. That was wrong, and it is corrected as of version 1.2.0.

What is Hardik's: the five core rules, the first four quick checks, the five-dimension scoring grid, the original sections of `references/phrases.md` (throat-clearing openers, emphasis crutches, business jargon, filler adverbs, meta-commentary) and `references/structures.md` (binary contrasts, dramatic fragmentation, rhetorical setups, formulaic constructions, rhythm patterns), and examples 1 to 5.

What Gaurav Tiwari added: the severity model ("How I Read a Match"), rules 6 to 9, "What I Keep," the self-audit, the scored pass, "What It Won't Do," the remaining quick checks, the other sections of both reference files, and examples 6 to 13. Example 4's em dash became a colon. The folder's [LICENSE](./stop-slop/LICENSE) carries both copyright lines, and the whole skill is MIT.

## Adapted from impeccable (Apache License 2.0)

- `clarify`, `distill`, `quieter`, `polish`, `harden`

These five skills are derived from the command references in [impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus, used under the Apache License 2.0. A copy of that license is in [LICENSE-APACHE-2.0](./LICENSE-APACHE-2.0).

The body text of each skill is Paul Bakaus's, taken nearly verbatim from impeccable's `.claude/commands/*.md` files as they stood in January 2026, including the context-gathering preamble and the stop-and-ask step. Changes made in this repository: standalone `SKILL.md` frontmatter so each command works as its own Claude Code skill; on 2026-08-21, the hard "do not proceed until the frontend-design skill has executed" dependency was replaced with a soft "load it if installed" instruction so the skills run without a companion project; and an attribution note. The method, checklists, and examples remain Paul Bakaus's work. These folders stay under Apache-2.0; the MIT license of this repository does not cover them. impeccable itself is at [impeccable.style](https://impeccable.style).

## Red Pen by Rich Tabor (no upstream license)

- `red-pen`

`red-pen` is [Rich Tabor's skill](https://github.com/richtabor/agent-skills/tree/main/skills/red-pen), redistributed here with attribution. The only changes are the attribution note under the title and the frontmatter metadata. The upstream repository does not publish a license file, so this folder is **not** covered by this repository's MIT license and no license is granted for it here. If you need license terms for red-pen, ask the author. If you prefer to install it from the source, run `npx skills add richtabor/agent-skills`.

## Reference works cited inside the skills

- George Orwell, "Politics and the English Language" (1946), cited by `red-pen`.
- Matthew Butterick, *Practical Typography*, cited by `red-pen`.
