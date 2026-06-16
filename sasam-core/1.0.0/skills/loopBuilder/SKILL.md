---
name: loopBuilder
description: Design a well-formed autonomous agent loop for a given subject, then launch it. Use when the user wants to "build a loop", "set up a loop", "loop this", "make Claude run this on its own", "design a loop for X", "automate this end to end", or move from hand-prompting to a self-running goal-driven cycle. Inspects the working directory first, drafts a candidate loop (goal, context, action policy, verification, stop condition), enforces mandatory guardrails, gets approval, then fires it as an in-session /loop or a multi-agent Workflow.
---

# loopBuilder

Turn a fuzzy "keep doing this until it's done" into a **well-formed loop** — then launch it.

## The idea (why this skill exists)

In the prompting era you are the connective tissue between every step: you write a prompt, read the output, decide what's next, write the next prompt. A prompt buys you one output. You're in the loop manually, every iteration.

A *loop* moves up a level of abstraction. You stop specifying steps and start specifying **outcomes plus verification**, then let the agent run the cycle itself:

```
context → decide → tool → result → context → …  (until a stop condition trips)
```

The human stops being the prompter and becomes the person who **designs and supervises the loop**. This skill is the design-and-launch step. It does not invent a new runtime — it composes a sound loop and fires it on an existing substrate (`/loop` or `Workflow`).

> Karpathy's "autonomy slider": autocomplete suggested your next line; copilots drafted while you verified everything; loops own larger stretches of the gather → act → verify cycle. As you slide toward autonomy you spend less time generating each step and more time specifying outcomes, designing verification, and setting boundaries. This skill is the boundary-setting step.

## The anatomy of a loop

Every loop this skill produces has **five parts**. A loop missing any of them is not ready to launch.

| Part | What it is | Bad / Good |
| --- | --- | --- |
| **Goal** | The outcome, stated as a verifiable end-state — not an activity | ✗ "improve the tests"  ✓ "every file in `src/` has a test and the suite passes" |
| **Context** | What the agent needs in hand each cycle: files, commands, tools, prior results | repo paths, the test command, which skills/tools are in play |
| **Action policy** | What the agent is allowed to do per iteration, and in what order | "read failing test → patch source → re-run → record" |
| **Verification** | The check run each cycle that decides pass / fail / continue | the agent verifies its own output; never trusts it |
| **Stop condition** | The verifiable state that ends the loop | "suite green", "10 found", "2 consecutive empty rounds" |

## Procedure

### Step 1 — Auto-inspect first (do this before asking anything)

Ground the design in what is actually runnable *here*. Without being asked, gather:

- **Repo shape** — top-level layout, language, where the code under the subject lives (`Glob`/`Explore`).
- **Runnable checks** — test/build/lint commands (`package.json` scripts, `Makefile`, `pyproject`, CI config). These become the verification method.
- **Available skills & tools** — scan the session's skill list and tools; a loop that can call `/code-review`, a project test command, or a domain skill is stronger than one that re-derives everything.
- **Git state** — branch, dirty/clean, whether work should be isolated.

From this, **draft a candidate loop** filling in all five anatomy parts as far as the environment allows. Note explicitly what you could not infer.

### Step 2 — Confirm-only questions (minimal)

You inspected first specifically to ask less. Only ask about gaps the environment cannot answer — and follow the house interview style (one question at a time, multiple-choice where possible):

- The **true subject/goal** if ambiguous (what "done" looks like).
- The **success bar** — when is the output good enough to stop.
- Any **boundary** the user cares about (don't touch X, cap spend at Y, supervised vs walk-away).

Do not re-ask anything the inspection already established. If the draft is solid, confirm it rather than interrogate.

### Step 3 — Enforce the guardrails (mandatory — no launch without all four)

The breathless coverage skips this; you do not. Drift and infinite retries are the dominant failure mode of autonomous loops. Every loop **must** carry all four before it can launch:

1. **Explicit stop condition** — a written, verifiable termination state. "Until done" is not a stop condition.
2. **Iteration / budget cap** — a hard ceiling (max iterations, token budget, or wall-clock) so a stuck loop self-terminates even if the stop condition never trips.
3. **Verification method** — an explicit per-cycle check producing pass/fail/continue. No verification ⇒ no launch.
4. **No-progress / drift detector** — break out when consecutive iterations stop making progress (identical result, repeated retries) rather than burning the whole budget.

If you cannot define one of these for the subject, say so and stop — that is a signal the task is not loop-shaped (see "When NOT to loop").

### Step 4 — Route the substrate (the design picks)

Choose based on the task shape, not user preference:

| Choose… | When |
| --- | --- |
| **In-session `/loop`** | A single repeating prompt/check; the user wants to supervise and can interrupt; cadence-based polling or "run until green". Self-paced (model decides cadence) or fixed interval. |
| **`Workflow` orchestration** | The cycle needs **parallel subagents** (fan-out finders, multi-lens verification, pipeline over a worklist), or a deterministic find → verify → synthesize structure. Heavier; for multi-agent loops, not one recurring prompt. |

Default to `/loop` for supervised single-prompt cycles; reach for `Workflow` only when genuine parallelism or deterministic multi-stage control flow is required. (No cron/`/schedule` path — this skill launches loops that run now.)

### Step 5 — Present the design, require approval

Render the full design and **wait for explicit approval or edits** before launching. Use this template:

```
LOOP DESIGN — <subject>

Goal            <verifiable end-state>
Context         <files / commands / skills / tools in play>
Action policy   <what each iteration does, in order>
Verification    <the per-cycle check → pass/fail/continue>
Stop condition  <verifiable state that ends the loop>

Guardrails
  • Iteration/budget cap   <e.g. max 12 iterations / 400k tokens>
  • Drift detector         <e.g. stop after 2 rounds with no new progress>

Substrate       /loop (self-paced | interval N)  OR  Workflow (N agents)
```

Offer the user three responses: **approve**, **edit** (adjust any field, re-render), or **cancel**.

### Step 6 — Launch

On approval, fire it:

- **In-session `/loop`** — invoke the `loop` skill with the composed prompt/command and cadence (self-paced when the model should decide timing; interval when polling external state). Bake the stop condition and caps into the looped prompt so each iteration self-checks.
- **`Workflow`** — author a script whose control flow encodes the action policy, verification, stop condition, and caps (loop-until-dry / loop-until-budget patterns, adversarial verify). Launch via the `Workflow` tool.

After launching, tell the user how to watch it and how to stop it.

## When NOT to loop (say so honestly)

Not every task benefits. Push back when:

- The goal can't be stated as a verifiable end-state — greenfield exploration, highly ambiguous requirements, and "use judgement" work still need a human in each step.
- A single pass would do — a loop adds cost and drift risk for nothing.
- You can't define verification or a stop condition — that's the tell the task isn't loop-shaped yet. Help the user sharpen the goal first, then loop.

A loop is leverage when the goal is crisp and verification is cheap. It is a money-burner when neither holds.
