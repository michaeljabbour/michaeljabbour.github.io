# Workspace Conventions

This behavior defines how Amplifier instances use shared document storage for collaboration.

## Folder Structure

```
Amplifier/
├── inbox/           # Tasks waiting to be picked up
├── in-progress/     # Currently being worked on
├── completed/       # Finished work products
├── handoffs/        # Context for task handoffs
└── shared/          # Reusable artifacts, templates, data
```

## File Naming Convention

```
[date]_[type]_[description].[ext]

Examples:
- 2026-01-20_analysis_user-auth-review.md
- 2026-01-20_report_q4-metrics.json
- 2026-01-20_handoff_api-integration-context.md
```

## Workflow

### Starting Work
1. Check `inbox/` for task files
2. Move task to `in-progress/` (rename with your session prefix)
3. Post to Teams that you're starting

### Completing Work
1. Upload artifacts to `completed/`
2. Clean up `in-progress/`
3. Post summary to Teams with links

### Handing Off
1. Create handoff document in `handoffs/`
2. Include: context, progress, blockers, next steps
3. Post to `handoffs` channel with link

## Handoff Document Template

```markdown
# Handoff: [Task Name]

## Status
- Started: [timestamp]
- Progress: [percentage or description]
- Reason for handoff: [completion/timeout/blocked/error]

## Context
[What this task is about, why it matters]

## Work Done
- [x] Completed item 1
- [x] Completed item 2
- [ ] Pending item 3

## Key Files
- [link to artifact 1]
- [link to artifact 2]

## Next Steps
1. [What needs to happen next]
2. [And then this]

## Blockers/Notes
[Any issues the next instance should know about]
```

## Best Practices

1. **Atomic uploads** - One logical unit per file
2. **Self-documenting names** - File name should explain content
3. **Clean as you go** - Remove temporary files
4. **Version with dates** - Don't overwrite, append dates
5. **Link in channels** - Always post document links to channels
