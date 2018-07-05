#!/usr/bin/env python3

import grpc

import validator_pb2
import validator_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

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

number_iterator = create_iterator()
for out in stub.Validate(number_iterator):
    print(out.value)
