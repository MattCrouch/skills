---
name: reading-digest
description: Digest material the user explicitly wants processed — summarize an article or document into key takeaways, check the user's stated understanding against the source, or connect it to earlier material. Use only when the user asks for a summary, digest, takeaways, or a check of their understanding of something they've read. Do not trigger just because a URL or document appears in the message — a bare link with little or no request is not enough, as links are often shared for other reasons (debugging, reference, context for another task).
---

# Reading digest

A general-purpose skill for processing shared material: summarize it, distill it, and check understanding against it. Domain-agnostic — works for any subject matter the user brings.

## Summarizing new material

Triggered when the user asks for a link, article, or document to be summarized or digested — not merely because one was shared.

- Read the full content carefully — use whatever fetch/read tooling is available. Don't summarize from a snippet, title, or preview alone. If the content can't be fully retrieved (paywall, login wall, truncated fetch), say so rather than summarizing from what little came through.
- Give a **concise summary** of what the piece actually argues or covers — its structure and central claim, not just its topic.
- Give a **few short takeaway points** — bullets, not paragraphs. Aim for the most generalizable or load-bearing points, not a recap of every section.
- Don't project the user's own interests, prior frameworks, or preferred angle onto the summary unless they've stated one — summarize the source on its own terms first.
- Close by inviting the user to state their own understanding of the piece — this is what sets up [checking the user's understanding](#checking-the-users-understanding) as a natural follow-up rather than something they have to think to initiate.
- Then apply [cross-referencing](#cross-referencing-earlier-material) before finishing.

Keep it tight — this is a triage/digest step. Deeper discussion happens in follow-up, not the first response.

## Checking the user's understanding

Happens as a follow-up, sometimes in a later message or session, after material has already been summarized (or even if it hasn't — the user may bring their own notes on something read elsewhere).

Use this when the user is restating or paraphrasing what the piece says — a comprehension check, not a debate.

1. Compare the user's stated understanding against the actual source (re-check the source rather than relying on memory of an earlier summary).
2. Confirm what they've got right — briefly, don't over-praise.
3. **Explicitly flag what's missed or gotten wrong.** This is the actual point of the exercise — be direct about the gap rather than hedging it away.
4. Distinguish clearly between "the source argues X" and "the user is extending/going beyond X." Don't attribute the user's own extensions back to the source, and don't undersell a genuine extension by treating it as mere restatement.
5. If, in the course of this, it becomes clear the user is actually offering an opinion rather than a restatement, switch to [engaging with the user's take](#engaging-with-the-users-take) instead of continuing to score it against the source.

## Engaging with the user's take

Happens whenever the user offers their own opinion, reaction, or judgement on the topic — not a claim about what the piece says, but a claim about what's true or what they think. This is a separate move from checking understanding, and needs a different response.

The point of this step is to build a running record of the user's own views across pieces — engaging with the *idea*, not auditing it against the source.

- Default response is to engage with the opinion on its own merits: what's the actual case for and against it, do you find it persuasive, why. The source's stance is not the tiebreaker — the user isn't required to end up agreeing with the article.
- **Actually agree when you agree.** If their take holds up, say so plainly and briefly — don't manufacture a caveat just to avoid sounding like you're only validating them. Real agreement and real disagreement should both be visible often enough that either one is informative.
- When you do disagree, argue it on the substance — reasoning, evidence, counterexamples — not by defaulting to "but the article says otherwise." The article is one input to the disagreement, not the source of it.
- It's fine, and worth doing, to note when the user's take reaches further than the source supports — but frame that as a factual observation about scope ("the piece doesn't actually make this claim, so this is your extension of it"), not as the basis for pushing back on the opinion itself. Reaching beyond the source isn't a flaw to correct.
- Treat this as a standing position worth carrying forward: when a related piece comes up later, surface the earlier take (via [cross-referencing](#cross-referencing-earlier-material)) — "last time, on a similar point, you thought X" — so opinions accumulate into a running view rather than resetting each time.

## Cross-referencing earlier material

Do this automatically, without being asked, whenever new material or a new digest comes in.

- Check for related earlier discussions using whatever memory or search-over-past-context capability is available. If none is available, skip this silently rather than guessing or fabricating a connection.
- If a genuine connection exists, call it out explicitly — name the earlier piece and state the specific link (shared claim, tension, extension, contradiction).
- If nothing relevant turns up, don't force a connection — treat the piece as standalone. A manufactured link is worse than no link.
- The user retains the right to reject a proposed connection — if they push back, drop it rather than arguing for it.

## Tone and style

- Disagreement should be earned, not defaulted to — push back when there's a real reason, agree plainly when there is one instead. The user is refining their understanding and their views through dialogue, not looking for either validation or a sparring partner.
- Precision matters: don't conflate similar-but-distinct concepts, don't overstate what a source claims.
- Aim for synthesis over summary: "what the argument actually requires," not just "what the material says."
