from constants import RESET_POWER

import nucleo_controller
import motor_driver
import state
import clock_controller
import request_handler
import network_controller

# controllers to handle
def init():
    """
    Called on start up. Locks nucleo_controller from resetting. Determines wakeup reason
    """
    reset_reason = nucleo_controller.get_reset_reason()

    # if powering up reinitialize the state
    if reset_reason == RESET_POWER:
        state.reinitialize()
    # provide the reset reason to the state
    state.update(dict(wakeup_reason=reset_reason))
    # set up the time from the board
    clock_controller.init_time(c32.get_clock_time())
    return 'CONNECT_NETWORK'


def connect_network():
    """
    Connect to the network
    """
    return 'GET_SERVER' if network_controller.connect() else 'CHECK_TO_SPRAY'


def get_server():
    """
    Get new server information if possible
    """
    data = request_handler.get_server_info()
    if data is not None:
        state.update(data)
    return 'CHECK_TO_SPRAY'


def check_to_spray():
    """
    See if server requested spray or past spray interval time
    """
    # check if within 10 seconds of next spray time
    if clock_controller.get_time() + 10 >= state.get('last_spray_time') + state.get('interval'):
        motor_driver.spray()
        state.update(dict(
            last_spray_time=clock_controller.get_time(),
            spray_now=False
        ))
    elif state.get('spray_now'):
        motor_driver.spray()
        state.update(dict(
            spray_now=False,
        ))
    return 'SLEEP'


def go_to_sleep():
    """
    Put the device to sleep for a specified number of seconds
    """
    wait_time = (clock_controller.get_time() - state.get('last_spray_time')) % 60
    # if more than 60 seconds to wait for interval,
    # and wait_time smaller than 20 seconds. Extend wait time
    next_spray_time = state.get('last_spray_time') + state.get('interval')
    next_wake_time = clock_controller.get_time() + wait_time
    if wait_time < 20 and  next_wake_time + 60 < next_spray_time:
        wait_time += 60
    nucleo_controller.reset_clock_time(wait_time)
    # it should die after reaching here
    while True: # spin lock to allow time for the nucleo to kill this processor
        pass


phase_funcs = {
    'INIT': init,
    'CONNECT_NETWORK': connect_network,
    'GET_SERVER': get_server,
    'CHECK_TO_SPRAY': check_to_spray,
    'SLEEP': go_to_sleep
}


def check_spray_button_pressed():
    """
    Check if the real spray button was pressed by the user
    """
    if nucleo_controller.check_spray_button_pressed():
        motor_driver.spray()


def loop(curr_phase):
    """
    Loop function for all the phases
    """
    global phase_funcs
    print(phase)
    return phase_funcs[curr_phase]() if curr_phase in phase_funcs else 'SLEEP'


phase = 'INIT'
while True:
    """
    Loop that iterates through the loop function and then checks if spray button pressed
    """
    next_phase = loop(phase)
    phase = next_phase
    check_spray_button_pressed()
