import ujson

DEFAULT_STATE = dict(
    last_spray_time=0,   # gives the last time the device sprayed, ms since 1970
    interval=10,            # the interval in minutes to spray
    wait_time=60,           # how many seconds to recheck the server
    current_time=0,      # stores the current time, ms since 1970
    wakeup_reason=None,      # specifies the wake up reason for the device
    reached_server=False,
    spray_now=False
)


class State:

    def __init__(self, file):
        """
        Use file to read the state
        """
        self.file = file
        try:
            self.state = self.__read()
        except OSError:
            self.state = DEFAULT_STATE
            self.__store()

    def reinitialize(self):
        # reinitialize but keep old interval
        old_interval = self.get('interval')
        self.update(DEFAULT_STATE)
        self.update(dict(interval=old_interval))

    def update(self, newState):
        for state_prop, val in newState.items():
            self.state[state_prop] = val
        self.__store()

    def __read(self):
        f = open(self.file, 'r')
        stored_state = ujson.loads(f.read())
        f.close()
        return stored_state

    def __store(self):
        f = open(self.file, 'w')
        f.write(ujson.dumps(self.state))
        f.close()

    def get(self, state_prop):
        return self.state[state_prop] if state_prop in self.state else None
