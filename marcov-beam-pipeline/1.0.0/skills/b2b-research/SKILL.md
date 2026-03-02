---
name: MBP:b2b-research
description: Research and identify B2B engagement opportunities for a target company. Use when the user provides a company name to research as a potential client, partner, or engagement opportunity. Also supports broad pipeline building when no specific target is given. Conducts structured web research, compiles intelligence dossiers, maps decision-makers, and produces actionable engagement strategies with branded HTML reports and outreach templates. Output is designed to feed directly into the BEAM selling framework.
---

# B2B Research Agent Skill

Research and identify business-to-business engagement opportunities with a **problem-first** approach. This skill conducts structured web research to find problems worth solving, validate qualification, map buying committees, and produce intelligence that earns the right to a diagnostic conversation.

## Core Philosophy: Earn the Right

This skill is built on the principle that **progression is earned, not claimed**. Research should honestly assess:

1. **Is there a real problem we can solve?** — Not assumed, but evidenced
2. **Do we have access to authority?** — Specific people, not vague roles
3. **Is there willingness to engage?** — Signals of openness, not assumptions

The goal is not to "sell" — it's to **qualify whether a conversation is worth having**, and if so, to earn the right to have it.

## BEAM Integration

This skill produces output designed to feed directly into the **marcov.BEAM** (Bayesian Evidence-Advancing Markov) selling framework. Every dossier includes:

- **BEAM Qualification Readiness**: Pre-assessment of Stage 1 gate criteria
- **Problem Domain Analysis**: Evidence-based articulation of problems worth solving
- **Buying Committee Mapping**: Stakeholders by BEAM buying role
- **Qualification Signals**: Evidence supporting each Stage 1 gate

### BEAM Stage 1 Gates (What Research Must Support)

| Gate | Research Must Provide |
|------|----------------------|
| **Problem domain identified** | Specific, evidenced problems — not assumptions or generic categories |
| **Access to authority** | Named individuals with buying roles — not "someone in IT" |
| **Willingness to diagnose** | Signals that suggest openness to a conversation — or honest assessment of barriers |

**Qualifying out is a valid outcome.** If research reveals no real problem or no path to authority, that's valuable intelligence — don't force-fit an opportunity that doesn't exist.

## Overview

This skill helps you:

- **Problem Discovery**: Find specific, evidenced problems the prospect is experiencing — the foundation for any engagement
- **Qualification Assessment**: Honestly evaluate whether this prospect warrants pursuit under BEAM criteria
- **Buying Committee Mapping**: Identify stakeholders by BEAM buying role (Economic Buyer, Technical Evaluator, Champion, Gatekeeper)
- **Access Path Analysis**: Map routes to authority — warm introductions, events, content hooks
- **Engagement Readiness**: Assess signals of willingness to have a diagnostic conversation
- **Competitive Intelligence**: Understand what solutions prospects currently use and where gaps create problems
- **Pipeline Building**: Produce qualified prospect lists ranked by fit, timing, and qualification strength

## Input

This skill accepts a **target company name** as its primary input. The user provides the company they want to research, and the skill produces a full engagement dossier and HTML report for that company.

### Invocation Examples

```
/MBP:b2b-research GeelongPort
/MBP:b2b-research Research BHP for asset management consulting opportunities
/MBP:b2b-research Analyse Yarra Trams as a potential client for edge AI
```

When a target company is provided, **skip straight to the focused discovery questions below** — do not ask broad questions about target market, ICP, or how many prospects they need. The target is already known.

---

## Discovery Process (CRITICAL)

**Before conducting any research, you MUST conduct a brief discovery interview to understand the engagement context and what problem you're trying to solve for them.** Adapt the questions based on what was provided in the invocation.

### When a Target Company Is Provided (Most Common)

Ask only what you need to know about the **user's side** of the engagement. Skip target market and ICP questions — the target is already identified. Focus on understanding what problem your offering solves.

1. **Your Business & Problem You Solve**
   - What does your company do? (elevator pitch)
   - What **problem** does your offering solve? (be specific — not "improve efficiency" but the actual pain)
   - What does life look like for a prospect *before* they work with you? (the pain state)
   - What does life look like *after*? (the solved state)
   - Why should they choose you over doing nothing or using an alternative?

2. **Engagement Context**
   - What is the goal? (advisory engagement, product sale, partnership, tender response)
   - What triggered this interest in [Company]? (event, referral, news, cold opportunity)
   - Have you engaged with this company before? What happened?
   - Do you have any existing relationship or warm introduction path?
   - Is there an upcoming event, deadline, or trigger driving urgency?

3. **Qualification Criteria**
   - What signals would tell you this company has the problem you solve?
   - What would make this company a *bad* fit? (disqualifying criteria)
   - What level of authority do you typically need to engage? (C-suite, director, manager)

4. **Output Preferences**
   - Any specific focus areas? (e.g., focus on their technology landscape, or on decision-makers)
   - Do you need outreach templates included?
   - Will this feed into a BEAM engagement? (affects qualification depth)

Then proceed directly to **Phase 3: Deep-Dive Intelligence** for that specific company.

### When No Target Company Is Provided (Pipeline Mode)

If the user asks for broad prospect identification (e.g., "find companies in mining for us"), conduct the full discovery:

1. **Your Business**
   - What does your company do? (elevator pitch)
   - What products or services are you looking to sell or partner on?
   - What is your unique value proposition — why should a prospect choose you over alternatives?
   - What is your typical deal size and sales cycle length?

2. **Target Market**
   - What industry or vertical are you targeting? (e.g., mining, utilities, transport, government)
   - What company size are you targeting? (revenue range, employee count, geographic scope)
   - Are there specific geographies or regions you are focused on?
   - Are there any companies you already have in mind?

3. **Ideal Customer Profile (ICP)**
   - What business problems does your solution solve?
   - What does the ideal buyer look like? (role, department, seniority)
   - What technologies, systems, or processes does a good-fit company typically have in place?
   - Are there any disqualifying criteria? (too small, wrong industry, existing competitor contract)

4. **Engagement Goals**
   - What is the goal of this research? (cold outreach, conference preparation, partnership exploration, tender response)
   - Do you have an upcoming event, conference, or deadline driving this?
   - What does a successful engagement look like? (meeting booked, proposal sent, partnership signed)
   - How many prospects do you need?

5. **Existing Intelligence**
   - Do you have any existing prospect lists, CRM data, or past proposals to build on?
   - Have you engaged with any of these companies before? What happened?
   - Are there any warm introductions or mutual connections you know of?

6. **Output Preferences**
   - What format do you need? (HTML report, Markdown, CSV prospect list, outreach email drafts)
   - How detailed should each prospect profile be?
   - Do you need outreach templates customised per prospect?

