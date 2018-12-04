import machine
import time
import ujson

import socket_handler
import constants
# import nucleo_controller
import motor_driver
import state
import clock_controller
import request_handler
import network_controller

import esp
print(esp.check_fw())

# controllers to handle
def init():
    """
    Called on start up. Locks nucleo_controller from resetting. Determines wakeup reason
    """
    return 'CONNECT_NETWORK'


def connect_network():
    """
    Connect to the network
    """
    if network_controller.connect()
        return 'GET_SERVER'
    state.update(dict(current_time=state.get('current_time') + state.get('sleep_time')))
    return CHECK_TO_SPRAY


def get_server():
    """
    Get new server information if possible
    """
    data = request_handler.get_server_info()
    print('Received:', data)
    if data is not None:
        state.update(data)
    else:
        state.update(dict(current_time=state.get('current_time') + state.get('sleep_time')))
    clock_controller.init_time(state.get('current_time'))
    return 'CHECK_TO_SPRAY'


def check_to_spray():
    """
    See if server requested spray or past spray interval time
    """
    if not state.get('spray_on') or state.get('last_spray_time') == -1:
        # move last spray time forward so it wont instantly spray after turning spray interval back on
        state.update(dict(last_spray_time=clock_controller.get_time()))
    elif state.get('spray_on') and clock_controller.get_time() + 5 >= state.get('last_spray_time') + state.get('interval'):
        socket_handler.send('spraying interval')
        motor_driver.spray()
        state.update(dict(
            last_spray_time=clock_controller.get_time(),
        ))
    if state.get('spray_now'):
        socket_handler.send('spraying now')
        motor_driver.spray()
        state.update(dict(
            spray_now=False,
        ))
    return 'SLEEP'


def go_to_sleep():
    """
    Put the device to sleep for a specified number of seconds
    """
    next_spray_time = state.get('last_spray_time') + state.get('interval')
    sleep_time = max(min(60, next_spray_time - clock_controller.get_time()), 5)
    state.update(dict(sleep_time=sleep_time))


    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after sleep_time seconds (waking the device)
    print("Sleeping for ", sleep_time)
    rtc.alarm(rtc.ALARM0, sleep_time * 1000)

    print("Going to Sleep")
    # put the device to sleep
    machine.deepsleep()


    # shouldn't even reach here
    return 'FINISHED'

phase_funcs = {
    'INIT': init,
    'CONNECT_NETWORK': connect_network,
    'GET_SERVER': get_server,
    'CHECK_TO_SPRAY': check_to_spray,
    'SLEEP': go_to_sleep
}



def loop(curr_phase):
    """
    Loop function for all the phases
    """
    global phase_funcs
    socket_handler.send(phase)
    socket_handler.send(state.state_string())
    return phase_funcs[curr_phase]() if curr_phase in phase_funcs else 'SLEEP'



phase = 'INIT'
while True:
    """
    Loop that iterates through the loop function and then checks if spray button pressed
    """
    if phase == 'FINISHED':
        break
    next_phase = loop(phase)
    phase = next_phase

print('FINISHED')
