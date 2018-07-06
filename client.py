#!/usr/bin/env python3

import grpc

import validator_pb2
import validator_pb2_grpc

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
    stub = validator_pb2_grpc.ValidatorStub(channel)


def create_iterator():
    while(True):
        inp = input()
        number = validator_pb2.String(value=inp)
        yield number

metadata = [('ip', '127.0.0.1')]
number_iterator = create_iterator()
for out in stub.Validate(number_iterator,metadata=metadata):
    print(out.value)
