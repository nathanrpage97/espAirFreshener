import utime
wakeup_time = 0

def init_time(time):
    wakeup_time = time

def get_time():
    return utime.time() + wakeup_time
