---
name: microsoft365
description: |
  Manage Microsoft 365 services from the CLI. Use when the user asks about:
  - Reading, sending, replying to, or searching emails
  - Listing inbox, checking for unread messages, or triaging email
  - Email drafts, reviewing before sending, attachments, or email signatures
  - Calendar events, scheduling meetings, finding meeting times, checking availability, or today's agenda
  - Contacts or searching people in the organisation
  - Microsoft Teams channels, messages, or posting to Teams
  - Teams chat, sending chat messages, or reading conversations
  - Presence status (available, busy, away, do not disturb)
  - Creating or joining online Teams meetings
  - To-Do tasks, task lists, creating or completing tasks
  - OneDrive or SharePoint files: upload, download, share links, search
  - Microsoft 365 setup, authentication, or Microsoft Graph access
  - "check my email", "what's on my calendar", "send a message", "schedule a meeting"
  - "teams messages", "post to teams", "set my status", "who's available"
  - "my tasks", "create a task", "what's my schedule", "morning briefing"
  - "share a file", "upload to OneDrive", "what changed in my inbox"
version: 2.0.0
---

# Microsoft 365 CLI Skill

Interact with Microsoft 365 services via the `outlook` CLI tool (source: `/Users/sasreliability/Documents/Repos/outlookMCP`, repo: `SAS-Asset-Management/outlookCLI`). Covers **Outlook Mail, Calendar, Contacts, To-Do Tasks, Teams, Chat, Presence, Online Meetings, Signatures, OneDrive, and SharePoint** through the Microsoft Graph API.

## Prerequisites

The CLI is globally installed as `outlook`. Authentication uses MSAL device code flow. Config lives at `~/.outlook-cli/config.json`; signatures in `~/.outlook-cli/signatures/`; delta sync state in `~/.outlook-cli/delta/`.

If any command returns an auth error, prompt the user to run `! outlook auth login` (requires browser interaction).

## Output Format

All commands output **JSON to stdout** and human messages to stderr. Pipe through `jq` or python for field extraction. Add `--pretty` to any list command for table output. `outlook menu` opens an interactive menu for humans — never use it as an agent.

---

## Command Reference

### Authentication

```bash
outlook auth status              # Check auth state + account info
outlook auth login               # Authenticate via device code (interactive)
outlook auth logout              # Clear cached tokens
outlook auth init --client-id <id> --tenant <id>   # Join an existing app registration (consultant onboarding, no Azure CLI)
outlook auth setup               # One time self registration via Azure CLI (already done on this machine)
outlook auth scopes              # List requested Graph API scopes
```

### Email (Outlook Mail)

```bash
# List messages (default: top 20 from Inbox, newest first)
outlook mail list
outlook mail list --top 50
outlook mail list --folder Sent
outlook mail list --unread
outlook mail list --search "quarterly report"   # search cannot combine with --unread/--filter

# Read a single email — ALWAYS prefer --text as an agent (a fraction of the tokens of HTML)
outlook mail get <messageId> --text
outlook mail get <messageId>          # full HTML body when markup matters

# Send email (signature appended automatically; see signature section)
outlook mail send --to "a@b.com" --subject "Subject" --body "<p>Body</p>" --html
outlook mail send --to "a@b.com,b@c.com" --cc "d@e.com" --subject "Hi" --body "<p>Hello</p>" --html --importance high
outlook mail send --to "a@b.com" --subject "Report" --body "<p>Attached.</p>" --html --attach /path/report.html /path/data.zip

# Draft workflow — the PREFERRED path for replies and sends (review before send)
outlook mail reply <messageId> --body "<p>Thanks</p>" --html --draft   # creates a reply draft, returns draftId
outlook mail draft --to "a@b.com" --subject "WIP" --body "<p>Draft</p>" --html   # new draft (supports --cc --bcc --attach --importance)
outlook mail drafts                                # list current drafts
outlook mail get <draftId> --text                  # review a draft
outlook mail send-draft <draftId>                  # send after approval

# Reply / Forward (immediate send — only after explicit user approval)
outlook mail reply <messageId> --body "<p>Thanks</p>" --html
outlook mail reply <messageId> --body "<p>Noted</p>" --html --all
outlook mail forward <messageId> --to "c@d.com" --comment "FYI"

# Triage — mark messages handled so loops never reprocess them
outlook mail mark-read <messageId> [<messageId2> ...]
outlook mail mark-unread <messageId>
outlook mail flag <messageId>                 # flag for follow up
outlook mail flag <messageId> --complete      # or --clear
outlook mail categories <messageId> --set "Client,Urgent"
outlook mail categories <messageId> --clear

# Incremental sync — returns ONLY what changed since the last call (ideal for polling)
outlook mail delta                  # first run establishes a baseline from now
outlook mail delta --folder Inbox   # subsequent runs return changed + removed message ids
outlook mail delta --reset          # discard state and start a new baseline

# Attachments
outlook mail attachments list <messageId>
outlook mail attachments download <messageId> --dir /tmp        # all file attachments
outlook mail attachments download <messageId> --id <attachmentId>

# Organise
outlook mail move <messageId> --folder Archive
outlook mail delete <messageId>

# Search (full text across mailbox) and folders
outlook mail search "project update"
outlook mail search "budget" --folder Inbox --top 10
outlook mail folders
```

