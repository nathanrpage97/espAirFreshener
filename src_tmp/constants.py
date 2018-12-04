DEBUG = True


# network constants
WIFI_ESSID = 'iPhone'
WIFI_PASSWORD = '12345678'

# state constants
STATE_FILE = 'state.json'

DEFAULT_STATE = dict(
    last_spray_time=0,      # gives the last time the device sprayed (within its interval), seconds since last power up
    interval=600,            # the interval in seconds to spray
    wakeup_reason=None,     # specifies the wake up reason for the device
    spray_now=False,
    spray_on=True,
    current_time=0,
    sleep_time=0
)

# server constants
SERVER_URL = 'http://172.20.10.6:8000/Downloads/filename.json'

# i2c pins
I2C_SCL = 5 # clock pin
I2C_SDA = 4 # data pin

# nucelo constants
NUCLEO_ADDRESS = 0x3A

NUCLEO_COMMANDS = dict(
    put_to_sleep = dict(commmand=0),
    get_reset_reason = dict(command=1, bytes=4),
    get_clock_time = dict(command=2, bytes=8),
    check_spray_button_pressed = dict(command=3, bytes=4)
)

RESET_TIME = 0
RESET_BUTTON = 1
RESET_POWER = 2

# motor constants
MOTOR_DIR = 4 # specify the gpio pin of motor dir
# dont use pin 1, it seems to freeze up when doing so
MOTOR_PWM = 5 # specify the gpio pulse width value

SPRAY_TIME = 0.95 # timers for spraying duration
PAUSE_TIME = 0.1

OFF = 0
ON = 1
