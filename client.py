#!/usr/bin/env python3

import socket

host="127.0.0.1"
port=12345

def print_data(data):
    print(data.decode("utf-8"))

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

while True:
    inp = input()
    s.sendall(inp.encode('UTF-8'))
    data=s.recv(1024)
    print_data(data)

s.close()

