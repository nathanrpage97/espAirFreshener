import os
import network
import machine
import motor_driver
import esp
import ure
import time
import urequests
import constants
from state import State
from network_controller import Network_Controller
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
    process_controls.unlock_reset()
    return 'CHECK_SPRAY_BUTTON_PRESSED'

def check_spray_button_pressed():
    # have to determine way to detect reset type was for button spray
    print(machine.Pin(2, machine.Pin.IN).value())
    if machine.reset_cause() == machine.HARD_RESET: # user pressed the spray button


        motor_driver.spray()
        state.update(dict(button_pressed=True))
    return 'CONNECT_NETWORK'

def connect_network():
    global state
    net_controller = Network_Controller(constants.WIFI_ESSID, constants.WIFI_PASSWORD)
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

phase_funcs = {
    'INIT': init,
    'CHECK_SPRAY_BUTTON_PRESSED': check_spray_button_pressed,
    'CONNECT_NETWORK': connect_network,
    'GET_SERVER': get_server,
    'CHECK_TO_SPRAY': check_to_spray
}

def loop(phase):
    global phase_funcs
    print(phase)
    return phase_funcs[phase]() if phase in phase_funcs else 'SLEEP'

phase = 'INIT'
while phase != 'SLEEP':
    next_phase = loop(phase)
    phase = next_phase

process_controls.deepsleep(state.get('wait_time'))
