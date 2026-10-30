def original(tool, due, desk):
    msg = 'Borrow, mend, repeat. '
    if desk == 'North':
        msg += tool + ' — return to North'
    else:
        msg += tool + ' — return to ' + desk
    msg += ' by '
    msg += due
    return msg

def step1(tool, due, desk):
    msg = 'Borrow, mend, repeat. '
    msg += tool + ' — return to ' + desk
    msg += ' by '
    msg += due
    return msg

def better(tool, due, desk):
    return f'Borrow, mend, repeat. {tool} — return to {desk} by {due}'

def worse(tool, due, desk):
    return f'{tool} — return to {desk} by {due}'

# Checks executed separately during preparation; see execution.md.
