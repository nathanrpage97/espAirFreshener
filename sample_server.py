from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import json
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print('Get Requested')
        self.send_response(200)
        self.end_headers()
        epoch_time = int(time.time())
        response = dict(current_time=epoch_time, interval=600, spray_now=True, spray_on=True)
        self.wfile.write(json.dumps(response).encode('utf-8'))


httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
