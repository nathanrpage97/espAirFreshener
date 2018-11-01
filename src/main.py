from machine import RTC
import machine
import utime as time
import constants
import motor_driver
from state import State
from network_controller import Network_Controller
from nucleo_controller import NucleoController
import request_handler

# Phases INIT, CHECK_SPRAY_BUTTON_PRESSED, CONNECT_NETWORK, GET_SERVER, CHECK_TO_SPRAY, SLEEP

# phase = 'INIT'

nc32 = NucleoController()
state = State(constants.STATE_FILE)


def init():
    """
    Called on start up. Locks nc32 from resetting. Determines wakeup reason
    """
    global state
    nc32.lock_reset()  # stop it from resetting if user presses spray button
    reset_reason = nc32.get_reset_reason()

    # if powering up reinitialize the state
    if reset_reason == 2:
        state.reinitialize()
    # provide the reset reason to the state
    # also indicate it didn't reach server yet
    state.update(dict(wakeup_reason=reset_reason, reached_server=False))

    return 'CONNECT_NETWORK'


def connect_network():
    global state
    net_controller = Network_Controller(constants.WIFI_ESSID, constants.WIFI_PASSWORD)
    return 'GET_SERVER' if net_controller.is_connected() else 'CHECK_TO_SPRAY'


def get_server():
    global state
    data = request_handler.get_server_info()
    if data is None:
        return 'UNREACHED_SERVER'
    state.update(data)
    return 'CHECK_TO_SPRAY'


def unreached_server():
    # if starting up re-powered
    nc32_time = nc32.get_clock_time()
    if not state.get('reached_server'):
        state.update(dict(current_time=state.get('current_time') + nc32_time*1000, wait_time=get_wait_time()))
    else:
        state.update(dict(wait_time=get_wait_time()))
    return check_to_spray()


def check_to_spray():
    global state
    # if starting up re-powered

    if state.get('current_time') + 5*1000 > state.get('last_spray_time') + state.get('interval') * 60 * 1000:
        motor_driver.spray()
        state.update(dict(
            wait_time=60,
            spray_now=False,
            last_spray_time=state.get('current_time')
        ))
        return 'SLEEP'
    elif state.get('spray_now'):
        motor_driver.spray()

    state.update(dict(
        wait_time=get_wait_time(),
        spray_now=False,
    ))
    return 'SLEEP'


def go_to_sleep():
    nc32.reset_clock_time(state.get('wait_time'))
    nc32.unlock_reset()
    machine.deepsleep()


phase_funcs = {
    'INIT': init,
    'CONNECT_NETWORK': connect_network,
    'GET_SERVER': get_server,
    'CHECK_TO_SPRAY': check_to_spray,
    'SLEEP': go_to_sleep
}


def check_spray_button_pressed():
    if nc32.check_spray_button_pressed():
        motor_driver.spray()


def loop(curr_phase):
    global phase_funcs
    print(phase)
    return phase_funcs[curr_phase]() if curr_phase in phase_funcs else 'SLEEP'


def get_wait_time():
    nc32_time = nc32.get_clock_time()
    wait_time = 60 - (nc32_time % 60)
    return wait_time if wait_time > 5 else 60


phase = 'INIT'
while True:
    next_phase = loop(phase)
    phase = next_phase
    check_spray_button_pressed()
