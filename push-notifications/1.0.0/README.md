# Push Notifications Skill

Send push notifications via Microsoft Teams and macOS desktop when workflows complete, errors occur, or attention is needed.

## Features

- **Microsoft Teams** - Rich Adaptive Card notifications via incoming webhook
- **Desktop (macOS)** - Native notifications via terminal-notifier
- **Five notification types** - success, error, warning, info, attention
- **Integration ready** - Other skills can trigger notifications on completion
- **Persistent configuration** - Setup once, use everywhere

## Quick Start

```
/push-notifications setup      # First-time configuration
/push-notifications test       # Verify both channels work
/push-notifications "Done!"    # Send a notification
```

## Notification Types

| Type | Icon | Use When |
|------|------|----------|
| success | ✓ | Task completed |
| error | ✗ | Task failed |
| warning | ⚠ | Completed with issues |
| info | ℹ | General update |
| attention | 👁 | Input needed |

## Commands

| Command | Description |
|---------|-------------|
| `setup` | Configure notification channels |
| `test` | Send test to all channels |
| `status` | Show config and statistics |
| `send [msg]` | Send notification |
| `teams [msg]` | Teams only |
| `desktop [msg]` | Desktop only |

## Setup Requirements

### Microsoft Teams
- Create an incoming webhook in your Teams channel
- See `skills/push-notifications/references/setup-guide-teams.md`

### Desktop (macOS)
- Install terminal-notifier: `brew install terminal-notifier`
- See `skills/push-notifications/references/setup-guide-desktop.md`

## Configuration

Configuration is stored in `.notifications/config.json` (created on first setup).

## Integration with Other Skills

Other skills can trigger notifications when they complete:

- `beam-selling` → "BEAM engagement updated"
- `tender-assessment` → "Assessment complete - N shortlisted"
- `b2b-research-agent` → "Dossier ready"

## Files

```
push-notifications/1.0.0/
├── README.md                          # This file
├── .claude-plugin/
│   └── plugin.json                    # Skill metadata
└── skills/push-notifications/
    ├── SKILL.md                       # Main skill instructions
    └── references/
        ├── config-template.json       # Configuration schema
        ├── teams-message-templates.json  # Adaptive Card templates
        ├── setup-guide-teams.md       # Teams webhook setup
        └── setup-guide-desktop.md     # Desktop notification setup
```

## Version

1.0.0

## Author

SAS-AM

## Licence

MIT
