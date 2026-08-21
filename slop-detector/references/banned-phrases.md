# Banned Phrases

These phrases are editorial defaults, not a raw-string guilt test. Apply the severity model below before editing. A quotation, product name, technical term, legal phrase, or sentence discussing a phrase may match the same words without being defective.

## Enforcement Severity

The machine-readable source is `slop-detector.json` in the skill root. It uses one severity model:

| Severity | Meaning | What to do |
|---|---|---|
| `hard_fail` | Exact, high-confidence production or process narration in editable reader-facing copy | Block publication and rewrite. Hard fails are not rescued by a low score. |
| `warn_if_repeated` | A scaffold that may be intentional once but becomes model-shaped through repetition | Count the family across the piece and warn only at its configured threshold. |
| `contextual_review` | A broad word, phrase, or style signal with legitimate uses | Read the sentence, check quotation/code/proper-name/technical context, then keep or revise. Never auto-replace blindly. |
| `structural_diagnostic` | A document-level pattern such as symmetry, density, or duplicated structure | Diagnose why it occurred. Do not add fragments, emotion, entities, or asymmetry merely to satisfy a detector. |

Section mapping:

- **Hard fail:** the exact constructions under Production Commentary and the `always_fail` subset of Process Leakage.
- **Warn if repeated:** repetitive parallel structures, mirrored contrasts, repeated claim-boundary disclaimers, and templated per-item filler.
- **Contextual review:** lexical lists, connectors, modifiers, hype, conclusion phrases, and listicle/teaching language.
- **Structural diagnostic:** dead table columns, repeated sibling boilerplate, count mismatches, paragraph uniformity, and similar document-level patterns.

Truth and source fidelity sit above this severity model. An unsupported claim, invented first-person experience, false attribution, or source-fidelity breach blocks publication even when no slop phrase matches.

## Landscape and Journey Metaphors

**Avoid in ordinary prose; review literal and technical uses in context:**
- "In today's world/digital landscape/fast-paced world"
- "In the ever-evolving world of"
- "In this day and age"
- "Navigate" (unless actual GPS)
- "Journey" (unless actual travel)
- "Landscape" (unless actual scenery)
- "Realm," "Space" (as in "the SaaS space"), "Arena," "Sphere," "Domain" (unless technical)
- "Tapestry," "Fabric" (as in "fabric of society")

**Instead:** Be specific. "Running an online business is harder than it was five years ago. Here's what's changed."

## Throat-Clearing Phrases

Usually delete these when they only delay the point. Keep quoted language or a literal use when the sentence needs it.

