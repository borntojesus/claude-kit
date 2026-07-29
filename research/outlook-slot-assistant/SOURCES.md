# Джерела

Дата перевірки: 29 липня 2026.

## Microsoft Graph

- getSchedule, вільний і зайнятий час: <https://learn.microsoft.com/en-us/graph/api/calendar-getschedule?view=graph-rest-1.0>
- Огляд роботи з free/busy в Outlook: <https://learn.microsoft.com/en-us/graph/outlook-get-free-busy-schedule>
- findMeetingTimes, включно з обмеженням для особистих скриньок outlook.com: <https://learn.microsoft.com/en-us/graph/api/user-findmeetingtimes?view=graph-rest-1.0>
- Приклад використання findMeetingTimes: <https://learn.microsoft.com/en-us/graph/findmeetingtimes-example>
- dateTimeTimeZone, формати часу: <https://learn.microsoft.com/en-us/graph/api/resources/datetimetimezone?view=graph-rest-1.0>
- supportedTimeZones, формати Windows та IANA: <https://learn.microsoft.com/en-us/graph/api/outlookuser-supportedtimezones?view=graph-rest-1.0>
- Огляд Calendar API: <https://learn.microsoft.com/en-us/graph/api/resources/calendar-overview?view=graph-rest-1.0>

Ключові факти, які впливають на дизайн:

1. Найменший потрібний дозвіл для `getSchedule` це `Calendars.Read`, для `findMeetingTimes` це `Calendars.Read.Shared`.
2. `findMeetingTimes` працює для робочих і навчальних скриньок M365, для особистих outlook.com не працює.
3. За замовчуванням час повертається в UTC, іншу зону задає заголовок `Prefer: outlook.timezone`.
4. Між зонами Windows та IANA немає відповідності один до одного: одна зона Windows накриває кілька зон IANA.
5. `getSchedule` вважає вільним увесь час у вікні, крім наявних подій, тому робочі години й буфери потрібно тримати у власному конфізі.

## Outlook: пріоритезація пошти

- Conditional Formatting у класичному Outlook для Windows: <https://support.microsoft.com/en-us/office/conditional-formatting-in-classic-outlook-for-windows-ee281b41-5be4-47e4-81fb-1d8a202870df>
- Правила умовного формату для вхідних: <https://support.microsoft.com/en-us/office/use-conditional-formatting-rules-to-change-incoming-messages-in-outlook-4efbf993-fb00-4f2c-9a3f-78e64e4455ec>
- Copilot, пріоритезація вхідних, вимагає ліцензії Microsoft 365 Copilot: <https://support.microsoft.com/en-us/topic/prioritize-my-inbox-65e37040-2c90-4ee3-86d9-e95d5ba0e3cb>
- Microsoft To Do з флагами з Outlook: <https://support.microsoft.com/en-us/office/using-microsoft-to-do-with-flagged-email-from-outlook-f90c37b0-4453-4756-a6d5-e2ef8d33b395>

Розфарбовування рядків за відправником доступне тільки в класичному Outlook для
Windows. У новому Outlook і у веб-версії його немає, тому пакет будує підсвічування
на категоріях плюс серверних правилах.

## Планування

- GTD, шість горизонтів фокусу: <https://gettingthingsdone.com/2011/01/the-6-horizons-of-focus/>
- GTD про виведення пріоритетів згори вниз: <https://gettingthingsdone.com/2010/01/getting-your-arms-around-your-priorities/>
- EOS Vision Traction Organizer: <https://www.eosworldwide.com/vto>
- Вісім питань V/TO: <https://www.ninety.io/eos/blog/8-eos-vision-questions>
- 12 Week Year, ведення рахунку й орієнтир 85 відсотків: <https://www.oreilly.com/library/view/the-12-week/9781119475248/c05.xhtml>

## Планувальники як альтернатива власному боту

- Cal.com, API v2, версія v1 вимикається 28 лютого 2026: <https://cal.com/blog/calcom-v5-6>
- Гайд зі self-hosting Cal.com: <https://ossalt.com/guides/self-hosting-guide-calcom-2026>

Закриті підписки на кшталт Sunsama, Akiflow або Superhuman у цьому пакеті не
розглядаються: до них немає доступу з боку агента, тому вони не можуть бути
частиною системи, де половину роботи виконує бот.
