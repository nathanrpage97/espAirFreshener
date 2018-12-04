import utime
wakeup_time = 0

def init_time(time):
    global wakeup_time
    wakeup_time = time

def get_time():
    global wakeup_time
    return utime.time() + wakeup_time
