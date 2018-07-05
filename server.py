#!/usr/bin/env python3

import grpc
from concurrent import futures
import time

import validator_pb2
import validator_pb2_grpc


class ValidatorServicer(validator_pb2_grpc.ValidatorServicer):
    def Validate(self, request, context):

        # metadata is a list of arbitrary key-value pairs that the client can send along with a reques
        metadata = dict(context.invocation_metadata())
        print(metadata)

        for req in request:
            val = int(req.value)
            if(val%2==0):
                response = validator_pb2.String()
                response.value = "even"
                yield response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_ValidatorServicer_to_server`
# to add the defined class to the server
validator_pb2_grpc.add_ValidatorServicer_to_server(ValidatorServicer(), server)

print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
