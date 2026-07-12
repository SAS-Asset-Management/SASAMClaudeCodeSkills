# Trend Spotter — Output Templates

Three artefacts: the ranked trend report, the reusable hook/format templates, and the handoff brief. Australian English, no hyphens in prose, no emojis, no hashtags.

## 1. Ranked trend report

```markdown
# Trend Scan — <topic or creator set> — <DD/MM/YYYY>

Scope: <platforms> · Timeframe: <window> · Creators: <n> · Posts examined: <n> (<n> discarded, no measurable signal)
Data tier this run: <reliable tier used / native MCP used> · See confidence tags per row.

## Top outliers

| # | Creator | Platform | Date | Metric basis | Conf. | Multiple over baseline | Hook (trigger) | Format | Topic / angle | Why it worked |
|---|---------|----------|------|--------------|-------|------------------------|----------------|--------|---------------|---------------|
| 1 | ... | LinkedIn | DD/MM | comments+reposts | Med | 3.25x | "<first line>" (specific number) | data-as-hero | data quality / data you collect is wasted | precise uncomfortable figure |
| 2 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Trends (clustered, ranked)

1. **<trend name>** — appears across <n> creators. Mean strength <x>x over baseline. SAS-AM fit: <high/med/low>.
   - Pattern: <trigger> + <format> on <topic>.
   - Evidence: outliers #1, #4, #7.
2. ...

## Honesty notes

- Platforms with only low confidence signal this run: <list>.
- Figures marked "not available" where the platform exposed no reliable count: <where>.
- Native APIs not connected: <list> (see dataSources.md to enable).
```

## 2. Reusable hook & format templates

One block per strong trend. The pattern is learned, not copied — the example hook is original SAS-AM phrasing, never a competitor's words.

```markdown
### Template — <trend name>

- Trigger: <specific number / uncomfortable truth / confrontation / ...>
- Skeleton: <the reusable shape, e.g. "<precise %> of <thing the audience does> never <expected payoff>. If you have ever wondered whether <quiet doubt> — <resolution>.">
- SAS-AM example hook: "<original hook adapted to SAS-AM voice>"
- Maps to linkedin-post-generator format: <Quick Insight / Myth vs Reality / This Not That / SLAY / BABLA / Pillar Promotion / Carousel>
- Requires from the user's interview: <the real story / number the downstream skill must supply — Trend Spotter supplies the angle, not the fact>
```

## 3. Handoff brief

Compact block the next skill consumes directly.

```
=== Trend Handoff ===
Trend: <one line description of the winning pattern>
Recommended format(s): <mapped to linkedin-post-generator formats>
Candidate hooks (SAS-AM voice):
  1. <hook>
  2. <hook>
  3. <hook>
Source outliers (evidence): <creator/platform/date + one line why it worked>
Suggested SAS-AM theme/sector: <from Q4 / audience fit>
Next skill: /linkedin-post-generator   (Q5=B)
          or /content-campaign          (Q5=C — trend becomes the campaign topic)
Reminder: the downstream interview still supplies the real story and numbers.
Trend Spotter supplies the angle and hook only — nothing fabricated.
```
