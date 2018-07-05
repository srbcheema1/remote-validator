import grpc

import calculator_pb2
import calculator_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = calculator_pb2_grpc.CalculatorStub(channel)

while(True):
    val = int(input())
    number = calculator_pb2.Number(value=val)
    response = stub.Even(number)
    print(response.value)
