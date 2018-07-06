#!/usr/bin/env python3

import grpc
import threading

import validator_pb2 as message
import validator_pb2_grpc as rpc

# open a gRPC channel

port = 12321
channel = grpc.insecure_channel('localhost:'+str(port))
metadata = [('name', 'srb')]

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
        inp = input()
        inp = message.String(value=inp)
        yield inp

def receive_output():
    for note in stub.Get_result(message.Empty(),metadata=metadata):
        print(note.value)


threading.Thread(target=receive_output, daemon=True).start()

number_iterator = create_iterator()
stub.Validate(number_iterator,metadata=metadata)