- "It's important to note that"
- "It's worth mentioning"
- "It's no secret that"
- "It goes without saying"
- "Needless to say"
- "First and foremost"
- "Last but not least"
- "Without further ado"
- "Let's unpack/dive in/dive deep/break this down/explore/take a closer look/get started"
- "Here's the deal"
- "Here's what you need to know"
- "So, what exactly is [X]?"
- "But wait, there's more"
- "The short answer is... The long answer is..."
- "At the end of the day"
- "The fact of the matter is"
- "When all is said and done"
- "As we delve into"
- "In this article, we will..."
- "In this guide, you'll learn..."
- "By the end of this article..."
- "Have you ever wondered..."
- "Picture this:" / "Imagine this:"
- "What if I told you..."
- "You might be wondering..."
- "The truth is..." / "The reality is..."
- "That being said" / "Having said that" / "With that being said" / "That said"
- "Here's what nobody tells you" / "What no one tells you about..." / "The thing nobody talks about" / "...that nobody talks about" (secret-reveal framing; if the fact is genuinely underreported, show that with a source, don't announce it)

**"Here's the thing" is retired in ordinary reader-facing prose** (this supersedes the older mid-paragraph carve-out). A quotation or discussion of the phrase is contextual review, not an automatic failure. It once worked as a genuine pull-forward with an immediate payoff, but every model now leans on it, so it reads as AI even when a human types it. Cut the phrase and keep the payoff: "Math teachers love to say 'let x equal the unknown.' But nobody explains why that simple trick is so powerful. Equations are the reason we can solve problems that would take hours of guesswork in seconds."

## Corporate Buzzwords

- "Delve" / "Dive into" / "Deep dive"
- "Leverage" / "Utilize"
- "Cutting-edge" / "State-of-the-art" / "Bleeding-edge"
- "Game-changer" / "Revolutionary" / "Groundbreaking" / "Trailblazing"
- "Seamless" / "Seamlessly"
- "Robust" / "Comprehensive" / "Holistic"
- "Best practices" (say "what actually works")
- "Synergy" / "Paradigm" / "Ecosystem"
- "End-to-end" / "Turnkey" / "Scalable" (unless technical)
- "World-class" / "Industry-leading" / "Best-in-class" / "Top-tier"
- "Future-proof" / "Next-generation" / "Next-level"
- "Enterprise-grade" / "Mission-critical"
- "Thought leader" / "Value proposition" / "Core competency"
- "Low-hanging fruit" / "Move the needle" / "Circle back"
- "Bandwidth" (unless actual network) / "Pivot" / "Disrupt"
- "Solutions" (as standalone noun) / "Offerings" / "Deliverables"
- "Actionable insights" / "Data-driven" / "Results-driven"
- "Bespoke" / "Curated" / "Hand-picked" / "Carefully selected"

## Overused Verbs

- "Empower" / "Foster" / "Elevate" / "Unlock" / "Harness"
- "Supercharge" / "Streamline" / "Transform" / "Revolutionize"
- "Take to the next level" / "Level up" / "Amplify"
- "Skyrocket" / "Turbocharge" / "Accelerate" / "Maximize"
- "Boost" / "Propel" / "Fuel" (as in "fuel growth")
- "Drive" (as in "drive results") / "Deliver" (as in "deliver value")
- "Enable" / "Ensure" / "Craft" / "Curate" / "Tailor"
- "Resonate" / "Underscore" / "Showcase" / "Boast"
- "Embody" / "Encompass" / "Facilitate" / "Champion" / "Pioneer"

**Instead of:** "This tool empowers marketers to unlock their full potential."
**Write:** "This tool saves about 3 hours per week on campaign setup. For a team of five, that's 15 hours."

## Fancy Words That Sound Impressive But Aren't

- "Myriad" / "Plethora" / "Invaluable" / "Paramount" / "Pivotal"
- "Quintessential" / "Aforementioned" / "Whilst" / "Amongst"
- "Ascertain" / "Cognizant" / "Optimal" / "Substantial"
- "Multifaceted" / "Nuanced" / "Intricacies"
- "Meticulous" / "Intricate" / "Vibrant" / "Dynamic"
- "Crucial" / "Essential" / "Vital" / "Imperative" / "Fundamental" / "Integral"

**Use instead:** many, a lot, several, important, key, before, while, among, try, help, start, end, use

## Academic/Formal Connectors

**Review repeated sentence openings and simplify when the replacement preserves meaning:**
Furthermore, Moreover, Additionally, Subsequently, Consequently, Therefore, Thus, Hence, Indeed, Henceforth, Notwithstanding

**Use instead:** And, But, So, Also, Then, Because

## Passive Constructions

- "It has been observed that..."
- "It is recommended that..."
- "Mistakes were made..."
- "It was determined/should be noted/can be said that..."

**Be direct:** "I've watched WordPress sites slow down as their databases grow."

## Audience Hedges

- "Whether you're a beginner or an expert"
- "For businesses of all sizes"
- "Perfect for everyone"
- "No matter your skill level"

**Be specific:** "This guide is for people who've been blogging for at least a year and want to turn it into real income."

## ChatGPT-Specific Tells

- "I'd be happy to help" / "Great question!" / "Absolutely!" / "Certainly!"
- "Let me explain" / "Allow me to"
- Starting lists with "Here are..."
- "There are several [X] to consider"
- "[X] is a [adjective] way to [verb]"
- "When it comes to [X]"
- "[X] plays a crucial role in"
- "[X] has become increasingly popular"
- "[X] offers a wide range of" / "provides a variety of"
- "[X] is designed to" / "allows you to" / "enables you to" / "helps you to"
- "Whether you're looking to [X] or [Y]"
- "From [X] to [Y]" / "Not only... but also"
- "It's worth noting that" / "It's important to mention"
- "It's clear that" / "It's evident that"
- "It's safe to say" / "Suffice it to say"
- "stands as a testament to"
- "paving the way for" / "setting the stage for"
- "a game-changer in" / "a breath of fresh air"
- "boasts" (as a verb for features)
- Starting paragraphs with "When it comes to"
- "If you're looking for... look no further"

## Empty Intensifiers (Contextual Review)

Extremely, Incredibly, Absolutely, Truly, Really, Very, Highly, Totally, Completely, Entirely, Utterly, Remarkably, Exceptionally, Amazingly, Stunningly, Undeniably, Undoubtedly, Definitely, Certainly

## Hype Adjectives (Contextual Review)

Amazing, Awesome, Incredible, Fantastic, Wonderful, Excellent, Outstanding, Exceptional, Remarkable, Extraordinary, Phenomenal, Spectacular, Stunning, Mind-blowing, Unparalleled, Unprecedented

## Meaningless Modifiers (Remove)

Effectively, Efficiently, Easily, Quickly, Simply, Properly, Correctly, Carefully, Thoughtfully, Beautifully, Elegantly, Effortlessly, Flawlessly, Perfectly

**Instead of:** "You can easily and quickly set up your website efficiently."
**Write:** "Setup takes 10 minutes."

## Conclusion Cliches

Avoid these as default endings: In conclusion, To summarize, All in all, Wrapping up, Final thoughts, Key takeaways, The bottom line is, So there you have it, Thanks for reading!, I hope this helps!, Let me know in the comments, What do you think?, Share your thoughts below

**Instead:** Just end. The last useful point IS your conclusion.

## Repetitive Parallel Structure (AI Tell)

**Warn when this pattern reaches its repeat threshold:**
```
No X. Just Y.
No A. Just B.
No C. Just D.
```

One "No X. Just Y." is fine for emphasis. Three in a row screams AI-generated.

The same governs the rule of three generally. Adjective triples ("fast, simple, and reliable"), three-item parallel examples, and "No X. No Y. No Z." punchlines are model signatures when they recur. One deliberate triad per article; after that, vary list lengths. Two or four items read more human than perpetual threes, and a list whose length matches the evidence beats one padded or trimmed to hit three.

## Mirrored Contrast Scaffolds (AI Tell)

The "not X, but Y" snap in all its costumes:

- "It's not just X. It's Y."
- "It's not about X. It's about Y."
- "X isn't the problem. Y is."
- "This isn't X. This is Y."
- "X isn't dead. Lazy X is."

One mirrored contrast can carry a real turn. The tell is the reflex: models reach for the flip every few paragraphs, and the sentence pretends to add depth while restating the same claim backwards. If the Y half can't survive as its own sentence with evidence behind it, the construction was decoration. Name the specific casualty or consequence instead of flipping the sentence.

## Filler Phrases (Contextual Review)

- "As a matter of fact" / "For all intents and purposes"
- "In terms of" / "With regard to" / "In reference to"
- "In order to" (say "to") / "Due to the fact that" (say "because")
- "In the event that" (say "if") / "Prior to" (say "before")
- "At this point in time" (say "now") / "A large number of" (say "many")
- "The vast majority of" (say "most")

## Review & Listicle Slop

Phrases that signal lazy listicle writing:

- "stands out from the crowd" / "stands out as" / "stands out for"
- "excels at" / "shines when" / "where it really shines"
- "is a popular choice" / "is a great option" / "is a solid choice" / "is an excellent choice"
- "one of the best" / "one of the top" / "one of the most popular"
- "is known for" / "is well-known for" / "is famous for"
- "is perfect for" / "is ideal for" / "is great for" (use "Best for:" one-liner instead)
- "comes with a wide range of" / "offers a comprehensive set of" / "comes packed with"
- "takes things to the next level" / "takes it a step further"
- "what sets [X] apart" / "what makes [X] unique" / "what makes [X] special"
- "a must-have for" / "an essential tool for" / "a go-to tool for"
- "boasts an impressive" / "boasts a wide range"
- "seamlessly integrates with" / "integrates seamlessly"
- "at an affordable price point" / "at a reasonable price point" / "won't break the bank"

**Instead of:** "Rank Math stands out as one of the best SEO plugins, offering a comprehensive set of features at an affordable price point."
**Write:** "Rank Math's free tier covers what Yoast Pro charges $99/year for: schema markup, redirections, and keyword tracking. I switched 30+ sites over 2 years."

## Production Commentary in Reader-Facing Copy

Captions, alt text, callouts, and article prose must not narrate the content-production decision. These lines sound self-conscious and AI-written because they tell the reader that the author avoided a worse visual instead of explaining the evidence on screen.

**Hard fail when these exact constructions narrate production:**

- "A fresh capture" or "a fresh screenshot"
- "Captured with Playwright" or the name of any capture/render tool
- "Not a generic dashboard/mockup/image"
- "A real screenshot beats another stock photo"
- "More useful than another stock laptop image"
- "Created/generated with AI, ChatGPT, Midjourney, DALL-E, Canva, or another production tool"
- Any caption whose point is "this visual is authentic" rather than what the visual shows

**Write:** `Semrush's affiliate program page inside Impact.`

**Or omit the caption.** If the alt text already explains the image and no additional fact helps the reader, an empty caption is better than production commentary.

## Process Leakage in Body Copy, Bullets, and Tables

The caption rule above has a bigger sibling. Research narration leaks into prose, spec bullets, and table columns, where it reads as an apology and quietly tells the reader your work is incomplete. Cut every one of these before publishing.

**First, what is allowed.** One scope statement bounding a specific claim is correct practice, not slop:

> I have not run the same cloned checkout test on its current stack, so I rank it on architecture and plan transparency, not an invented latency number.

That prevents an overclaim and earns trust. A third scope disclaimer triggers `warn_if_repeated` review. The defect below is the same admission repeated per item, promoted to a "Weak spot", or hardened into a table column.

**Warn if repeated:**

- "In this study" / "for this update" / "in this round of testing" as a hedge stapled to every claim
- "I didn't test this" as a per-item disclaimer, repeated down a list
- "I haven't attached a fresh price" or another repeated statement about what you could not fetch or verify

**Hard fail when these exact constructions narrate tooling or turn a research gap into a reader-facing label:**

- "The text browser used for this update", "the scraper", "the tool I used", or any research tooling
- "Feature review only" or "Status in this study" as table columns or cells
- "Not an unverified accuracy crown", "I won't turn marketing into a score", or any refusal narrated to the reader
- A "Weak spot" that names a gap in your testing rather than a flaw in the product

**Contextual review:** bare terms such as "text browser", "Access reviewed", or "no independently verified result" can describe legitimate subject matter or a necessary claim boundary. Review their role instead of blocking on the words alone.

**Structural diagnostic:** review any *data* column whose value is identical in every row. "Source date: July 28, 2026" ×10, "Keyword Database: Monthly" ×7, and "Review basis: Production experience" ×14 carry zero information. After confirmation, delete the column and state the fact once beside the table. This does not apply to action columns: a column of links or buttons ("Download", "Try free") is a UI affordance, and identical labels there are expected.

**Write instead:** state the claim boundary once, in the methodology, as a rule rather than an apology.

> No tool receives an accuracy score unless it was queried under matching settings.

**Test:** delete every clause about how you researched or what you could not check. If nothing factual remains, the sentence was never for the reader.

## Templated Per-Item Filler

In roundups and listicles, per-item sections come from one shape. Any sentence that survives unchanged across every item is padding.

**Warn when repeated** (real examples, each found 210 times across 21 roundups on one site):

- "That makes the book useful when your immediate goal matches its teaching style, not merely because the title is popular."
- "Read the table of contents and a sample chapter before buying."
- "A clear sample at the right level is more valuable than another impressive book left unopened."
- "Check Amazon.com or Amazon.in for the exact edition, format, and current seller terms."

Advice that applies to every item goes once, in the intro or buying section. The same holds across sibling articles: a "common buying mistakes" section that is word-for-word identical in twenty roundups is padding in nineteen of them.

**Test:** swap another item's name into the closing sentence. If it still reads correctly, delete it.

## Teaching-Context Slop

When you're explaining or teaching, a different family of slop creeps in. It wears the costume of approachability or thoroughness, but it labels instead of demonstrating.

**Cutesy condescension fillers.** Verbal tics and emoji that perform friendliness while talking down to the reader:

- "Definition time" / "Time for some math" / "Buckle up"
- "Happy?" / "Make sense?" / "Got it?" / "Cool?" (when used to jolly the reader along, not to genuinely check understanding)
- "Fun fact:" / "Spoiler alert:" as a substitute for the fact itself
- Emoji standing in for substance (a checkmark or fire emoji where an example belongs)

The reader is an adult who wants to understand, not a child to be jollied. The real failure looks like this: "Definition time. ... Fire point: ... Happy?" Those interjections stand in for the explanation. Cut them and you lose nothing but the tic. Respect the reader instead: assume they're smart and just haven't seen this yet, then supply the missing information.

**Over-labeling without demonstration.** Asserting that something is important, powerful, or interesting instead of showing it:

- "This is powerful" / "This is a key concept" / "This is fundamental" (then no example proves it)
- "This boosts performance" / "This is essential for X" (with nothing concrete the reader can picture)
- Naming a property and moving on, when the property needed a worked example

Real failure: "Two qubits can become entangled... This allows powerful coordination between qubits, boosting performance. ... This drastically boosts computing power. Essential for quantum algorithms." It labels ("powerful," "boosts," "essential") without one example. Make the claim, then make it happen in front of the reader. Demonstration is the proof.

**"A great way to."** A brochure tell that promises value without delivering a single specific:

- "[X] is a great way to [Y]"
- "[X] makes it extremely easy to [Y]"
- "The best thing about [X] is..."

Real failure: "Widgets are a great way to add content and additional features to your website. They make it extremely easy for you to simply drag and drop several elements." Empty intensifiers, nothing a learner can do or picture. Name the specific thing and show it: what it does, on what, with what result.

**Restating one idea three ways instead of showing it once.** Saying the same thing in three rephrasings reads as thoroughness but teaches nothing. One demonstration beats three labels.

- "This boosts power. It drastically increases capability. It dramatically improves results."
- Three sentences that each gesture at the same vague payoff with no example between them

The fix is a single worked example with the reasoning visible. (Teaching cadence has its own honest repetition, saying a number again in words to let weight land, as in "that's 12,000 monthly visitors gone. Twelve thousand visitors you already earned." That's a deliberate pause on one concrete fact, not three vague restatements of an abstract claim. Know the difference.)

**Instead of:** "Entangled qubits work together, sharing states instantly. This drastically boosts computing power. Essential for quantum algorithms."
**Write:** "Entangle two qubits and measuring one instantly fixes the other, even across a room. Einstein called it 'spooky action at a distance.' It's real, and it's what lets a quantum computer check many paths at once instead of one at a time."

## Quick Self-Test

Search your draft for these 10 red flags. If any appear, rewrite:

1. "landscape" 2. "journey" 3. "dive/delve" 4. "leverage" 5. "utilize"
6. "seamless" 7. "robust" 8. "empower" 9. "game-changer" 10. "Furthermore/Moreover/Additionally"

## The Ultimate Test

Read your content aloud. If it sounds like a LinkedIn post, press release, college essay, or corporate memo, rewrite. If it sounds like something you'd actually say to a friend, ship it.
