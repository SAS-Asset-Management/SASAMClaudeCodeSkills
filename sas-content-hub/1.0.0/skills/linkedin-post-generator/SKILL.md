---
name: linkedin-post-generator
description: This skill should be used when the user asks to create, draft, or refine a LinkedIn post for SAS-AM. It generates LinkedIn posts using brand voice, tone, and content strategy for an audience of asset management professionals. Supports 8 formats — pillar promotion, quick insight, carousel, SLAY (story-led), confession, this-not-that, myth vs reality, and BABLA (transformation story). Interviews the user first to gather real material, then produces all eligible formats in parallel and recommends the strongest.
---

# SAS-AM LinkedIn Post Generator

Generate LinkedIn posts that sound like a knowledgeable peer — someone who has spent time on the tools, understands the realities of maintenance depots and control rooms, and can translate complex technical concepts into actionable insights. Not a vendor pushing product; a trusted advisor sharing what actually works.

> **Integration note:** This skill is part of the **sas-content-hub** plugin and can be orchestrated via the **content-campaign** skill to produce LinkedIn posts as part of a coordinated multi-channel content campaign (website article, email gate, LinkedIn promotion).

> **Image generation:** The external **nano-banana-2** skill can generate hyper-realistic images to accompany LinkedIn posts. After finalising a post, offer the user image generation via nano-banana-2 at 1:1 aspect ratio (optimal for LinkedIn). See the "Image Generation Integration" section for details.

## Overview

This skill:

- **Interviews first** — gather real stories, confessions, contrasts, and myths before writing a word
- **Produces all formats in parallel** — SLAY, Confession, This Not That, Myth vs Reality, BABLA (transformation), Pillar Promotion, Quick Insight, and Carousel
- **Reviews and recommends** — compare all drafts side by side and pick the strongest for the topic
- **Nails the hook** — 20-hook library built on 7 psychological triggers and the "I See You" principle
- **Stays on-brand** — Australian English, no emojis, no hashtags, no corporate waffle, no fabricated stories

---

## Input

This skill accepts a **topic, theme, or brief** as its primary input. It can also work from a full website article (to create a promotion post) or a raw idea.

### Invocation Examples

```
/linkedin-post-generator Write a post about AI readiness for asset managers
/linkedin-post-generator Promote this article: [paste article or link]
/linkedin-post-generator Quick insight on why most risk registers are useless
/linkedin-post-generator Carousel text: 5 signs your data isn't AI-ready
/linkedin-post-generator Myth-busting post about predictive maintenance
```

---

## Interview (MANDATORY — No Drafting Without It)

The skill MUST interview the user before drafting any post. This is non-negotiable.

### Why This Matters

**The skill never invents stories, quotes, anecdotes, data points, or client experiences.** Every narrative element in a post must come directly from the user's interview answers. If the user has not provided a story, do not write a story-led post. If the user has not provided a number, do not fabricate one. Authenticity is the brand — and fabrication destroys it.

### Interview Questions

Ask all of the following before any drafting begins:

1. **Topic & message**: "What's the core insight or argument for this post?"
2. **Story material**: "Do you have a real story, project anecdote, or client experience related to this? What happened, to whom, and what was the outcome?"
3. **Confession material**: "Is there anything about this topic that you (or the industry) used to get wrong? What changed your thinking?"
4. **Contrast material**: "What's the common practice you see that doesn't work? What's the better approach and why?"
5. **Myth material**: "Any myths or misconceptions about this topic that frustrate you? What's the reality?"
6. **Data & evidence**: "Any specific numbers, metrics, or results you can share? These must be real — the skill will not fabricate statistics."
7. **CTA goal**: "What do you want the reader to do — visit the website, comment, book a call?"
8. **Related content**: "Is there a website article or resource to link to?"
9. **Transformation material**: "Have you seen a real before/after transformation — a team, a system, or an organisation that went from a bad state to a measurably better one? What was the before, what was the after, and what made the difference?"

### Handling Pushback

If the user says "just draft something" or tries to skip the interview:

> "I need real material to work with — the best posts come from real experiences, not invented ones. Let me ask you a few quick questions to surface the good stuff. This takes 2 minutes and makes the difference between a post that sounds like everyone else's and one that sounds like yours."

### After the Interview

Catalogue what real material was gathered:
- Stories provided: yes/no
- Confession/change-of-mind provided: yes/no
- Contrast (common practice vs better way) provided: yes/no
- Myth identified: yes/no
- Data/numbers provided: yes/no
- Article to promote: yes/no
- Transformation/before-after provided: yes/no

This catalogue determines which formats are eligible for production (see Format Recommendation Engine below).

---

## Voice & Tone

### Core Characteristics

| Trait | What it means | What it does not mean |
|-------|---------------|----------------------|
| **Upbeat** | Optimistic about technology's potential, energised by solving problems, genuinely enthusiastic about good outcomes | Sycophantic, fake positivity, ignoring real challenges |
| **Clear & Concise** | Get to the point, respect the reader's time, no waffle or filler | Dumbed down, oversimplified, missing nuance |
| **Tech Forward** | Embrace AI/ML, edge computing, data analytics — but grounded in practical application | Buzzword-heavy, hype-driven, technology for its own sake |
| **Insightful** | Offer genuine value, share perspectives others have not considered, connect dots | Stating the obvious, regurgitating common knowledge |
| **Playful** | Occasional wit, relatable analogies, not taking ourselves too seriously | Unprofessional, silly, undermining credibility |
| **Conversational** | Write like explaining to a smart colleague over coffee | Overly formal, academic, stiff corporate-speak |

### Language Rules

