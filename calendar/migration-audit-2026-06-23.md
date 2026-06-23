# Calendar Migration Audit - 2026-06-23

## Target Routing

- GitHub ICS feed: real-life schedule events only.
- Proton Calendar `Glaucon - Proton`: OpenClaw automation / cron / scheduled-task visibility.

## Current Manual Events

### Keep In GitHub ICS

| UID | Summary | Owner | Reason |
| --- | --- | --- | --- |
| `giskard-soccer-1-5-2yrs-pinetree-2026-05@openclaw-manual` | LL: Soccer 1.5-2yrs | Giskard | Child class / real-life commitment |
| `hippocrates-leah-ophthalmology-2026-05-26@openclaw-manual` | Leah 眼科就诊（时间待补） | Hippocrates | Medical appointment |
| `confucius-daycare-family-activity-2026-05-29@openclaw-manual` | LL Daycare Family Activity | Confucius | Daycare / family activity |
| `hippocrates-leah-allergy-2026-06-01@openclaw-manual` | Leah 过敏门诊 | Hippocrates | Medical appointment |
| `confucius-harper-3rd-birthday-party-2026-06-20@openclaw-manual` | Harper's 3rd Birthday Party | Confucius | Social / birthday event |
| `giskard-vso-mini-music-makers-coquitlam-2026-08@openclaw-manual` | Luka: VSO Mini Music Makers | Giskard | Child class / real-life commitment |
| `giskard-vso-mini-music-makers-prestart-reminder-2026-08-05@openclaw-manual` | 提醒：Luka VSO Mini Music Makers 本周开课 | Giskard | Preparation reminder for a real-life class; keep unless user wants all prep reminders in Proton |
| `hippocrates-user-family-doctor-ldl-2026-06-10@openclaw-manual` | 本人家庭医生电话问诊：Dr. Wang | Hippocrates | Medical appointment |

### Move To Proton Calendar `Glaucon - Proton`

| UID | Summary | Owner | Reason |
| --- | --- | --- | --- |
| `hippocrates-luka-ear-followup-2026-05-27@openclaw-manual` | Luka 右耳不适回访提醒 | Hippocrates | OpenClaw follow-up task |
| `plato-402v-transfer-reminder-2026-10-01@openclaw-manual` | 402v.com 域名转移提醒 | Plato | OpenClaw reminder task |
| `hippocrates-leah-cough-followup-2026-06-12@openclaw-manual` | Leah 短促咳嗽继续观察一周回访提醒 | Hippocrates | OpenClaw follow-up task |
| `hippocrates-user-ldl-monthly-tracking@openclaw-manual` | 每月 LDL 跟踪提醒 | Hippocrates | Recurring OpenClaw tracking task |
| `hippocrates-children-adenoid-chen-referral-followup-2026-06-24@openclaw-manual` | 回访：陈医生腺样体转诊是否回复 | Hippocrates | OpenClaw follow-up task |
| `amou-taptap-phone-migration-2026-06-19@openclaw-manual` | 提醒：修改 TapTap 账号绑定手机号 | Amou | OpenClaw reminder task |
| `amou-biligame-sanguosha-tianming-result-2026-06-16@openclaw-manual` | 检查：BiliGame 三国杀天命棋局首测资格 | Amou | OpenClaw check task |
| `socrates-weekly-workspace-github-backup@openclaw-manual` | Socrates: 每周 workspace GitHub 备份 | Socrates | Recurring OpenClaw automation |
| `confucius-bullet-journal-daily-plan-generation@openclaw-manual` | Confucius: 2026 Bullet Journal daily plan generation | Confucius | Recurring OpenClaw automation |
| `confucius-bullet-journal-nightly-archive@openclaw-manual` | Confucius: 2026 Bullet Journal nightly Daily Journal archive | Confucius | Recurring OpenClaw automation |
| `confucius-bullet-journal-weekly-habit-review@openclaw-manual` | Confucius: 2026 Bullet Journal weekly Habit review | Confucius | Recurring OpenClaw automation |
| `confucius-fifa-2026-daily-vancouver-match-brief@openclaw-manual` | Confucius: FIFA World Cup 2026 daily Vancouver match brief | Confucius | Recurring OpenClaw automation |
| `giskard-ll-twin-class-separation-monthly-check@openclaw-manual` | Giskard: 图南北培 3 岁分班每月追踪 | Giskard | Recurring OpenClaw tracking task |
| `giskard-ll-basketball-fall-light-scan-2026-08-07@openclaw-manual` | Giskard: LL basketball Fall 2026 轻扫 | Giskard | OpenClaw scan task |
| `giskard-ll-basketball-winter-main-scan-2026-11-20@openclaw-manual` | Giskard: LL basketball Winter 2027 主扫描 | Giskard | OpenClaw scan task |
| `giskard-ll-basketball-winter-registration-2026-11-24@openclaw-manual` | Giskard: LL basketball Winter 2027 报名前提醒 | Giskard | OpenClaw registration reminder task |

## Cron Store Events Previously Merged By Generator

The old generator merged enabled recurring cron jobs from `/Users/glaucon/.openclaw/cron/jobs.json.migrated`.
Because the GitHub ICS is now real-life only, these must be represented in Proton Calendar `Glaucon - Proton` instead.

| Cron ID | Name | Agent | Schedule |
| --- | --- | --- | --- |
| `c3c79a59-cb29-43f1-a786-46a12178ae5d` | socrates-weekly-governance-brief | main / Socrates | `0 10 * * 1` |
| `700a800e-426d-4e04-a320-f425916662d1` | llm-wiki:weekly-maintenance | Aristotle | `0 4 * * 1` |
| `b5c7a4f6-9e4e-47fa-914d-70703c476ed3` | ll-monthly-growth-reminder | Giskard | `0 9 1 * *` |
| `f41462dc-6551-419a-ac46-0167fd1aa636` | lordguan-weekly-asset-review-kickoff | Lordguan | `30 9 * * 2` |
| `e9e816cf-2530-4064-9f0f-366b0eb2a31f` | lordguan-weekly-asset-review-followup | Lordguan | `0 10-23 * * 2` |
| `d5c47c3d-1f0f-4029-b38e-0519be36ea77` | LL weekend classes seasonal sweep | Giskard | `30 9 * * 5` |
| `af965a5c-3834-48e0-9cd7-845fa4a16fab` | ll-weekly-weekend-activity-radar | Confucius | `0 11 * * 5` |
| `e53709cf-90aa-4152-8f39-bd4cc86fdbbb` | ai-intel:weekly-brief | Plato | `0 11 * * 0` |
| `2fcf7f7e-af5d-48ad-9178-d570da8fee6d` | ai-intel:notebooklm-preload-daily | Plato | `0 20 * * *` |

## Migration Status

- GitHub ICS generator has been changed to read only `manual-events.json`.
- GitHub ICS display name has been changed to `Glaucon Life Calendar`.
- Proton Calendar `Glaucon - Proton` import completed for the automation entries listed above.
- The first Proton import accepted 33 events; `confucius: ll-weekly-weekend-activity-radar` was imported separately after correcting its first occurrence to a Friday.
- Four past one-off automation reminders were imported separately so historical automation entries are not left in the real-life feed.
- With `OpenClaw Cron Jobs` hidden in Proton Calendar, the 2026-06-22 week shows the imported automation entries under `Glaucon - Proton`.
- The 16 manual automation entries have been removed from `manual-events.json`.
- `cron-calendar.ics` has been regenerated with 8 real-life events.
