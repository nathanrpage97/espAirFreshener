from machine import Pin, I2C
# construct an I2C bus
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

def put_to_sleep(seconds):
    """
    Puts the controller to sleep for specified # of seconds
    """
    i2c.writeto(NUCLEO_ADDRESS, NUCLEO_COMMANDS['put_to_sleep']['command'].to_bytes(1, byteorder='big'))
    i2c.writeto(NUCLEO_ADDRESS, seconds)
def get_reset_reason():
    """
    0 = Timer
    1 = Button Pressed
    2 = Re-powered whole device
    :return:
    """
    i2c.writeto(NUCLEO_ADDRESS, NUCLEO_COMMANDS['get_reset_reason']['command'].to_bytes(1, byteorder='big'))
    return i2c.readfrom(NUCLEO_ADDRESS, NUCLEO_COMMANDS['get_reset_reason']['bytes'])

def get_clock_time():
    """
    Gives clock time in number of seconds
    """
    i2c.writeto(NUCLEO_ADDRESS, NUCLEO_COMMANDS['get_clock_time']['command'].to_bytes(1, byteorder='big'))
    return i2c.readfrom(NUCLEO_ADDRESS, NUCLEO_COMMANDS['get_clock_time']['bytes'])

def check_spray_button_pressed():
    i2c.writeto(NUCLEO_ADDRESS, NUCLEO_COMMANDS['check_spray_button_pressed']['command'].to_bytes(2, byteorder='big'))
    return i2c.readfrom(NUCLEO_ADDRESS, NUCLEO_COMMANDS['check_spray_button_pressed']['bytes'])
