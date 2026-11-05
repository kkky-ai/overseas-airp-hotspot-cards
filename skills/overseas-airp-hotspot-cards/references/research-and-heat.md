# Trend Research And Heat Qualification

Use this reference for every trend-discovery run. The goal is not to find merely interesting news; it is to prove that the event has enough current public attention to justify bot supply.

## Market priority

Search in this order and spend more candidate slots on higher-priority markets:

| Market | Weight | Default share of candidate search |
| --- | ---: | ---: |
| United States | 1.00 | 35% |
| United Kingdom | 0.92 | 20% |
| Canada | 0.84 | 12% |
| Australia | 0.78 | 10% |
| Germany | 0.72 | 9% |
| New Zealand | 0.66 | 7% |
| Russia | 0.60 | 7% |

These are discovery priorities, not factual confidence weights. A lower-ranked country may qualify when its event clearly crosses into higher-priority markets.

## Discovery window

- Default: events that broke or materially accelerated in the last 7 days.
- Fast social trends: prefer the last 24-72 hours.
- Ongoing events up to 30 days old may qualify only with fresh acceleration evidence, such as a new chart peak, major announcement, meme resurgence, or second-wave coverage.
- Record event time, evidence capture time, and timezone. Do not present an old event as current because a retrospective article was newly published.

## Source roles

Use multiple evidence types rather than several copies of the same press release.

- **Fact confirmation:** AP, Reuters, BBC, CBC, ABC Australia, major national newspapers/broadcasters, official statements, chart providers, court or organization records.
- **Social velocity:** native public post metrics or platform trend surfaces on TikTok, Instagram, YouTube, X, Reddit, Twitch, or equivalent.
- **Search interest:** Google Trends or another transparent search-ranking surface, scoped to a target country when possible.
- **Cultural breadth:** independent coverage in multiple target markets, chart placement, remix/meme proliferation, creator participation, or repeated audience discussion.

Search snippets are discovery aids, not final evidence. Open the source. Record the URL, publisher/platform, publication time, observed metric, geography, and capture time.

## Hard heat gate

An event qualifies only when all conditions A-D pass.

### A. Fact integrity

- At least one direct/official source or reputable fact-reporting source confirms the event.
- Material claims are corroborated when controversy or reputational harm is involved.
- Unresolved allegations are labeled as allegations; a card must not imply guilt.

### B. Independent attention evidence

Have at least **two different evidence types** from the source roles above. Syndicated copies count as one source. Two posts from the same account count as one signal.

### C. Breakout pattern

At least one pattern must be visible and recorded:

1. **Cross-media breakout:** three or more independent major outlets cover it within 72 hours, including coverage in at least two priority markets; or
2. **Social breakout:** one relevant public post exceeds 100,000 views or 10,000 engagements within 72 hours, plus an independent second-platform or major-media signal; or
3. **Search breakout:** Google Trends reports `Breakout`, or index >= 50 and rising in a target market, plus reputable factual confirmation; or
4. **Chart/rank breakout:** top-10 placement on a relevant national/platform chart or trend list, plus independent audience or media evidence; or
5. **Exceptional scale:** a lower raw count is acceptable only when a platform- or market-relative ranking proves exceptional reach. Record the benchmark and comparison.

If metrics are hidden or inaccessible, do not estimate them. Qualify through another documented pattern or leave the event on the watchlist.

### D. Heat score

Score each component from the captured evidence, then multiply the subtotal by the market weight. Maximum is 100.

| Component | Points | What earns the points |
| --- | ---: | --- |
| Recency and acceleration | 0-15 | Current rise, not merely recent publication |
| Reach / quantitative scale | 0-25 | Verifiable views, engagement, chart rank, search interest |
| Cross-platform breadth | 0-20 | Independent attention across platforms/source types |
| Major-media coverage | 0-15 | Multiple original reports, not syndication |
| Target-market relevance | 0-10 | Clear relevance to priority-market audiences |
| AIRP convertibility | 0-15 | Relationship engine, user role, visual hook, sustainable stakes |

`weighted_heat_score = round(component_subtotal * market_weight)`

- **Qualified:** score >= 70 and A-C all pass.
- **Watchlist:** 55-69, or strong attention with one missing gate. Do not make a card yet.
- **Rejected:** <55, failed fact integrity, or failed independent evidence.

The United States weight is 1.00. For a genuinely cross-market event, use the highest market weight only when the event has direct evidence in that market; do not add market weights together.

## Anti-false-positive rules

- One niche article has a maximum score of 35 regardless of how dramatic it sounds.
- A publisher calling its own story viral is not a metric.
- Large follower count is not event engagement.
- Old cumulative views do not prove current acceleration.
- Several outlets repeating one press release are one evidence lineage.
- A celebrity's fame does not automatically make every update hot.
- Never fabricate TikTok, Instagram, X, YouTube, Reddit, or Google Trends counts.

## Selection balance

After qualification, prefer events with strong AIRP conversion rather than simply taking the highest score. Avoid a batch dominated by one celebrity, fandom, platform, or conflict type. A useful batch usually mixes romance/social identity, competition or career stakes, mystery/controversy, nostalgia/comeback, and high-concept visual moments.

## Evidence record

For each evidence item save:

- `event_id`
- `evidence_type`
- `platform_or_publisher`
- `url`
- `published_at`
- `captured_at`
- `country`
- `metric_name`
- `metric_value`
- `metric_window`
- `is_independent`
- `notes`

Use these canonical `evidence_type` values so the workbook validator can distinguish proof from attention: `fact confirmation`, `social velocity`, `search interest`, `major media coverage`, `chart/rank breakout`, `cultural breadth`. Include at least one `fact confirmation` item and at least one separate, independent attention item. For social breakout, record the native `views` or `engagements` count and the observed time window. For cross-media breakout, enter each original outlet as its own item with publisher and country; syndicated copies do not count as separate outlets.

In the event summary, state why it qualified in one concrete sentence, such as: "Three national outlets in the US and UK covered the event within 48 hours, while the original video passed 2.1M views in 36 hours." Do not write vague conclusions such as "very popular online."
