#!/usr/bin/env python3

import socket
import sys
import subprocess as sp
from util.enc_dec import enc, dec

host="127.0.0.1"
port=12345

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)

def print_data(data):
    print("got",end=' ')
    print(data)

def endl(data):
    if(data[-1] == enc('\n')):
        return data
    else:
        return data + enc('\n')

def verify_data(b,data):
    print("verifying ")
    b.stdin.write(endl(data))
    b.stdin.flush()
    return b.stdout.readline()

conn,addr=s.accept()
print('Connected by :',addr)
b = sp.Popen(["./tests/test_popen/even.out"], stdin=sp.PIPE,stdout=sp.PIPE)

while True:
    if (b.poll() == None):
        data=conn.recv(1024)
        if not data : break
        print_data(data)
        reply = verify_data(b,data)
        conn.sendall(reply)
    else:
        print("validation completes :)")
        break

conn.close()
