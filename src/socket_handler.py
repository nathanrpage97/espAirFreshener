import socket


s = socket.socket()
s.connect(('172.20.10.2', 65430))

def send(data):
    s.send(bytes(data, 'utf-8'))
