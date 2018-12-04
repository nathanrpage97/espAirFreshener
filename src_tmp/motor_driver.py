import time
from machine import Pin
import constants

motor_pin_a = Pin(constants.MOTOR_DIR, Pin.OUT, value=constants.OFF)
motor_pin_b = Pin(constants.MOTOR_PWM, Pin.OUT, value=constants.OFF)


def spray():
    """
    Very basic spray algorithm. Spray down for select period of time then wait and then back up
    """
    print("--- SPRAYING NOW ---")
    motor_pin_a.on()
    motor_pin_b.off()
    time.sleep(constants.SPRAY_TIME)
    motor_pin_a.off()
    motor_pin_b.off()
    time.sleep(constants.PAUSE_TIME)
    motor_pin_a.off()
    motor_pin_b.on()
    time.sleep(constants.SPRAY_TIME)
    motor_pin_a.off()
    motor_pin_b.off()
