# Microsoft Teams Webhook Setup Guide

This guide walks you through creating an incoming webhook for Microsoft Teams to receive notifications from Claude Code.

## Prerequisites

- Microsoft Teams desktop or web app
- Permission to add connectors to a Teams channel (contact your IT admin if restricted)

## Step-by-Step Setup

### 1. Open Microsoft Teams

Launch Teams on desktop or navigate to [teams.microsoft.com](https://teams.microsoft.com) in your browser.

### 2. Navigate to the Target Channel

Go to the team and channel where you want to receive notifications.

**Recommendation:** Create a dedicated channel like "Claude Code Alerts" to keep notifications organised.

### 3. Access Channel Settings

1. Click the **three dots (...)** next to the channel name
2. Select **Connectors** from the dropdown menu

If you don't see "Connectors", your organisation may have restricted this feature. Contact your IT administrator.

### 4. Find Incoming Webhook

1. In the Connectors panel, search for **"Incoming Webhook"**
2. Click **Configure** (or **Add** if not already added)

### 5. Configure the Webhook

1. **Name:** Enter a descriptive name like "Claude Code Notifications"
2. **Image:** (Optional) Upload a custom icon - a robot or notification bell works well
3. Click **Create**

### 6. Copy the Webhook URL

After creation, Teams displays the webhook URL. It looks like:

```
https://outlook.office.com/webhook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx@yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy/IncomingWebhook/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa
```

**Important:**
- Click **Copy** to copy the full URL
- Save this URL securely - it's like a password for posting to your channel
- Anyone with this URL can send messages to your channel

### 7. Click Done

Close the configuration panel. Your webhook is now active.

## Testing the Webhook

You can test the webhook with a simple curl command:

```bash
curl -H "Content-Type: application/json" -d '{"text":"Hello from Claude Code!"}' "YOUR_WEBHOOK_URL"
```

If successful, you'll see "Hello from Claude Code!" appear in your Teams channel.

## Security Considerations

- **Keep the URL private** - Treat it like a password
- **Don't commit to git** - The URL should be stored in `.notifications/config.json` which should be in `.gitignore`
- **Regenerate if compromised** - You can delete and recreate the webhook if the URL is exposed
- **URLs don't expire** - The webhook remains active until you delete it

## Troubleshooting

### "Connectors" option not visible
Your organisation may have disabled connectors. Contact your IT administrator.

### Webhook created but messages don't appear
1. Verify the URL is complete (no truncation when copying)
2. Check the channel - messages may be in a different channel
3. Try the curl test above to isolate the issue

### "403 Forbidden" when posting
The webhook may have been deleted or the URL is incorrect. Recreate the webhook.

### Messages appear but look broken
Ensure you're sending valid JSON. For Adaptive Cards, use the templates in `references/teams-message-templates.json`.

## Next Steps

Once you have the webhook URL:

1. Run `/push-notifications setup`
2. Select "Microsoft Teams" when prompted
3. Paste the webhook URL
4. The skill will send a test message to verify it works

---

*Last updated: 2026-02-25*
