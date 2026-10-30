I’d stop here. Two improvement rounds are complete and there is no extended budget. The current one-line formatter keeps the full output visible in one place; extracting constants, adding a template layer, or renaming parameters would add another change without evidence of a maintenance problem worth that cost.

Keep the implementation:

```python
def notice(tool, due, desk):
    return f'Borrow, mend, repeat. {tool} — return to {desk} by {due}'
```

Correctness by inspection: for the stated nonempty-string inputs, it inserts the supplied values without normalization and preserves the chosen wording and punctuation. Execution checks were not run; broader behavior and maintenance benefits remain unverified. No live project was edited.

Updated decision note:

- Retain “Borrow, mend, repeat.” because the prior note records the librarian’s deliberate choice. Preserve supplied names and dates exactly as the user requires.
- Retain the current formatter: its complete output is visible in one expression, and the two-round implementation budget is exhausted. No further improvement round is proposed now.
- Reopen wording only with a new librarian/user instruction; reopen formatting behavior only with an explicit revised input/output contract. The maps remain discussion aids, not acceptance criteria.
- If a future budget is authorized, first identify one concrete maintenance failure—such as duplicated notice text requiring synchronized edits—to establish whether another abstraction would help.
