import ujson
import constants

state = {}

def reinitialize():
    old_interval = get('interval')
    old_spray_on = get('spray_on')
    update(constants.DEFAULT_STATE)
    update(dict(interval=old_interval, spray_on=old_spray_on))

def update(new_state):
    global state
    for state_prop, val in new_state.items():
        state[state_prop] = val
    __store()

def get(state_prop):
    global state
    return state[state_prop] if state_prop in state else None

def __read():
    try:
        f = open(constants.STATE_FILE, 'r')
        file_data = f.read()
        print(file_data)
        stored_state = ujson.loads(file_data)
        f.close()
        return stored_state
    except:
        print("ERROR READING FILE")
        return constants.DEFAULT_STATE

def __store():
    global state
    f = open(constants.STATE_FILE, 'w')
    f.write(ujson.dumps(state))
    f.close()

def print_state():
    print(state)

def state_string():
    return ujson.dumps(state)

state = __read()
