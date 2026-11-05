#!/usr/bin/env python3
"""Append AIRP hotspot research and bot cards to one formatted Excel workbook."""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


BOT_COLUMNS = [
    "Run ID", "Event ID", "Research date", "Country", "Country weight", "Heat score",
    "Heat tier", "Event date", "事件名字", "热点事件", "Source URLs", "Fiction boundary",
    "卡片名", "相关角色", "相关剧情", "制卡价值", "Cover", "Character name", "Bot ID",
    "Gender", "Type", "Short intro (public)", "Detailed intro (public)", "Opening",
    "Detailed settings (private)", "Tags", "Cover image prompt", "QA status", "Created at",
]

CANDIDATE_COLUMNS = [
    "Run ID", "Event ID", "Research date", "Country", "Country weight", "Event date",
    "事件名字", "热点事件", "Source URLs", "Recency (0-15)", "Reach (0-25)",
    "Breadth (0-20)", "Major media (0-15)", "Market relevance (0-10)",
    "AIRP convertibility (0-15)", "Subtotal", "Weighted score", "Fact integrity gate",
    "Independent evidence gate", "Breakout pattern gate", "Breakout pattern", "Heat tier", "Qualification reason",
    "Rejection reason",
]

EVIDENCE_COLUMNS = [
    "Run ID", "Event ID", "evidence_type", "platform_or_publisher", "url", "published_at",
    "captured_at", "country", "metric_name", "metric_value", "metric_window",
    "is_independent", "notes",
]

RUN_COLUMNS = [
    "Run ID", "Research date", "Freshness window", "Requested count", "Qualified count",
    "Watchlist count", "Rejected count", "Output path", "Notes",
]

SHEET_HEADERS = {
    "Bots": BOT_COLUMNS,
    "热点候选": CANDIDATE_COLUMNS,
    "热度证据": EVIDENCE_COLUMNS,
    "运行记录": RUN_COLUMNS,
}

MARKET_WEIGHTS = {
    "United States": 1.00,
    "United Kingdom": 0.92,
    "Canada": 0.84,
    "Australia": 0.78,
    "Germany": 0.72,
    "New Zealand": 0.66,
    "Russia": 0.60,
}

FIELD_NOTES = [
    ("Heat gate", "Qualified requires weighted score >=70, all 3 gates true, and a documented breakout pattern."),
    ("Evidence", "Two different evidence types required. Syndicated duplicates and repeated posts by one account are not independent."),
    ("Bots", "One row per bot. Card copy is English; research and production rationale may be Chinese."),
    ("卡片视图", "Fields in rows and each bot in a column, matching the supplied Word example."),
    ("Bot ID", "Use TBD until the product assigns an ID. Never fabricate an ID."),
    ("Fact/fiction", "Keep reported facts separate from the original fictional character, plot, and relationships."),
    ("Cover", "Store generated image path or URL; if no image is available, use Prompt ready or blank."),
]


def bool_value(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "是", "通过"}


def numeric_value(value):
    match = re.search(r"\d+(?:\.\d+)?", str(value or "").replace(",", ""))
    return float(match.group()) if match else None


def metric_within_hours(value, max_hours):
    number = numeric_value(value)
    if number is None:
        return False
    text = str(value).lower()
    if "day" in text or "天" in text:
        return number * 24 <= max_hours
    if "week" in text or "周" in text:
        return number * 168 <= max_hours
    if "hour" in text or "小时" in text or "hr" in text:
        return number <= max_hours
    return False


