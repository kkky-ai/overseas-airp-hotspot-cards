---
name: overseas-airp-hotspot-cards
description: Research genuinely high-attention events in prioritized overseas markets, turn qualified events into original English-language AIRP bot cards, and maintain all research evidence and card assets in one Excel workbook. Use for recurring overseas trend-to-bot supply, card ideation from current events, or updating the AIRP bot master sheet; do not use for generic news summaries without card production.
---

# Overseas AIRP Hotspot Cards

Produce original AIRP bot supply for overseas users from current, demonstrably hot events. Treat news and social posts as factual inputs, never as permission to fictionalize claims about real people.

## Required workflow

1. Confirm the research date, target count, freshness window, and output workbook. Default to 5 qualified cards from the last 7 days, appending to `海外AIRP热点制卡总表.xlsx` in the user's requested location or current workspace.
2. Research broadly across news, entertainment, TikTok, Instagram, YouTube, X, Reddit, Google Trends, charts, and other publicly observable signals. Prioritize countries in this order: United States, United Kingdom, Canada, Australia, Germany, New Zealand, Russia. Use available search/browsing connectors and public pages; do not use private accounts, bypass access controls, or claim to have scraped a platform when only its page was inspected.
3. Apply the qualification rules in [research-and-heat.md](references/research-and-heat.md). Do not create a card unless the event passes the heat gate. Save rejected and watchlist candidates with reasons; never inflate or invent metrics. If fewer than the requested number qualify, output fewer cards rather than padding with niche stories.
4. Separate verified facts from fictional adaptation. Use real events only as inspiration for an original adult character, setting, and relationship dynamic. Avoid copying a living person's identity, private life, scandal, or likeness into the bot.
5. Read [card-design.md](references/card-design.md) before writing card assets. Draft from two simultaneous viewpoints: an experienced Western AIRP player deciding whether to click and continue, and an experienced card creator engineering sustainable tension.
6. Create every requested field: 事件名字, 热点事件, 卡片名, 相关角色, 相关剧情, 制卡价值, Cover, Character name, Bot ID, Gender, Type, Short intro (public), Detailed intro (public), Opening, Detailed settings (private), Tags, Cover image prompt. Public-facing card fields must be natural English; research notes and rationale may be Chinese.
7. Generate a cover with `$imagegen` when available and requested. Use the source image only for broad visual guidance unless the user explicitly owns and requests identity preservation. If image generation is unavailable, keep `Cover` empty or mark it `Prompt ready`; always provide the complete prompt and never claim an image was generated.
8. Validate the card: immediate user role, user leverage, unresolved choice, no user puppeteering, at least three sustainable story threads, adult characters, and clear fact/fiction boundaries.
9. Serialize the run to the JSON contract in [workbook-schema.md](references/workbook-schema.md), then run `scripts/build_workbook.py`. Append rather than overwrite unless explicitly asked. The workbook is the source of truth; do not leave completed card assets only in chat.

## Non-negotiable quality gates

- A single article, a niche publication, or an unsupported claim that something is "viral" cannot qualify an event.
- Passing heat score alone is insufficient: the event must also have at least two independent evidence types and satisfy one breakout pattern in the research reference.
- `Bot ID` is `TBD` until the product returns an ID. Never invent one.
- The opening must put the user inside a consequential scene in the first paragraph and end with room for a meaningful response.
- Do not dictate the user's gender, appearance, thoughts, feelings, dialogue, or decision unless the user requested a fixed persona.
- Keep real names out of the fictional bot card unless the user explicitly requests an authorized real-person card. Prefer original names, institutions, shows, and brands.

## Excel output

The workbook contains `Bots`, `热点候选`, `热度证据`, `卡片视图`, `运行记录`, and `字段说明`. `Bots` is one row per bot for filtering; `卡片视图` mirrors the provided Word example with fields in rows and bots in columns. See [workbook-schema.md](references/workbook-schema.md) for exact fields and execution.
