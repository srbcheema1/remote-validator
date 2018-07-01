#!/usr/bin/env python3

import argparse
import socket
import sys
import subprocess as sp
from util.enc_dec import enc, dec

class vcf_server:
    def __init__(self, port=12345):
        self.port = port
        self.hostname = socket.gethostname() # srb-pc
        self.host = "127.0.0.1"
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #dono
        self.soc.bind((self.host, self.port))
        self.soc.listen(5)

        self.socketlist = []
        print('ChatServer [ %s ] started at port [ %s ]' % (self.host, self.port))


    def print_data(self,data):
        print("got",end=' ')
        print(data)

    def endl(self,data):
        if(data[-1] == enc('\n')):
            return data
        else:
            return data + enc('\n')

    def verify_data(self,validator,data):
        print("verifying ")
        validator.stdin.write(self.endl(data))
        validator.stdin.flush()
        return validator.stdout.readline()

    def run(self):
        conn,addr=self.soc.accept()
        print('Connected to :',addr)
        validator = sp.Popen(["./tests/test_popen/even.out"], stdin=sp.PIPE,stdout=sp.PIPE)

        while True:
            if (validator.poll() == None): # is alive
                data=conn.recv(1024)
                if not data :
                    break
                self.print_data(data)
                reply = self.verify_data(validator,data)
                conn.sendall(reply)
            else:
                print("validation completes :)")
                break

        conn.close()


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port",default="12345", help="PORT number eg:- 12345")
    args = parser.parse_args()

    if(args.port):
        port = int(args.port)
    else:
        port = 12345

    remote_validator = vcf_server(port)
    remote_validator.run()