def breakout_supported(event):
    evidence = event.get("evidence", [])
    pattern = str(event.get("breakout_pattern", "")).strip().lower()
    if pattern == "cross-media":
        media = [item for item in evidence if item.get("evidence_type", "").strip().lower() == "major media coverage" and bool_value(item.get("is_independent"))]
        publishers = {str(item.get("platform_or_publisher", "")).strip().lower() for item in media if item.get("platform_or_publisher")}
        countries = {str(item.get("country", "")).strip().lower() for item in media if item.get("country")}
        return len(publishers) >= 3 and len(countries) >= 2
    if pattern == "social":
        for item in evidence:
            if item.get("evidence_type", "").strip().lower() != "social velocity" or not bool_value(item.get("is_independent")):
                continue
            metric = str(item.get("metric_name", "")).lower()
            value = numeric_value(item.get("metric_value"))
            if value is None or not metric_within_hours(item.get("metric_window"), 72):
                continue
            if ("view" in metric and value >= 100000) or ("engagement" in metric and value >= 10000):
                return True
        return False
    if pattern == "search":
        return any(
            item.get("evidence_type", "").strip().lower() == "search interest"
            and bool_value(item.get("is_independent"))
            and ("breakout" in str(item.get("metric_value", "")).lower() or (numeric_value(item.get("metric_value")) or 0) >= 50)
            for item in evidence
        )
    if pattern == "chart-rank":
        return any(
            item.get("evidence_type", "").strip().lower() == "chart/rank breakout"
            and bool_value(item.get("is_independent"))
            and numeric_value(item.get("metric_value")) is not None
            and numeric_value(item.get("metric_value")) <= 10
            for item in evidence
        )
    if pattern == "exceptional-scale":
        return any(
            bool_value(item.get("is_independent"))
            and str(item.get("metric_value", "")).strip()
            and "benchmark" in str(item.get("notes", "")).lower()
            for item in evidence
        )
    return False


def ensure_sheet(wb, name, headers=None):
    ws = wb[name] if name in wb.sheetnames else wb.create_sheet(name)
    if headers and ws.cell(1, 1).value is None:
        for col, value in enumerate(headers, start=1):
            ws.cell(1, col, value)
    return ws


def style_sheet(ws, widths=None):
    if ws.max_row == 0:
        return
    header_fill = PatternFill("solid", fgColor="233746")
    header_font = Font(name="Aptos", size=10, bold=True, color="FFFFFF")
    body_font = Font(name="Aptos", size=10, color="263238")
    thin_gray = Side(style="hair", color="D6DEE3")
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = Border(bottom=Side(style="thin", color="91A4B1"))
    ws.row_dimensions[1].height = 34
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font = body_font
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = Border(bottom=thin_gray)
        ws.row_dimensions[row[0].row].height = 54 if len(row) > 10 else 36
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    if widths:
        for col, width in widths.items():
            ws.column_dimensions[col].width = width
    else:
        for idx, cell in enumerate(ws[1], start=1):
            ws.column_dimensions[get_column_letter(idx)].width = min(max(len(str(cell.value or "")) + 3, 14), 32)


def init_workbook(path):
    if path.exists():
        wb = load_workbook(path)
    else:
        wb = Workbook()
        wb.active.title = "Bots"
    for name, headers in SHEET_HEADERS.items():
        ws = ensure_sheet(wb, name, headers)
        if ws.cell(1, 1).value is None:
            ws.append(headers)
    for name in ("卡片视图", "字段说明"):
        ensure_sheet(wb, name)
    return wb


def clean_tags(tags):
    if isinstance(tags, list):
        return " · ".join(str(tag) for tag in tags)
    return str(tags or "")


def event_gate(event):
    gates = event.get("gates", {})
    score = event.get("score", {})
    country = event.get("country", "")
    weight = float(event.get("country_weight", MARKET_WEIGHTS.get(country, 0)))
    parts = ["recency", "reach", "breadth", "media", "market", "airp"]
    subtotal = sum(float(score.get(key, 0)) for key in parts)
    weighted = round(subtotal * weight)
    evidence_types = {
        str(item.get("evidence_type", "")).strip().lower()
        for item in event.get("evidence", [])
        if bool_value(item.get("is_independent")) and str(item.get("evidence_type", "")).strip()
    }
    breakout_pattern = str(event.get("breakout_pattern", "")).strip().lower()
    allowed_patterns = {"cross-media", "social", "search", "chart-rank", "exceptional-scale"}
    has_fact_confirmation = "fact confirmation" in evidence_types
    passed = (
        event.get("heat_tier") == "Qualified"
        and weighted >= 70
        and bool_value(gates.get("fact_integrity"))
        and bool_value(gates.get("independent_attention"))
        and bool_value(gates.get("breakout_pattern"))
        and len(evidence_types) >= 2
        and has_fact_confirmation
        and breakout_pattern in allowed_patterns
        and breakout_supported(event)
        and bool(event.get("qualification_reason", "").strip())
    )
    return weight, subtotal, weighted, passed


