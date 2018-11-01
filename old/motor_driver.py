from machine import Pin
import uasyncio as asyncio
from uasyncio.synchro import Lock


MOTOR_DIR = 4 # specify the gpio pin of motor dir
# dont use pin 1, it seems to freeze up when doing so
MOTOR_PWM = 5 # specify the gpio pulse width value

SPRAY_TIME = 1 # timers for spraying duration
PAUSE_TIME = 0.2

OFF = 0
ON = 1

motor_pin_a = Pin(MOTOR_DIR, Pin.OUT, value=OFF)
motor_pin_b = Pin(MOTOR_PWM, Pin.OUT, value=OFF)


motor_lock = Lock()


async def spray():
    await motor_lock.acquire()
    motor_pin_a.on()
    motor_pin_b.off()
    await asyncio.sleep(SPRAY_TIME)
    motor_pin_a.off()
    motor_pin_b.off()
    await asyncio.sleep(PAUSE_TIME)
    motor_pin_a.off()
    motor_pin_b.on()
    await asyncio.sleep(SPRAY_TIME)
    motor_pin_a.off()
    motor_pin_b.off()
    motor_lock.release()
