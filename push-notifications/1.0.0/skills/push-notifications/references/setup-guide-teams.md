# Microsoft Teams Webhook Setup Guide

This guide walks you through creating an incoming webhook for Microsoft Teams using the **Workflows app** (the new method replacing the retired Connectors approach).

> **Note:** The old "Incoming Webhook" connector was retired on 31 December 2025. This guide uses the new Workflows-based approach.

## Prerequisites

- Microsoft Teams desktop or web app
- Permission to create workflows in your organisation (contact your IT admin if restricted)

## Step-by-Step Setup

### 1. Open Microsoft Teams

Launch Teams on desktop or navigate to [teams.microsoft.com](https://teams.microsoft.com) in your browser.

### 2. Navigate to the Target Channel

Go to the team and channel where you want to receive notifications.

**Recommendation:** Create a dedicated channel like "Claude Code Alerts" to keep notifications organised.

### 3. Open Workflows

1. Click the **three dots (...)** next to the channel name
2. Select **Workflows** from the dropdown menu

If you don't see "Workflows", your organisation may have restricted this feature. Contact your IT administrator.

### 4. Create a New Workflow

1. In the Workflows panel, click **Create a workflow** or search for **"Post to a channel when a webhook request is received"**
2. Select the **"Post to a channel when a webhook request is received"** template
3. Click **Next**

### 5. Configure the Workflow

1. **Name your workflow:** Enter a descriptive name like "Claude Code Notifications"
2. **Select the team:** Choose the team containing your target channel
3. **Select the channel:** Choose the channel for notifications
4. Click **Add workflow** or **Create**

### 6. Copy the Webhook URL

After creation, Teams displays the webhook URL. It looks like:

```
https://[tenant-id].ad.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/[workflow-id]/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=[signature]
```

The URL format may vary slightly by region, but will typically contain `powerplatform.com` or `logic.azure.com`.

**Important:**
- Click **Copy** to copy the full URL
- Save this URL securely - it's like a password for posting to your channel
- Anyone with this URL can send messages to your channel

### 7. Workflow is Now Active

Your webhook is ready to receive messages.

## Message Format

The Workflows webhook accepts a simpler JSON format than the old Adaptive Cards:

### Simple Text Message

```bash
curl -H "Content-Type: application/json" -d '{
  "type": "message",
  "attachments": [{
    "contentType": "application/vnd.microsoft.card.adaptive",
    "content": {
      "type": "AdaptiveCard",
      "version": "1.4",
      "body": [{
        "type": "TextBlock",
        "text": "Hello from Claude Code!",
        "wrap": true
      }]
    }
  }]
}' "YOUR_WEBHOOK_URL"
```

### With Title and Formatting

```bash
curl -H "Content-Type: application/json" -d '{
  "type": "message",
  "attachments": [{
    "contentType": "application/vnd.microsoft.card.adaptive",
    "content": {
      "type": "AdaptiveCard",
      "version": "1.4",
      "body": [
        {
          "type": "TextBlock",
          "text": "Build Complete",
          "weight": "Bolder",
          "size": "Medium"
        },
        {
          "type": "TextBlock",
          "text": "The deployment finished successfully.",
          "wrap": true
        }
      ]
    }
  }]
}' "YOUR_WEBHOOK_URL"
```

## Testing the Webhook

Test with a simple curl command:

```bash
curl -H "Content-Type: application/json" -d '{"type":"message","attachments":[{"contentType":"application/vnd.microsoft.card.adaptive","content":{"type":"AdaptiveCard","version":"1.4","body":[{"type":"TextBlock","text":"Test notification from Claude Code!"}]}}]}' "YOUR_WEBHOOK_URL"
```

If successful, you'll see the message appear in your Teams channel.

## Security Considerations

- **Keep the URL private** - Treat it like a password
- **Don't commit to git** - The URL should be stored in `.notifications/config.json` which should be in `.gitignore`
- **Delete workflow if compromised** - You can delete and recreate the workflow if the URL is exposed
- **URLs include a signature** - The `sig` parameter provides some protection

## Managing Your Workflow

To edit or delete your webhook:

1. In Teams, click the **Apps** icon in the sidebar
2. Search for and open **Workflows**
3. Find your workflow in the list
4. Click to edit settings or delete

## Troubleshooting

### "Workflows" option not visible
Your organisation may have disabled Power Automate/Workflows. Contact your IT administrator.

### "Post to a channel" template not found
1. Open the Workflows app directly from the Apps menu
2. Click **Create** and search for "webhook"
3. Select a template that posts to Teams

### "401 Unauthorized" or "403 Forbidden"
The workflow may have been deleted or the URL has expired. Recreate the workflow.

### Messages not appearing
1. Verify the URL is complete (the `sig` parameter is essential)
2. Check the channel - messages may be in a different channel
3. Ensure JSON is valid (use a JSON validator)
4. Check workflow run history in the Workflows app

### Workflow shows "Failed" in run history
1. Open the workflow run details
2. Check the error message
3. Common issues: invalid JSON, missing required fields

## Next Steps

Once you have the webhook URL:

1. Run `/push-notifications setup`
2. Select "Microsoft Teams" when prompted
3. Paste the webhook URL
4. The skill will send a test message to verify it works

---

*Last updated: 2026-02-25 (Updated for Workflows app - Connectors retired Dec 2025)*
