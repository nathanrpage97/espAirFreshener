import ujson
DEFAULT_STATE = dict(
    last_spray_time=0,
    interval=1,
    ticks=-1,
    spray_now=False,
    button_pressed=False,
    wait_time=60,
    current_time=0
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