### Calendar

```bash
# Today's agenda (times returned in Australia/Melbourne by default; --timezone to change)
outlook calendar today

# Events in a date range
outlook calendar list --start 2026-06-08 --end 2026-06-14

# Single event details
outlook calendar get <eventId> --text

# Find meeting times that work for everyone (ranked suggestions)
outlook calendar find-times --attendees "a@b.com,c@d.com" --duration 45
outlook calendar find-times --attendees "a@b.com" --duration 30 --start "2026-06-15T08:00" --end "2026-06-19T18:00" --max 5

# Create an event (timezone defaults to Australia/Melbourne)
outlook calendar create --subject "Standup" --start "2026-06-15T09:00" --end "2026-06-15T09:30"
outlook calendar create --subject "Review" --start "2026-06-15T14:00" --end "2026-06-15T15:00" --attendees "a@b.com,c@d.com" --online --location "Level 3"

# Update / delete / respond
outlook calendar update <eventId> --subject "New Title" --start "2026-06-15T10:00"
outlook calendar delete <eventId>
outlook calendar respond <eventId> --action accept     # accept | decline | tentative

# Raw free/busy blocks and calendar listing
outlook calendar freebusy --emails "a@b.com,c@d.com" --start "2026-06-15T08:00" --end "2026-06-15T18:00"
outlook calendar calendars
```

### Signatures

Graph has no signature API, so the CLI stores one per account in `~/.outlook-cli/signatures/` and appends it automatically to send, reply, forward, and draft. Pass `--no-signature` to skip.

```bash
outlook signature show                    # inspect the stored signature
outlook signature sync                    # derive from recent Sent Items (dominant cluster heuristic)
outlook signature set --file sig.html     # manual override
outlook signature clear
```

Do **not** include "Regards" or a sign off block in composed bodies — the signature carries it.

### OneDrive and SharePoint Files

```bash
outlook files list                                  # OneDrive root
outlook files list --path "Deliverables/clientX"
outlook files upload report.html --path "Deliverables/clientX"   # large files chunk automatically
outlook files download "Deliverables/clientX/report.html" --out ./report.html
outlook files share <itemId> --type view            # organisation scoped link (or --type edit)
outlook files search "maturity assessment"
outlook files sites "Ensemble"                      # discover SharePoint sites
outlook files site-drives <siteId>                  # list a site's drives; browse with files list --drive <driveId>
```

### Contacts & People

```bash
outlook contacts list
outlook contacts list --search "Jane"               # startswith matching on name/email
outlook contacts get <contactId>
outlook contacts search "John Smith"                # organisation people search (GAL)
```

### To-Do Tasks

```bash
outlook tasks lists
outlook tasks list <listId> --filter "status ne 'completed'"
outlook tasks create <listId> --title "Review PR" --due 2026-06-15 --importance high
outlook tasks update <listId> <taskId> --status inProgress
outlook tasks complete <listId> <taskId>
```

### Teams Channels

```bash
outlook teams list
outlook teams channels <teamId>
outlook teams messages <teamId> <channelId> --top 50
outlook teams send <teamId> <channelId> --body "Update: deployment complete"
outlook teams reply <teamId> <channelId> <messageId> --body "Agreed"
```

### Teams Chat

```bash
outlook chat list
outlook chat messages <chatId> --top 50
outlook chat send <chatId> --body "Hey, quick question"
```

### Presence

