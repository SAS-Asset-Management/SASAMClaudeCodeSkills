---
name: emailVoice
description: |
  Profile how Shane writes email and capture it as a reusable voice guide, so every draft composed through the microsoft365 tool sounds like him. Use when the user says:
  - "profile my email voice", "learn my writing style", "capture my email voice"
  - "refresh my voice profile", "update how I sound", "re-sample my sent mail"
  - "/emailVoice", or asks why a drafted email does or does not sound like them
version: 1.0.0
---

# emailVoice

A sub skill of the `microsoft365` email tooling. It samples Shane's own Sent mail, classifies his writing voice, and captures it in a single profile file that the `microsoft365` tool reads before composing any email. Draft once, sound like Shane every time.

## Where the profile lives

`~/.outlook-cli/voiceProfile.md`

This sits beside the signature and other per account state in the `outlook` CLI config directory. It is personal and stays local — it is never committed to any repository. The `microsoft365` tool points at this exact path.

## What "voice" means here

The profile captures **style, not content**: register and warmth, how he opens and closes, sentence and paragraph rhythm, punctuation habits, characteristic vocabulary and tics, and how tone shifts by recipient. It never stores confidential material — no client names, deal specifics, numbers, or private detail. Any example phrase carries placeholders in place of identifying details.

## Building or refreshing the profile

Run this whenever the user asks, and consider offering a refresh every few months (voice drifts, and the sample is weighted to recent mail).

1. **Sample.** Pull roughly 100 recent sent messages:
   `outlook mail list --folder Sent --top 100`
   Parse the JSON, keep each `id`, `subject`, and `sentDateTime`, and record the date range for provenance.
2. **Read a spread.** Read the bodies of about 30 to 40 messages spread across the list (not only the newest), always with `outlook mail get <id> --text`. Skip anything that will not reveal voice: bare forwards, single line acknowledgements, calendar and automatic replies. Favour substantive prose he actually typed. Ignore the appended signature block when reading — analyse only the words above it.
3. **Classify.** Extract specific, observed patterns into the section structure below. Be concrete, not generic.
4. **Delegate for privacy.** Prefer running the sampling and classification in a subagent so raw email content stays out of the main context; have it return only the finished profile markdown.
5. **Write** the result to `~/.outlook-cli/voiceProfile.md`, replacing the `{{DATE}}` placeholder with today's date in DD/MM/YYYY.
6. **Confirm** back to the user with the sample size, the date range covered, and a one line summary of the voice captured.

## Profile structure

The file must contain these sections, each filled with observed specifics:

- **Provenance** — sample size read, total listed, date range, generated date.
- **Voice in one line** — the overall persona in a single sentence.
- **Formality and register** — how formal, warm, and direct; whether it varies by recipient.
- **Openings** — how he actually starts messages.
- **Closings before the signature** — what he types right before the automatic signature. The signature already supplies "Regards," and his name, so flag any redundant sign off.
- **Sentence and paragraph rhythm** — length, density, use of lists.
- **Punctuation and mechanics** — em dashes, commas, exclamation marks, capitalisation, emoji, Australian spelling, and his hyphen habit.
- **Vocabulary and idiom** — characteristic words, transitions, hedges, and recurring tics with de identified examples.
- **Tone by context** — internal versus client versus vendor, where distinguishable.
- **Do** — concrete rules for sounding like him.
- **Don't** — things that break the illusion.

## How it is consumed

The `microsoft365` tool has a Voice section instructing it to read `~/.outlook-cli/voiceProfile.md` before composing any mail and to match it. Because `sendAndLog` delegates its drafting to `microsoft365`, it inherits the voice automatically. Nothing else needs wiring.

## Guardrails

- Style only. Never copy sentences, client detail, or confidential content from the sampled mail into the profile or into new drafts.
- The profile shapes tone and phrasing. It never overrides an explicit instruction from the user about a specific email.
- Australian English throughout, consistent with the global rules.
