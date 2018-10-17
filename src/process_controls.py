import machine


reset_lock = machine.Pin(2, machine.Pin.OUT, value=1)
def deepsleep(duration):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # set RTC.ALARM0 to fire after duration seconds (waking the device)
    rtc.alarm(rtc.ALARM0, 1000 * duration)
    # put the device to sleep
    machine.deepsleep()

def lock_reset():
    reset_lock.on()  # on meaning turned high (so it cant reset)
def unlock_reset():
    reset_lock.off()
