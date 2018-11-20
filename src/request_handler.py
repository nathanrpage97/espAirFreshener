import urequests
import ujson
from constants import SERVER_URL

def get_server_info():
    try:
        raw_server_info = urequests.get(SERVER_URL)
        return ujson.loads(raw_server_info)
    except:
        return None
    return dict(interval=1, spray_now=False)
