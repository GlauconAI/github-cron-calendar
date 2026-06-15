#!/usr/bin/env python3
"""Generate an ICS feed from enabled OpenClaw cron jobs."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JOBS_PATH = Path("/Users/glaucon/.openclaw/cron/jobs.json")
MIGRATED_JOBS_PATH = Path("/Users/glaucon/.openclaw/cron/jobs.json.migrated")
CALENDAR_DIR = Path(__file__).resolve().parents[1] / "calendar"
OUT = CALENDAR_DIR / "cron-calendar.ics"
MANUAL_EVENTS_PATH = CALENDAR_DIR / "manual-events.json"
NOW_UTC = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
TZ_DEFAULT = "America/Vancouver"

DAY_MAP = {
    "0": "SU",
    "1": "MO",
    "2": "TU",
    "3": "WE",
    "4": "TH",
    "5": "FR",
    "6": "SA",
    "7": "SU",
}

FIRST_OCCURRENCE = {
    "30 17 * * 0": "20260524T173000",
    "10 7 * * *": "20260523T071000",
    "0 10 * * 1": "20260525T100000",
    "0 11 * * 1": "20260525T110000",
    "0 11 * * 0": "20260531T110000",
    "0 4 * * 1": "20260525T040000",
    "0 9 1 * *": "20260601T090000",
    "30 9 * * 2": "20260526T093000",
    "0 10-23 * * 2": "20260526T100000",
    "30 9 * * 5": "20260529T093000",
    "0 11 * * 5": "20260523T110000",
    "0 20 * * *": "20260608T200000",
    "15 22 * * *": "20260612T221500",
    "0 7 * * *": "20260616T070000",
    "0 23 * * *": "20260615T230000",
}

DURATIONS_MIN = {
    "0 10-23 * * 2": 60,
}


def escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", r"\;")
        .replace(",", r"\,")
        .replace("\n", r"\n")
    )


def add_minutes(local_dt: str, minutes: int) -> str:
    dt = datetime.strptime(local_dt, "%Y%m%dT%H%M%S")
    from datetime import timedelta

    return (dt + timedelta(minutes=minutes)).strftime("%Y%m%dT%H%M%S")


def cron_to_rrule(expr: str) -> str:
    minute, hour, dom, month, dow = expr.split()

    if expr == "0 10-23 * * 2":
        return "FREQ=WEEKLY;BYDAY=TU;BYHOUR=10,11,12,13,14,15,16,17,18,19,20,21,22,23;BYMINUTE=0;BYSECOND=0"
    if dom != "*" and month == "*" and dow == "*":
        return f"FREQ=MONTHLY;BYMONTHDAY={dom};BYHOUR={hour};BYMINUTE={minute};BYSECOND=0"
    if dow != "*" and dom == "*" and month == "*":
        return f"FREQ=WEEKLY;BYDAY={DAY_MAP[dow]};BYHOUR={hour};BYMINUTE={minute};BYSECOND=0"
    if dom == "*" and month == "*" and dow == "*":
        return f"FREQ=DAILY;BYHOUR={hour};BYMINUTE={minute};BYSECOND=0"
    raise ValueError(f"Unsupported cron expr: {expr}")


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


def build_event(job: dict) -> str:
    schedule = job["schedule"]
    expr = schedule["expr"]
    tz = schedule.get("tz", TZ_DEFAULT)
    start = FIRST_OCCURRENCE[expr]
    duration = DURATIONS_MIN.get(expr, 30)
    end = add_minutes(start, duration)
    summary = f"{job.get('agentId', job.get('sessionKey', 'job'))}: {job['name']}"
    description_parts = []
    if job.get("description"):
        description_parts.append(job["description"])
    description_parts.append(f"cron: {expr} @ {tz}")
    description = "\n".join(description_parts)
    uid = f"{job['id']}@openclaw-cron"
    rrule = cron_to_rrule(expr)
    return build_vevent(uid=uid, tz=tz, start=start, end=end, summary=summary, description=description, rrule=rrule)


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
    jobs_path = JOBS_PATH if JOBS_PATH.exists() else MIGRATED_JOBS_PATH
    data = json.loads(jobs_path.read_text(encoding="utf-8"))
    jobs = [
        job
        for job in data["jobs"]
        if job.get("enabled") and job.get("schedule", {}).get("kind") == "cron"
    ]
    events = [build_event(job) for job in jobs]
    events.extend(load_manual_events())
    ics = "\n".join(
        [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Glaucon//OpenClaw Cron Calendar//EN",
            "CALSCALE:GREGORIAN",
            "X-WR-CALNAME:OpenClaw Cron Jobs",
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
