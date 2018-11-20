import time
from machine import Pin
from constants import MOTOR_DIR, MOTOR_PWM, SPRAY_TIME, PAUSE_TIME, OFF, ON

motor_pin_a = Pin(MOTOR_DIR, Pin.OUT, value=OFF)
motor_pin_b = Pin(MOTOR_PWM, Pin.OUT, value=OFF)


def spray():
    motor_pin_a.on()
    motor_pin_b.off()
    time.sleep(SPRAY_TIME)
    motor_pin_a.off()
    motor_pin_b.off()
    time.sleep(PAUSE_TIME)
    motor_pin_a.off()
    motor_pin_b.on()
    time.sleep(SPRAY_TIME)
    motor_pin_a.off()
    motor_pin_b.off()
