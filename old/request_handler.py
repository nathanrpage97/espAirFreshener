import urequests
import ure
g_getTimeSearch = ure.compile('\"currentFileTime\"\:(\d+)')

# def get_time():
#     global g_getTimeSearch
#     print('getting time')
#     curr_time = 0
#     try:
#         while not curr_time:
#
#             try:
#                 curr_time_data = urequests.get('http://worldclockapi.com/api/json/utc/now')
#                 print(curr_time_data.text)
#                 currTimeMatch = g_getTimeSearch.search(curr_time_data.text)
#             except:
#                 currTimeMatch = None
#             if currTimeMatch is not None:
#                 # get time in seconds since 1601 (look up filetime for more information)
#                 curr_time = int(currTimeMatch.group(1))/int(1e7)
#                 break
#     except:
#         curr_time = 20
#     return curr_time

def get_server_info():
    print('getting server info')
    # server_info = ''
    # while server_info == '':
    #     # server_info = connection.http_get('http://worldclockapi.com/api/json/utc/now')
    #     server_info = dict(interval=1, spray_now=False)  # until we develop the server
    #     if server_info != '':
    #         break
    #     time.sleep(0.2)
    return dict(interval=1, spray_now=False, current_time=453452345235)
