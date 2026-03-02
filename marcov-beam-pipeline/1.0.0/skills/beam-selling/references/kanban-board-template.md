# marcov.BEAM — Kanban Board

## {{COMPANY_NAME}} — {{DEAL_NAME}}

**Win Probability**: {{WIN_PROBABILITY}}% | **Days Active**: {{DAYS_ACTIVE}} | **Target Close**: {{TARGET_CLOSE}} | **Deal Value**: {{DEAL_VALUE}}

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│  1. QUALIFY      │  2. DIAGNOSE    │  3. ALIGN       │  4. PROPOSE     │  5. COMMIT      │  6. DELIVER     │
│  ○ Situation     │  ○ Problem →    │  ○ Implication → │  ○ Need-payoff  │  ○ Validation   │  ○ Continuous   │
│                  │    Implication   │    Need-payoff   │                 │                 │    Discovery    │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│                  │                 │                 │                 │                 │                 │
│ {{QUALIFY_CARDS}}│{{DIAGNOSE_CARDS}}│ {{ALIGN_CARDS}} │{{PROPOSE_CARDS}}│ {{COMMIT_CARDS}}│{{DELIVER_CARDS}}│
│                  │                 │                 │                 │                 │                 │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ GATE:           │ GATE:           │ GATE:           │ GATE:           │ GATE:           │ GATE:           │
│ {{QUALIFY_GATE}} │ {{DIAGNOSE_GATE}}│ {{ALIGN_GATE}}  │ {{PROPOSE_GATE}}│ {{COMMIT_GATE}} │ {{DELIVER_GATE}}│
└─────────────────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

---

## Card Types

Cards on the kanban board represent activities, evidence, and blockers within each stage.

### Activity Cards

```
┌───────────────┐
│ [icon] TITLE  │
│ Status: ...   │
│ Due: ...      │
│ Owner: ...    │
└───────────────┘
```

**Card statuses**:
- `TODO` — Not yet started
- `DOING` — In progress
- `DONE` — Completed
- `BLOCKED` — Waiting on external input

**Card icons**:
- `[R]` Research — desk research or web search activity
- `[M]` Meeting — call, meeting, or conversation
- `[E]` Evidence — evidence captured or documented
- `[D]` Document — deliverable produced (proposal, memo, agenda)
- `[S]` Stakeholder — stakeholder identified or engaged
- `[!]` Blocker — something preventing progress
- `[?]` Question — open question needing an answer

---

## Example Board (Populated)

### Acme Corp — Edge AI Platform

**Win Probability**: 35% | **Days Active**: 23 | **Target Close**: 2026-04-15 | **Deal Value**: $180K

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│  1. QUALIFY      │  2. DIAGNOSE    │  3. ALIGN       │  4. PROPOSE     │  5. COMMIT      │  6. DELIVER     │
│  ● COMPLETE      │  ● IN PROGRESS  │  ○ NOT STARTED  │  ○ NOT STARTED  │  ○ NOT STARTED  │  ○ NOT STARTED  │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│                  │                 │                 │                 │                 │                 │
│ [R] B2B dossier  │ [M] Discovery   │                 │                 │                 │                 │
│ DONE  2026-02-01 │ call #1         │                 │                 │                 │                 │
│                  │ DONE  2026-02-10│                 │                 │                 │                 │
│ [S] Identified   │                 │                 │                 │                 │                 │
│ Jane Smith (CTO) │ [E] 3 problems  │                 │                 │                 │                 │
│ DONE  2026-02-01 │ articulated     │                 │                 │                 │                 │
│                  │ DONE  2026-02-10│                 │                 │                 │                 │
│ [M] Intro call   │                 │                 │                 │                 │                 │
│ DONE  2026-02-05 │ [E] Quantified  │                 │                 │                 │                 │
│                  │ $2.1M impact    │                 │                 │                 │                 │
│ [E] ICP fit      │ DONE  2026-02-15│                 │                 │                 │                 │
│ confirmed (5/5)  │                 │                 │                 │                 │                 │
│ DONE  2026-02-01 │ [M] Discovery   │                 │                 │                 │                 │
│                  │ call #2         │                 │                 │                 │                 │
│                  │ TODO  2026-02-25│                 │                 │                 │                 │
│                  │                 │                 │                 │                 │                 │
│                  │ [?] Cost of     │                 │                 │                 │                 │
│                  │ inaction — need │                 │                 │                 │                 │
│                  │ CFO buy-in      │                 │                 │                 │                 │
│                  │ BLOCKED         │                 │                 │                 │                 │
│                  │                 │                 │                 │                 │                 │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│ GATE: 3/3 ██████ │ GATE: 2/3 ████░░│ GATE: 0/4 ░░░░░░│ GATE: 0/4 ░░░░░░│ GATE: 0/3 ░░░░░░│ GATE: 0/4 ░░░░░░│
│ [x] Problem dom. │ [x] Problems    │ [ ] Problem def.│ [ ] Addresses   │ [ ] Commitment  │ [ ] Outcomes    │
│ [x] Authority    │ [x] Implications│ [ ] Success crit│ [ ] Terms clear │ [ ] Terms agreed│ [ ] Relationship│
│ [x] Willing diag.│ [ ] Cost of     │ [ ] Stakeholders│ [ ] Decision    │ [ ] Handover    │ [ ] Future needs│
│                  │     inaction    │ [ ] Decision    │ [ ] Objections  │                 │ [ ] Case study  │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

