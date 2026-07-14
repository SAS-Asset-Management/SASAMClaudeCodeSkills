---
name: emailVoice
description: |
  Profile how Shane writes email and capture it as a reusable voice guide, so every draft composed through the microsoft365 tool sounds like him. Use when the user says:
  - "profile my email voice", "learn my writing style", "capture my email voice"
  - "refresh my voice profile", "update how I sound", "re-sample my sent mail"
  - "/emailVoice", or asks why a drafted email does or does not sound like them
version: 1.1.0
---

# emailVoice

A sub skill of the `microsoft365` email tooling. It samples Shane's own Sent mail, classifies his writing voice, captures it in a single profile file that the `microsoft365` tool reads before composing any email, and then proves the profile by drafting a sample email in that voice and calibrating it against Shane's feedback. Draft once, sound like Shane every time.

## Where the profile lives

`~/.outlook-cli/voiceProfile.md`

This sits beside the signature and other per account state in the `outlook` CLI config directory. It is personal and stays local — it is never committed to any repository. The `microsoft365` tool points at this exact path.

## What "voice" means here

The profile captures **style, not content**: register and warmth, how he opens and closes, sentence and paragraph rhythm, punctuation habits, characteristic vocabulary and tics, and how tone shifts by recipient. It never stores confidential material — no client names, deal specifics, numbers, or private detail. Any example phrase carries placeholders in place of identifying details.

## Building or refreshing the profile

Run this whenever the user asks, and consider offering a refresh every few months (voice drifts, and the sample is weighted to recent mail). The flow is: sample, classify, write the profile, then demonstrate it with a sample email and calibrate against feedback.

1. **Sample.** Pull roughly 100 recent sent messages:
   `outlook mail list --folder Sent --top 100`
   Parse the JSON, keep each `id`, `subject`, and `sentDateTime`, and record the date range for provenance.
2. **Read a spread.** Read the bodies of about 30 to 40 messages spread across the list (not only the newest), always with `outlook mail get <id> --text`. Skip anything that will not reveal voice: bare forwards, single line acknowledgements, calendar and automatic replies. Favour substantive prose he actually typed. Ignore the appended signature block when reading — analyse only the words above it.
3. **Classify.** Extract specific, observed patterns into the section structure below. Be concrete, not generic.
4. **Delegate for privacy.** Prefer running the sampling and classification in a subagent so raw email content stays out of the main context; have it return only the finished profile markdown.
5. **Write** the result to `~/.outlook-cli/voiceProfile.md`, replacing the `{{DATE}}` placeholder with today's date in DD/MM/YYYY.
6. **Confirm** back to the user with the sample size, the date range covered, and a one line summary of the voice captured.

## Demonstrate and calibrate

An abstract profile is easy to nod along to and hard to trust. Prove it with a real draft and let the user correct it. This runs every time the profile is built or refreshed, and can also be run on its own when the user just wants to see or tune the voice.

7. **Draft a sample.** Compose one short, realistic sample email, roughly 120 to 180 words, that exercises the captured voice: a typical opening, the paragraph rhythm, at least two characteristic tics from the Vocabulary and idiom section, an em dash, open compounds rather than hyphenated ones, and a forward looking close with no redundant sign off (the signature owns "Regards" and his name). Pick a plausible everyday scenario, most often his warmest register — a warm follow up to a prospect or a delivery update to a client — and label the scenario so the user reads it in context. Keep the font Arial, consistent with the `microsoft365` hub. Present it for the user to read, and note in one line which tics it is exercising so the user knows what to judge.
8. **Ask for feedback.** Ask directly whether it sounds like him and what is off, with a few specific prompts rather than a blank "thoughts?" — for example: is the opener right, is any phrase one he would never use, is the register too formal or too matey for that recipient, is a signature tic missing.
9. **Fold feedback back in.** Apply the corrections to the profile (usually the Do and Don't sections, sometimes Openings, Closings, or Tone by context), rewrite `~/.outlook-cli/voiceProfile.md`, then redraft the sample and show it again. Repeat until the user signs off. The sample exists for calibration, not decoration — a correction that changes the profile is the whole point.

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

- Style only. Never copy sentences, client detail, or confidential content from the sampled mail into the profile, the sample email, or new drafts. The sample email uses invented, plausible scenarios with placeholders, never a real client or deal.
- The profile shapes tone and phrasing. It never overrides an explicit instruction from the user about a specific email.
- Australian English throughout, consistent with the global rules.
