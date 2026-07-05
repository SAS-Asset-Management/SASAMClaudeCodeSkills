---
name: sendAndLog
description: Draft an email with Shane's standard footer via the microsoft365 skill, push it to Outlook DRAFTS only, and NEVER send without explicit user confirmation. On the user replying "sent", update the linked record — the BEAM opportunity, the Ensemble task, or the engagement hub, whichever the context indicates. Use when the user says "draft an email", "push the draft to outlook", "send and log", "draft to <person>", or wants an email drafted and its outcome tracked against a deal, task, or engagement.
---

# sendAndLog

Draft once, confirm before sending, log automatically. This skill closes the loop that used to run by hand 60+ times: draft in Outlook, tell Shane it's ready, wait for "sent", then go and update BEAM, Ensemble, or the engagement hub to match.

## Hard rule — never send without explicit confirmation

**This skill only ever pushes a DRAFT to Outlook. It never calls send.**

- Every email produced by this skill goes to Outlook DRAFTS via the `microsoft365` skill's draft capability, never its send capability.
- Do not send under any circumstance in this skill — not on a deadline, not because the draft looks final, not because a previous message implied urgency.
- The only trigger that moves a drafted email out of "pending" state is Shane replying with confirmation that he sent it (e.g. "sent", "sent it", "just sent that"). Treat this as a statement of fact about something Shane did in Outlook, not a request for this skill to send.
- If a reply is ambiguous about whether the email actually went, ask one direct question before touching any linked record: "Confirming — did you send the draft to <recipient>?"

## What this skill does

1. **Draft** — compose the email body, apply Shane's standard footer/signature, and hand off to the `microsoft365` skill to create an Outlook draft (never send). Confirm back to Shane which recipient, subject, and linked record (if known) the draft is for.
2. **Wait** — do nothing further until Shane confirms the draft was sent.
3. **Log** — on confirmation, update exactly one linked record, chosen from context:
   - **BEAM opportunity** (`beam-selling` skill / `mcp__ensemble__ensemble_*` opportunity tools) — when the email is part of an active sales engagement.
   - **Ensemble task** (`mcp__ensemble__ensemble_update_task` / `ensemble_update_project_task`) — when the email is tied to a delivery task or project.
   - **Engagement hub** — when the email is general engagement communication with no specific opportunity or task attached; log a note against the engagement record instead.
   
   If it is not obvious which of the three applies, ask Shane rather than guessing — a wrong log entry is worse than a short delay.
4. **Never log before confirmation.** If Shane hasn't said "sent" yet, do not touch BEAM, Ensemble, or the hub, even if the draft has existed for a while.

## Per recipient routing rules

Support a configurable list of routing constraints that restrict who a given topic or engagement may be emailed to, e.g. "only ever email Manju on the DoH engagement." Before drafting:

- Check whether the recipient and topic match an existing routing rule.
- If a rule restricts the engagement to a specific recipient and the requested recipient doesn't match, stop and flag the mismatch to Shane before drafting — don't draft to the wrong person and rely on him to catch it during review.
- Routing rules are simple `engagement → allowed recipient(s)` pairs. Ask Shane to supply or confirm the rule the first time an engagement is mentioned if none is on record; don't invent one.

## Procedure

1. Identify recipient, subject, and body content from the request.
2. Check per recipient routing rules for the engagement/topic; flag and stop if there's a conflict.
3. Draft the email with Shane's standard footer, via the `microsoft365` skill, into Outlook DRAFTS. Do not send.
4. Tell Shane the draft is ready and which linked record it maps to (BEAM opportunity / Ensemble task / engagement hub), or ask if unclear.
5. Wait for explicit confirmation that the email was sent.
6. On confirmation, update the one linked record identified in step 4.
7. Confirm the log update back to Shane in one line.
