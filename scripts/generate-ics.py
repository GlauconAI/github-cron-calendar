#!/usr/bin/env python3
"""Write a simple ICS feed for selected OpenClaw cron jobs."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'calendar' / 'cron-calendar.ics'

ICS = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Glaucon//Cron Calendar//EN
CALSCALE:GREGORIAN
X-WR-CALNAME:Cron Calendar
X-WR-TIMEZONE:America/Vancouver
BEGIN:VEVENT
UID:socrates-weekly-governance-brief@glaucon
DTSTAMP:20260522T204500Z
DTSTART:20260525T100000
DTEND:20260525T103000
RRULE:FREQ=WEEKLY;BYDAY=MO
SUMMARY:Socrates weekly governance brief
DESCRIPTION:每周一上午 10:00 生成上一自然周治理周报并发送 Telegram 摘要。
END:VEVENT
END:VCALENDAR
"""

OUT.write_text(ICS, encoding='utf-8')
print(f'wrote {OUT}')
