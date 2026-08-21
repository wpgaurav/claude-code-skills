# AI Tells: How AI Writing Betrays Itself

Use this as a diagnostic checklist. A tell is evidence to inspect, not proof that a passage was AI-generated. Confirm the pattern in context before scoring or rewriting it.

Every illustrative sentence in this file is a pattern or an anti-example. None of them records a real result, price, test, purchase, preference, or biography, and none may be reused as published copy.

## Severity Model

`slop-detector.json` in the skill root is the machine-readable authority:

- **`hard_fail`:** exact high-confidence production/process constructions only. These block publication and are not scored.
- **`warn_if_repeated`:** one occurrence may be intentional; warn only when the family crosses its repeat threshold.
- **`contextual_review`:** lexical or sentence-level signal. Check quotation, code, proper-name, technical, and evidence context before editing.
- **`structural_diagnostic`:** document-level heuristic. Diagnose the cause; never manufacture roughness or personality to clear it.

Truth, provenance, source fidelity, and authorial intention remain separate publication gates. A clean slop score cannot rescue an unsupported claim or invented experience.

## Structural Tells

### 1. The Perfect Three-Part List
Model-shaped prose often defaults to groups of three with identical sentence structures. One evidence-led triad is not a defect; repetition is the signal.

**AI pattern:**
> - Streamline your workflow
> - Enhance your productivity
> - Transform your results

**Human pattern:**
> It saves about 2 hours a week on repetitive tasks. The dashboard is cleaner than what I was using before. And honestly, the reporting alone justified the $49/month.

### 2. The Symmetric Pros/Cons
Every pro has a perfectly matched con. Review whether the symmetry came from the evidence or from the template.

**AI pattern:** 3 pros, 3 cons, each roughly the same length.
**Human pattern:** 5 things you love, 2 things that bug you, one of which you've worked around.

### 3. The Comprehensive Coverage Syndrome
Model-shaped drafts often try to cover every angle. Strong editorial judgment makes priorities visible and skips what does not matter.

**AI pattern:** "There are several aspects to consider: performance, pricing, ease of use, customer support, integration capabilities, and scalability."
**Human pattern:** "Two things matter here: speed and price. Everything else is a bonus."

### 4. Identical Paragraph Lengths
Model-shaped drafts can settle into suspiciously similar paragraph lengths. Treat uniformity as a document-level diagnostic, not an instruction to add arbitrary short paragraphs.

**Test:** Inspect a sustained run of similarly shaped paragraphs and ask whether
the thought actually needs that repetition. Uniformity may be correct in a
reference or procedure. Fix it only when it flattens emphasis or comprehension;
never insert one-sentence punches to imitate a distribution.

### 5. The Robotic Introduction
Model-shaped openings often begin with generic context-setting. Lead with the point when the format and reader intent support it.

**AI pattern:** "[Topic] has become increasingly important in recent years. As businesses continue to evolve, understanding [topic] is crucial for success."
**Human pattern:** "The second caching plugin didn't make the site faster. It made the cart unreliable because both plugins tried to own the same response."

## Language Tells

### 6. Over-hedging
Model-shaped prose often stacks hedges until no usable judgment remains. Keep uncertainty that changes the claim boundary.

**AI:** "While there are many factors to consider, it might be worth exploring whether this could potentially work for your specific use case."
**Human:** "This works for a single-site blog. Multisite behavior is still unverified, so don't extend the recommendation to a network install."

### 7. Connector Words From Academic Papers
Repeated academic connectors can make conversational prose sound staged. They remain valid in quotations, formal registers, and sentences where they are the precise transition.

### 8. The Passive Epidemic
AI defaults to passive voice to avoid taking a stance.

**AI:** "It has been observed that performance can be improved..."
**Human:** "TTFB fell 40% under the same workload because the repeated database query moved into memory."

### 9. Perfectly Balanced Arguments
AI presents both sides as equally valid. Humans have preferences.

**AI:** "Both WordPress and Webflow are excellent platforms with their own strengths and weaknesses."
**Human:** "WordPress wins. Here's why, and here's the one scenario where I'd pick Webflow instead."

### 10. Empty Superlatives
AI throws in "incredible," "amazing," "powerful" without evidence.

**AI:** "This incredible tool offers an amazing set of powerful features."
**Human:** "It cut my build time from 45 seconds to 8. That's the feature that matters."

## Rhythm Tells

### 11. Monotonous Sentence Length
Model-shaped copy can cluster too many sentences in the same middle-length band. Diagnose monotony across several paragraphs rather than treating any word-count range as proof.

