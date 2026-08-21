# Notices and attribution

This repository collects Agent Skills from three sources. Each folder's `SKILL.md` frontmatter names its license; this file explains the provenance so nothing here reads as more original than it is.

## Written here (MIT)

- `stop-slop` by Gaurav Tiwari.
- `slop-detector` by Gaurav Tiwari. The severity model, `slop-detector.json`, the reference files, and the scripts were built for a private publishing system and released here after removing site-specific references.
- Repository scaffolding: `install.sh`, `scripts/`, the GitHub workflow, and this documentation.

Covered by [LICENSE](./LICENSE).

## Adapted from impeccable (Apache License 2.0)

- `clarify`, `distill`, `quieter`, `polish`, `harden`

These five skills are derived from the command references in [impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus, used under the Apache License 2.0. A copy of that license is in [LICENSE-APACHE-2.0](./LICENSE-APACHE-2.0).

Changes made in this repository: added standalone `SKILL.md` frontmatter so each command works as its own Claude Code skill; added a context-gathering preamble and an explicit stop-and-ask step; replaced the hard dependency on impeccable's design-guideline loader with a soft "load it if installed" instruction so the skills run without the parent project; and light copy edits. The underlying method, checklists, and examples remain Paul Bakaus's work. These folders stay under Apache-2.0; the MIT license of this repository does not cover them.

## Red Pen by Rich Tabor (no upstream license)

- `red-pen`

`red-pen` is [Rich Tabor's skill](https://github.com/richtabor/agent-skills/tree/main/skills/red-pen), redistributed here with attribution. The only changes are the attribution note under the title and the frontmatter metadata. The upstream repository does not publish a license file, so this folder is **not** covered by this repository's MIT license and no license is granted for it here. If you need license terms for red-pen, ask the author. If you prefer to install it from the source, run `npx skills add richtabor/agent-skills`.

## Reference works cited inside the skills

- George Orwell, "Politics and the English Language" (1946), cited by `red-pen`.
- Matthew Butterick, *Practical Typography*, cited by `red-pen`.
