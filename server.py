#!/usr/bin/env python3

import socket
import sys
host="127.0.0.1"
port=12345

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(1)

def print_data(data):
    print("got",end=' ')
    print(data)


conn,addr=s.accept()
print('Connected by :',addr)
while True:
    data=conn.recv(1024)
    if not data : break
    print_data(data)
    conn.sendall(data+data)

conn.close()