**Human rhythm:** Short. Then medium. Then a longer sentence that builds on the idea and provides the detail readers need. Then short again.

### 12. Uniform Sentence Band

A long piece whose sentences all occupy the same middle-length band may feel mechanical. The absence of fragments alone is not a defect, and fragments are never a humanity requirement.

**Diagnostic:** Read for monotonous sentence shape across several paragraphs. If the thought naturally needs a blunt landing, use one. Do not insert "Not even close" or "Nope" merely to vary the metric.

### 13. Performed Interruptions

Models now insert interruptions to perform spontaneity. A real interruption follows a genuine change in thought or evidence; a decorative one only roughens the surface.

> I was going to recommend WP Rocket, but then I checked the pricing. $99/year for one site? When FlyingPress does the same thing for $60? Pass.

### 14. Performed Corrections or Pivots

A correction is useful only when the source or current work contains a real change of mind. "Actually," "wait," and "scratch that" become model tells when they are invented for texture.

> Managed hosting sounds like the obvious answer. Actually, no. Under the same traffic and cache policy, a well-configured $7 VPS can beat a $30/month managed host.

## Content Tells

### Production-Commentary Tell

AI-written captions often explain why an image was selected: "fresh capture," "not a generic mockup," or "a real screenshot beats a stock photo." Human editorial copy names the interface, action, number, or evidence and stops. Never mention Playwright, renderers, prompts, generation tools, stock alternatives, or the choice to avoid a mockup in reader-facing copy.

**Test:** Delete every clause about how the asset was made or why another visual would have been worse. If nothing factual remains, omit the caption.

### Process-Leakage Tell

The same instinct escapes the caption and gets into the article. The writer narrates the research, setup, tests, and validation: which tools were queried, what accounts were available, what was installed, which page failed, which cache was purged, and which environment versions happened to be present. It feels like rigor. It reads as an apology or a lab notebook.

**Human editorial copy states the result and a decision-relevant boundary.** AI-shaped copy repeats per-item confessions and eventually builds a table column out of them.

**AI:** "Weak spot: I didn't independently score its accuracy against the other paid tools."
**Human:** "Weak spot: daily tracking costs more than the default setup."

**AI:** a "Status in this study" column reading "Feature review only" in 9 of 12 rows.
**Human:** no such column. Either the comparison excludes the score or one compact criteria note states that unmatched results are not scored.

**Test:** delete every clause about how the article, test, screenshot, or conclusion was produced. Keep only the variables needed to interpret a result. If the reader loses no decision-relevant information, the clause stays deleted.

### Template-Filler Tell

Roundup items generated from one shape carry a sentence that fits any item, so it informs about none. On one site, 21 book roundups each closed all 10 entries with the same 4 sentences.

**AI:** "That makes the book useful when your immediate goal matches its teaching style, not merely because the title is popular."
**Human:** "Skip it if you already own Strang. The overlap is most of the first six chapters."

**Test:** swap another item's name into the sentence. If it still reads correctly, it carries no information.

### 15. Vague or Decorative Numbers
AI defaults to vague descriptors, then overcorrects with arbitrary counts and versions. Human writing uses a number only when it gives scale, comparison, a threshold, or a decision boundary.

**AI:** "significantly improved performance"
**Human:** "TTFB dropped from 1.2s to 0.18s"

### 16. Compulsory Personal Mistakes
AI often inserts a tidy first-person mistake because a template demands vulnerability. A real mistake belongs only when it changes the warning or solution.

> Two caching layers can both work in isolation and still corrupt cart behavior together. Use one page-cache owner.

### 17. No Trade-off Acknowledgment
AI presents features as pure positives. Humans know everything has a cost.

> Redis is amazing for performance. It also means one more service to monitor, one more thing that can fail at 3am, and one more configuration to back up.

### 18. Generic Examples
AI uses fake or generic examples. Humans reference real products, real numbers, real situations.

**AI:** "For example, a small business might see improved results."
**Human:** "My client's WooCommerce store went from 12 orders/day to 23 after we fixed the checkout speed. That's a $2,400/month difference."

### 19. Uniform Emotional Temperature
A piece can feel flat when its subject contains a real consequence but the prose never registers it. Absence of an emotional spike is not itself a defect; do not invent excitement, frustration, or surprise for texture.

> Look, I've tried to like Elementor. I really have. Five separate attempts over four years. And every time, I end up back at GenerateBlocks because the output is just... cleaner.

### 20. The "Comprehensive" Trap
AI tries to be exhaustive. Humans curate ruthlessly.

