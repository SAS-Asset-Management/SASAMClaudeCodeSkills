---
name: handoff
description: Hand a piece of work to the Ensemble — write a task packet and push it to the engagement repo's queue branch for the Norbert-poller to claim. Use when a consultant says "hand this off", "create a handoff", "send this to the Ensemble/an agent", "queue this task", or wants an agent to pick up a project or task in the current engagement.
---

# /handoff — push a task packet to the engagement queue

This skill writes one **handoff task packet** to `handoffs/inbox/HX-<date>-<slug>.md`
and **fast-forward pushes that single commit to the `queue` branch** — the consultant
mailbox the Norbert-poller watches. This is the *only* direct push a consultant makes.
Results never come back on `queue`; they arrive later as a **PR into `main`**
(`handoffs/outbox/<id>/`).

Run this from **inside a tethered engagement repo** (one with `.ensemble/project.json`).
The script calls `ens_require_tethered` and aborts if you are not.

## How to run it

1. **Confirm you are in the right engagement.** The script reads the engagement
   (`scope_tag`) from `.ensemble/project.json` and stamps it on the packet — you do
   not supply it. If the consultant is unsure which repo they are in, run
   `git rev-parse --show-toplevel` and show them the `scope_tag` before proceeding.

2. **Interview the consultant** for the fields below. Gather them conversationally;
   do not dump a form. Use sensible defaults and only ask about a default when the
   work clearly diverges from it.

   - **brief** (required) — what needs doing, in prose. This becomes the packet's
     `## Brief` body. Draw it out properly: the agent that claims this has only the
     packet to work from, so capture the real intent, constraints, and any context a
     newcomer would need. One or two tight paragraphs beats a one-liner.
   - **slug** (required) — a short kebab-case label for the id, e.g. `draft-samp`,
     `acme-renewal-model`. Keep it ≤24 chars; the script kebab-normalises and
     truncates, but propose a clean one. Make it descriptive — it is how humans will
     refer to this handoff.
   - **definition_of_done** (required, **one or more**) — the verbatim acceptance
     criteria the result will be judged against. Push for concrete, checkable items
     ("SAMP covers all four asset classes", "ISO 55001 line-of-sight table present"),
     not vague aspirations. Each criterion is a separate `--dod` flag.
   - **inputs** (optional, repeatable) — **repo-relative** paths the agent should read
     (briefs, data, prior artefacts). Only list files that exist in the repo. Large
     binary/data inputs must live under `data/` or match an LFS pattern in
     `.gitattributes` (see the guard below).
   - **kind** (default `project`) — `project` routes to larsFrederickson for intake /
     planning / team / fan-out; `task` routes to agnarBergstrom for triage. Use
     `project` for a body of work, `task` for a single discrete action.
   - **review_tier** (default `full`) — who must approve the result PR before it lands:
     `auto` (no review, auto-merges on green), `light` (any engagement consultant),
     `full` (you, the requester, must approve), `founder` (@scriv must approve). When
     unsure, keep `full`.
   - **deadline** (default `none`) — an ISO 8601 timestamp (e.g.
     `2026-06-20T17:00:00+10:00`) or the literal `none`.
   - **route_hint** (default `api`) — leave as `api`. `local-bulk` is **deferred** and
     the script rejects it.
   - **context** (optional, repeatable) — PR numbers or prior packet ids the agent
     should read for background (e.g. `pr#42`, `HX-2026-0601-discovery`).
   - **requested_by** — the requesting consultant's GitHub handle. The script
     auto-detects it via `gh api user` or git config; only pass `--requested-by`
     explicitly if that is wrong (it matters: under `full` tier this handle is the one
     that must approve the result).

3. **Pre-flight the inputs.** For any input file the consultant names, sanity-check it
   exists and, if it is large (>10MB) and binary, that it sits under `data/` or matches
   an LFS pattern in `.gitattributes`. The script enforces this and will abort with a
   clear message, but catching it in conversation saves a round-trip. If an input is
   too big and not LFS-covered, tell the consultant to either add a matching pattern to
   `.gitattributes` or move the file under `data/` and `git add` it (so it becomes an
   LFS pointer) — **do not** edit `.gitattributes` for them without asking.

4. **Read the brief and DoD back** to the consultant in one short summary and get a
   yes before pushing. This packet is going to the queue the moment you run the script.

5. **Invoke the script** in this folder with the gathered fields. Repeat `--input`,
   `--dod`, and `--context` once per item:

   ```bash
   bash "$CLAUDE_SKILL_DIR/handoff.sh" \
     --brief "<the full brief prose>" \
     --slug "<kebab-slug>" \
     --dod "<first acceptance criterion>" \
     --dod "<second acceptance criterion>" \
     --input "<repo/relative/path.md>" \
     --kind project \
     --review-tier full \
     --deadline none \
     --context "pr#42"
   ```

   The script prints progress to **stderr** and the **bare packet id to stdout** — you
   can capture it (`ID=$(bash handoff.sh ... 2>/tmp/h.log)`) to refer to the handoff
   afterwards. Use `--no-push` if the consultant wants to build and review the commit
   locally before it leaves the laptop; otherwise the push is part of the run.

## What the script does (so you can explain it)

1. `ens_require_tethered` — aborts unless you are in an engagement repo.
2. Validates the fields (kind / review_tier enums; rejects `local-bulk`; needs ≥1 DoD).
3. **Large-input guard** — any input >10MB not covered by an `.gitattributes` LFS
   filter stops the run with instructions to fix it. It also installs a **pre-push
   hook** that rejects any >10MB non-LFS blob, so a bad blob can never reach GitHub.
4. Computes `id = HX-<YYYY-MMDD>-<slug>` and **guarantees it is unique** across the
   queue inbox, claimed packets, the `main` outbox, **and all of git history** — it
   aborts on any collision so two handoffs never share an id.
5. Writes the packet, **validates it against the engagement repo's
   `schemas/packet.schema.json`** (via the shared lib), commits `handoff: <id>`, and
   **fast-forward pushes just that one commit to `queue`** — never to `main`, never
   forced. It leaves you back on the branch you started on.
6. Confirms with the id and a reminder that the **Norbert-poller polls every ~2 min**.

## After the handoff

- The poller claims the packet into `handoffs/claimed/<agentId>/` within ~2 minutes.
- The result returns as a **PR into `main`** under `handoffs/outbox/<id>/`. Approve it
  per the `review_tier` you set (for `full`, that approval is yours to give).
- If a fast-forward push fails because the queue advanced, just **re-run /handoff** —
  it rebases onto the new tip and the id stays unique.
