#!/usr/bin/env python3

import argparse
import grpc
import sys
import threading
import time

import validator_pb2 as message
import validator_pb2_grpc as rpc

from util.string_constants import default_ip, default_port, connection_timeout

# open a gRPC channel

class User:
    def __init__(self, ip=default_ip, port=default_port):
        self.input_iterator = self.create_iterator()
        self.user_id = None
        self.metadata = None
        self.stub = None
        self.is_connected = False
        self.ip = ip
        self.port = port

    def create_connection(self):
        channel = grpc.insecure_channel(self.ip+':'+str(self.port))
        try:
            # try a connection
            grpc.channel_ready_future(channel).result(timeout=connection_timeout)
        except grpc.FutureTimeoutError:
            sys.exit('Error connecting to server')
        else:
            # create a stub (client)
            self.stub = rpc.ValidatorStub(channel)

    def get_user_id(self):
        user_id = self.stub.Get_user_id(message.Empty())
        self.user_id = user_id.value
        self.metadata = [('user_id', str(self.user_id))]

    def create_iterator(self):
        while(True):
            try:
                inp = input()
            except:
                yield message.String(value="bye")
                break
            inp = message.String(value=inp)
            yield inp

    def receive_output(self):
        for note in self.stub.Get_result(message.Empty(),metadata=self.metadata):
            if(note.value == "bye"):
                break
            print(note.value)

    def send_input(self):
        self.stub.Validate(self.input_iterator,metadata=self.metadata)

    def validate(self):
        if (self.stub == None):
            user.create_connection()
        if (self.user_id == None):
            self.get_user_id()

        threading.Thread(target=self.send_input, daemon=True).start()
        self.receive_output()

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port",default=default_port, help="PORT number eg:- 12345")
    parser.add_argument("-i", "--ip",default=default_ip, help="IP adress eg:- 127.0.0.1")
    args = parser.parse_args()

    ip = args.ip
    port = int(args.port)

    user = User(ip, port)
    user.validate()
