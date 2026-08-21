---
name: stop-slop
description: Remove AI writing patterns from prose. Use when drafting, editing, or reviewing text to eliminate predictable AI tells.
argument-hint: "[text or file]"
license: MIT
metadata:
  version: 1.1.0
  author: Gaurav Tiwari
---
# Stop Slop

Eliminate predictable AI writing patterns from prose.

## Core Rules

1. **Cut filler phrases.** Remove throat-clearing openers and emphasis crutches. See [references/phrases.md](references/phrases.md).

2. **Break formulaic structures.** Avoid binary contrasts, dramatic fragmentation, rhetorical setups. See [references/structures.md](references/structures.md).

3. **Vary rhythm.** Mix sentence lengths. Two items beat three. End paragraphs differently.

4. **Trust readers.** State facts directly. Skip softening, justification, hand-holding.

5. **Cut quotables.** If it sounds like a pull-quote, rewrite it.

## Quick Checks

Before delivering prose:

- Three consecutive sentences match length? Break one.
- Paragraph ends with punchy one-liner? Vary it.
- Em-dash before a reveal? Remove it.
- Explaining a metaphor? Trust it to land.
- Same concept called three different names? Pick one and repeat it.
- "Serves as" or "stands as" where "is" works? Use "is."
- Stacked "from X to Y" ranges? Pick one specific example.
- Closing paragraph could apply to any article? Make it specific.
- Caption or alt text explains how the image was made, or why it beats a stock photo? Replace it with what the image shows, or remove it.

## Self-Audit (Final Pass)

After writing, ask: **"What makes this obviously AI-generated?"** Read every paragraph looking for:

1. Synonym cycling (same thing, different words each time)
2. -ing gerund clusters (highlighting, showcasing, fostering)
3. Significance inflation (testament, pivotal, transformative)
4. False comprehensiveness (from X to Y, whether A or B)
5. Generic optimistic closing

Fix every instance found. Then read once more.

## Scoring

Rate 1-10 on each dimension:

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |

Below 35/50: revise.

This grid is a quick self-check, not a gate. For a scored audit with severity tiers, run the sibling [slop-detector](../slop-detector) skill: exact production-narration constructions fail outright, broad lexical matches only prompt review, and the advisory score (0 to 5 clean, 6 to 15 needs editing, 16+ rewrite) decides pass or fail.

## Examples

See [references/examples.md](references/examples.md) for before/after transformations.

## License

MIT
