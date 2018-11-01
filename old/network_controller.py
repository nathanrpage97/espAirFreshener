import network
import uasyncio as asyncio

class NetworkController:
    def __init__(self, essid, password):
        self.wlan = network.WLAN(network.STA_IF)
        self.essid = essid
        self.password = password
        self.connect()

    def is_connected(self):
        return self.wlan.isconnected()

    async def connect(self):
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print('connecting to network...')
            self.wlan.connect(self.essid, self.password)
            for i in range(20):
                if self.wlan.isconnected():
                    break
                await asyncio.sleep(0.25)

            if self.wlan.isconnected():
                print('network config:', self.wlan.ifconfig())
            else:
                print('unable to connect')

