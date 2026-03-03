# Hooks — Project Control Library

## Recommended Session Hooks

Add these to your `.claude/settings.json` to enable automatic session management:

### Session Start Hook
Runs when a new Claude Code session starts in this project.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 scripts/project-scanner.py --register 2>/dev/null; python3 scripts/port-manager.py --cleanup 2>/dev/null; echo 'Project control library initialized. Run /catalog view to see all available skills, commands, and agents.'"
          }
        ]
      }
    ]
  }
}
```

### Pre-Commit Hook
Validates that housekeeping was run before committing.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo ''"
          }
        ]
      }
    ]
  }
}
```

## How to Install

Copy the relevant hook configuration into your `.claude/settings.json` file, or use the `session-start-hook` skill to set it up automatically.
