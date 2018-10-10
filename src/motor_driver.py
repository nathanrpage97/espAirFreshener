import time
from machine import Pin

MOTOR_DIR = 0 # specify the gpio pin of motor dir
# dont use pin 1, it seems to freeze up when doing so
MOTOR_PWM = 2 # specify the gpio pulse width value

SPRAY_TIME = 1 # timers for spraying duration
PAUSE_TIME = 0.2

SPRAY_RELEASE = 0 # specify the direction to spray
SPRAY_PUSH = 1

OFF = 0
ON = 1

motor_dir_pin = Pin(MOTOR_DIR, Pin.OUT, value=SPRAY_RELEASE) # create motor direction pin
motor_pwm_pin = Pin(MOTOR_PWM, Pin.OUT, value=OFF) # create motor pulse width modulation


def spray():
    motor_dir_pin.value(SPRAY_PUSH) # forward direction
    motor_pwm_pin.value(ON) # turn spray on
    time.sleep(SPRAY_TIME) # let it push down
    motor_pwm_pin.value(OFF) # stop spray
    time.sleep(PAUSE_TIME)
    motor_dir_pin.value(SPRAY_RELEASE) # forward direction
    motor_pwm_pin.value(ON)
    time.sleep(SPRAY_TIME)
    motor_pwm_pin.value(OFF)
