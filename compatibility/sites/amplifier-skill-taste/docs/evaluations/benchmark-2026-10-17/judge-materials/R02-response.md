All three versions below preserve the librarian’s chosen line, “Borrow, mend, repeat.” They also preserve supplied tool names, desk names, and dates exactly, including case and whitespace.

Here, **taste** means how well the choices fit this neighborhood library’s purpose and voice. **Elegance** means how simply and clearly the code produces the required result. The assessments are illustrative judgments, not measured scores: a shorter function need not have better taste.

### Original

```python
def notice(tool, due, desk):
    msg = 'Borrow, mend, repeat. '
    if desk == 'North':
        msg += tool + ' — return to North'
    else:
        msg += tool + ' — return to ' + desk
    msg += ' by '
    msg += due
    return msg
```

| Taste | Elegance |
| --- | --- |
| Good fit: keeps the deliberate library voice and supplied details. | Clear but repetitive: the North branch produces the same text as the general branch; the closing phrase is assembled in small fragments. |

### Plausible worse version

This is a plausible attempt to make each case explicit. It preserves behavior, but duplicates the whole message and creates two places for future wording changes to drift apart.

```python
def notice(tool, due, desk):
    if desk == 'North':
        return (
            'Borrow, mend, repeat. '
            + tool
            + ' — return to North by '
            + due
        )
    else:
        return (
            'Borrow, mend, repeat. '
            + tool
            + ' — return to '
            + desk
            + ' by '
            + due
        )
```

| Taste | Elegance |
| --- | --- |
| Same good fit: the reader receives the same notice and the chosen line survives. | Lower: duplicated copy and message structure increase editing effort without adding useful behavior. |

### Better version

```python
def notice(tool, due, desk):
    return f'Borrow, mend, repeat. {tool} — return to {desk} by {due}'
```

| Taste | Elegance |
| --- | --- |
| Same good fit: preserves the librarian’s voice and the exact supplied details. | Higher: one readable message, no redundant branch, and no repeated copy to synchronize. |

The improvement is chiefly in elegance. There is no reason to rewrite a line the librarian deliberately selected just to demonstrate a change in taste.

### Small-step path

Expected path: **worse → original → remove the redundant branch → consolidate the message**. Taste stays steady; elegance improves as duplication disappears.

Starting from the original, the first useful edit is:

```python
def notice(tool, due, desk):
    msg = 'Borrow, mend, repeat. '
    msg += tool + ' — return to ' + desk
    msg += ' by '
    msg += due
    return msg
```

Then replace that assembly with the better version above. Each edit can be reviewed independently: first remove an unnecessary distinction, then simplify how the string is written. The worse version is a comparison, not a recommended intermediate change.

### Context for the next editor

The current contract is one string in this exact form:

```text
Borrow, mend, repeat. {tool} — return to {desk} by {due}
```

Inputs are nonempty strings. Preserve them verbatim: do not trim, capitalize, parse, or reformat names or dates. Keep the em dash and surrounding spaces. North currently has no special output behavior; removing its branch preserves the supplied code’s behavior. If North later needs different instructions, establish that requirement before adding a special case.

Suggested regression checks for the better version:

```python
assert notice('Hand drill', 'June 4', 'North') == (
    'Borrow, mend, repeat. Hand drill — return to North by June 4'
)
assert notice('Hand drill', 'June 4', 'South') == (
    'Borrow, mend, repeat. Hand drill — return to South by June 4'
)
assert notice(' McKay’s saw ', '04/06/2027', 'north') == (
    'Borrow, mend, repeat.  McKay’s saw  — return to north by 04/06/2027'
)
```

These checks are proposed, not executed here. No changes to the library’s actual code or messaging have been applied.