**AI approach:** Cover 15 caching plugins with a paragraph each.
**Human approach:** Cover the 3 that matter. Mention 2 others briefly. Ignore the rest because they're not worth your time.

## Authorial Intention Tells

These failures can survive a normal anti-slop pass because the prose looks varied and specific. The missing element is a reason for the variation or specificity.

### Simulated roughness

Random fragments, typos, fake self-corrections, arbitrary paragraph lengths, and decorative asides are added to make polished prose appear human. None of them follows thought, pressure, source material, or character.

**Fix:** Remove the performance. Let rhythm change only when importance, difficulty, emotion, or the source changes.

### Consequence-free detail

A version, object, color, number, anecdote, or local detail appears specific but changes nothing in the argument, decision, mood, verification, or next action.

**Fix:** Give the detail a job or cut it.

### Explained implication

The draft shows the evidence, image, or action, then states the meaning again because it does not trust the reader.

**Fix:** Keep the evidence and one necessary practical consequence. Delete the redundant explanation.

### Template symmetry

Every option, objection, chapter, or example receives equal space even though they do not matter equally.

**Fix:** Let priority become visible. Spend space where the decision, difficulty, or emotional weight lives.

## Teaching Anti-Tells

These are the tells specific to explaining and teaching. A passage can pass every tell above and still fail here, because it's a smart person who isn't actually teaching. When you hit one, the fix is a teaching move, not a phrase swap.

### 25. The Slop-Teacher (labels instead of teaches)
States that things matter without showing why. Stacks disconnected one-line labels and calls it explanation. Restates one idea three different ways instead of demonstrating it once. Hides behind "it's important to note," "a great way to," "extremely easy."

**AI pattern (real anti-example):**
> Two qubits can become entangled, so changing one instantly affects the other, even if they're far apart. This allows powerful coordination between qubits, boosting performance. Entangled qubits work together, sharing states instantly. This drastically boosts computing power. Essential for quantum algorithms.

That says "boosts power" three ways with no example, no analogy, no person talking.

**AI pattern (real anti-example):**
> Widgets are a great way to add content and additional features to your website. They make it extremely easy for you to simply drag and drop several elements.

Empty intensifiers, no specifics, nothing a learner can do or picture. **Test:** if a paragraph could describe any topic, it teaches none.
**Fix:** Show one worked example, and name the term then translate it in the same breath. Demonstrate once instead of asserting three times.

### 26. The Condescending Teacher (talks down)
Uses cutesy filler and verbal tics to perform approachability while actually patronizing. Treats the reader as slow rather than new.

**AI pattern (real anti-example):**
> Definition time. ... Fire point: ... Happy?

"Happy?" condescends. The interjections stand in for substance. The reader isn't a child to be jollied along.
**Human pattern (real):**
> If you got 5000, you're in good company. Most people do. And most people are wrong. The correct answer is 4100. Go back and check.

That respects the reader because it immediately shows the why. **Fix:** assume intelligence, supply only the missing information. Name a confusion as common ("this trips up almost everyone") instead of jollying the reader along.

### 27. The Showing-Off Teacher (writes to look smart)
Uses the locked-out technical register. Defaults to passive voice. Skips the obvious step because explaining it would feel beneath them. Never audits an analogy, because that would admit a limit.

**AI pattern (real anti-example):**
> The cellular organization gives rise to a plethora of physiological, biochemical, and behavioral processes that lead to the genesis of life itself.

Inflated nouns, passive voice, zero concrete image, no reader in the room.

**AI pattern (real anti-example):**
> Soon after 1900, it was shown by scientists that the air in an ionization chamber, which was completely protected against penetration of α, β and γ rays by surrounding it with thick lead walls, was still conductive.

One serpentine passive-voice sentence, no narrative, no signpost of why it matters. The opposite of "let me show you."
**Fix:** Name the term, then translate it, and don't skip the obvious step. The showoff knows the term and stops. The teacher knows the term and translates it.

### 28. The Salesman in Teacher's Clothing (asserts excitement instead of earning it)
Stacks superlatives. Promises payoff with no proof. Asserts excitement instead of building understanding.

**AI pattern (real anti-example):**
> affiliate marketing is the most popular and the highest yielding online money-making marketing strategy. ... If done properly, you won't even need to bother around for a job in your whole life.

Hype and unbacked superlatives, no evidence, no nuance. It sells. It doesn't teach.
**Human pattern:** opinion, then relevant evidence, then the impact the reader couldn't see. "FlyingPress cut LCP from 3.2s to 0.8s on the same page" is a stance with proof. "the highest yielding strategy" is a stance with a megaphone.
**Fix:** every strong stance gets relevant evidence behind it. That may be a number, fair comparison, mechanism, observed behavior, or source.

