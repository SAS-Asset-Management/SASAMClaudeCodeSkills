# Maturity Assessment — Hook Battery

Eight config driven Python scripts that enforce the method's hard rules structurally rather than by prompt text alone. All scripts are Python 3 standard library only, read the hook event JSON from stdin, locate the engagement repo by walking up from the target file path to the nearest `engagement.yaml` (falling back to the `CLAUDE_PROJECT_DIR` environment variable, which is also how the SessionStart and Bash hooks resolve since they carry no target file), and load YAML through the engine loader (`engine/configLoader.py` imported via `importlib`, never a private parser).

**The silent no engagement exit.** The plugin is installed globally, and most sessions are not engagements. Every script exits 0 silently when no `engagement.yaml` resolves — the battery is invisible outside an engagement repo.

## The battery

| Hook | Event | Enforces |
| --- | --- | --- |
| `scoringGate.py` | PreToolUse on Write, Edit, MultiEdit | No score without ledger evidence. Blocks a first write to `scoring/NN_*.md` unless subject NN in `scoreLedger.json` carries at least one evidence record whose artefact exists on disk (scoring is numbered by subject, reviews by artefact intake order — the ledger is the join); edits to existing files pass. Also blocks `scoreLedger.json` writes whose evidence records cite reviews that do not exist on disk |
| `sovereigntyGate.py` | PreToolUse on Bash | Raw evidence never reaches a remote. On `git push` or `git commit`, denies when the staged or outgoing diff touches `evidence/` or `interviews/` (tolerates a missing upstream). Warns via systemMessage when `data.api` is not `zdr-no-training` |
| `findingAuthorGate.py` | PreToolUse on Write, Edit, MultiEdit | A finding needs both sides, read from the subject's `scoreLedger.json` evidence: a say source (a `reviews/` path) and a do source (an `interviews/` path, or `sayScore` and `doScore` both set). Denies the write when either is missing, and reminds every write that only the finding-synthesiser agent authors findings |
| `proseRules.py` | PostToolUse on Write, Edit, MultiEdit | Mechanical prose checks on `scoring/`, `findings/`, `deliverable/`: US to AU spelling, the hyphen ban (code spans, URLs, CLI flags, identifiers exempt), paragraph length capped by the pack `qaRules.yaml` `proseRules.maxParagraphSentences` (default 4), DD/MM/YYYY display dates, and banned phrasings from `engagement.yaml` plus the pack `qaRules.yaml` (flat strings or entries carrying nested `seedPatterns`). Non blocking — violations return as additionalContext; semantic enforcement lives in the report-qa agent |
| `plotBlocker.py` | PreToolUse on Write, Edit, MultiEdit | JS plots only, closed catalogue. Under `deliverable/`, denies imports of Python plotting libraries (matplotlib, seaborn, plotnine, pylab, altair) and any render function outside renderDomainRadar, renderSubjectConfidence, renderRunTrend, renderPeerPercentile (a soft tripwire, stated in the reason) |
| `coverageWarner.py` | SessionStart | Surfaces the resolved pack's `coverageManifest.yaml` knownGaps as additionalContext so coverage holes are stated caveats |
| `sessionPrimer.py` | SessionStart | Zero touch progress snapshot derived live: week N of `engagement.weeks` from `engagement.start`, artefact and review counts, subjects scored out of the taxonomy total from the ledger, open disputes. Nothing hand maintained |
| `contractValidator.py` | SessionStart | The drift killer. Verifies every agent and skill the plugin CLAUDE.md references exists on disk, that pack directories required by `pack.yaml` flags exist (`calcPack/`, `reportSpec/`), and that `scoreLedger.json` parses with the contract top level keys. Discrepancies as additionalContext |

## Wiring

`hooks/hooks.json` registers the battery when the plugin is installed. Order matters on the write matcher: scoringGate, then findingAuthorGate, then plotBlocker.

Engagement repos wanting a local subset (for example when the plugin is not installed globally) can copy this into `.claude/settings.json`, replacing the plugin root path:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          { "type": "command", "command": "python3 /path/to/maturity-assessment/1.0.0/hooks/scripts/scoringGate.py" },
          { "type": "command", "command": "python3 /path/to/maturity-assessment/1.0.0/hooks/scripts/findingAuthorGate.py" }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python3 /path/to/maturity-assessment/1.0.0/hooks/scripts/sovereigntyGate.py" }
        ]
      }
    ]
  }
}
```

## Output shapes

- **Deny (PreToolUse):** `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "…"}}`
- **Non blocking nudge:** `additionalContext` inside `hookSpecificOutput`, or a top level `systemMessage`.

## Guardrail classification

Every hard rule in the suite is classified as hook enforced (a script blocks the action), structurally enforced (impossible by construction), or prompt only (stated in skill or agent text — the bucket to minimise).

| Hard rule | Classification | Mechanism |
| --- | --- | --- |
| No score without ledger evidence backed by a filed review | Hook enforced | `scoringGate.py` |
| Raw evidence and interviews never pushed to a remote | Hook enforced | `sovereigntyGate.py` |
| ZDR API posture asserted | Hook enforced (warn) | `sovereigntyGate.py` systemMessage |
| Only finding-synthesiser writes `findings/`, both say and do inputs present | Hook enforced | `findingAuthorGate.py` (plus prompt reinforcement in the agent) |
| JS plots only, closed catalogue of four | Hook enforced | `plotBlocker.py` |
| Australian English, hyphen ban, paragraph length, display dates, banned phrasings (literal) | Hook enforced (non blocking) | `proseRules.py` |
| Pack coverage gaps stated as caveats | Hook enforced | `coverageWarner.py` |
| Documented surface matches shipped surface | Hook enforced | `contractValidator.py` |
| Only `engine/aggregate.py` writes final, ci, history, flag | Structurally enforced | The engine rewrites the ledger deterministically each run; agent prompts never carry the aggregation maths |
| report-qa and citation never modify files | Structurally enforced | No Write or Edit in their tools list |
| artefact-triage never scores | Prompt only (agent text), backed by `scoringGate.py` catching any scoring write without ledger evidence | Agent constraints plus the gate |
| Banned concepts expressed as synonyms (ownership, delivery horizons) | Prompt only — semantic | report-qa agent semantic battery; patterns alone are gameable by paraphrase |
| No personal names — speaker roles only | Prompt only | transcript-extractor, commitment-tracker, email-finder constraints |
| Tie break table applied in reconciliation | Prompt only | finding-synthesiser procedure (inputs gated by `findingAuthorGate.py`) |
| Recommendations carry no horizons or owners | Prompt only, with literal patterns caught by `proseRules.py` and semantics by report-qa | Layered |

The target across releases is to keep moving rules out of the prompt only bucket and into the top two.