---

## Research Methodology

### Phase 1: Define the Problem Domain

Before researching the company, establish clarity on what you're looking for:

1. **Articulate the problem hypothesis** — what specific problem do you believe this company has?
2. **Define problem signals** — what evidence would indicate they have this problem? (job postings, news, technology gaps, regulatory pressures)
3. **Define disqualifying signals** — what would tell you they *don't* have this problem or are a poor fit?
4. **Set research scope** — depth of research, time allocated

### Phase 2: Problem Signal Identification

Research with a problem-first lens — actively seek evidence that validates or invalidates your problem hypothesis:

1. **Pain signals in news** — incidents, complaints, regulatory issues, operational challenges
2. **Job postings** — roles that signal they're trying to solve problems you address
3. **Technology gaps** — systems that create problems your offering addresses
4. **Strategic priorities** — initiatives where your problem domain is relevant
5. **Industry benchmarks** — are they underperforming peers in your problem area?
6. **Executive commentary** — what are leaders saying about challenges?

**Be honest**: If you don't find evidence of the problem, document that. Qualifying out is valuable.

### Phase 3: Deep-Dive Intelligence

For each shortlisted prospect, compile with a **problem-centric focus**:

| Category | Details to Capture | BEAM Relevance |
|----------|-------------------|----------------|
| **Company Overview** | Name, HQ, revenue, employees, industry, sub-vertical | Context for fit assessment |
| **Business Model** | What they do, who they serve, how they make money | Understanding their world |
| **Problem Evidence** | **Specific evidence** that they have the problem you solve — not assumptions | **Gate 1: Problem domain** |
| **Pain Quantification** | What is this problem *costing* them? (dollars, time, risk, reputation) | BEAM Stage 2 preparation |
| **Technology Landscape** | Current systems and their limitations — *problems* created by their tech stack | Problem evidence |
| **Buying Committee** | Stakeholders mapped to BEAM buying roles (see below) | **Gate 2: Access to authority** |
| **Access Path** | How can you reach authority? Warm intros, events, content, cold | Gate 2 support |
| **Willingness Signals** | Evidence they're open to conversation — responding to content, attending events, issuing RFPs | **Gate 3: Willingness** |
| **Competitive Landscape** | Current vendors — are they *happy* or is there vendor fatigue/dissatisfaction? | Problem/timing signal |
| **Qualification Assessment** | Honest evaluation: is this a real opportunity or are we forcing it? | BEAM integrity |

#### Decision-Maker Identification via LinkedIn (CRITICAL)

**You MUST use web search with `site:linkedin.com/in` to find and identify key decision-makers.** This is a core part of every dossier.

**Search strategy — run these searches for each target company:**

1. **C-Suite and senior leadership:**
   ```
   site:linkedin.com/in "[Company Name]" CEO OR "Managing Director" OR "General Manager"
   ```

2. **Operational / technical leaders (adapt titles to the offering):**
   ```
   site:linkedin.com/in "[Company Name]" "Head of" OR "Director" OR "VP" operations OR technology OR engineering OR "asset management"
   ```

3. **Financial decision-makers:**
   ```
   site:linkedin.com/in "[Company Name]" CFO OR "Chief Financial" OR "Finance Director" OR "Head of Finance"
   ```

4. **Procurement / buying roles:**
   ```
   site:linkedin.com/in "[Company Name]" procurement OR purchasing OR "vendor management" OR "strategic sourcing"
   ```

