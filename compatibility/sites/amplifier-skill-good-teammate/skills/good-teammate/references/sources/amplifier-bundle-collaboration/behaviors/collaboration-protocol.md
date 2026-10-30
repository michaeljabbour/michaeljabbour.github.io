# Collaboration Protocol

This behavior defines how Amplifier instances coordinate work through collaboration platforms.

## Communication Channels

| Channel | Purpose | When to Use |
|---------|---------|-------------|
| `general` | Status updates, completions | After completing significant work |
| `alerts` | Urgent issues, blockers | When encountering errors or needing help |
| `handoffs` | Task delegation, coordination | When passing work to another instance |

## Message Formats

### Status Update
```python
collab_channels(
    operation="post",
    channel_name="general",
    title="✅ Task Complete",
    message="**Task:** [description]\n**Result:** [outcome]\n**Artifacts:** [links if any]"
)
```

### Alert
```python
collab_channels(
    operation="post",
    channel_name="alerts",
    title="🚨 Alert: [type]",
    message="**Issue:** [description]\n**Context:** [what was happening]\n**Need:** [what help is needed]"
)
```

### Handoff
```python
collab_channels(
    operation="post",
    channel_name="handoffs",
    title="🔄 Handoff: [task name]",
    message="**Task:** [description]\n**Context:** [relevant background]\n**Files:** [document links]\n**Next Steps:** [what the receiving instance should do]"
)
```

## Coordination Patterns

### 1. Claim-Work Pattern
Before starting significant work:
1. Check `handoffs` channel for unclaimed tasks
2. Post a "claiming" message with your session ID
3. Proceed with work
4. Post completion to `general`

### 2. Escalation Pattern
When stuck or encountering issues:
1. Post to `alerts` with details
2. Upload relevant context to shared documents
3. Include links in the alert message
4. Another instance can pick up and help

### 3. Artifact Sharing Pattern
For work products that others might need:
1. Upload to shared documents: `Amplifier/[date]/`
2. Post summary to `general` with link
3. Include metadata: what it is, why it matters, how to use it

## Session Identification

Always include your session context in handoff messages:
- Session ID (for tracing)
- What you were working on
- Why you're handing off (completion, timeout, error)

## Best Practices

1. **Be concise** - Channel messages are summaries, details go in documents
2. **Link don't paste** - Upload files, share links
3. **Context is king** - Always explain the "why"
4. **Fail loudly** - Post to alerts immediately when stuck
5. **Complete the loop** - Always post completion status
