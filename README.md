# Claude Code Skills

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-FFDD00?style=flat&logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/gauravtiwari)

An opinionated toolkit of [Agent Skills](https://code.claude.com/docs/en/skills) for fighting AI slop in copy, design, and code.

Each folder is a self-contained skill: a `SKILL.md` with instructions, plus reference files and scripts where they earn their place. The files are plain Markdown and Python, so they work in Claude Code, Codex, Cursor, and any agent that reads a `SKILL.md`.

## Skills

| Skill | What it does | Origin | License |
|---|---|---|---|
| [stop-slop](./stop-slop) | Five drafting rules that remove predictable AI writing patterns: filler phrases, formulaic structures, metronomic rhythm, hand-holding, and pull-quote sentences. | Gaurav Tiwari | MIT |
| [slop-detector](./slop-detector) | Scores a draft or page against a four-tier severity model. Exact production narration fails outright, rhetorical scaffolds warn when repeated, lexical tells become review prompts, and document-level patterns are diagnosed. Ships a scanner, a caption linter, and regression tests. | Gaurav Tiwari | MIT |
| [red-pen](./red-pen) | Strict line editor built on Orwell's "Politics and the English Language" and Butterick's *Practical Typography*. Returns marked-up issues with a reason per change. | [Rich Tabor](https://github.com/richtabor/agent-skills) | See [NOTICE.md](./NOTICE.md) |
| [clarify](./clarify) | Rewrites UX copy: button labels, error messages, helper text, empty states. Says what happened, what to do next, and cuts the rest. | Adapted from [impeccable](https://github.com/pbakaus/impeccable) | Apache-2.0 |
| [distill](./distill) | Strips a design to its essence. The default mode of a model doing UI is to add; this skill subtracts. | Adapted from impeccable | Apache-2.0 |
| [quieter](./quieter) | Tones down loud designs without flattening them: lower saturation, looser spacing, lighter weight. | Adapted from impeccable | Apache-2.0 |
| [polish](./polish) | Final pass before a UI ships: spacing, alignment, radii, hover and focus states, the small bugs that expose a rushed build. | Adapted from impeccable | Apache-2.0 |
| [harden](./harden) | Makes interfaces survive real use: long text, RTL, missing data, slow networks, error states, keyboard and screen-reader access. | Adapted from impeccable | Apache-2.0 |

## Install

### With the installer

```bash
git clone https://github.com/wpgaurav/claude-code-skills.git
cd claude-code-skills
./install.sh claude                      # every skill into ~/.claude/skills/
./install.sh claude stop-slop slop-detector
./install.sh codex                       # ~/.codex/skills/
./install.sh cursor                      # ~/.cursor/skills/
```

Set `SKILLS_INSTALL_DIR` to install somewhere else. The installer copies folders; it never touches skills it was not asked to install.

### With symlinks

```bash
git clone https://github.com/wpgaurav/claude-code-skills ~/claude-code-skills
for s in stop-slop slop-detector red-pen clarify distill quieter polish harden; do
  ln -s ~/claude-code-skills/$s ~/.claude/skills/$s
done
```

Symlinks track the repository, so `git pull` updates every skill.

### Other agents

Point the agent at the folder's `SKILL.md`. For project-level use, add a line to the nearest agent instruction file:

```markdown
Before delivering prose, follow ./claude-code-skills/stop-slop/SKILL.md.
Before publishing, score the draft with ./claude-code-skills/slop-detector/scripts/scan.py.
```

Restart Claude Code after installing. Invoke a skill with its slash command (`/stop-slop`, `/slop-detector`, `/clarify`) or by asking for the job ("clean up this prose", "score this for AI tells", "review this error message").

## Score a file

```bash
python3 slop-detector/scripts/scan.py draft.md
```

```text
hard_fail (1)
  - production_commentary: 'captured with Playwright'  [block 14, figcaption]

warn_if_repeated (1)
  - repeated_scaffolds/mirrored_contrast: "It's not just faster. It's cheaper."  +2
      3 occurrences, threshold 2

contextual_review (4)
  - broad_lexical_tells: 'robust'  [block 9, body_prose]
  ...

HARD FAIL: 1 blocking construction(s). Rewrite before publishing; the score below cannot rescue them.
Advisory score from automatic findings: 2 (clean)
Ceiling if every contextual prompt is confirmed: 6 (needs editing). Review the 4 prompt(s) in context.
```

Matches inside quotation marks, blockquotes, and code are downgraded to review prompts, because a sentence that discusses "leverage" is not a sentence that leverages. `--json` gives machine-readable output, `--fail-on needs_editing` makes the exit code stricter for CI, and `slop-detector/scripts/check-assets.py` checks only captions and alt text.

## Why these exist

A cold draft from any model is a smooth, confident, context-free paragraph. The first design is a gradient mesh and three pricing cards. The first commit is happy-path only. Each skill here is a checklist that runs before that output reaches you.

The rationale and worked examples are in [Stop Slop Skill: 5 Rules I Use to Remove AI Slop](https://gauravtiwari.org/stop-slop-ai-slop/). The design-side companion, [design-slop](https://github.com/wpgaurav/design-slop), lives in its own repository.

## Development

```bash
./scripts/validate.sh                       # frontmatter, links, private-path gate, tests
python3 slop-detector/scripts/test-severity.py
```

The GitHub workflow runs the same validation on every push and pull request.

## Contributing

Pull requests welcome. The bar is the one the skills enforce: short, opinionated, immediately actionable. A new detector pattern needs a must-fail and a must-pass case in `test-severity.py`. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Support This Project

These free skills catch AI slop in copy, design and code, using plain Markdown and Python files that work in Claude Code, Codex and Cursor. I wrote stop-slop and slop-detector, and a GitHub workflow validates the whole repo and runs its tests on every push.

You can buy me a coffee if slop-detector flagged an AI tell in one of your drafts before your readers saw it.

<a href="https://buymeacoffee.com/gauravtiwari"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy me a coffee" height="50"></a>

A star is welcome, and when you find an AI tell the detector misses, a pull request with the pattern plus its must-fail and must-pass cases is the most useful thing you can send.

## License and attribution

`stop-slop`, `slop-detector`, and the repository scaffolding are MIT ([LICENSE](./LICENSE)). The five impeccable-derived skills are Apache-2.0 ([LICENSE-APACHE-2.0](./LICENSE-APACHE-2.0)). `red-pen` is Rich Tabor's work, redistributed with attribution and without a license grant. Details in [NOTICE.md](./NOTICE.md).