def bot_row(run_id, run, event, created_at):
    card = event["card"]
    weight, subtotal, weighted, _ = event_gate(event)
    values = {
        "Run ID": run_id,
        "Event ID": event.get("event_id", ""),
        "Research date": run.get("research_date", ""),
        "Country": event.get("country", ""),
        "Country weight": weight,
        "Heat score": weighted,
        "Heat tier": event.get("heat_tier", ""),
        "Event date": event.get("event_date", ""),
        "事件名字": event.get("event_name", ""),
        "热点事件": event.get("fact_summary", ""),
        "Source URLs": "\n".join(event.get("source_urls", [])),
        "Fiction boundary": event.get("fiction_boundary", ""),
        "卡片名": card.get("card_name", ""),
        "相关角色": card.get("related_roles", ""),
        "相关剧情": card.get("related_plot", ""),
        "制卡价值": card.get("card_value", ""),
        "Cover": card.get("cover", ""),
        "Character name": card.get("character_name", ""),
        "Bot ID": card.get("bot_id") or "TBD",
        "Gender": card.get("gender", ""),
        "Type": card.get("type", "Character"),
        "Short intro (public)": card.get("short_intro", ""),
        "Detailed intro (public)": card.get("detailed_intro", ""),
        "Opening": card.get("opening", ""),
        "Detailed settings (private)": card.get("detailed_settings", ""),
        "Tags": clean_tags(card.get("tags", [])),
        "Cover image prompt": card.get("cover_image_prompt", ""),
        "QA status": card.get("qa_status", "Pending"),
        "Created at": created_at,
    }
    return [values.get(col, "") for col in BOT_COLUMNS]


def rebuild_card_view(wb):
    ws = wb["卡片视图"]
    if ws.max_row:
        ws.delete_rows(1, ws.max_row)
    ws.append(["Field"])
    bots = wb["Bots"]
    headers = [cell.value for cell in bots[1]]
    bot_rows = list(bots.iter_rows(min_row=2, values_only=True))
    bot_indices = {header: index for index, header in enumerate(headers)}
    display_fields = [
        "事件名字", "热点事件", "卡片名", "相关角色", "相关剧情", "制卡价值", "Cover",
        "Character name", "Bot ID", "Gender", "Type", "Short intro (public)",
        "Detailed intro (public)", "Opening", "Detailed settings (private)", "Tags",
        "Cover image prompt", "Heat score", "Country", "Source URLs", "Fiction boundary", "QA status",
    ]
    for col_idx, bot in enumerate(bot_rows, start=2):
        card_name = bot[bot_indices["Character name"]] or bot[bot_indices["卡片名"]] or f"Bot {col_idx - 1}"
        ws.cell(1, col_idx, str(card_name))
    for field in display_fields:
        row = [field]
        idx = bot_indices.get(field)
        for bot in bot_rows:
            row.append(bot[idx] if idx is not None else "")
        ws.append(row)


