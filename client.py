#!/usr/bin/env python3

import grpc
import sys
import threading
import time

import validator_pb2 as message
import validator_pb2_grpc as rpc

# open a gRPC channel

port = 12321
channel = grpc.insecure_channel('localhost:'+str(port))

try:
    # try a connection
    grpc.channel_ready_future(channel).result(timeout=10)
except grpc.FutureTimeoutError:
    sys.exit('Error connecting to server')
else:
    # create a stub (client)
    stub = rpc.ValidatorStub(channel)


def create_iterator():
    while(True):
        try:
            inp = input()
        except:
            yield message.String(value="bye")
            break
        inp = message.String(value=inp)
        yield inp

def receive_output():
    for note in stub.Get_result(message.Empty(),metadata=metadata):
        print(note.value)
        if(note.value == "bye"):
            break

def send_input():
    number_iterator = create_iterator()
    stub.Validate(number_iterator,metadata=metadata)

user_id = stub.Get_user_id(message.Empty())
user_id = user_id.value
metadata = [('user_id', str(user_id))]

threading.Thread(target=send_input, daemon=True).start()
receive_output()

