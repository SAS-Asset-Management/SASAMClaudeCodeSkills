# Desktop Notifications Setup Guide

This guide covers setting up native desktop notifications for macOS, Linux, and Windows.

## macOS: terminal-notifier

### Installation

**Using Homebrew (recommended):**

```bash
brew install terminal-notifier
```

**Using MacPorts:**

```bash
sudo port install terminal-notifier
```

### Verification

Check installation:

```bash
which terminal-notifier
# Should output: /opt/homebrew/bin/terminal-notifier (Apple Silicon)
# Or: /usr/local/bin/terminal-notifier (Intel Mac)
```

### Test Notification

```bash
terminal-notifier -title "Test" -message "Notifications working!" -sound default
```

You should see a notification in the top-right corner of your screen.

### Grant Permissions

If notifications don't appear:

1. Open **System Preferences** > **Notifications**
2. Find **terminal-notifier** in the list
3. Enable **Allow Notifications**
4. Set alert style to **Alerts** or **Banners**

### Common Options

```bash
terminal-notifier \
  -title "Title Here" \
  -message "Message body" \
  -sound "default" \        # Or: Glass, Basso, Sosumi, Ping, etc.
  -group "claude-code" \    # Groups notifications (newer replaces older)
  -activate "com.apple.Terminal"  # Opens Terminal when clicked
```

**Sound options:** default, Basso, Blow, Bottle, Frog, Funk, Glass, Hero, Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink

---

## Linux: notify-send

### Installation

**Ubuntu/Debian:**

```bash
sudo apt install libnotify-bin
```

**Fedora:**

```bash
sudo dnf install libnotify
```

**Arch Linux:**

```bash
sudo pacman -S libnotify
```

### Verification

```bash
which notify-send
# Should output: /usr/bin/notify-send
```

### Test Notification

```bash
notify-send "Test" "Notifications working!"
```

### Common Options

```bash
notify-send "Title" "Message" \
  --urgency=normal \      # low, normal, critical
  --expire-time=5000 \    # milliseconds (0 = never expire)
  --icon=dialog-information  # or path to icon file
```

**Urgency levels:**
- `low` - Background info
- `normal` - Standard notification
- `critical` - Stays on screen until dismissed

---

## Windows: PowerShell Toast Notifications

### No Installation Required

Windows 10/11 includes toast notification support via PowerShell.

### Test Notification

Open PowerShell and run:

```powershell
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
$template.SelectNodes("//text[@id='1']")[0].AppendChild($template.CreateTextNode("Test"))
$template.SelectNodes("//text[@id='2']")[0].AppendChild($template.CreateTextNode("Notifications working!"))
$toast = [Windows.UI.Notifications.ToastNotification]::new($template)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Claude Code").Show($toast)
```

### Alternative: BurntToast Module

For more features, install the BurntToast PowerShell module:

```powershell
Install-Module -Name BurntToast
```

Then use:

```powershell
New-BurntToastNotification -Text "Title", "Message body"
```

---

## Cross-Platform Considerations

### Detecting Platform

The skill will auto-detect your platform:

```bash
# macOS
uname -s  # Returns "Darwin"

# Linux
uname -s  # Returns "Linux"

# Windows (in Git Bash or WSL)
uname -s  # Returns "MINGW64_NT-10.0" or "Linux" for WSL
```

### Fallback Behaviour

If desktop notifications are unavailable:
1. Teams notification is sent (if configured)
2. Message is printed to console as fallback
3. Error is logged but doesn't block workflow

---

## Troubleshooting

### macOS: Notifications not appearing

1. Check System Preferences > Notifications > terminal-notifier
2. Ensure "Allow Notifications" is enabled
3. Check Focus Mode isn't blocking notifications
4. Try: `killall NotificationCenter` then retry

### Linux: "No notification daemon running"

Install a notification daemon:

```bash
# Ubuntu/GNOME
sudo apt install notification-daemon

# For headless servers, notifications won't display
# Use Teams notifications instead
```

### Windows: "ToastNotificationManager not found"

Ensure you're running PowerShell 5.0+ on Windows 10/11. Older Windows versions don't support toast notifications natively.

---

## Next Steps

Once desktop notifications are working:

1. Run `/push-notifications setup`
2. Select "Desktop (macOS)" when prompted
3. The skill will verify terminal-notifier is installed
4. A test notification will be sent to confirm setup

---

*Last updated: 2026-02-25*
