import ujson
from constants import STATE_FILE, DEFAULT_STATE

state = None

def init():
    try:
        state = self.__read()
    except OSError:
        state = DEFAULT_STATE
        __store()

def reinitialize():
    # reinitialize but keep old interval
    old_interval = get('interval')
    update(DEFAULT_STATE)
    update(dict(interval=old_interval))

def update(new_state):
    for state_prop, val in new_state.items():
        state[state_prop] = val
    __store()

def get(state_prop):
    return state[state_prop] if state_prop in state else None

def __read():
    f = open(STATE_FILE, 'r')
    stored_state = ujson.loads(f.read())
    f.close()
    return stored_state

def __store():
    f = open(STATE_FILE, 'w')
    f.write(ujson.dumps(state))
    f.close()
