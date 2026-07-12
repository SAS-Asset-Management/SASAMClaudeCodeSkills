# Trend Spotter — Outlier Method

Trends are relative. A post is a trend signal not because it got a big number, but because it beat what THAT creator normally gets. This controls for audience size and surfaces what the algorithm and audience rewarded, creator by creator.

## Step 1 — Assemble the post set

For each creator, collect every post inside the timeframe (default 30 days). Per post record:

- `creator`, `platform`, `postDate`
- `hookText` (the first line as shown before the "see more" fold)
- `format` (story-led, contrarian comparison, myth-bust, list/carousel, confession, data-as-hero, transformation, question/poll)
- `topic`, `angle` (the specific stance)
- `metrics` — whatever is reliably visible: `comments`, `reactions`, `reposts`, `views`
- `metricBasis` (which of the above were actually available) and `confidence` (high/medium/low — see `dataSources.md`)

Discard posts where nothing measurable is visible; note how many were discarded.

## Step 2 — Performance score per post

Engagement is skewed and comments are the stronger intent and algorithmic signal, so weight them. A workable default when comments, reactions and reposts are visible:

```
performanceScore = comments * 3 + reposts * 2 + reactions * 1
```

If only reactions are visible for a platform, score on reactions alone and mark the whole platform's ranking as reaction based. If only YouTube style counts are available, score on `comments * 3 + likes * 1` against views where views are known. Never mix a fabricated field in — a missing field is zero weight, not an invented number.

## Step 3 — Creator baseline

Use the **median** performanceScore across the creator's in window posts, not the mean — a single viral post would drag a mean upward and hide the very outlier you are hunting.

```
baseline = median(performanceScore across that creator's in window posts)
```

Require a minimum sample before trusting the baseline. With fewer than ~5 in window posts the median is unstable — flag the creator as low sample and lean on the strict decile rule below rather than the multiple.

## Step 4 — Outlier flag

A post is an outlier when it clears BOTH, or the stricter one on small samples:

- **Multiple rule** — `performanceScore >= 2 * baseline` (2x the creator's own median).
- **Decile rule** — the post is in the top 10% of that creator's in window posts by performanceScore.

Report each outlier's `multipleOverBaseline = performanceScore / baseline` so strength is comparable across creators of very different sizes.

Tune the multiple with the user if needed: 1.5x for a broad sweep, 3x for only the sharpest spikes.

## Step 5 — Reverse engineer each outlier

Decompose every flagged post into a reusable pattern:

- **Hook trigger** — map the first line to the `linkedin-post-generator` trigger taxonomy: uncomfortable truth, specific number, permission to fail, confrontation, open loop, status threat, shared enemy.
- **Format** — from the list in Step 1.
- **Topic + angle** — subject and the specific stance taken.
- **Why it worked** — one line hypothesis linking the hook/format/timing to the overperformance (e.g. "specific number + status threat, posted midweek, named a frustration the audience never says out loud").

## Step 6 — Cluster and rank the trends

Group outliers by recurring (trigger, format, topic). Rank the resulting trends by:

1. **Cross creator recurrence** — a pattern seen across several creators is a real trend, not one creator's lucky day. This dominates the ranking.
2. **Outlier strength** — mean `multipleOverBaseline` of the posts in the cluster.
3. **SAS-AM fit** — relevance to the asset management audience and the Q4 theme bias.

Down weight anything resting only on low confidence metrics.

## Worked example (illustrative — numbers are placeholders, not real data)

Creator A, 8 posts in 30 days, median performanceScore = 40. One post scores 130.
- `multipleOverBaseline` = 130 / 40 = 3.25x → clears the 2x rule and is top decile → OUTLIER.
- Hook: "73% of condition data never makes it into a maintenance decision." → trigger = specific number.
- Format = data-as-hero. Topic = data quality. Angle = the data you collect is wasted.
- Why: a precise, uncomfortable figure that names a frustration the audience feels but rarely quantifies.

Creator B, independently, has an outlier with the same specific number + data quality shape. Two creators, same pattern → this clusters into a ranked trend: **"specific number hooks about wasted condition data are overperforming."** That becomes a hook template and a handoff to `linkedin-post-generator`.
