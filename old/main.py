import uasyncio as asyncio
import motor_driver
import constants
from state import State
from network_controller import NetworkController
from nucleo_controller import NucleoController
import request_handler
import process_controls

# Phases INIT, CHECK_SPRAY_BUTTON_PRESSED, CONNECT_NETWORK, GET_SERVER, CHECK_TO_SPRAY, SLEEP

# phase = 'INIT'

state = None

def init():
    """
    Called on start up no matter what
    """
    global state
    state = State(constants.STATE_FILE)
    return 'CHECK_SPRAY_BUTTON_PRESSED'

def connect_network():
    global state
    net_controller = NetworkController(constants.WIFI_ESSID, constants.WIFI_PASSWORD)
    return 'GET_SERVER' if net_controller.is_connected() else 'CHECK_TO_SPRAY'

def get_server():
    global state
    process_controls.lock_reset()
    data = request_handler.get_server_info()
    if data is None:
        return 'ERROR'
    state.update(data)
    return 'CHECK_TO_SPRAY'

def check_to_spray():
    global state

    if state.get('button_pressed'):
        wait_time = max(60 - (int((state.get('last_spray_time') - state.get('current_time'))) % 60), 5)
        state.update(dict(spray_now=False, wait_time=wait_time))
    else:
        state.update(dict(ticks=state.get('ticks') + 1, wait_time=60))
        if state.get('ticks') >= state.get('interval'):
            motor_driver.spray()
            state.update(dict(
                ticks=0,
                spray_now=False,
                wait_time=60,
                last_spray_time=state.get('current_time')
            ))
        elif state.get('spray_now'):
            motor_driver.spray()
            state.update(dict(
                ticks=0,
                spray_now=False,
                wait_time=60,
                last_spray_time=state.get('current_time')
            ))
    process_controls.unlock_reset()
    return 'SLEEP'

def put_to_sleep():
    process_controls.deepsleep(state.get('wait_time'))

phase_funcs = {
    'INIT': init,
    'CHECK_SPRAY_BUTTON_PRESSED': check_spray_button_pressed,
    'CONNECT_NETWORK': connect_network,
    'GET_SERVER': get_server,
    'CHECK_TO_SPRAY': check_to_spray,
    'SLEEP': put_to_sleep
}


async def update(phase):
    global phase_funcs
    print(phase)
    return phase_funcs[phase]() if phase in phase_funcs else 'SLEEP'


async def button_press_check():
    NucleoController.check_spray_button_pressed()

phase = 'INIT'

while phase != 'SLEEP':
    next_phase = loop(phase)
    phase = next_phase


