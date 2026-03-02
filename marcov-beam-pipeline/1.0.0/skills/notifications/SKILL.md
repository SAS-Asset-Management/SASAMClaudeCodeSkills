---
name: MBP:notifications
description: Send push notifications via Microsoft Teams webhook and macOS desktop notifications. Use when workflows complete, errors occur, tasks need attention, or other skills finish. Supports integration events and custom alerts.
---

# Push Notifications Skill

Send notifications to Microsoft Teams and macOS desktop when tasks complete, errors occur, or attention is needed.

## Overview

This skill provides two notification channels:

1. **Microsoft Teams** - Send messages to a Teams channel via incoming webhook (Adaptive Card format)
2. **Desktop (macOS)** - Native notifications via terminal-notifier with sound and click actions

Use notifications for:
- Workflow alerts (task complete, errors, needs attention)
- Integration events (notify when other skills finish)
- Custom messages to colleagues

## Notification Types

| Type | Icon | Colour | Use When |
|------|------|--------|----------|
| `success` | ✓ | Green | Task completed successfully |
| `error` | ✗ | Red | Task failed, requires attention |
| `warning` | ⚠ | Amber | Task completed with issues |
| `info` | ℹ | Blue | General information update |
| `attention` | 👁 | Purple | User input required |

## Commands

| Command | Action |
|---------|--------|
| `setup` | Run setup wizard for one or both channels |
| `test` | Send test notification to all configured channels |
| `status` | Show current configuration and statistics |
| `send [message]` | Send a custom notification (default: info type) |
| `teams [message]` | Send to Teams only |
| `desktop [message]` | Send to desktop only |
| `disable [channel]` | Temporarily disable a channel |
| `enable [channel]` | Re-enable a disabled channel |
| `log` | Show recent notification history |

## Invocation Examples

```
/MBP:notifications setup                           # First-time configuration
/MBP:notifications test                            # Test all channels
/MBP:notifications "Build complete"                # Send info notification
/MBP:notifications "Deployment failed" --type error
/MBP:notifications teams "Ready for review"        # Teams only
/MBP:notifications desktop "Process finished"      # Desktop only
/MBP:notifications status                          # Show config
```

---

## Discovery Process

### Check Configuration State

Before sending any notification, check if `.notifications/config.json` exists.

**If config exists:**
1. Load configuration from `.notifications/config.json`
2. Validate webhook URL is still set (if Teams enabled)
3. Check `terminal-notifier` availability (if desktop enabled): `which terminal-notifier`
4. Proceed with notification

**If config does NOT exist:**
1. Run first-time setup interview
2. Guide through channel configuration
3. Create config file
4. Then proceed with notification

### First-Time Setup Questions

When no configuration exists, ask:

1. **Notification Channels**
   - Which notification channels would you like to enable?
   - Options: Microsoft Teams, Desktop (macOS), Both

2. **Microsoft Teams Setup** (if selected)
   - Do you have a Teams incoming webhook URL ready?
   - If yes: Ask for the URL
   - If no: Provide setup guide from `references/setup-guide-teams.md`

3. **Desktop Setup** (if selected)
   - Check if terminal-notifier is installed: `which terminal-notifier`
   - If not installed: Provide installation guide from `references/setup-guide-desktop.md`

4. **Default Preferences**
   - Should notifications include sound? (default: yes)
   - Default notification type? (default: info)

---

## Configuration State

Store configuration in `.notifications/config.json`:

```json
{
  "schema_version": "1.0.0",
  "created_at": "2026-02-25T10:30:00Z",
  "updated_at": "2026-02-25T10:30:00Z",
  "channels": {
    "teams": {
      "enabled": true,
      "webhook_url": "https://outlook.office.com/webhook/...",
      "verified_at": "2026-02-25T10:30:00Z"
    },
    "desktop": {
      "enabled": true,
      "tool": "terminal-notifier",
      "verified_at": "2026-02-25T10:30:00Z"
    }
  },
  "preferences": {
    "default_channel": "both",
    "sound_enabled": true,
    "default_type": "info"
  },
  "statistics": {
    "total_sent": 0,
    "teams_sent": 0,
    "desktop_sent": 0,
    "last_sent_at": null
  }
}
```

See `references/config-template.json` for the full schema.

---

## Sending Notifications

### Teams Notifications

Use the Bash tool to send via curl:

```bash
curl -H "Content-Type: application/json" -d @- "WEBHOOK_URL" << 'EOF'
{
  "type": "message",
  "attachments": [{
    "contentType": "application/vnd.microsoft.card.adaptive",
    "content": {
      "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
      "type": "AdaptiveCard",
      "version": "1.4",
      "body": [
        {
          "type": "TextBlock",
          "text": "✓ {{TITLE}}",
          "weight": "Bolder",
          "size": "Medium",
          "color": "Good"
        },
        {
          "type": "TextBlock",
          "text": "{{MESSAGE}}",
          "wrap": true
        },
        {
          "type": "FactSet",
          "facts": [
            {"title": "Skill", "value": "{{SKILL_NAME}}"},
            {"title": "Time", "value": "{{TIMESTAMP}}"}
          ]
        }
      ]
    }
  }]
}
EOF
```

