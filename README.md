# Glaucon Life Calendar

Static ICS feed for real-life schedule events subscribed from Proton Calendar.

This calendar is for family, health, children classes, daycare / school,
birthdays, travel, appointments, and other real-world commitments. OpenClaw
automation / cron visibility belongs in Proton Calendar `Glaucon - Proton`,
not in this GitHub ICS feed.

## Files
- `calendar/cron-calendar.ics`: published ICS feed. The filename is retained for subscription URL stability.
- `calendar/manual-events.json`: source events for the real-life calendar feed.
- `scripts/generate-ics.py`: ICS generator.

## Publishing model
This repo is intended to be published via GitHub Pages so Proton Calendar can subscribe to a stable URL.
