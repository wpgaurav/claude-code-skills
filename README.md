# Claude Code Skills

A small, opinionated toolkit of [Claude Code Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) for fighting AI slop in design, code, and copy.

Each folder is a self-contained skill. Drop the folder into your `~/.claude/skills/` directory and Claude Code auto-discovers it on the next session. All skills are MIT-licensed.

## Skills in this repo

| Skill | What it does |
|---|---|
| [stop-slop](./stop-slop) | Removes predictable AI writing patterns from prose. Banned-phrase list, structural anti-patterns, rhythm rules, and a 1-10 self-audit grid. |
| [red-pen](./red-pen) | Strict editorial reviewer. Applies principles from George Orwell's *Politics and the English Language* and Matthew Butterick's *Practical Typography*. Returns line-by-line edits with justifications. |
| [clarify](./clarify) | Improves UX copy: button labels, error messages, microcopy, form helper text, empty states. Tells the user what happened, what to do next, and cuts the rest. |
| [distill](./distill) | Strips designs to their essence. Removes unnecessary visual complexity. Default mode of LLM UI generation is to add; this skill subtracts. |
| [quieter](./quieter) | Tones down overly bold or visually aggressive designs. Reduces saturation, loosens spacing, drops a font weight. |
| [polish](./polish) | Final quality pass before shipping. Catches inconsistent spacing, off-by-one alignment, mismatched border radii, missing hover states. |
| [harden](./harden) | Makes UI and code production-ready: long-text overflow, RTL layouts, missing data, slow networks, error states, keyboard and screen-reader accessibility. |

## Installation

```bash
git clone https://github.com/wpgaurav/claude-code-skills ~/claude-code-skills
ln -s ~/claude-code-skills/stop-slop ~/.claude/skills/stop-slop
ln -s ~/claude-code-skills/red-pen   ~/.claude/skills/red-pen
ln -s ~/claude-code-skills/clarify   ~/.claude/skills/clarify
ln -s ~/claude-code-skills/distill   ~/.claude/skills/distill
ln -s ~/claude-code-skills/quieter   ~/.claude/skills/quieter
ln -s ~/claude-code-skills/polish    ~/.claude/skills/polish
ln -s ~/claude-code-skills/harden    ~/.claude/skills/harden
```

Or copy individual folders into `~/.claude/skills/` directly.

Restart Claude Code, then invoke a skill via slash command (`/stop-slop`, `/clarify`, etc.) or trigger it implicitly by asking for the relevant job ("clean up this prose", "review this UX copy", "polish this layout").

## Why these exist

The first draft of any LLM is a smooth, confident, context-free paragraph that reads like a LinkedIn post written by someone who's never met you. The first design is a gradient mesh and three pricing cards. The first code commit is happy-path only.

Each of these skills is a checklist that runs before the cold output reaches you, so you ship work that doesn't need an extra hour of editing. Read more on the rationale at [gauravtiwari.org/stop-slop](https://gauravtiwari.org/stop-slop/).

## Contributing

Pull requests welcome. The criterion for accepting an addition is the same criterion the skills enforce: short, opinionated, and immediately actionable. If a rule needs more than three sentences to explain, it probably isn't a rule yet.

## License

MIT. See [LICENSE](./LICENSE).
