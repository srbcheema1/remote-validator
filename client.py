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
        try:
            inp = input()
            if(int(inp) == 0):
                break
        except:
            print("exiting . . .")
            break
        inp = message.String(value=inp)
        yield inp
    yield message.String(value="0")

def receive_output():
    for note in stub.Get_result(message.Empty(),metadata=metadata):
        print(note.value)

def send_input():
    number_iterator = create_iterator()
    stub.Validate(number_iterator,metadata=metadata)

threading.Thread(target=send_input, daemon=True).start()
receive_output()