def rebuild_field_notes(wb):
    ws = wb["字段说明"]
    if ws.max_row:
        ws.delete_rows(1, ws.max_row)
    ws.append(["項目", "说明"])
    for row in FIELD_NOTES:
        ws.append(row)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="UTF-8 JSON payload")
    parser.add_argument("--output", required=True, help="Workbook path (.xlsx)")
    parser.add_argument("--allow-duplicate", action="store_true", help="Allow duplicate Event ID + Character name entries")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    run = payload.get("run", {})
    run_id = run.get("run_id") or datetime.now().strftime("%Y%m%d-%H%M")
    events = payload.get("events", [])
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb = init_workbook(output_path)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    bot_ws = wb["Bots"]
    existing = set()
    for row in bot_ws.iter_rows(min_row=2, values_only=True):
        if len(row) >= len(BOT_COLUMNS):
            existing.add((str(row[BOT_COLUMNS.index("Event ID")] or ""), str(row[BOT_COLUMNS.index("Character name")] or "")))

    qualified = watchlist = rejected = added_bots = 0
    for event in events:
        weight, subtotal, weighted, gate_passed = event_gate(event)
        tier = event.get("heat_tier", "Rejected")
        if tier == "Qualified" and gate_passed:
            qualified += 1
        elif tier == "Watchlist":
            watchlist += 1
        else:
            rejected += 1

        ev_id = event.get("event_id", "")
        score = event.get("score", {})
        gates = event.get("gates", {})
        candidate_values = {
            "Run ID": run_id,
            "Event ID": ev_id,
            "Research date": run.get("research_date", ""),
            "Country": event.get("country", ""),
            "Country weight": weight,
            "Event date": event.get("event_date", ""),
            "事件名字": event.get("event_name", ""),
            "热点事件": event.get("fact_summary", ""),
            "Source URLs": "\n".join(event.get("source_urls", [])),
            "Recency (0-15)": score.get("recency", 0),
            "Reach (0-25)": score.get("reach", 0),
            "Breadth (0-20)": score.get("breadth", 0),
            "Major media (0-15)": score.get("media", 0),
            "Market relevance (0-10)": score.get("market", 0),
            "AIRP convertibility (0-15)": score.get("airp", 0),
            "Subtotal": subtotal,
            "Weighted score": weighted,
            "Fact integrity gate": bool_value(gates.get("fact_integrity")),
            "Independent evidence gate": bool_value(gates.get("independent_attention")),
            "Breakout pattern gate": bool_value(gates.get("breakout_pattern")),
            "Breakout pattern": event.get("breakout_pattern", ""),
            "Heat tier": tier if gate_passed or tier != "Qualified" else "Rejected",
            "Qualification reason": event.get("qualification_reason", ""),
            "Rejection reason": event.get("rejection_reason", "") or ("Failed one or more heat qualification gates" if tier == "Qualified" and not gate_passed else ""),
        }
        wb["热点候选"].append([candidate_values.get(col, "") for col in CANDIDATE_COLUMNS])

        for evidence in event.get("evidence", []):
            evalues = {
                "Run ID": run_id,
                "Event ID": ev_id,
                **evidence,
            }
            wb["热度证据"].append([evalues.get(col, "") for col in EVIDENCE_COLUMNS])

        if gate_passed and event.get("card"):
            card = event["card"]
            key = (str(ev_id), str(card.get("character_name", "")))
            if not args.allow_duplicate and key in existing:
                print(f"Skipping duplicate Event ID + Character name: {key}", file=sys.stderr)
                continue
            if len(card.get("short_intro", "")) > 140:
                raise ValueError(f"Short intro exceeds 140 characters for {card.get('character_name')}")
            if not card.get("bot_id"):
                card["bot_id"] = "TBD"
            bot_ws.append(bot_row(run_id, run, event, now))
            existing.add(key)
            added_bots += 1

    wb["运行记录"].append([
        run_id,
        run.get("research_date", ""),
        run.get("freshness_window", "7 days"),
        run.get("requested_count", 0),
        qualified,
        watchlist,
        rejected,
        str(output_path),
        run.get("notes", ""),
    ])

    rebuild_card_view(wb)
    rebuild_field_notes(wb)
    style_sheet(wb["Bots"], {get_column_letter(i + 1): width for i, width in enumerate([
        20, 18, 16, 19, 15, 13, 14, 16, 36, 56, 42, 42, 28, 48, 60, 42, 32, 22, 16, 14, 17, 45, 60, 70, 80, 38, 70, 16, 27
    ])})
    style_sheet(wb["热点候选"])
    style_sheet(wb["热度证据"])
    style_sheet(wb["运行记录"])
    style_sheet(wb["卡片视图"])
    style_sheet(wb["字段说明"], {"A": 24, "B": 110})
    for row in range(2, wb["卡片视图"].max_row + 1):
        wb["卡片视图"].row_dimensions[row].height = 72 if wb["卡片视图"].cell(row, 1).value in {"Opening", "Detailed settings (private)", "相关剧情", "热点事件", "Detailed intro (public)"} else 42
    wb.save(output_path)
    print(json.dumps({
        "output": str(output_path),
        "events": len(events),
        "qualified": qualified,
        "watchlist": watchlist,
        "rejected": rejected,
        "bots_added": added_bots,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
