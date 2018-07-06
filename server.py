#!/usr/bin/env python3

import argparse
import grpc
import queue
import time
import subprocess as sp
import threading

from concurrent import futures
from select import select

import validator_pb2 as message
import validator_pb2_grpc as rpc

from util.enc_dec import enc, dec
from util.string_constants import vcf_path, out_path

class ValidatorServicer(rpc.ValidatorServicer):
    def __init__(self):
        self.alive = True
        self.get_res_alive = False
        self.validator = None

    def endl(self,data):
        if (type(data) is str):
            data = enc(data)

        if(data[-1] == enc('\n')):
            return data
        else:
            return data + enc('\n')

    def Validate(self, request, context):
        # metadata is a list of arbitrary key-value pairs that the client can send along with a reques
        metadata = dict(context.invocation_metadata())
        print(metadata)


        self.validator = sp.Popen([vcf_path], stdin=sp.PIPE)
        for req in request:
            if (self.validator.poll() == None): # is alive
                print("got req ",req.value)
                if(req.value == "bye"):
                    # end the validator with EOF
                    self.validator.stdin.write(enc('^D'))
                    self.alive = False
                    break
                self.validator.stdin.write(self.endl(req.value))
                self.validator.stdin.flush()

            else:
                print("validation completes :)")
                break

        print("validator alive : ",end = "")
        print(self.validator.poll() == None)
        return message.Empty()

    def Get_result(self, request, context):
        sp.Popen(["touch",out_path])
        output_vcf = sp.Popen(["tail -f "+out_path], shell=True, stdout=sp.PIPE)
        q = queue.Queue()
        t = threading.Thread(target=self.enqueue_output, args=(output_vcf.stdout, q))
        t.start()

        while (self.validator.poll() == None): # validator alive
            try:
                reply = q.get(timeout = 0)
            except queue.Empty: # no line yet
                print('no output yet')
            else: # got line
                reply = dec(reply)
                print("reply : ",end='')
                print(reply)
                response = message.String()
                response.value = reply
                yield response

        print("Result completes :)")
        response = message.String()
        response.value = "bye"
        yield response

    def enqueue_output(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

if (__name__=="__main__"):
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # use the generated function `add_ValidatorServicer_to_server`
    # to add the defined class to the server
    rpc.add_ValidatorServicer_to_server(ValidatorServicer(), server)

    port=12321
    print('Starting server. Listening on port '+str(port)+'.')
    server.add_insecure_port('[::]:'+ str(port))
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