```bash
outlook presence get
outlook presence set --availability Available --activity Available
outlook presence set --availability Busy --activity InACall --expiry 30
outlook presence set --availability DoNotDisturb --activity Presenting --expiry 120
outlook presence user <userId_or_email>
```

### Online Meetings

```bash
outlook meeting create --subject "Sprint Review" --start "2026-06-15T14:00" --end "2026-06-15T15:00"
outlook meeting get <meetingId>
```

---

## Common Workflows

### Morning Briefing

```bash
outlook calendar today
outlook mail list --unread --top 10
outlook presence get
```

### Email Triage

```bash
outlook mail list --unread --top 20
outlook mail get <messageId> --text          # read the important ones cheaply
outlook mail mark-read <id1> <id2> <id3>     # mark handled so they are not reprocessed
outlook mail flag <id>                       # needs follow up
```

### Inbox Polling (scheduled agents)

```bash
outlook mail delta        # one cheap call returning only changes since last run
```

### Reply With Review (preferred outbound path)

1. `outlook mail reply <id> --body "<p>...</p>" --html --draft` → returns draftId
2. Show the user the draft content and recipients, ask for approval
3. `outlook mail send-draft <draftId>`

### Schedule a Meeting

1. `outlook calendar find-times --attendees "..." --duration 45` → ranked slots everyone can make
2. Confirm the slot with the user
3. `outlook calendar create --subject "..." --start "..." --end "..." --attendees "..." --online`

### Share a Deliverable

1. `outlook files upload report.html --path "Deliverables/clientX"`
2. `outlook files share <itemId> --type view` → organisation link to paste into mail or Teams

---

## MANDATORY: Approval Before Sending

**NEVER send an email, reply, forward, or Teams/chat message without explicit user approval.** This is a hard rule with no exceptions.

The draft workflow is the preferred mechanism: create the draft (`mail reply --draft` or `mail draft`), present recipients, subject, and body to the user, and only run `mail send-draft` after an affirmative response. For Teams/chat messages, show the message text and destination before running send.

If the user says "send an email to X about Y", compose and draft first. Do NOT send in the same step as composing.

## MANDATORY: Always Send as HTML

**Always include the `--html` flag** on every `outlook mail send`, `outlook mail reply`, and `outlook mail draft`. Compose bodies with HTML tags: `<p>` paragraphs, `<br>` breaks, `<strong>` bold, `<a href="...">` links, `<ul>/<li>` lists. Never send plain text.

## MANDATORY: Always Arial

**Every font in outbound mail must be Arial**, matching the signature. Wrap the composed body in a container that fixes the typeface, and do not introduce any other font anywhere in the body:

```html
<div style="font-family:Arial,sans-serif;font-size:14px;color:#3c4045;line-height:1.4;">
  <p style="margin:0 0 12px;">Body paragraph…</p>
</div>
```

## MANDATORY: Voice — sound like Shane

**Before composing any email body (send, reply, forward, or draft), read `~/.outlook-cli/voiceProfile.md` and match that voice** — its register, openings, closings, rhythm, punctuation habits, and vocabulary. This profile is generated by the `emailVoice` sub skill from a sample of Shane's own sent mail.

- If the profile file is missing, compose in a clear, professional Australian English register and tell Shane he can run `/emailVoice` to capture his real voice.
- The profile shapes tone and phrasing only. An explicit instruction from Shane about a specific email always wins.
- The signature already carries "Regards," and his name, so never add a redundant sign off block in the body.

---

## Important Notes

- **Message IDs** are long base64 strings returned by list commands. Always extract the `id` field from list results before using get/reply/forward/move/delete.
- **Token economy**: always read bodies with `--text`; only fetch HTML when markup matters.
- **Date format**: ISO 8601 (e.g. `2026-06-15T14:00`). Calendar commands default to `Australia/Melbourne`.
- **Rate limiting**: the CLI retries 429 (honouring Retry-After) and transient 5xx automatically — no manual backoff needed.
- **Auth expiry**: tokens refresh silently. If auth fails, prompt the user to run `! outlook auth login`.
- **Network**: the launcher prefers direct IPv4 (some networks advertise unroutable IPv6). `OUTLOOK_CLI_IPV6=1` opts back in.
- **Sensitive content**: email bodies and chat messages may contain confidential information. Do not summarise or repeat sensitive content unless the user explicitly asks.
