#!/usr/bin/env python3
"""Placeholder generator for cron -> ICS publishing."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'calendar' / 'cron-calendar.ics'

ICS = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Glaucon//Cron Calendar//EN
CALSCALE:GREGORIAN
X-WR-CALNAME:Cron Calendar
X-WR-TIMEZONE:America/Vancouver
BEGIN:VEVENT
UID:cron-test-20260522T133000@glaucon
DTSTAMP:20260522T202900Z
DTSTART:20260522T133000
DTEND:20260522T140000
SUMMARY:Cron Test
DESCRIPTION:Initial placeholder event for Proton Calendar subscription testing.
END:VEVENT
END:VCALENDAR
"""

OUT.write_text(ICS, encoding='utf-8')
print(f'wrote {OUT}')