## Search and Citation Diagnostics

Citation behavior differs by query, system, retrieval mode, and date. The checks
below improve clarity and support, but none is a guaranteed ranking or citation
factor. A style tell does not by itself mean a page will fail search or answer
engines.

### 21. Zero Information Gain
Every section restates what competitors already say. No first-party data, no original testing, no unique insight.

**AI pattern:** "WordPress is a popular CMS used by millions of websites worldwide. It offers many plugins for various needs."
**Human pattern:** "Across 12 matched VPS instances over 30 days, FlyingPress's median TTFB was 38ms lower than WP Rocket's."

### 22. Low Entity Precision
Generic descriptions can hide which product, source, policy, or measurement a
claim concerns. Name an entity only when it improves precision, verification, or
the reader's decision. Entity density is not a target.

**AI pattern:** "Several popular hosting providers offer managed WordPress solutions at competitive prices."
**Human pattern:** "Cloudways starts at $14/month, Kinsta at $35/month, and a Hetzner VPS with CloudPanel costs $7/month. The price gap buys support and convenience, not automatically faster origins."

### 23. Buried Answer
Search-led decision sections can bury the useful answer beneath hedging and
background. Move it earlier when the matching format and query intent call for
that movement. Narrative, source-led, exploratory, and some teaching sections
may need context or demonstration first.

**AI pattern:** "When considering the best caching plugin, there are many factors to evaluate, including performance, ease of use, and price."
**Human pattern:** "FlyingPress is the stronger speed-first choice at $60/year, about 40% less than WP Rocket. WP Rocket remains easier for users who want conservative defaults."

### 24. Unwarranted Sentence Temperature
Emotion can become mechanical when every section receives the same excitement,
frustration, or dry aside. A quiet technical piece may need no emotional turn.

**Test:** Check whether each reaction follows a source-backed event or a real
reader consequence. Remove evenly distributed personality beats that have no
cause; never add emotion because a passage is neutral.

## The Detection Formula

Do not score raw string hits. First remove false positives from quotations, code, proper names, precise technical language, and evidence-bearing sentences. Exact `hard_fail` matches block independently and receive no points.

Score only confirmed advisory findings:

| Severity | Points |
|---|---:|
| `warn_if_repeated` after its threshold | +2 |
| confirmed `contextual_review` finding | +1 |
| high-priority `structural_diagnostic` | +3 |
| medium-priority `structural_diagnostic` | +2 |
| low-priority `structural_diagnostic` | +1 |

The thresholds match `slop-detector.json`:

- **0–5:** clean after contextual review
- **6–15:** needs editing
- **16+:** rewrite the affected passages or structure

The score estimates editorial cleanup. It does not identify authorship, and it cannot override truth, source fidelity, or authorial-intention failures.

## The Fix

For every confirmed tell, fix the underlying cause rather than mechanically applying the opposite:

1. Monotonous rhythm -> Follow the thought; vary sentence shape only where explanation, pressure, or judgment earns it
2. No opinions -> Pick a side
3. Passive voice -> Name the actor or mechanism that matters
4. Vague claims -> Add relevant evidence; use a number only when it changes scale or the decision
5. Perfect balance -> Show your actual preference
6. Generic prose -> Add a specific observation, comparison, interaction, or human consequence; do not force a story
7. Academic connectors -> Simplify when meaning and rhythm improve; preserve precise or quoted language
8. Empty superlatives -> Replace with evidence
9. Zero information gain -> Add observed behavior, a fair comparison, mechanism, decision rule, or source-backed fact
10. Low entity precision -> Name only the tools, prices, metrics, dates, or versions that improve the answer
11. Buried answer -> Lead with the answer when the format and reader intent require it
12. Uniform temperature -> Check whether the subject warrants an emotional turn; never add one as decoration
13. Labels instead of teaches -> Show one worked example; name then translate the term
14. Cutesy condescension -> Assume intelligence; "this trips up everyone" instead of "Happy?"
15. Show-off register -> Translate the term, don't just name it; cut passive voice
16. Unbacked superlatives -> Replace the label with relevant evidence, which may be a fair comparison, mechanism, observed behavior, or verified number
17. Simulated roughness -> Remove the tic; let structure follow thought, pressure, or source
18. Consequence-free detail -> Give the detail a job or cut it
19. Explained implication -> Trust the reader after the evidence lands
20. Template symmetry -> Spend space according to importance and difficulty
