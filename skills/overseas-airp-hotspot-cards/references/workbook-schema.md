# Excel Workbook Contract

Use one workbook for every run. Append by default. The generated workbook preserves the user's Word-example layout in `卡片视图` while also providing normalized sheets for sorting and audit.

## Sheets

### `Bots`

One row per completed bot. Required columns:

`Run ID`, `Event ID`, `Research date`, `Country`, `Country weight`, `Heat score`, `Heat tier`, `Event date`, `事件名字`, `热点事件`, `Source URLs`, `Fiction boundary`, `卡片名`, `相关角色`, `相关剧情`, `制卡价值`, `Cover`, `Character name`, `Bot ID`, `Gender`, `Type`, `Short intro (public)`, `Detailed intro (public)`, `Opening`, `Detailed settings (private)`, `Tags`, `Cover image prompt`, `QA status`, `Created at`

### `热点候选`

One row per researched event, including rejected and watchlist items. Store score components, gate status, qualification reason, and rejection reason. A card row may be created only for `Qualified` events.

### `热度证据`

One row per evidence item using the fields listed in `research-and-heat.md`.

### `卡片视图`

Fields are rows and each bot occupies one column, matching the supplied Word example. This view is rebuilt from `Bots` on every script run.

### `运行记录`

One row per research run: run ID, dates, freshness window, requested/qualified/rejected counts, output path, and notes.

### `字段说明`

Static data dictionary and heat-gate reminders.

## JSON input

Save a UTF-8 JSON payload with this shape:

```json
{
  "run": {
    "run_id": "2026-11-05-us-01",
    "research_date": "2026-11-05",
    "freshness_window": "7 days",
    "requested_count": 5,
    "notes": ""
  },
  "events": [
    {
      "event_id": "evt-001",
      "country": "United States",
      "country_weight": 1.0,
      "event_date": "2026-11-04",
      "event_name": "Chinese research-facing name",
      "fact_summary": "Verified facts only",
      "source_urls": ["https://example.com/source"],
      "fiction_boundary": "What was factual and what was invented",
      "score": {
        "recency": 15,
        "reach": 20,
        "breadth": 16,
        "media": 12,
        "market": 10,
        "airp": 13,
        "subtotal": 86,
        "weighted": 86
      },
      "gates": {
        "fact_integrity": true,
        "independent_attention": true,
        "breakout_pattern": true
      },
      "breakout_pattern": "cross-media",
      "heat_tier": "Qualified",
      "qualification_reason": "Concrete evidence-based sentence",
      "rejection_reason": "",
      "evidence": [
        {
          "evidence_type": "social velocity",
          "platform_or_publisher": "YouTube",
          "url": "https://example.com/post",
          "published_at": "2026-11-04T10:00:00-05:00",
          "captured_at": "2026-11-05T09:00:00+08:00",
          "country": "United States",
          "metric_name": "views",
          "metric_value": "1200000",
          "metric_window": "23 hours",
          "is_independent": true,
          "notes": "Native public counter"
        }
      ],
      "card": {
        "card_name": "English title",
        "related_roles": "Bot and user roles",
        "related_plot": "Opening conflict, reversal, sustained threads, boundary",
        "card_value": "Click and retention rationale",
        "cover": "/absolute/path/to/generated-cover.png",
        "character_name": "Original name",
        "bot_id": "TBD",
        "gender": "Male",
        "type": "Character",
        "short_intro": "<=140 English characters",
        "detailed_intro": "English public copy",
        "opening": "English opening scene",
        "detailed_settings": "English private prompt",
        "tags": ["OC (Original Character)", "Romance"],
        "cover_image_prompt": "English production prompt",
        "qa_status": "Passed"
      }
    }
  ]
}
```

For watchlist or rejected events, omit `card`. `breakout_pattern` must be one of `cross-media`, `social`, `search`, `chart-rank`, or `exceptional-scale`. Use canonical `evidence_type` values from `research-and-heat.md`. The script independently checks the score, all gates, fact-confirmation evidence, evidence-type diversity, and whether the declared breakout pattern has supporting metrics; it refuses to add a bot if the event is not qualified.

## Command

```bash
python3 scripts/build_workbook.py --input /absolute/path/run.json --output /absolute/path/海外AIRP热点制卡总表.xlsx
```

Use the bundled workspace Python when available because it includes `openpyxl`. The script creates the workbook if absent and appends when present. It rejects duplicate `Event ID` + `Character name` pairs unless `--allow-duplicate` is provided.
