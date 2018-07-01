#!/usr/bin/env python3

import socket
from util.enc_dec import dec, enc


def print_data(data):
    print(dec(data))

def get_input():
    data = input()
    return enc(data)

def create_connection():
    host="127.0.0.1"
    port=12345
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    return s

if (__name__ == "__main__"):
    s = create_connection()
    while True:
        inp = get_input()
        s.sendall(inp)
        data=s.recv(1024)
        print_data(data)

    s.close()
