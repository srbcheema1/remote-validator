#!/usr/bin/env python3

import grpc

import calculator_pb2
import calculator_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

try:
    # try a connection
    grpc.channel_ready_future(channel).result(timeout=10)
except grpc.FutureTimeoutError:
    sys.exit('Error connecting to server')
else:
    # create a stub (client)
    stub = calculator_pb2_grpc.CalculatorStub(channel)


def create_iterator():
    while(True):
        inp = int(input())
        number = calculator_pb2.Number(value=inp)
        yield number

number_iterator = create_iterator()
for out in stub.Even(number_iterator):
    print(out.value)
