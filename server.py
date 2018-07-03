#!/usr/bin/env python3

import argparse
import socket
import subprocess as sp
import sys
import time
import threading

from util.enc_dec import enc, dec
from util.string_constants import vcf_path


looplock = threading.Lock()

class Sender(threading.Thread):
    def __init__(self, validator, conn):
        threading.Thread.__init__(self)
        self.validator = validator
        self.conn = conn
        self.alive = True
        self.can_start = False

    def run(self):
        while (not self.can_start):
            pass

        while (self.alive):
            looplock.acquire()
            if (self.validator.poll() == None): # is alive
                reply = self.validator.stdout.readline()
                self.conn.sendall(reply)
            else:
                print("validation completes :)")
                break
            looplock.release()

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
        print('Server [ %s ] started at port [ %s ]' % (self.host, self.port))


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

    def run(self):
        conn,addr=self.soc.accept()
        print('Connected to :',addr)
        validator = sp.Popen([vcf_path], stdin=sp.PIPE,stdout=sp.PIPE)
        sender = Sender(validator,conn)
        sender.start()

        while True:
            looplock.acquire()
            sender.can_start = True
            print("lock acquired")
            if (validator.poll() == None): # is alive
                data=conn.recv(1024)
                if not data :
                    sender.alive = False
                    break
                self.print_data(data)
                self.verify_data(validator,data)
            else:
                selder.alive = False
                print("validation completes :)")
                break
            if (validator.poll() != None): # is dead
                selder.alive = False
                break
            print("lock released")
            looplock.release()

        print("out of loop")
        time.sleep(1)
        conn.close()



if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port",default="12345", help="PORT number eg:- 12345")
    args = parser.parse_args()

    port = int(args.port)

    remote_validator = vcf_server(port)
    remote_validator.run()