See `references/teams-message-templates.json` for templates per notification type.

**Colour mapping for Adaptive Cards:**
- success: `"color": "Good"` (green)
- error: `"color": "Attention"` (red)
- warning: `"color": "Warning"` (amber)
- info: `"color": "Default"` (blue)
- attention: `"color": "Accent"` (purple)

### Desktop Notifications (macOS)

Use terminal-notifier via Bash:

```bash
terminal-notifier \
  -title "{{TITLE}}" \
  -message "{{MESSAGE}}" \
  -sound "default" \
  -group "claude-code"
```

**For different notification types:**
- success: `-sound "Glass"`
- error: `-sound "Basso"`
- warning: `-sound "Sosumi"`
- info: `-sound "default"`
- attention: `-sound "Ping"`

### Alternative Platforms

**Linux (notify-send):**
```bash
notify-send "{{TITLE}}" "{{MESSAGE}}" --urgency=normal
```

**Windows (PowerShell toast):**
```powershell
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
$template.SelectNodes("//text[@id='1']")[0].AppendChild($template.CreateTextNode("{{TITLE}}"))
$template.SelectNodes("//text[@id='2']")[0].AppendChild($template.CreateTextNode("{{MESSAGE}}"))
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Claude Code").Show([Windows.UI.Notifications.ToastNotification]::new($template))
```

---

## Integration with Other Skills

When another skill completes, it can trigger a notification. The pattern is:

```
--- Skill Complete ---

[Summary of what was done]

Sending notification...
```

Then send the notification using the configured channels.

**Integration Examples:**

| Skill | Trigger | Message |
|-------|---------|---------|
| `MBP:beam-selling` | Engagement saved | "BEAM engagement [Company] updated - Stage [N]" |
| `MBP:tender` | Assessment complete | "Tender assessment complete - [N] shortlisted" |
| `MBP:b2b-research` | Dossier generated | "B2B dossier ready: [Company]" |
| `MBP:data-quality` | Report generated | "Data quality report ready - Rating: [X]" |

---

## Error Handling

### Teams Webhook Unreachable

If Teams notification fails:

```
⚠ Teams notification failed

Error: Unable to reach webhook endpoint
HTTP Status: [status code]

Possible causes:
- Network connectivity issues
- Webhook URL expired or revoked
- Teams service disruption

Action taken:
- Desktop notification sent as fallback (if configured)
- Error logged

To fix:
- Check network connectivity
- Verify webhook URL is still valid in Teams
- Run `/MBP:notifications setup teams` to reconfigure
```

### terminal-notifier Not Installed

If desktop notification fails:

```
⚠ Desktop notification unavailable

Error: terminal-notifier not found in PATH

To install (macOS):
  brew install terminal-notifier

For Linux (alternative):
  sudo apt install libnotify-bin
  # Then use: notify-send "Title" "Message"

Action taken:
- Teams notification sent (if configured)
- Desktop notification skipped
```

### No Channels Configured

```
⚠ No notification channels configured

Run `/MBP:notifications setup` to configure:
- Microsoft Teams (incoming webhook)
- Desktop notifications (terminal-notifier)
```

---

## Security Considerations

**Webhook URL Protection:**
- Store webhook URL in `.notifications/config.json` (should be in .gitignore)
- Never display full webhook URL - mask it: `https://outlook.office.com/webhook/...abc123`
- Validate URL starts with `https://` before saving

**Testing Webhook:**
When user provides a webhook URL, send a test message to verify it works before saving to config.

---

## Notification Workflow

1. **Parse Command** - Determine if setup, test, send, or channel-specific
2. **Load Config** - Read `.notifications/config.json` or trigger setup
3. **Validate Channels** - Check enabled channels are still functional
4. **Format Message** - Apply notification type styling (icon, colour)
5. **Send Notification** - Execute curl (Teams) and/or terminal-notifier (desktop)
6. **Update Statistics** - Increment counters in config
7. **Report Result** - Confirm success or explain failure

---

## Pre-Delivery Checklist

Before sending a notification, verify:

- [ ] Configuration loaded from `.notifications/config.json`
- [ ] At least one channel is configured and enabled
- [ ] Message is not empty
- [ ] Message type is valid (success, error, warning, info, attention)
- [ ] Teams webhook URL is HTTPS (if Teams enabled)
- [ ] terminal-notifier exists in PATH (if desktop enabled on macOS)

After sending:

- [ ] Update statistics in config (total_sent, channel counts, last_sent_at)
- [ ] Report success or failure to user

---

## Content Guidelines

**Notification Messages:**
- Keep titles under 50 characters
- Keep messages under 200 characters
- Be specific: "Tender assessment complete - 3 shortlisted" not "Task done"
- Include context: which skill, what happened, what to do next
- Use Australian English spelling throughout

---

## Reference Files

- `references/config-template.json` - Configuration schema
- `references/teams-message-templates.json` - Adaptive Card templates per type
- `references/setup-guide-teams.md` - Teams webhook setup instructions
- `references/setup-guide-desktop.md` - Desktop notification setup instructions