5. **Domain-specific roles (tailor to what you're selling):**
   ```
   site:linkedin.com/in "[Company Name]" "digital transformation" OR "innovation" OR "data" OR "analytics"
   ```

**For each decision-maker found, capture:**

| Field | What to Record |
|-------|---------------|
| **Full Name** | As shown on their LinkedIn profile |
| **Title** | Current job title |
| **Department** | Inferred from title (e.g., Operations, IT, Finance, Strategy) |
| **LinkedIn URL** | Direct link to their profile (e.g., `https://linkedin.com/in/firstname-lastname`) |
| **Relevance** | Why this person matters for the engagement (budget authority, technical evaluator, operational sponsor, etc.) |
| **Background Notes** | Career history, prior companies, education, shared connections — anything useful for personalisation |
| **Engagement Angle** | How to approach this person specifically (what to reference, what pain point to lead with) |

**Map the BEAM buying committee** — identify at minimum:

| BEAM Role | Description | Typical Titles | What They Care About |
|-----------|-------------|----------------|---------------------|
| **Economic Buyer** | Controls the budget; makes the final financial decision | CEO, CFO, VP, GM | ROI, risk, strategic fit |
| **Technical Evaluator** | Assesses solution fit and technical feasibility | CTO, Head of IT, Engineering Director | Will it work? Integration? |
| **Champion / Sponsor** | Internally advocates for your solution; *feels the pain most* | Director, Senior Manager, Program Lead | Solving their problem |
| **Gatekeeper** | Controls access to decision-makers and process | EA, Procurement Manager, PMO | Process, compliance, vendor management |

**CRITICAL**: For BEAM Stage 1, you need at least one **named individual** you can access — not just "someone in IT". The skill will challenge vague answers.

### Phase 4: BEAM Qualification Assessment

Before producing engagement strategy, **honestly assess BEAM Stage 1 gate readiness**:

#### Gate 1: Problem Domain Identified

| Assessment | Criteria |
|------------|----------|
| **STRONG** | Multiple specific problems evidenced with sources; problems align directly to your offering |
| **MODERATE** | Some problem signals found but not highly specific; requires validation in discovery |
| **WEAK** | Assumed problems based on industry norms; no company-specific evidence |
| **NONE** | No evidence of the problem you solve; consider qualifying out |

#### Gate 2: Access to Authority

| Assessment | Criteria |
|------------|----------|
| **STRONG** | Named individual identified; existing relationship or warm introduction path |
| **MODERATE** | Named individual identified; no relationship but clear outreach path |
| **WEAK** | Roles identified but no specific names; requires LinkedIn research |
| **NONE** | No path to authority visible; consider qualifying out |

#### Gate 3: Willingness to Diagnose

| Assessment | Criteria |
|------------|----------|
| **STRONG** | Active signals: issued RFP, attending your events, responded to content |
| **MODERATE** | Passive signals: in relevant industry groups, hiring in your area |
| **WEAK** | No signals but no negative indicators either |
| **NONE** | Negative signals: recently bought competitor, stated no interest |

#### Qualification Verdict

Based on the gate assessment, issue a verdict:

| Verdict | Criteria | Recommended Action |
|---------|----------|-------------------|
| **QUALIFIED** | 2+ gates STRONG, none NONE | Proceed to engagement strategy |
| **EXPLORATORY** | Mixed signals; worth pursuing with lower investment | Light-touch outreach; validate problem first |
| **NURTURE** | Weak signals; not ready now | Add to content nurture; revisit in 6 months |
| **DISQUALIFIED** | Any gate NONE; fundamental misalignment | Document reasons; do not pursue |

### Phase 5: Engagement Strategy (If Qualified)

For qualified prospects, produce:

1. **BEAM Gate Readiness** — assessment of each Stage 1 gate with supporting evidence
2. **Fit Score** (1–5) based on ICP alignment and problem evidence strength
3. **Timing Score** (1–5) based on buying signals and urgency
4. **Qualification Strength** — STRONG, MODERATE, or EXPLORATORY
5. **First Contact Goal** — earn the right to a diagnostic conversation (not sell!)
6. **Problem-Led Talking Points** — 3–5 points leading with their problem, not your solution
7. **Discovery Questions** — SPIN-aligned questions to validate problem in first conversation
8. **Outreach Sequence** — multi-touch plan focused on earning the right to a conversation

---

## Output Formats

### 1. Executive Opportunity Summary

**Always lead with this summary before presenting the full dossier.** It gives the user an immediate read on whether the prospect qualifies and at what confidence level.

```markdown
# [Company Name] — Engagement Opportunity

## BEAM Qualification Readiness

| Gate | Status | Evidence Summary |
|------|--------|-----------------|
| **Problem Domain** | [STRONG/MODERATE/WEAK/NONE] | [1-line evidence summary] |
| **Access to Authority** | [STRONG/MODERATE/WEAK/NONE] | [Named contact or access path] |
| **Willingness to Diagnose** | [STRONG/MODERATE/WEAK/NONE] | [Signal or barrier] |

**Qualification Verdict: [QUALIFIED / EXPLORATORY / NURTURE / DISQUALIFIED]**

---

## Key Findings

🎯 **Problem We Can Solve**
- [Specific problem identified — evidenced, not assumed]
- [Impact of this problem on their business]
- [Why your offering addresses this problem specifically]

⏰ **Timing Signals**
- [Evidence of urgency — deadline, event, initiative]
- [Window of opportunity]
- [Risk if timing is missed]

🔑 **Buying Committee**
- **Economic Buyer**: [Name] ([Title]) — [access status]
- **Champion**: [Name] ([Title]) — [relationship status]
- **Technical Evaluator**: [Name] ([Title]) — [relevance]
- **Gatekeeper**: [Name/role] — [known or unknown]

💡 **Access Path**
- [Best route to a conversation — warm intro, event, content, cold]
- [Relationship leverage points]
- [Barriers to access and mitigation]

📊 **Qualification Confidence**
- [Fit Score]: [X/5] — [1-line rationale]
- [Timing Score]: [X/5] — [1-line rationale]
- [Overall]: [HIGH/MEDIUM/LOW] confidence this warrants pursuit

---

**First Contact Goal**: Earn the right to a diagnostic conversation — validate problem hypothesis, not pitch solution.

**If DISQUALIFIED**: [Reason] — document and move on. Qualifying out is a success.
```

---

### 2. Prospect Intelligence Dossier (Per Company)

The full detailed output for deep research on a single prospect.

```markdown
# [Company Name] — Engagement Dossier

## Company Snapshot

| Field | Detail |
|-------|--------|
| **Company** | [Name] |
| **Website** | [URL] |
| **Headquarters** | [City, State/Country] |
| **Industry** | [Primary vertical] |
| **Revenue** | [Annual revenue or range] |
| **Employees** | [Headcount or range] |
| **Ownership** | [Public/Private/Government] |

## Business Overview

[2–3 paragraph summary of what the company does, who they serve, and their market position.]

## Strategic Priorities

- [Priority 1 — with source/evidence]
- [Priority 2 — with source/evidence]
- [Priority 3 — with source/evidence]

## Pain Points & Challenges

- [Pain point 1 — how it relates to your offering]
- [Pain point 2 — how it relates to your offering]
- [Pain point 3 — how it relates to your offering]

## Technology Landscape

| System | Vendor/Product | Notes |
|--------|---------------|-------|
| ERP | [e.g., SAP S/4HANA] | [Implementation date, known issues] |
| EAM | [e.g., IBM Maximo] | [Version, satisfaction level] |
| CRM | [e.g., Salesforce] | [Usage context] |
| Other | [Relevant systems] | [Notes] |

## Decision-Makers

*Found via `site:linkedin.com/in` web search*

| Name | Title | Department | Buying Role | Relevance | LinkedIn |
|------|-------|------------|-------------|-----------|----------|
| [Name] | [Title] | [Dept] | Economic Buyer | [Why they matter] | [linkedin.com/in/...] |
| [Name] | [Title] | [Dept] | Technical Evaluator | [Why they matter] | [linkedin.com/in/...] |
| [Name] | [Title] | [Dept] | Champion / Sponsor | [Why they matter] | [linkedin.com/in/...] |
| [Name] | [Title] | [Dept] | Gatekeeper | [Why they matter] | [linkedin.com/in/...] |

## Buying Signals

- [Signal 1 — date, source, interpretation]
- [Signal 2 — date, source, interpretation]

## Competitive Intelligence

| Competitor | Product/Service | Relationship Status | Vulnerability |
|-----------|----------------|--------------------:|--------------|
| [Vendor] | [Product] | [Active/Expiring/Dissatisfied] | [Why you could displace] |

## Engagement Strategy

### Fit Score: [X/5] | Timing Score: [X/5] | Priority: [HIGH/MEDIUM/LOW]

### Recommended Approach
[Specific approach — e.g., "Warm introduction via [mutual contact] targeting [decision-maker] at [upcoming event]"]

### Personalised Talking Points
1. [Point linking your value prop to their specific situation]
2. [Point referencing their recent initiative/announcement]
3. [Point addressing a known pain point]
4. [Point differentiating from their current vendor]

### Potential Objections & Responses
| Objection | Response |
|-----------|----------|
| "[Expected objection]" | "[How to counter]" |

### Outreach Sequence
| Step | Channel | Timing | Action |
|------|---------|--------|--------|
| 1 | Email | Day 1 | [Initial outreach — personalised cold email] |
| 2 | LinkedIn | Day 3 | [Connection request with note] |
| 3 | Email | Day 7 | [Follow-up with value-add content] |
| 4 | Phone | Day 10 | [Call script — reference email] |
| 5 | Email | Day 14 | [Break-up email or pivot to different contact] |

---

*Research compiled: [Date]*
*Sources: [List key sources]*
```

### 3. Prospect Pipeline (Multi-Company)

For batch research across multiple prospects.

```markdown
# B2B Prospect Pipeline — [Target Vertical / Campaign Name]

## Research Parameters

- **Your Company**: [Name]
- **Offering**: [Product/Service]
- **Target Vertical**: [Industry]
- **Target Geography**: [Region]
- **ICP Criteria**: [Summary]
- **Date**: [Research date]

## Pipeline Summary

| # | Company | Industry | Revenue | Fit | Timing | Priority | Recommended Approach |
|---|---------|----------|---------|-----|--------|----------|---------------------|
| 1 | [Name] | [Vertical] | [Rev] | [1-5] | [1-5] | HIGH | [Approach] |
| 2 | [Name] | [Vertical] | [Rev] | [1-5] | [1-5] | HIGH | [Approach] |
| 3 | [Name] | [Vertical] | [Rev] | [1-5] | [1-5] | MEDIUM | [Approach] |

## Tier 1 Prospects (High Priority)

### [Company 1]
[Brief paragraph — why they are Tier 1, key trigger, recommended next step]

**Key Contact**: [Name, Title]
**Trigger**: [What makes this timely]
**Next Step**: [Specific action]

### [Company 2]
...

## Tier 2 Prospects (Medium Priority)

### [Company 3]
...

## Tier 3 Prospects (Monitor)

### [Company N]
...

## Recommended Actions (Next 30 Days)

1. [Action 1 — specific, measurable, with owner and deadline]
2. [Action 2]
3. [Action 3]

---

*Pipeline compiled: [Date]*
```

### 4. Outreach Email Templates

Personalised email sequences for each prospect.

```markdown
# Outreach Templates — [Company Name]

## Email 1: Initial Outreach

**Subject**: [Personalised subject line referencing their situation]
**To**: [Decision-maker name and title]

---

Hi [First Name],

[Opening line referencing a specific trigger — their recent announcement, a shared connection, or industry event.]

[1–2 sentences connecting their challenge to your value proposition. Be specific to their situation, not generic.]

[Social proof — a brief reference to a similar company you've helped, with a measurable outcome.]

[Clear, low-commitment call to action — e.g., "Would a 15-minute call next week make sense to explore whether this could work for [Company]?"]

Best regards,
[Your Name]
[Your Title] | [Your Company]
[Phone] | [Email]

---

## Email 2: Follow-Up (Day 7)

**Subject**: Re: [Original subject] — [Value-add hook]

---

Hi [First Name],

[Reference previous email briefly — don't guilt-trip.]

[Provide genuine value — share a relevant insight, article, case study, or data point that's useful to them regardless of whether they buy.]

[Reiterate the CTA with a slight variation.]

Best regards,
[Your Name]

---

## Email 3: Break-Up (Day 14)

**Subject**: Should I close your file?

---

Hi [First Name],

[Acknowledge they're busy. No pressure.]

[One final value statement — "If [specific outcome] is still a priority for [Company], I'd welcome the chance to share how [your company] helped [similar company] achieve [result]."]

[Permission-based close — "If the timing isn't right, no worries at all. I'll keep an eye out for anything relevant to share."]

Best regards,
[Your Name]
```

### 5. Conference / Event Prep Brief

For preparing engagement strategies around a specific event.

```markdown
# Event Engagement Brief — [Event Name]

## Event Details

| Field | Detail |
|-------|--------|
| **Event** | [Name] |
| **Date** | [Date range] |
| **Location** | [Venue, City] |
| **Website** | [URL] |
| **Our Presence** | [Exhibiting/Attending/Speaking/Sponsoring] |

## Target Attendees

| # | Company | Contact | Title | Booth/Session | Engagement Plan |
|---|---------|---------|-------|---------------|----------------|
| 1 | [Company] | [Name] | [Title] | [Location] | [Approach] |

## Pre-Event Outreach

[Email templates to send before the event requesting meetings.]

## On-Site Talking Points

### For [Company 1]
- [Point 1]
- [Point 2]
- [Point 3]

## Post-Event Follow-Up

[Follow-up email template referencing the conversation at the event.]
```

### 6. HTML Report (Standalone Web Document)

**The preferred delivery format.** A polished, branded HTML report with SAS-AM styling, light/dark mode toggle, sidebar navigation, and interactive elements. Opens directly in any browser.

#### File Structure

```
report-folder/
├── report.html          # Main report file
├── styles.css           # Report theme styles (from references/report-styles.css)
└── assets/              # Logos and images
    ├── sas-logo-light.png
    └── sas-logo-dark.png
```

#### How to Build

1. Create a new directory for the report
2. Copy `report-styles.css` from references as `styles.css`
3. Copy `report-template.html` from references as the scaffold
4. Replace all `{{PLACEHOLDER}}` values with research findings
5. Add or remove sections, table rows, cards, and timeline steps as needed
6. Place logo assets in `assets/`

#### Key Features

- **Light/Dark Mode**: Toggle via header button, saved to localStorage
- **Sidebar Navigation**: Sticky nav with scroll-tracking highlights (IntersectionObserver)
- **Executive Summary Cards**: Grid of finding cards with icons (🎯 ⏰ 💡 🔑 📊)
- **Score Badges**: Colour-coded circular badges (1–5) for Fit and Timing scores
- **Priority Badges**: HIGH (red), MEDIUM (amber), LOW (grey) pill badges
- **Outreach Timeline**: Vertical timeline with day markers and channel badges
- **Summary Callout**: Green-bordered highlight box for the executive conclusion
- **Responsive**: Collapses sidebar on small screens, stacks cards on mobile
- **Print-Ready**: Hides interactive elements, clean page layout

#### Design System

Uses the same SAS-AM brand system as the presentation skill:

| Element | Light Mode | Dark Mode |
|---------|-----------|-----------|
| Brand Blue | `#002244` | `#1a4d7a` |
| Brand Green | `#69BE28` | `#7AD33B` |
| Background | `#ffffff` | `#0a0f1a` |
| Text Primary | `#002244` | `#f4fbff` |
| Card Background | `#ffffff` | `#141d2b` |

**Typography**: Source Sans Pro (300, 400, 600, 700 weights) from Google Fonts
**Icons**: Font Awesome 6.5.1 from CDN

---

## Scoring Rubric (CRITICAL — Pessimistic by Default)

**Philosophy**: Default to skepticism. A prospect must *earn* a high score through concrete evidence, not assumptions or optimism. If you're uncertain, score down. It's better to undersell a qualified opportunity than to overcommit to a dud.

### Fit Score (1–5) — Assume Low Until Proven Otherwise

| Score | Criteria | Evidence Required | Red Flags That Drop Score |
|-------|----------|-------------------|---------------------------|
| **5 — Perfect Fit** | Has **documented evidence** of the exact problem you solve; matches ALL ICP criteria with proof | Direct quotes, specific incident reports, job postings explicitly describing the problem, regulatory filings showing the issue | Never assume 5 without multiple independent evidence sources |
| **4 — Strong Fit** | Has **multiple signals** of the problem; matches most ICP criteria | At least 2 independent evidence sources confirming problem domain | Single evidence source = max score 3 |
| **3 — Moderate Fit** | Some evidence of potential problem; matches core ICP criteria | At least 1 concrete signal; plausible fit argument | Industry-level assumptions without company-specific evidence |
| **2 — Weak Fit** | Industry suggests potential fit but **no company-specific evidence** of the problem | ICP match on paper only | Assuming need based on what "companies like them" typically have |
| **1 — Poor Fit** | No evidence of problem; disqualifying criteria present | N/A — this is the absence of evidence | Evidence of recent competitor purchase; stated no need; misaligned industry |

**Default starting point**: Score 2 until evidence moves it up. Optimism doesn't earn points.

### Timing Score (1–5) — Assume Cold Until Proven Hot

| Score | Criteria | Evidence Required | Red Flags That Drop Score |
|-------|----------|-------------------|---------------------------|
| **5 — Immediate** | Active RFP mentioning your problem domain; **documented** budget allocation; leadership statement with deadline | Written RFP, board announcement with timeline, regulatory deadline | "They're probably looking" = max score 2 |
| **4 — Near-Term** | Recent trigger event **specifically** related to your problem domain; decision expected within 6 months | Job posting for role that would use your solution; incident report; leadership change with relevant mandate | Trigger event unrelated to your problem domain = score 3 max |
| **3 — Medium-Term** | Strategic alignment visible; no confirmed timeline; may be 6–12 months | Strategic plan mentions your problem area; preliminary discussions reported | No timeline visibility = cap at 3 regardless of fit |
| **2 — Long-Term** | Potential future need based on industry trends; **no company-specific signals** | Industry reports suggesting eventual need | Assuming timing based on "everyone will need this eventually" |
| **1 — No Signal** | No buying signals detected; no trigger events; no urgency indicators | N/A — this is the absence of evidence | Evidence of recent purchase or "not a priority" statement |

**Default starting point**: Score 2 until a specific, dated trigger event moves it up.

### Qualification Rigour Tests

Before assigning Fit or Timing scores, answer these questions honestly:

| Test | Question | If "No"... |
|------|----------|-----------|
| **Specificity** | Is this evidence specific to THIS company, or just industry-level assumptions? | Cap score at 2 |
| **Recency** | Is this evidence from the last 12 months? | Reduce score by 1 |
| **Independence** | Do you have 2+ independent sources? | Cap Fit at 3 |
| **Problem Match** | Does the evidence directly match YOUR problem domain, or just adjacent? | Cap Fit at 3 |
| **Timeline Clarity** | Is there a specific date, deadline, or decision event? | Cap Timing at 3 |
| **Access Reality** | Can you actually reach a decision-maker, or are you hoping? | Note barrier in assessment |

### Priority Matrix (Conservative)

**Default to NURTURE unless evidence compels higher priority.** Pursuing a weak opportunity costs more than missing a marginal one.

| | Timing 4–5 (Hot) | Timing 3 (Warm) | Timing 1–2 (Cold) |
|---|---|---|---|
| **Fit 5** | **HIGH** — Pursue immediately; rare — verify twice | **MEDIUM** — Nurture actively; timing may shift | **LOW** — Monitor; great fit but no urgency |
| **Fit 4** | **HIGH** — Strong case; validate access | **MEDIUM** — Worth light pursuit | **NURTURE** — Build relationship |
| **Fit 3** | **MEDIUM** — Validate problem first | **NURTURE** — Stay in touch | **SKIP** — Not worth the effort |
| **Fit 1–2** | **EXPLORATORY** at best — validate fit first | **SKIP** | **SKIP** |

### Evidence Quality Tiers

| Tier | Evidence Type | Score Multiplier |
|------|--------------|------------------|
| **Tier 1 (Gold)** | Direct quote from prospect; their written RFP; their public filing mentioning the problem | Full score valid |
| **Tier 2 (Silver)** | News article about them + the problem; job posting; investor report mentioning challenge | Score - 1 max unless corroborated |
| **Tier 3 (Bronze)** | Industry analyst report; peer company comparison; your assumption based on typical patterns | Cap at 3 regardless of logic |
| **Tier 4 (Lead)** | "Companies like them usually..." / "They must have..." / "I assume..." | Cap at 2; flag as unverified |

### Honest Assessment Output

For every Fit and Timing score, document:

```
Fit Score: X/5
- Evidence: [What specific evidence supports this?]
- Evidence Tier: [Gold/Silver/Bronze/Lead]
- Confidence Killer: [What would disprove this?]
- Honest Doubt: [What aren't you sure about?]

Timing Score: X/5
- Evidence: [What specific trigger/signal supports this?]
- Evidence Tier: [Gold/Silver/Bronze/Lead]
- Timeline Uncertainty: [What could delay or accelerate?]
- Honest Doubt: [What aren't you sure about?]

Overall Assessment: [QUALIFIED/EXPLORATORY/NURTURE/DISQUALIFIED]
Confidence Level: [HIGH/MEDIUM/LOW]
If Wrong: [What's the cost if this assessment is wrong?]
```

---

## Research Sources

When conducting research, prioritise these source types:

### Primary Sources (Most Reliable)
- Company website (About, Careers, News/Blog, Investor Relations)
- Annual reports and investor presentations
- SEC filings (for public companies)
- Government procurement portals and tender notices
- Official press releases

### LinkedIn Sources (Decision-Maker Identification — REQUIRED)
- **`site:linkedin.com/in "[Company]" [title]`** — find specific people by company and role
- **`site:linkedin.com/company "[Company]"`** — company page for employee count, industry, and overview
- **`site:linkedin.com/in "[Company]" "joined" OR "started"`** — recent hires signalling investment areas
- **`site:linkedin.com/posts "[Company]" [topic]`** — stakeholder posts revealing priorities and opinions

### Secondary Sources (Cross-Reference)
- Industry publications and trade journals
- Conference programmes and speaker lists
- Industry association member directories
- News aggregators and business media

### Signal Sources (Buying Intent)
- Job postings (especially for roles in your solution area)
- Technology review sites (G2, Gartner Peer Insights, Capterra)
- Patent filings and R&D announcements
- Regulatory filings and compliance reports
- Social media activity (LinkedIn posts from key stakeholders)

---

## Workflow

### Path A: Target Company Provided (Single-Company Dossier)

Use this path when the user provides a specific company name (the most common invocation).

**Step 1: Problem-First Discovery**
- Ask the focused discovery questions: what problem do you solve? what would evidence of that problem look like?
- Confirm the target company name and establish a problem hypothesis
- Clarify: what would make this company a *bad* fit?

**Step 2: Problem Evidence Research**
- Search for evidence that validates the problem hypothesis:
  - News articles mentioning challenges, incidents, or pain in your problem domain
  - Job postings for roles that signal they're trying to solve this problem
  - Technology limitations that create the problem you address
  - Executive statements about challenges or priorities
  - Industry benchmarks showing underperformance
- **Be honest**: Document both confirming AND disconfirming evidence
- If no problem evidence found, document that — qualifying out is valid

**Step 3: Buying Committee Mapping**
- **Search LinkedIn for decision-makers** using `site:linkedin.com/in "[Company]" [title]` queries:
  - Search for Economic Buyers (CEO, CFO, GM, VP)
  - Search for Technical Evaluators (CTO, Head of Engineering, IT Director)
  - Search for potential Champions (directors and managers in the problem domain)
  - Search for Gatekeepers (procurement, EA, PMO)
- For each person found: capture name, title, LinkedIn URL, BEAM buying role, and access assessment
- Identify the most viable access path — who can you actually reach?

**Step 4: BEAM Qualification Assessment**
- Assess each Stage 1 gate:
  - **Problem Domain**: Is there specific, evidenced problem or just assumptions?
  - **Access to Authority**: Do you have a named individual and a path to reach them?
  - **Willingness**: What signals suggest they'd engage in a conversation?
- Issue a qualification verdict: QUALIFIED, EXPLORATORY, NURTURE, or DISQUALIFIED
- If DISQUALIFIED: Document the reason and stop — this is valuable intelligence, not failure

**Step 5: Engagement Strategy (If Qualified)**
- Score fit and timing (1–5 each)
- Develop problem-led talking points (lead with their pain, not your features)
- Prepare SPIN discovery questions for the first conversation
- Design outreach focused on earning the right to a diagnostic conversation
- Anticipate barriers and prepare to address them

**Step 6: Delivery**
- Build the branded HTML report from the template
- **Lead with BEAM Qualification Readiness** — gate assessments and verdict
- Include the Executive Opportunity Summary
- Include full dossier, strategy, and outreach plan
- **First Contact Goal**: Earn the right to a diagnostic conversation
- Provide recommended next steps with dates
- **If DISQUALIFIED**: Deliver a brief disqualification report explaining why — this is still valuable output

### Path B: No Target Company (Pipeline Mode)

Use this path when the user asks for broad prospect identification across a market.

**Step 1: Full Discovery**
- Conduct the complete 6-section discovery interview
- Confirm ICP criteria, target vertical, geography, and scope

**Step 2: Research Planning**
1. Define the research scope (number of prospects, depth, geography)
2. Establish the scoring rubric (confirm or adjust default criteria)
3. Identify primary research sources for the target vertical

**Step 3: Prospect Identification**
1. Use web search to identify candidate companies
2. Apply ICP filters to create a shortlist
3. Validate each candidate against qualifying criteria

**Step 4: Deep-Dive Research**
For each shortlisted prospect:
1. Compile the company snapshot
2. Map decision-makers and buying committee
3. Identify pain points and engagement triggers
4. Assess competitive landscape
5. Score fit and timing

**Step 5: Strategy Development**
1. Rank prospects into tiers (High / Medium / Monitor)
2. Develop personalised engagement strategies per prospect
3. Draft outreach templates and talking points
4. Create a 30-day action plan

### Step 6: Delivery

1. **Build the HTML report** using the branded template (report-template.html + report-styles.css):
   - Create a report directory
   - Copy `report-styles.css` from references as `styles.css`
   - Copy `report-template.html` from references and populate all placeholders with research findings
   - Add/remove sections, table rows, and cards as needed
   - Place logo assets in `assets/`
2. Review for accuracy and completeness
3. Highlight the top 3 recommended next steps
4. Deliver the final report (HTML by default, Markdown if requested)

---

## Content Writing Guidelines

### Dossier Tone
- **Professional and analytical** — present findings as intelligence, not opinion
- **Evidence-based** — cite sources and dates for all claims
- **Actionable** — every insight should connect to a recommended action
- **Concise** — use tables for structured data, paragraphs for analysis

### Outreach Tone
- **Personalised** — reference specific company details, never generic
- **Value-first** — lead with insight, not a sales pitch
- **Respectful** — acknowledge their time; no pressure tactics
- **Credible** — include specific social proof with measurable outcomes
- **Australian English** — use Australian spelling conventions (organisation, colour, behaviour, prioritise)

### Formatting Standards
- **Default output is an HTML report** using the branded report template (report-template.html + report-styles.css)
- Fall back to Markdown if the user specifically requests it
- Use tables for structured/comparative data
- Use bullet points for lists of findings
- Use headings (H2/H3) to organise sections
- Include a date stamp on all deliverables
- Link to sources where possible

---

## Engagement Timeline Generation

The engagement timeline provides a **chronological view of all activities** related to a prospect. It complements the kanban board by showing the full history of engagement in an easy-to-scan format.

### When to Generate Timeline

Generate or update the timeline HTML file:
- After initial research dossier is complete
- When major activities occur (outreach, meetings, documents, decisions)
- At the end of each engagement session
- When advancing to a new BEAM stage

### Timeline File Structure

Store the timeline in the engagement directory:

```
.beam/
└── engagements/
    ├── {company}-timeline.html    # Visual timeline (HTML)
    ├── {company}-kanban.html      # Kanban board (HTML)
    └── {company}.json             # Engagement state (JSON)
```

### Timeline Entry Requirements

Each timeline entry MUST include:

| Field | Required | Description |
|-------|----------|-------------|
| `date` | Yes | Specific date in DD MMM YYYY format (e.g., "23 Feb 2026") |
| `type` | Yes | One of: outreach, meeting, document, evidence, decision, milestone, blocker |
| `stage` | Yes | BEAM stage number (1-6) |
| `title` | Yes | Specific action title — NOT generic (see specificity guidelines below) |
| `description` | Yes | 1-2 sentences explaining what happened |
| `details` | Recommended | Structured key:value pairs with specifics (channel, recipient, file, etc.) |
| `outcome` | Recommended | success, pending, or blocked with description |

### Timeline Entry Specificity (CRITICAL)

**BAD (too generic):**
```
title: "Outreach to James Hicks"
description: "Sent message requesting catch-up"
```

**GOOD (specific and actionable):**
```
title: "LinkedIn message sent to James Hicks"
description: "Sent personalised message referencing AMPEAK2024 conference and Bega consolidation news, requesting coffee catch-up to discuss asset management challenges."
details:
  Channel: LinkedIn
  Recipient: James Hicks (Group Manager Asset Management)
  Message: "Hi James, Hope you're well! I've been following the Bega consolidation news..."
outcome: pending — Awaiting response
```

### Timeline Template

Use `references/engagement-timeline-template.html` as the scaffold. Replace placeholders:

| Placeholder | Value |
|-------------|-------|
| `{{COMPANY_NAME}}` | Prospect company name |
| `{{CURRENT_STAGE}}` | BEAM stage number (1-6) |
| `{{WIN_PROBABILITY}}` | Current win probability percentage |
| `{{DAYS_ACTIVE}}` | Days since engagement started |
| `{{ACTIVITY_COUNT}}` | Total number of timeline entries |
| `{{GENERATED_DATE}}` | Current date |
| `{{TIMELINE_ENTRIES}}` | HTML for each timeline entry (see template comments) |

---

## Kanban Board Management

The kanban board visualises current activities and BEAM gate progress. It should be **updated immediately** when activities are proposed, started, completed, or blocked.

### Kanban Update Triggers

Update the kanban board when:

| Trigger | Action |
|---------|--------|
| **Research completed** | Add card with status "done" |
| **Outreach sent** | Add card with status "doing", awaiting response |
| **Meeting scheduled** | Add card with status "todo", include date |
| **Meeting held** | Move card to "done", add outcome notes |
| **Document created** | Add card with status "done", reference file |
| **Evidence captured** | Add card with status "done", link to gate |
| **Blocker identified** | Add card with status "blocked", describe issue |
| **Gate criteria met** | Update gate in JSON, add evidence card |
| **Stage transition** | Move cards to archive, update stage status |

### Kanban Card Specificity (CRITICAL)

Every kanban card MUST be specific enough that someone reading it understands exactly what happened without needing to investigate further.

**BAD EXAMPLES:**

| Card | Problem |
|------|---------|
| "Research complete" | What research? What was found? |
| "Outreach to James" | What channel? What was said? When? |
| "Meeting scheduled" | With whom? When? What's the agenda? |
| "Document created" | What document? Where is it? |

**GOOD EXAMPLES:**

| Card | Why It Works |
|------|-------------|
| "B2B dossier ingested — Fit: 5/5, Timing: 5/5, 21 manufacturing sites identified" | Specific outcome, quantified |
| "LinkedIn message sent to James Hicks 23 Feb — referenced AMPEAK2024, requested coffee" | Channel, date, content summary |
| "Discovery call scheduled: James Hicks, 28 Feb 2pm AEDT, Teams" | All logistics clear |
| "Pilot proposal drafted: bega-pilot-proposal.html — $35K, 5 weeks, 2-3 sites" | File reference, commercial terms |

### Card Notes Requirements

The `notes` field on each kanban card should include:

1. **What was done** — specific action taken
2. **Evidence captured** — any quotes, data, or signals gathered
3. **Outcome/status** — result of the action
4. **Next step dependency** — what's waiting on this card

Example:
```json
{
  "id": "1-004",
  "type": "meeting",
  "title": "LinkedIn message sent to James Hicks 23 Feb",
  "status": "doing",
  "notes": "Sent personalised message via LinkedIn referencing AMPEAK2024 and Bega consolidation. Message: 'Hi James, Hope you're well! I've been following the Bega consolidation news...' Awaiting response. Follow up Day 3 (26 Feb) if no reply. Gate: access_to_authority depends on positive response.",
  "gate_ref": "access_to_authority",
  "created_at": "2026-02-23"
}
```

### Kanban State Consistency

The kanban board and engagement JSON must stay in sync:

1. **activity_log[]** in JSON should match kanban cards
2. **timeline.milestones[]** should reflect completed kanban cards
3. **stages.{stage}.evidence[]** should reference evidence-type cards
4. **kanban.{stage}.cards[]** should have correct status reflecting JSON state

---

## Activity Update Protocol

When ANY of the following activities occur, you MUST update both the **kanban board** and **timeline**:

### Immediate Update Activities

| Activity | Kanban Update | Timeline Update |
|----------|---------------|-----------------|
| **Outreach sent** (email, LinkedIn, call) | Add card: type=meeting, status=doing | Add entry: type=outreach |
| **Response received** | Update card status to done/blocked | Add entry: type=evidence or blocker |
| **Meeting scheduled** | Add card: type=meeting, status=todo | Add entry: type=meeting (scheduled) |
| **Meeting held** | Update card status to done | Add entry: type=meeting (held) |
| **Document created** | Add card: type=document, status=done | Add entry: type=document |
| **Evidence captured** | Add card: type=evidence, status=done | Add entry: type=evidence |
| **Gate criteria met** | Update gate in JSON, add evidence card | Add entry: type=milestone |
| **Stage transition** | Archive previous stage cards | Add stage-transition block |
| **Blocker identified** | Add card: type=blocker, status=blocked | Add entry: type=blocker |
| **Decision made** | Add card: type=evidence, status=done | Add entry: type=decision |

### Update Process

1. **Identify activity type** from the list above
2. **Capture specifics** — date, channel, participants, content summary, outcome
3. **Update engagement JSON** — add to `activity_log[]`, update relevant stage, add to `timeline.milestones[]`
4. **Update kanban HTML** — add/update card in appropriate stage column
5. **Update timeline HTML** — add entry with full details
6. **Save all files** — JSON, kanban HTML, timeline HTML

### Session Summary Updates

At the END of every session, update the session log:

```markdown
# Session Log — {{COMPANY}} — {{DATE}}

## What We Covered
- [List of activities completed this session]

## Evidence Collected
| ID | Type | Description | Date | Supports |
|----|------|-------------|------|----------|
| ev-XXX | ... | ... | ... | ... |

## Gate Progress
| Gate | Verdict | Evidence |
|------|---------|----------|
| ... | ... | ... |

## Next Steps
1. [Specific next action with date]
2. ...

## Current State
- Stage: X
- Win Probability: X%
- Gates Met: X/X
```

---

## Context Orchestration Protocol (CRITICAL)

Long-running engagements span multiple sessions. Use this protocol to **manage context windows** by saving work to files and resuming cleanly.

### The Problem

- Context windows are limited
- Sales engagements can span weeks or months
- Without orchestration, context is lost between sessions
- Duplicate work occurs when previous context isn't loaded

### The Solution: Save → Clear → Resume Pattern

```
┌─────────────────────────────────────────────────────────────┐
│  SESSION START                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Load Context from Files                               │    │
│  │ • Read {company}.json                                 │    │
│  │ • Read latest session log                             │    │
│  │ • Review kanban board state                           │    │
│  └─────────────────────────────────────────────────────┘    │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Work in Session                                       │    │
│  │ • Perform activities                                  │    │
│  │ • Capture evidence                                    │    │
│  │ • Update state incrementally                          │    │
│  └─────────────────────────────────────────────────────┘    │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Save Context to Files (CRITICAL)                      │    │
│  │ • Update {company}.json with all changes              │    │
│  │ • Update kanban HTML with new cards                   │    │
│  │ • Update timeline HTML with new entries               │    │
│  │ • Write session log with summary                      │    │
│  └─────────────────────────────────────────────────────┘    │
│  SESSION END                                                 │
└─────────────────────────────────────────────────────────────┘
```

### Context Files Structure

```
{research_directory}/
├── .beam/
│   ├── config.json                     # Seller context (persists across all engagements)
│   ├── engagements/
│   │   ├── {company}.json              # MASTER STATE — all engagement data
│   │   ├── {company}-kanban.html       # Visual kanban board
│   │   └── {company}-timeline.html     # Visual timeline
│   └── sessions/
│       ├── {company}-{date}.md         # Session log (one per session)
│       └── ...
├── {company}-dossier.html              # Initial research dossier
├── {company}-proposal.html             # Proposal document (when created)
└── styles.css                          # Shared styles
```

### Session Start Protocol

When resuming an engagement, ALWAYS:

1. **Read the master JSON file** — `{company}.json` contains full state
2. **Read the latest session log** — understand where we left off
3. **Review current kanban state** — what's in progress, blocked, or completed
4. **Summarise context for user** — "Last session we... Next steps were..."

Example prompt to user:
```
📋 **Resuming Bega Group engagement**

**Last session (23 Feb 2026):**
- LinkedIn message sent to James Hicks
- Pilot proposal drafted ($35K, 5 weeks)
- Conversation prep materials created

**Current state:**
- Stage: 1 — Qualify (1/3 gates passed)
- Win probability: 10%
- Pending: Awaiting James Hicks response

**Next steps from last session:**
1. Wait for James response
2. Follow up Day 3 (26 Feb) if no reply
3. Send value-add content Day 7

**What would you like to do?**
```

### Session End Protocol (CRITICAL)

At the END of every session, ALWAYS:

1. **Update master JSON** — capture ALL changes to engagement state
2. **Update kanban HTML** — reflect current card states
3. **Update timeline HTML** — add all activities from this session
4. **Write session log** — summarise what was done, evidence collected, next steps
5. **Confirm save** — tell the user files have been updated

Example:
```
✅ **Session saved**

Updated files:
- `.beam/engagements/bega-group.json` — engagement state
- `.beam/engagements/bega-group-kanban.html` — 2 cards updated
- `.beam/engagements/bega-group-timeline.html` — 3 entries added
- `.beam/sessions/bega-group-2026-02-26.md` — session log

**Pick up next session by reading the session log.**
```

### Activity Checkpoints

Some activities are natural checkpoints where you should save context:

| Activity | Save? | Rationale |
|----------|-------|-----------|
| Research dossier complete | **Yes** | Major deliverable, captures all discovery work |
| Outreach sent | **Yes** | Activity logged, waiting for external response |
| Meeting completed | **Yes** | Evidence captured, next steps defined |
| Stage transition | **Yes** | Major milestone, previous stage archived |
| Document created | **Yes** | Asset saved to file system |
| Proposal delivered | **Yes** | Critical commercial milestone |
| User requests pause | **Yes** | Explicit checkpoint requested |

### Loading Previous Context

When loading context, prioritise files in this order:

1. **`{company}.json`** — master state (most authoritative)
2. **Latest session log** — recent activity summary
3. **Kanban board** — visual state verification
4. **Timeline** — chronological activity history

### Minimal Context for Resume

To resume an engagement with minimal context load, read:

```json
{
  "current_stage": 1,
  "win_probability": 10,
  "last_session": "2026-02-23",
  "gates_met": ["problem_domain_identified"],
  "gates_pending": ["access_to_authority", "willing_to_diagnose"],
  "last_activity": "LinkedIn outreach to James Hicks",
  "next_steps": ["Await response", "Follow up Day 3"]
}
```

This summary can be extracted from the master JSON and presented to the user without loading full context.

---

## Checklist

### Research Delivery Checklist

Before delivering initial research, verify:

- [ ] Discovery interview completed and ICP confirmed
- [ ] Research scope and scoring rubric agreed
- [ ] All prospects validated against ICP criteria
- [ ] Company snapshots complete (no missing fields)
- [ ] Decision-makers identified with names and titles
- [ ] Buying signals documented with dates and sources
- [ ] Fit and timing scores assigned with justification
- [ ] Prospects ranked into priority tiers
- [ ] Engagement strategies personalised per prospect
- [ ] Outreach templates drafted and customised
- [ ] Sources cited for key claims
- [ ] Australian English spelling used throughout
- [ ] 30-day action plan included
- [ ] HTML report: light/dark mode toggle works
- [ ] HTML report: sidebar navigation tracks on scroll
- [ ] HTML report: all placeholder values replaced
- [ ] HTML report: score badges and priority badges display correctly
- [ ] Output delivered in requested format (HTML default, Markdown if requested)

### Kanban Board Checklist

When updating the kanban board, verify:

- [ ] All card titles are **specific** (include date, channel, recipient, content summary)
- [ ] Card notes explain what was done, evidence captured, and outcome
- [ ] Card status is accurate (todo, doing, done, blocked)
- [ ] Gate references are linked for evidence-type cards
- [ ] Stage progress bar reflects current gate criteria state
- [ ] Activity log in JSON matches kanban cards
- [ ] No generic card titles like "Outreach sent" or "Meeting held"

### Timeline Checklist

When generating/updating timeline, verify:

- [ ] All entries have specific dates (DD MMM YYYY format)
- [ ] Entry types are correctly categorised (outreach, meeting, document, evidence, milestone, blocker)
- [ ] Entry titles are specific (not generic)
- [ ] Details section includes channel, recipients, content summary
- [ ] Outcomes are marked (success, pending, blocked)
- [ ] Stage transitions are highlighted as separate blocks
- [ ] Filters work correctly
- [ ] Entry count matches actual activities

### Session End Checklist (CRITICAL)

Before ending ANY session, verify:

- [ ] Master JSON file updated with all engagement changes
- [ ] Kanban HTML updated with new/modified cards
- [ ] Timeline HTML updated with all activities from this session
- [ ] Session log written with:
  - [ ] What was covered
  - [ ] Evidence collected (table format)
  - [ ] Gate progress
  - [ ] Next steps with dates
  - [ ] Current state summary
- [ ] User informed of saved files and how to resume

### Session Start Checklist

When resuming an engagement, verify:

- [ ] Master JSON file read and state understood
- [ ] Latest session log read for context
- [ ] User briefed on last session summary
- [ ] Current state presented (stage, win probability, gates, pending activities)
- [ ] Next steps from last session reviewed
- [ ] User asked what they want to do this session
