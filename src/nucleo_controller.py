import constants
from machine import Pin, I2C
# construct an I2C bus
i2c = I2C(scl=Pin(constants.I2C_SCL), sda=Pin(constants.I2C_SDA), freq=100000)

def put_to_sleep(seconds):
    """
    Puts the controller to sleep for specified # of seconds
    """
    return
    i2c.writeto(constants.NUCLEO_ADDRESS, constants.NUCLEO_COMMANDS['put_to_sleep']['command'].to_bytes(1, byteorder='big'))
    i2c.writeto(constants.NUCLEO_ADDRESS, seconds)
def get_reset_reason():
    """
    0 = Timer
    1 = Button Pressed
    2 = Re-powered whole device
    :return:
    """
    return 0
    i2c.writeto(constants.NUCLEO_ADDRESS, constants.NUCLEO_COMMANDS['get_reset_reason']['command'].to_bytes(1, byteorder='big'))
    return i2c.readfrom(constants.NUCLEO_ADDRESS, constants.NUCLEO_COMMANDS['get_reset_reason']['bytes'])

def get_clock_time():
    """
    Gives clock time in number of seconds
    """
    return 10
    i2c.writeto(constants.NUCLEO_ADDRESS, constants.NUCLEO_COMMANDS['get_clock_time']['command'].to_bytes(1, byteorder='big'))
    return i2c.readfrom(constants.NUCLEO_ADDRESS, constants.NUCLEO_COMMANDS['get_clock_time']['bytes'])

def check_spray_button_pressed():
    return False
    i2c.writeto(constants.NUCLEO_ADDRESS, constants.NUCLEO_COMMANDS['check_spray_button_pressed']['command'].to_bytes(2, byteorder='big'))
    return i2c.readfrom(constants.NUCLEO_ADDRESS, constants.NUCLEO_COMMANDS['check_spray_button_pressed']['bytes'])
