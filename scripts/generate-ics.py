#!/usr/bin/env python3
"""Generate the GitHub-hosted real-life calendar ICS feed."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

CALENDAR_DIR = Path(__file__).resolve().parents[1] / "calendar"
OUT = CALENDAR_DIR / "cron-calendar.ics"
MANUAL_EVENTS_PATH = CALENDAR_DIR / "manual-events.json"
NOW_UTC = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
TZ_DEFAULT = "America/Vancouver"
CALENDAR_NAME = "Glaucon Life Calendar"


def escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", r"\;")
        .replace(",", r"\,")
        .replace("\n", r"\n")
    )


def build_vevent(*, uid: str, tz: str, start: str, end: str, summary: str, description: str, rrule: str | None = None, location: str | None = None) -> str:
    lines = [
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{NOW_UTC}",
        f"DTSTART;TZID={tz}:{start}",
        f"DTEND;TZID={tz}:{end}",
    ]
    if rrule:
        lines.append(f"RRULE:{rrule}")
    lines.append(f"SUMMARY:{escape(summary)}")
    lines.append(f"DESCRIPTION:{escape(description)}")
    if location:
        lines.append(f"LOCATION:{escape(location)}")
    lines.append("END:VEVENT")
    return "\n".join(lines)


def load_manual_events() -> list[str]:
    if not MANUAL_EVENTS_PATH.exists():
        return []
    data = json.loads(MANUAL_EVENTS_PATH.read_text(encoding="utf-8"))
    events = []
    for item in data:
        events.append(
            build_vevent(
                uid=item["uid"],
                tz=item.get("timezone", TZ_DEFAULT),
                start=item["dtstart"],
                end=item["dtend"],
                summary=item["summary"],
                description=item.get("description", ""),
                rrule=item.get("rrule"),
                location=item.get("location"),
            )
        )
    return events


def main() -> None:
    events = load_manual_events()
    ics = "\n".join(
        [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Glaucon//Life Calendar//EN",
            "CALSCALE:GREGORIAN",
            f"X-WR-CALNAME:{CALENDAR_NAME}",
            f"X-WR-TIMEZONE:{TZ_DEFAULT}",
            *events,
            "END:VCALENDAR",
            "",
        ]
    )
    OUT.write_text(ics, encoding="utf-8")
    print(f"wrote {OUT} with {len(events)} events")


if __name__ == "__main__":
    main()
