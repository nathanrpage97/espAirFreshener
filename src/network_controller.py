import network
import time
import constants

wlan = network.WLAN(network.STA_IF)

def is_connected(self):
    return wlan.isconnected()

def connect():
    try:
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect(constants.WIFI_ESSID, constants.WIFI_PASSWORD)
            for i in range(50):
                if wlan.isconnected():
                    break
                time.sleep(0.1)

            if wlan.isconnected():
                print('network config:', wlan.ifconfig())
                return True
            else:
                print('unable to connect')
                return False
        return True
    except:
        print("ERROR occurred in network")
        return False
