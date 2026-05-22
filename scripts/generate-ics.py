#!/usr/bin/env python3
"""Generate an ICS feed from enabled OpenClaw cron jobs."""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JOBS_PATH = Path("/Users/glaucon/.openclaw/cron/jobs.json")
OUT = Path(__file__).resolve().parents[1] / "calendar" / "cron-calendar.ics"
NOW_UTC = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
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
    "0 4 * * 1": "20260525T040000",
    "0 9 1 * *": "20260601T090000",
    "30 9 * * 2": "20260526T093000",
    "0 10-23 * * 2": "20260526T100000",
    "30 9 * * 5": "20260529T093000",
    "0 11 * * 5": "20260523T110000",
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
    return "\n".join(
        [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{NOW_UTC}",
            f"DTSTART;TZID={tz}:{start}",
            f"DTEND;TZID={tz}:{end}",
            f"RRULE:{rrule}",
            f"SUMMARY:{escape(summary)}",
            f"DESCRIPTION:{escape(description)}",
            "END:VEVENT",
        ]
    )


def main() -> None:
    data = json.loads(JOBS_PATH.read_text(encoding="utf-8"))
    jobs = [
        job
        for job in data["jobs"]
        if job.get("enabled") and job.get("schedule", {}).get("kind") == "cron"
    ]
    events = [build_event(job) for job in jobs]
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
