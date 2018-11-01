import ujson

DEFAULT_STATE = dict(
    last_spray_time=0,
    interval=1,
    ticks=-1,
    last_wake_time=0,
    wait_time=60
)


class State:
    def __init__(self, file):
        """
        Initialize the state object
        :param file: file to store it too
        """
        self.file = file
        try:
            self.state = self.__read()
        except OSError:
            self.state = DEFAULT_STATE
            self.__store()

    def update(self, new_state):
        """
        Update the state
        :param new_state:
        :return: None
        """
        for state_prop, val in new_state.items():
            self.state[state_prop] = val
        self.__store()

    def __read(self):
        """
        Read the state from file
        :return: state stored in the file
        """
        f = open(self.file, 'r')
        stored_state = ujson.loads(f.read())
        f.close()
        return stored_state

    def __store(self):
        """
        Store the state in file
        :return:
        """
        f = open(self.file, 'w')
        f.write(ujson.dumps(self.state))
        f.close()

    def get(self, state_prop):
        """
        Get specified property from state
        :param state_prop: key of property to get
        :return: value of property or None if it doesn't exist
        """
        return self.state[state_prop] if state_prop in self.state else None
