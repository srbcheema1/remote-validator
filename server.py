#!/usr/bin/env python3

import argparse
import grpc
import time
import subprocess as sp
import threading

from concurrent import futures

import validator_pb2
import validator_pb2_grpc

from util.enc_dec import enc, dec
from util.string_constants import vcf_path, out_path

class Sender(threading.Thread):
    def __init__(self, sender):
        threading.Thread.__init__(self)
        self.sender = sender
        self.alive = True

    def run(self):
        print("in run")
        # while (self.alive):
            # print("in run")
            # if (self.sender.poll() == None): # is alive
                # reply = self.sender.stdout.readline().decode('UTF-8')
                # response = validator_pb2.String()
                # response.value = reply
                # yield response
            # else:
                # print("validation completes :)")
                # break


class ValidatorServicer(validator_pb2_grpc.ValidatorServicer):
    def endl(self,data):
        if (type(data) is str):
            print("data type is string")
            data = enc(data)

        if(data[-1] == enc('\n')):
            return data
        else:
            return data + enc('\n')

    def Validate(self, request, context):

        # metadata is a list of arbitrary key-value pairs that the client can send along with a reques
        metadata = dict(context.invocation_metadata())
        print(metadata)

        # sp.Popen(["touch",out_path])
        # output_vcf = sp.Popen(["tail -f "+out_path], shell=True, stdout=sp.PIPE)
        # sender = Sender(output_vcf)
        # sender.start()

        validator = sp.Popen([vcf_path], stdin=sp.PIPE,stdout=sp.PIPE)
        for req in request:
            if (validator.poll() == None): # is alive
                print("got req ",req.value)
                # validator.stdin.write(enc(req.value))
                validator.stdin.write(self.endl(req.value))
                validator.stdin.flush()

                reply = validator.stdout.readline().decode('UTF-8')
                response = validator_pb2.String()
                response.value = reply
                yield response
            else:
                print("validation completes :)")
                break


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
