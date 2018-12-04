import urequests
import ujson
import constants

def get_server_info():
    try:
        raw_server_info = urequests.get('http://172.20.10.2:8000/')
        print(raw_server_info)
        print("Server info:", raw_server_info.json())
        return raw_server_info.json()
    except:
        return None

# def get_server_info():
#     raw_server_info = urequests.get('http://172.20.10.6:8000/Downloads/filename.json')
#     print(raw_server_info)
#     print("Server info:", raw_server_info.json())
#     return raw_server_info.json()