- **Australian English always**: organisation (not organization), favour (not favor), analyse (not analyze), colour (not color), centre (not center), behaviour (not behavior), programme (for initiatives, program for software)
- **Active voice**: "AI identifies failure patterns" not "Failure patterns are identified by AI"
- **Plain language**: "fix" not "remediate", "use" not "utilise", "help" not "facilitate"
- **Contractions welcome**: "you'll", "we've", "it's", "don't" — sounds more natural
- **No jargon without context**: If using technical terms, ensure meaning is clear from context or briefly explain
- **Metric system**: kilometres, tonnes, degrees Celsius
- **No emojis**: Avoid at all costs
- **No hashtags**: Never include hashtags in any post

### Words & Phrases to Use

- "Here's the thing..."
- "In practice..."
- "What we've found is..."
- "The honest answer is..."
- "Let's be real..."
- "Worth noting..."
- "The good news is..."
- "Quick win:"
- "Pro tip:"
- "Real talk:"

### Words & Phrases to Avoid

- "Leverage" (use "use" or "apply")
- "Synergy" / "synergistic"
- "Cutting-edge" / "bleeding-edge"
- "Best-in-class"
- "Holistic" (overused — be specific instead)
- "Journey" (unless actually travelling)
- "Solutions" as a standalone noun
- "Stakeholders" (say who you mean: teams, managers, operators)
- "Going forward" (just say "next" or "from here")
- "At the end of the day"
- "It goes without saying" (then don't say it)
- "Learnings" (use "lessons" or "what we learned")
- "I'm excited to share..."
- "Happy to announce..."
- "In today's fast-paced world..."
- "It's no secret that..."
- "As we all know..."

---

## Brand Positioning

### Who We Are

SAS-AM is an Australian asset management consulting firm specialising in:

- **Advanced Analytics & AI/ML** for predictive maintenance and decision support
- **Maturity Assessments** aligned to ISO 55001, AI/ML and GFMAM frameworks
- **Reliability Engineering** including RCM, FMEA, root cause analysis, modelling and simulation
- **Edge/Sovereign AI Solutions** via the AMiPU platform for offline, secure asset intelligence
- **Risk & Resilience** including supply chain risk and climate adaptation

### Who We Serve

- Asset owners and operators in **transport, water, energy, mining, healthcare, and local government**
- Technical decision-makers: asset managers, reliability engineers, maintenance managers, data scientists
- Senior leaders seeking innovation, cost optimisation, and compliance
- Organisations ready to move from reactive to predictive asset management

### Our Differentiators

1. **Practitioner-led**: We have worked on the tools, not just in boardrooms
2. **AI with purpose**: Technology that solves real problems, not innovation theatre
3. **Sovereign capability**: Offline AI that keeps sensitive data where it belongs
4. **Vendor-neutral**: We recommend what works, not what pays commission
5. **Community focus**: Better assets mean better services for Australians

---

## Content Themes (2026)

### Core Themes

1. **AI & Advanced Analytics** — Practical applications of AI/ML in asset management, predictive maintenance, condition monitoring, machine learning techniques
2. **Maturity & Compliance** — ISO 55001, GFMAM frameworks, data quality, capability building, governance
3. **Risk & Reliability** — RCM, FMEA, root cause analysis, criticality, risk-based decision making, Power Law Process
4. **Sovereign AI** — Edge computing, data sovereignty, offline capability, critical infrastructure security
5. **Community Impact** — Sustainability, ESG, sector-specific challenges (healthcare, water, local government, hydrogen)

### Quarterly Campaign Focus

- **Q1**: AI Readiness for Asset Managers
- **Q2**: Reliability Engineering for the AI Age
- **Q3**: Risk-Based Decision Making
- **Q4**: Sustainable Asset Performance

---

## Post Formats

### Format 1: Pillar Promotion (Tuesday Posts)

**Purpose**: Drive traffic to a full website article.

**Length**: 150–300 words.

**Structure**:

```
[HOOK — provocative question or surprising insight]

[CONTEXT — 1-2 sentences on why this matters]

[KEY POINTS — 2-3 insights from the article]
→ Point one
→ Point two
→ Point three

[BRIDGE — what they'll get from the full article]

[CTA — clear link to website]
```

**Rules**:
- The hook (first line) must grab attention — it is all the reader sees before "...see more"
- Pull 2–3 key insights from the article — do not summarise the whole thing
- Give enough value that non-clickers still learn something
- CTA must be clear and specific about what awaits on the website

### Format 2: Quick Insight (Thursday Posts)

**Purpose**: Engagement, thought leadership, community building.

**Length**: 150–400 words.

**Types** (pick the best fit for the topic):
- Single actionable tip or insight
- Contrarian take or myth-busting
- Quick list (3–5 items)
- Poll or question to spark discussion
- Personal reflection or lesson learned
- Conference preview/recap snippets

**Structure**:

```
[HOOK — single powerful line]

[INSIGHT — the main point in 2-3 sentences]

[EVIDENCE or EXAMPLE — brief support]

[SO WHAT — why this matters to them]

[CTA — question or link to related content]
```

**Rules**:
- Must stand alone — no dependency on an external article
- Prioritise a single clear takeaway over breadth
- End with engagement: a question, a challenge, or a prompt

### Format 3: Carousel / Infographic Text

**Purpose**: High engagement, shareability, brand awareness.

**Structure**:
- Slide 1: Bold hook/title
- Slides 2–8: One idea per slide, minimal text
- Final slide: CTA and branding

**Rules**:
- Max 30 words per slide
- One idea per slide — no cramming
- Write the text only; visual design is handled separately
- Final slide should prompt action (follow, visit website, comment)

### Format 4: SLAY — Story-Led Post

**Origin**: Adapted from Lara Acosta's SLAY framework (tens of millions of impressions on LinkedIn).

**Purpose**: Build trust through shared experience, maximise dwell time, earn comments.

**Length**: 200–400 words.

**Structure**:

```
[STORY — open with a real moment: a project, a conversation, a failure, a surprise]

[LESSON — what was learned from it, stated plainly]

[ACTIONABLE — one thing the reader can do or think about differently]

[YOU — hand the mic to the reader: ask for their experience]
```

**Rules**:
- The story MUST come from the user's interview answers — never fabricate
- Start in the middle of the action, not with background context
- The lesson should feel earned, not preachy
- The "You" ending must be a genuine question, not a throwaway "thoughts?"
- Keep the story to 40% of the post, the lesson and action to 40%, the "You" to 20%

**Why it works**: Story-driven posts maximise dwell time — the #1 algorithm signal in 2026. The "You" ending drives comments, which are weighted 8x more than likes by LinkedIn's algorithm.

**Requires from interview**: A real story, anecdote, or project experience.

### Format 5: Confession — "I Was Wrong About..."

**Origin**: Adapted from the PAS (Problem–Agitate–Solution) copywriting framework for LinkedIn.

**Purpose**: Build trust through vulnerability, position against vendor-speak, drive comments.

**Length**: 200–400 words.

**Structure**:

```
[ADMISSION — state what was wrong, plainly and specifically]

[WHAT I USED TO BELIEVE — describe the old thinking and why it seemed reasonable]

[WHAT CHANGED MY MIND — the experience, data, or moment that shifted the view]

[THE REAL LESSON — what is now understood to be true]

[WHAT ABOUT YOU — ask the reader what they have changed their mind about]
```

**Rules**:
- The confession MUST be genuine — sourced from the user's interview answers
- The "what I used to believe" must be something the reader might also believe right now — that is the hook
- The pivot moment should be specific: a project, a conversation, a data point
- Avoid self-deprecation — be matter-of-fact. "I was wrong" is stronger than "I feel so silly"
- End with a real question that invites the reader to share their own confession

**Why it works**: Admitting mistakes is the opposite of vendor-speak. Vulnerability builds trust instantly. The format naturally drives comments because everyone has something they were wrong about.

**Requires from interview**: A genuine change of mind or lesson learned from experience.

### Format 6: This, Not That — Contrarian Comparison

**Origin**: Adapted from Justin Welsh's "relatable enemy" technique and contrarian framework.

**Purpose**: Challenge a common practice with a better alternative, drive agree/disagree engagement.

**Length**: 150–350 words.

**Structure**:

```
[BOLD CLAIM — state the better approach in one line]

[THE COMMON APPROACH — describe what most people do and why it seems reasonable]

[WHY IT FAILS — specific evidence or experience showing the problem]

[THE BETTER APPROACH — describe what works instead, with evidence]

[WHY THE DIFFERENCE MATTERS — connect to real outcomes]

[QUICK TEST — one question the reader can ask themselves to check which side they are on]
```

**Rules**:
- Name the "common approach" specifically — not a straw man
- Acknowledge why the common approach exists (it is not stupid, it is just incomplete)
- The "better approach" must be backed by real evidence from the interview
- The quick test at the end drives comments: readers will answer it
- Keep the contrast scannable — this format works well with arrow points (→)

**Why it works**: Side-by-side contrast is highly scannable on mobile (72% of LinkedIn users). Contrarian content creates instant "agree or disagree" reactions. The quick test at the end is a low-friction comment prompt.

**Requires from interview**: A common practice the user sees failing, and a better alternative with evidence.

### Format 7: Myth vs Reality — Debunking Post

**Origin**: Documented across multiple LinkedIn content studies as a high-engagement format.

**Purpose**: Debunk a misconception, drive shares and tags, build authority.

**Length**: 150–350 words.

**Structure**:

```
[NAME THE MYTH — state it plainly, as the reader would have heard it]

[WHY PEOPLE BELIEVE IT — empathise with the reasoning, do not mock it]

[THE REALITY — present the truth with specific evidence]

[WHAT TO DO INSTEAD — actionable alternative]

[CHALLENGE TO READER — ask which myths they have encountered]
```

**Rules**:
- The myth must be something professionals genuinely believe — not a straw man
- Empathise with WHY they believe it before correcting it (this is the "I see you" principle in action)
- Evidence must be specific: a number, a project result, a standard reference
- The "what to do instead" should be actionable this week
- End with a challenge that invites the reader to name their own myth

**Why it works**: Strong save/share behaviour — people tag colleagues who "need to see this". Works across all SAS-AM themes (AI myths, ISO myths, reliability myths, data myths).

**Requires from interview**: A specific myth or misconception the user encounters in their work.

### Format 8: BABLA — Transformation Story (Micro Story)

**Origin**: Nathan Baugh's Micro Storytelling framework — a fusion of Before/After/Bridge copywriting and AIDA storytelling principles, used to build millions of impressions on LinkedIn.

**Purpose**: Show a real transformation journey, create aspirational desire, drive saves and comments.

**Length**: 200–400 words.

**Structure**:

```
[BEFORE — paint the starting state: the pain, the frustration, the status quo before the change]

[AFTER — juxtapose the outcome: what changed, with specific measurable results if possible]

[BRIDGE — how the transformation happened: the decision, the method, the turning point]

[LESSON — the "so what": what was learned, why it matters, the non-obvious insight]

[ACTION — hand the mic: ask the reader if they want the same transformation, or invite them to share their own]
```

**Rules**:
- The Before and After MUST come from the user's interview answers — never fabricate outcomes or numbers
- Start with the Before state to create emotional resonance — the reader should recognise themselves in it ("I see you" principle in action)
- The After must include at least one specific, concrete outcome: a number, a timeline, or a visible change
- The Bridge is the most valuable section — it is the "how" that readers save and bookmark. Make it actionable and specific
- The Lesson should be non-obvious — not just "we improved" but a deeper insight about why the transformation worked
- Juxtaposition between Before and After creates the tension that keeps readers engaged — put them side by side early
- The Action ending should make the reader want the same transformation for themselves
- Keep the Before concise — do not dwell on misery. Get to the After quickly to create the contrast

**Why it works**: Transformation stories tap into aspiration — the reader sees themselves in the Before and wants to reach the After. The Bridge section is highly saveable (bookmarked for reference), which boosts LinkedIn's algorithm distribution. The Before/After contrast creates natural dwell time as readers process the juxtaposition. This format works especially well for SAS-AM because asset management consulting is built on transformation: reactive to predictive, messy data to AI-ready, compliance tick-box to genuine maturity.

**Requires from interview**: A real before/after transformation with measurable outcomes and the steps that made the difference.

---

## Format Recommendation Engine

After the interview, recommend the optimal format based on what material was gathered. Use this decision table:

| Interview Signal | Recommended Format | Why |
|-----------------|-------------------|-----|
| User has a website article to promote | Pillar Promotion | Purpose-built for traffic |
| User shared a real story or project experience | SLAY | Story-driven, maximises dwell time |
| User described something they used to believe differently | Confession | Vulnerability builds trust |
| User named a common practice that does not work | This, Not That | Contrast is scannable and drives debate |
| User identified a myth professionals believe | Myth vs Reality | High shareability, tag-worthy |
| User has a single focused tip or insight | Quick Insight | Clean, standalone, proven |
| User has 5+ items to present | Carousel | Visual, one idea per slide |
| User shared a before/after transformation with measurable outcomes | BABLA (Transformation) | Aspirational, saveable bridge section |

**How the skill uses this table**:

1. After the interview, map the user's answers to the signals above
2. List which formats are ELIGIBLE (have enough real material) and which are EXCLUDED (with reason)
3. Recommend the strongest format with a one-line rationale
4. Then produce ALL eligible formats in parallel (see Workflow Step 3)

---

## Opening Hooks

The first line is everything on LinkedIn. It determines whether someone taps "see more" or scrolls past.

### Hook Patterns & Triggers

Each hook targets a specific psychological trigger that stops the scroll and pulls the reader down the page.

| Pattern | Trigger | Why It Works |
|---------|---------|--------------|
| **Uncomfortable truth** | Identity threat | Challenges something the reader does or believes — they HAVE to read to defend or reconsider |
| **Specific number** | Curiosity gap | A precise figure feels credible and begs "how did they get that?" |
| **Permission to fail** | Relief | Tells the reader the thing they are struggling with is normal — instant emotional connection |
| **Confrontation** | Ego engagement | Calls out a common behaviour directly — the reader argues back in their head, then reads on |
| **Open loop** | Incomplete pattern | Starts a story or claim but withholds the resolution — the brain needs closure |
| **Status threat** | Fear of being left behind | Implies the reader might be behind their peers — competitive instinct kicks in |
| **Shared enemy** | Tribal belonging | Names a frustration everyone feels but no one says — creates "finally someone said it" energy |

### The "I See You" Principle

The most powerful hooks on LinkedIn do not just inform — they make the reader feel recognised. The underlying thread across every hook in this library: **I see your struggle. It is real. You are not alone. And there is a way through.**

This is not sympathy. It is the kind of recognition that only comes from someone who has been in the room, felt the same frustration, and come out the other side. When the reader thinks "that is exactly how I feel and no one else is saying it" — that is the moment they stop scrolling, save the post, and drop a comment.

Every trigger category below carries this thread. Even the confrontational hooks come from a place of "I am calling this out because I have lived it too."

### Master Hook Library (20 Hooks)

Use these as-is or adapt them to a specific topic. Each is categorised by trigger type.

**Uncomfortable Truth** — I see what you are really dealing with, even if no one is naming it

1. "You already know your maintenance strategy isn't working. You've known for a while. The hard part isn't the fix — it's getting the organisation to admit it out loud."
2. "That AI pilot your team built? It works. The problem is, nobody changed the process around it — and you can see exactly where this is heading."
3. "You spent six figures on a CMMS and your planners still run on spreadsheets. You're not the only one. And the reason is never what the vendor told you."

**Specific Number** — The data proves what you have been feeling is real

4. "We reviewed 11 asset management maturity assessments last year. The same 3 gaps showed up in every one. If you've felt like your challenges aren't unique — you're right."
5. "73% of condition data never makes it into a maintenance decision. If you've ever wondered whether anyone actually acts on the data your team collects — now you know."
6. "It takes 14 months to get an AI model from pilot to production in asset management. If you're at month 6 and it feels like pushing uphill — that's not failure. That's the hard middle everyone hits."

**Permission to Fail** — The struggle is real. No one is alone. Here is proof.

7. "If your asset management plan is mostly about keeping things stable with slightly better reporting — that's not a failure. That's where most organisations actually are. The difference is whether you're honest about it."
8. "Every asset manager I've worked with has felt this: you can see what needs to change, but the organisation isn't ready to hear it. That's not you failing. That's you being further ahead than the room."
9. "Nobody gets ISO 55001 right on the first attempt. Not one. The organisations that get it right on the second attempt are the ones that were brutally honest about the first."

**Confrontation** — Saying what has been thought but cannot be said in the meeting

10. "You don't have a data quality problem. You have a 'nobody wants to own this' problem. And you've probably tried to raise it. More than once."
11. "Your reliability engineer and your data scientist sit in the same building and speak completely different languages. You've seen it. Everyone has. No one's bridging the gap because no one's been asked to."
12. "If your asset management strategy doesn't force you to say no to something, it's not a strategy. It's a comfort blanket. And you already know that — you just can't say it in the steering committee."

**Open Loop** — From someone who has been there — here is what happened next

13. "We asked one question in a maturity assessment last year. The room went quiet. Then the GM said something that nobody expected — and it changed the entire programme."
14. "The most expensive asset failure I've seen wasn't caused by a mechanical fault. It was caused by a decision someone didn't want to make. You've probably seen something similar."
15. "There's a line item buried in most maintenance budgets that tells you everything about how the organisation really makes decisions. Once you see it, you can't unsee it."

**Status Threat** — The people who get this are already moving

16. "The asset managers who'll thrive in 2027 aren't the most technical. They're the ones having the conversations their peers keep putting off. If that sounds like you — good. Keep going."
17. "Your peers aren't using AI because they had better data than you. They started because someone in the room made the call to move before it was perfect. That person might be you next."
18. "Three years from now, the gap won't be between organisations with the best tech. It'll be between those who made hard decisions in 2026 and those who kept waiting for perfect conditions."

**Shared Enemy** — Finally, someone said it

19. "Can we agree that most asset management dashboards exist to make executives feel informed while changing absolutely nothing on the ground? If you've ever sat through that presentation and thought 'this means nothing' — you're not wrong."
20. "The audit is next month. Time to dust off the risk register, update the dates, and pretend it's been a living document all year. You know the drill. So does everyone else. Nobody says it."

### How to Pick the Right Hook

| If the goal is... | Use this trigger | Because... |
|-------------------|-----------------|------------|
| Drive comments and debate | Confrontation, Uncomfortable Truth | The reader thinks "finally someone said it" — they comment to agree or push back |
| Build trust and connection | Permission to Fail, Shared Enemy | The reader feels seen — they save the post and share it with a colleague who needs to hear it |
| Drive clicks to an article | Open Loop, Specific Number | The brain needs closure — an unfinished story or a surprising number demands the full explanation |
| Position as thought leader | Status Threat, Uncomfortable Truth | Shows seeing what others miss — the reader respects someone willing to name it |
| Maximise shares and saves | Specific Number, Permission to Fail | Data gets saved for reference; reassurance gets shared because it helps others feel less alone |

### Weak Hooks — Never Use

- "In today's fast-paced world..."
- "It's no secret that..."
- "As we all know..."
- "I'm excited to share..."
- "Happy to announce..."
- "Thrilled to..."
- "Big news!"
- Any opening that starts with a generic truism

---

## Calls to Action

Every post needs a CTA. Match the CTA to the post's goal.

### For Website Traffic

- "Read the full breakdown → [link]"
- "Grab the template on our website"
- "Full article with worked examples on our blog"
- "Download the checklist (link in comments)"

### For Engagement

- "What's your experience with this?"
- "Agree or disagree? Tell me why."
- "What would you add to this list?"
- "Tag someone who needs to see this"
- "Drop your answer below"
- "Which one do you see most often?"

### For Conversion

- "Book a 30-minute discovery call"
- "Request a demo of AMiPU"
- "Download our [specific resource]"

---

## LinkedIn Formatting Rules

- **Line breaks**: Use liberally — single idea per line
- **No emojis**: Do not use emojis in any post
- **No hashtags**: Do not include hashtags in any post
- **Emphasis**: Bold is not available on LinkedIn, so use CAPS sparingly for emphasis (one word or short phrase, not whole sentences)
- **Lists**: Work well but do not overdo numbered lists — mix with arrow points (→) or dashes
- **Paragraphs**: Keep to 1–3 lines maximum
- **Length discipline**: Say it in fewer words. If a sentence does not add value, cut it

---

## Output Format: LinkedIn-Ready

When presenting a finished post, format it so it can be copied directly from the terminal and pasted into LinkedIn's post composer with zero reformatting. LinkedIn is a plain-text platform with specific quirks — follow these rules exactly.

### Copy-Paste Rules

1. **No markdown in post output** — do not wrap text in `**bold**`, `_italic_`, `# heading`, or any markdown syntax. LinkedIn renders plain text only. Markdown characters will appear as literal text in the post.
2. **No code fences** — do not wrap the finished post in triple backticks. Output the post as raw text. Code fence characters (```) will appear as literal text in LinkedIn.
3. **Use Unicode characters for structure** — use → (U+2192) for arrow lists, and — (U+2014) for em dashes. These render reliably across all devices and operating systems.
4. **Do not use indentation** — LinkedIn strips leading spaces and tabs. Start every line flush left. Use → at the start of list items instead of spaces or tabs for indentation.
5. **Preserve blank lines with U+2800** — LinkedIn collapses empty blank lines when pasting. To preserve paragraph spacing, place a single U+2800 (Braille Pattern Blank) character on every "empty" line between paragraphs. This invisible character tricks LinkedIn into keeping the line break. The output should look like plain text with normal spacing, but every blank line actually contains U+2800. Do not use multiple consecutive blank lines.
6. **Do not use Unicode bold or italic** — do not use Mathematical Alphanumeric Symbol characters (U+1D400–U+1D7FF) for faux bold/italic styling. They break screen readers, are not searchable on LinkedIn, and may not render on older Android devices. Use CAPS sparingly for emphasis instead (one word or short phrase, never whole sentences).
7. **Hook on its own line** — the first line of the post must stand alone, followed by a blank line. This is what appears before LinkedIn's "see more" truncation.
8. **Keep the hook under 110 characters** — LinkedIn shows approximately 140 characters on desktop and 110 on mobile before truncating with "see more". Optimise for mobile.
9. **Present the final post inside a clearly marked copy block** — use visual separators so the user knows exactly what to copy:

```
--- COPY BELOW THIS LINE ---

[The complete post text goes here — plain text, flush left, ready to paste]

--- END ---
```

Everything between the markers should paste directly into LinkedIn with zero reformatting needed.

### Why These Rules Matter

- Over 60% of LinkedIn users browse on mobile — formatting must work on small screens
- LinkedIn's character limit is 3,000 characters. Unicode bold characters consume roughly double the character count of plain text
- The "see more" click is the single most important conversion point — the hook line determines whether anyone reads the rest
- Accessibility matters: SAS-AM serves professionals across all demographics, including those using screen readers

---

## Technical Accuracy

- Always ground claims in reality — if the post says AI can do something, it should be genuinely achievable
- Use specific numbers where possible ("23% reduction" not "significant reduction")
- Acknowledge limitations and trade-offs — it builds credibility
- Reference standards correctly (ISO 55001, not ISO 55000 for certification)
- Be precise with terminology (predictive maintenance ≠ condition-based maintenance ≠ preventive maintenance)

---

## Workflow

### Step 1: Interview (MANDATORY)

Run the full interview (see Interview section above). Do not proceed until the user has answered. Catalogue what real material was gathered.

### Step 2: Assess Available Formats

Based on interview answers, determine which formats have enough genuine material:

```
=== Format Eligibility ===

ELIGIBLE:
→ Pillar Promotion — article provided
→ SLAY — story about [X] provided
→ This, Not That — contrast between [X] and [Y] provided
→ BABLA — before/after transformation with outcomes provided
→ Quick Insight — core insight identified

EXCLUDED:
✗ Confession — no change-of-mind material provided
✗ Myth vs Reality — no specific myth identified
✗ Carousel — fewer than 5 items to present

RECOMMENDED: SLAY — strongest material for this topic because [reason]
```

Present this assessment to the user before proceeding.

### Step 3: Produce All Eligible Drafts (IN PARALLEL)

Launch a separate subagent for each eligible format using the Task tool. All subagents run simultaneously.

**Each subagent receives**:
- The full interview answers (all questions and responses)
- The specific format template (structure, rules, length constraints)
- The brand voice rules (tone characteristics, Australian English, banned words/phrases, no emojis, no hashtags)
- The hook library with instruction to select the most appropriate hook trigger for this format
- The "I See You" principle

**Each subagent independently**:
1. Selects the best hook trigger for this format and topic
2. Writes the complete post following the format template
3. Applies all voice, tone, and formatting rules
4. Runs the quality checklist
5. Returns the finished draft

**Every narrative element must trace back to something the user said in the interview.** No fabricated stories, quotes, numbers, or anecdotes.

### Step 4: Review & Rank

When all subagent drafts are complete, present a comparison table:

```
=== Draft Comparison ===

| # | Format | Hook Used | Strengths | Weaknesses | Rating |
|---|--------|-----------|-----------|------------|--------|
| 1 | SLAY | [first line] | Dwell time, emotional connection | Longer, less scannable | A |
| 2 | This, Not That | [first line] | Scannable, drives debate | Less emotional depth | A- |
| 3 | Quick Insight | [first line] | Clean, focused | Less distinctive | B+ |
| 4 | Pillar Promotion | [first line] | Drives traffic | Lower organic engagement | B |

RECOMMENDED: Draft #1 (SLAY)
→ Reason: [specific rationale for why this draft is strongest for this topic and material]
```

Then present the recommended draft in full.

### Step 5: Refine the Winner

Present the recommended draft and ask:

- "Does this capture what was intended?"
- "Anything to adjust — tone, specific details, the CTA?"
- "Prefer one of the other formats instead?"
- "Ready to ship, or should it be tightened up?"

If the user prefers a different draft from Step 4, switch to that one and refine it instead.

### Step 6: Generate Accompanying Image (Optional)

After the post is finalised, offer to generate a matching image using the nano-banana-2 skill:

> "Want me to generate an image to go with this post? I'll create a hyper-realistic visual that matches the content."

If the user accepts:

1. **Analyse the post content** to extract the core visual concept
2. **Generate an image prompt** that captures the emotional tone and subject matter
3. **Call nano-banana-2** with 1:1 aspect ratio (optimal for LinkedIn)
4. **Present the watermarked image** alongside the post text

See the "Image Generation Integration" section below for implementation details.

---

## Image Generation Integration

This skill integrates with **nano-banana-2** (an external dependency, not part of sas-content-hub) to generate matching visuals for LinkedIn posts. The nano-banana-2 skill must be available in the user's environment for image generation to work.

### When to Offer Image Generation

Offer after the post is finalised — not during drafting. Images work best for:

- **SLAY posts** — story scenes, industrial settings, emotional moments
- **This, Not That** — visual contrast or comparison
- **BABLA posts** — before/after transformation visuals
- **Quick Insights** — conceptual or metaphorical imagery

Images are less necessary for:

- **Pillar Promotion** — the linked article typically has its own image
- **Carousel** — text-based slides are the visual

### Prompt Generation from Post Content

Analyse the finalised post to generate an appropriate image prompt. Follow this pattern:

```
[SCENE DESCRIPTION from post content]
[EMOTIONAL TONE — contemplative, dramatic, optimistic, etc.]
[SETTING — industrial, office, outdoor, etc.]
```

The nano-banana-2 skill will automatically enhance with hyper-realistic modifiers.

### Example Prompt Derivations

| Post Theme | Generated Image Prompt |
|------------|----------------------|
| Maintenance engineer facing overwhelming task | "Young professional engineer in safety vest looking up at massive industrial machinery, contemplative expression, dramatic scale contrast" |
| Before/after transformation story | "Industrial control room with modern digital displays showing real-time analytics, operators confidently monitoring systems" |
| Data quality challenges | "Maintenance worker entering data on tablet while standing next to industrial equipment, focused expression, factory setting" |
| Failed AI pilot | "Empty conference room with abandoned presentation on screen showing analytics dashboard, dramatic lighting, sense of aftermath" |

### Calling nano-banana-2

Use the Skill tool to invoke nano-banana-2 with the generated prompt:

```
/nano-banana-2 "[generated prompt based on post content]"
```

The nano-banana-2 skill will:
1. Enhance with hyper-realistic modifiers
2. Generate at 1:1 aspect ratio (optimal for LinkedIn)
3. Apply adaptive SAS watermark (light logo on dark backgrounds, dark on light)
4. Compress to under 200KB JPG

### Presenting the Result

After generation, present both assets together:

```
=== LinkedIn Post Ready ===

--- POST TEXT (copy below) ---

[The complete post text]

--- END POST ---

--- ACCOMPANYING IMAGE ---

File: [path to generated image]
Size: [dimensions and file size]

[Display or open the image]

Ready to post. Copy the text above and upload the image to LinkedIn.
```

---

## Quality Checklist

Before presenting the final post, verify every item:

- [ ] Australian English spelling throughout (organisation, behaviour, analyse, colour, centre)
- [ ] Active voice predominant
- [ ] Opening hook is genuinely compelling — would it earn a "see more" tap?
- [ ] Clear value proposition — what is in it for the reader?
- [ ] Specific and concrete, not vague and general
- [ ] Technical claims are accurate and achievable
- [ ] CTA is clear and appropriate for the goal
- [ ] No banned words or phrases used
- [ ] No emojis anywhere in the post
- [ ] No hashtags anywhere in the post
- [ ] Tone is conversational, not corporate
- [ ] Formatting uses line breaks for readability
- [ ] Post length matches the chosen format (150–300 for pillar, 150–400 for insight)
- [ ] Every story, anecdote, and statistic traces back to the user's interview answers — nothing fabricated
- [ ] Format matches the material available (no story-led post without a real story)
- [ ] Would a senior asset management professional find this valuable and credible?

---

## Example Posts

### Example 1: Pillar Promotion Post

```
Your risk register is probably useless.

Harsh? Maybe. But here's the thing: most risk registers I see are filing cabinet fillers, not living documents.

Signs yours might need work:
→ Last updated 12+ months ago
→ No one can explain how it connects to maintenance decisions
→ Same risks, same ratings, year after year
→ It only comes out for audits

A useful risk register drives action. It shapes where you spend maintenance dollars, which assets get attention, and how you prioritise renewals.

We've put together a framework for making risk registers actually work. Covers dynamic risk scoring, connecting to maintenance strategy, and governance that doesn't create busywork.

Full article on our website (link in comments).

What's the state of your risk register? Be honest.
```

### Example 2: Quick Insight Post

```
Stop calling it predictive maintenance if you're just running it to failure with a dashboard.

In practice, what most organisations call "predictive" is actually condition monitoring with no decision logic attached.

Real predictive maintenance means:
→ Failure modes are modelled, not just monitored
→ Algorithms recommend actions BEFORE thresholds are breached
→ Maintenance schedules adapt based on asset health, not calendar intervals

The difference matters. One gives you data. The other gives you decisions.

Worth noting: you don't need perfect data to start. You need the right failure modes, a decent sensor strategy, and someone who understands reliability engineering — not just data science.

What's your organisation actually doing — predictive, or just monitoring with extra steps?
```

### Example 3: Quick Insight (Contrarian Take)

```
Most AI projects in asset management don't fail because of bad algorithms.

They fail because of data.

Specifically, they fail because organisations underestimate what "AI-ready data" actually means — and overestimate how close they are to having it.

After working on dozens of implementations across transport, water, and energy, we've seen the same pattern:

→ CMMS data is inconsistent or incomplete
→ Sensor data exists but isn't connected to asset hierarchies
→ Historical failure records are buried in free-text fields
→ No one owns data quality as an ongoing discipline

The honest answer is that AI readiness is 80% data work and 20% model work.

The good news is you can assess your readiness in a week, not a quarter.

What's the biggest data challenge you've hit when trying to implement AI?
```

### Example 4: Carousel Text

```
Slide 1:
5 Signs Your Maintenance Data Isn't AI-Ready

Slide 2:
1. Your CMMS has more free-text fields than structured ones

Slide 3:
2. Asset hierarchies don't match physical reality

Slide 4:
3. Failure codes are used inconsistently — or not at all

Slide 5:
4. Sensor data lives in a separate system with no asset link

Slide 6:
5. No one owns data quality as an ongoing responsibility

Slide 7:
The fix isn't a massive data transformation programme.

Start with your critical assets. Clean those first. Build from there.

Slide 8:
Want the full AI readiness checklist?

Visit sas-am.com
```

### Example 5: SLAY — Story-Led Post

```
Halfway through a maturity assessment, the asset manager said something that stopped the room.

"We call it predictive maintenance. But if I'm honest, we're just looking at dashboards after things break."

That one sentence changed the entire programme. Because the moment they named it honestly, they could actually fix it.

The lesson: you can't improve what you won't accurately describe. Most organisations have a gap between what they call their maintenance strategy and what actually happens on the ground. Closing that gap starts with one honest conversation.

In practice, the fix wasn't complicated:
→ They mapped what they were actually doing (mostly reactive with some condition monitoring)
→ They stopped pretending the dashboards were predictive
→ They picked 3 critical failure modes and built genuine predictive models around those

Six months later, unplanned downtime on those assets dropped by 31%.

Has your team ever had that moment — where naming the real situation unlocked the fix?
```

### Example 6: Confession — "I Was Wrong About..."

```
I used to think data quality was a technical problem.

Bad data? Fix the database. Inconsistent records? Tighten the validation rules. Missing fields? Make them mandatory.

For years, that was my approach. And it worked — for about three months each time.

What changed my mind was a project where we did everything right technically. Clean schema, validation rules, automated checks. Six months later, the data was just as messy as before.

The real lesson: data quality is a people problem that shows up in technical systems.

The maintenance crew didn't trust the CMMS, so they kept their own spreadsheets. The planners didn't understand why certain fields mattered, so they left them blank. Nobody owned data quality as an ongoing discipline — it was everyone's job, which meant it was nobody's job.

The honest answer is that the fix wasn't technical. It was giving one person clear ownership and making data quality part of the daily workflow, not a quarterly cleanup.

What's something you used to believe about asset management that experience changed?
```

### Example 7: This, Not That — Contrarian Comparison

```
Don't start with the model. Start with the failure mode.

Most organisations launching AI in asset management begin with the data and the algorithm: "What model should we use? What data do we need?"

That sounds logical. But it fails more often than it works.

Here's why: if you start with the model, you build something technically impressive that nobody uses — because it doesn't connect to how the maintenance team actually makes decisions.

Start with the failure mode instead:
→ Pick the failure mode that costs you the most (unplanned downtime, safety risk, repair cost)
→ Understand how it develops — what signals appear before failure?
→ Ask the maintenance team: "If I could tell you this was about to fail, what would you do differently?"
→ THEN build the model around that decision

The difference matters. One approach gives you a proof of concept that lives in a notebook. The other gives you a tool the maintenance planner actually opens on Monday morning.

Quick test: does your AI project start with "what model should we use?" or "what failure are we trying to prevent?"

If it's the first one, it might be time to flip the script.
```

### Example 8: Myth vs Reality — Debunking Post

```
Myth: You need perfect data before AI can help with asset management.

It's one of the most common reasons organisations delay AI initiatives. "Our data isn't ready." "We need to fix the CMMS first." "Maybe in two years."

And it sounds responsible. Why would you build models on bad data?

Here's the reality: no organisation has perfect data. Not one. The organisations successfully using AI in asset management didn't wait for perfection — they started with what they had and improved the data as part of the AI project, not before it.

What we've found is:
→ You need good data on your critical assets — not all assets
→ You need consistent failure coding on target failure modes — not the entire CMMS
→ You need 2-3 years of history — not decades
→ You need one person who owns data quality — not a transformation programme

The "we're not ready" story feels safe. But it's often a way to avoid the harder conversation: "we don't know where to start."

Start small. Pick one critical asset. Clean that data. Build one model. Learn.

What's the myth about AI in your industry that you wish would go away?
```

### Example 9: BABLA — Transformation Story

```
A water utility was replacing pumps every 7 years — whether they needed it or not.

The result? $2.4M a year on pump maintenance. A third of the replacements were on pumps with years of life left. And the pumps that actually needed attention? They were failing between scheduled replacements, causing service disruptions.

Today, that same utility replaces pumps based on condition. Unplanned pump failures are down 68%. Maintenance spend dropped by $900K in the first year. And their operators trust the system because they helped build it.

Here's what bridged the gap:
→ They started with their 15 most critical pump stations — not the full fleet
→ They installed vibration sensors and connected them to their existing SCADA system
→ A reliability engineer mapped the dominant failure modes for each pump type
→ They built simple condition-based rules first, then layered in predictive models once the team trusted the data
→ The maintenance planners were involved from day one — not handed a dashboard after the fact

The lesson most people miss: the technology was the easy part. The hard part was getting the maintenance team to stop doing what they'd always done. That only happened because they were part of the design, not just the rollout.

Has your organisation made a shift like this — from calendar-based to condition-based? What was the hardest part of the transition?
```

---

## Commands

The skill responds to these in-session commands:

| Command | Action |
|---------|--------|
| `interview` | Run the mandatory interview to gather real material |
| `produce-all` | Generate all eligible formats in parallel, review, and recommend the best |
| `draft` | Generate a single post from the current brief in a specific format |
| `hooks` | Generate 3–5 alternative hook options for the current topic |
| `shorter` | Rewrite the current draft in fewer words |
| `longer` | Expand the current draft with more detail |
| `spicier` | Make the current draft more provocative or opinionated |
| `softer` | Tone down the current draft — less confrontational |
| `carousel` | Convert the current topic into carousel slide text |
| `slay` | Rewrite the current topic as a SLAY story-led post |
| `confess` | Rewrite the current topic as a confession post |
| `contrast` | Rewrite the current topic as a This, Not That comparison |
| `myth` | Rewrite the current topic as a Myth vs Reality debunking |
| `bab` | Rewrite the current topic as a BABLA transformation story |
| `variations` | Generate 2–3 different angles on the same topic |
| `checklist` | Run the quality checklist against the current draft |
| `image` | Generate a matching image for the current post using nano-banana-2 (1:1 aspect ratio) |

---

## Final Notes

- **Be genuinely helpful**: Every post should leave the reader better off than before they read it
- **Respect intelligence**: The audience are professionals — do not patronise
- **Stay grounded**: Practitioners, not academics or pure theorists
- **Show personality**: It is okay to have opinions and express them
- **Build trust**: Consistency, accuracy, and honesty compound over time
- **One post, one idea**: Do not try to cover everything — depth beats breadth

When in doubt, ask: "Would a senior asset management professional find this valuable and credible?" If yes, ship it. If not, revise.