---

## Multi-Engagement Kanban (Pipeline View)

When managing multiple deals, show a summary board with one row per engagement:

```
=== marcov.BEAM — Pipeline Kanban ===

         │ 1.Qualify  │ 2.Diagnose │ 3.Align   │ 4.Propose │ 5.Commit  │ 6.Deliver │
─────────┼────────────┼────────────┼───────────┼───────────┼───────────┼───────────┤
Acme     │            │  ●━━━━━━━● │           │           │           │           │
$180K    │  COMPLETE  │ 2/3 gates  │           │           │           │           │
35% win  │            │  23 days   │           │           │           │           │
─────────┼────────────┼────────────┼───────────┼───────────┼───────────┼───────────┤
BHP      │            │            │           │ ●━━━━━━━● │           │           │
$450K    │  COMPLETE  │  COMPLETE  │ COMPLETE  │ 3/4 gates │           │           │
65% win  │            │            │           │  12 days  │           │           │
─────────┼────────────┼────────────┼───────────┼───────────┼───────────┼───────────┤
Geelong  │ ●━━━━━━━●  │            │           │           │           │           │
$90K     │ 1/3 gates  │            │           │           │           │           │
10% win  │   5 days   │            │           │           │           │           │
─────────┴────────────┴────────────┴───────────┴───────────┴───────────┴───────────┘

Legend: ● = current stage    ━ = progress within stage
```

---

## Kanban Card Detail Format

When the user clicks into or asks about a specific card:

```
=== Card Detail ===

[M] Discovery Call #1
Stage:    2. Diagnose
Status:   DONE
Date:     2026-02-10
Owner:    You
Duration: 45 minutes

--- Summary ---
Met with Jane Smith (CTO) and Mark Lee (Head of Ops).
Discussed current asset management challenges.

--- SPIN Notes ---
Problem:     "We're spending 40% of maintenance budget on reactive repairs"
Implication: "That's costing us roughly $2.1M per year in unplanned downtime"

--- Evidence Captured ---
- 3 specific problems articulated (reactive maintenance, data silos, manual reporting)
- $2.1M annual impact quantified
- Jane confirmed this is a board-level concern

--- Gates Affected ---
[x] Problems articulated — MET (from this meeting)
[x] Implications quantified — MET (from this meeting)

--- Follow-Up ---
- Schedule call with CFO to discuss cost of inaction
- Send summary email to Jane and Mark
```

---

## Kanban Update Rules

The kanban board is updated automatically when:

1. **New activity starts** → Add a card in the current stage with status `TODO` or `DOING`
2. **Activity completes** → Update card status to `DONE`, add completion date
3. **Evidence captured** → Add an `[E]` card with the evidence summary
4. **Stakeholder identified** → Add an `[S]` card with name and role
5. **Blocker identified** → Add a `[!]` card describing the blocker
6. **Question raised** → Add a `[?]` card with the open question
7. **Gate criterion met** → Update the gate progress bar in the stage footer
8. **Stage transition** → Mark the previous stage as `COMPLETE`, activate the next stage
9. **Session ends** → All in-progress activities frozen; next session resumes from current state

---

## Kanban State in JSON

The kanban board is derived from the engagement state JSON. Each stage's cards are stored as an array:

```json
{
  "kanban": {
    "1_qualify": {
      "cards": [
        {
          "id": "q-001",
          "type": "research",
          "icon": "R",
          "title": "B2B dossier review",
          "status": "done",
          "created_at": "2026-02-01",
          "completed_at": "2026-02-01",
          "owner": "seller",
          "notes": "Ingested MBP:b2b-research dossier. ICP fit 5/5.",
          "evidence_ref": null,
          "gate_ref": "problem_domain_identified"
        },
        {
          "id": "q-002",
          "type": "stakeholder",
          "icon": "S",
          "title": "Identified Jane Smith (CTO)",
          "status": "done",
          "created_at": "2026-02-01",
          "completed_at": "2026-02-01",
          "owner": "seller",
          "notes": "Technical evaluator. From b2b-research dossier.",
          "evidence_ref": null,
          "gate_ref": "access_to_authority"
        }
      ]
    },
    "2_diagnose": {
      "cards": []
    },
    "3_align": {
      "cards": []
    },
    "4_propose": {
      "cards": []
    },
    "5_commit": {
      "cards": []
    },
    "6_deliver": {
      "cards": []
    }
  }
}
```

### Card Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique card ID (stage prefix + sequential number) |
| `type` | enum | `research`, `meeting`, `evidence`, `document`, `stakeholder`, `blocker`, `question` |
| `icon` | string | Display icon: `R`, `M`, `E`, `D`, `S`, `!`, `?` |
| `title` | string | Short card title (max 40 chars) |
| `status` | enum | `todo`, `doing`, `done`, `blocked` |
| `created_at` | date | When the card was created |
| `completed_at` | date | When the card was completed (null if not done) |
| `due_date` | date | Optional due date for TODO items |
| `owner` | string | Who owns this activity (`seller`, `prospect`, or a name) |
| `notes` | string | Detailed notes or summary |
| `evidence_ref` | string | Link to evidence item in the stage evidence array |
| `gate_ref` | string | Which gate criterion this card relates to (if any) |

---

*Template version: 1.0.0*
