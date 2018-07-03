#!/usr/bin/env python3

import argparse
import sys
import socket
import threading
from util.enc_dec import dec, enc

class Receiver(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        self.alive = True

    def print_data(self,data):
        print(dec(data))

    def run(self):
        while (self.alive):
            print("waiting . . .")
            data=self.conn.recv(1024)
            print("got . . .")
            self.print_data(data)
        self.conn.close()

class vcf_client:
    def __init__(self, host="127.0.0.1", port=12345):
        self.port = port
        self.hostname = socket.gethostname() # srb-pc
        self.host = host
        self.conn = self.create_connection()


    def get_input(self):
        try:
            data = input()
        except:
            data = "bye"
            print("exiting . . .")
            # sys.exit()
        return enc(data)

    def create_connection(self):
        new_conn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        new_conn.connect((self.host,self.port))
        return new_conn

    def endl(self,data):
        if(data[-1] == enc('\n')):
            return data
        else:
            return data + enc('\n')

    def run(self):
        receiver = Receiver(self.conn)
        receiver.start()

        while True:
            inp = self.get_input()
            if(dec(inp) == "bye"):
                print("sent all data")
                break
            print("sending " + dec(inp))
            self.conn.sendall(self.endl(inp))
            print("sent " + dec(inp))


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port",default="12345", help="PORT number eg:- 12345")
    parser.add_argument("-a", "--host",default="127.0.0.1", help="HOST ip adress eg:- 127.0.0.1")
    args = parser.parse_args()

    host = args.host
    port = int(args.port)

    client = vcf_client(host,port)
    client.create_connection()
    client.run()
