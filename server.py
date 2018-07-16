#!/usr/bin/env python3

import argparse
import grpc
import queue
import time
import subprocess as sp
import threading

from concurrent import futures
from random import randint

import validator_pb2 as message
import validator_pb2_grpc as rpc

from util.enc_dec import enc, dec
from util.string_constants import vcf_path, end_of_report_neg, end_of_report
from util.defaults import default_port, default_ip
from util.files import get_files_in_dir, clean_folder, del_folder, verify_file

class ValidatorServicer(rpc.ValidatorServicer):
    def __init__(self):
        self.alive = True
        self.get_res_alive = False
        self.validator = None
        self.output_dir = "./bin/out/"
        self.user_list = {}

    def endl(self,data):
        if (type(data) is str):
            data = enc(data)

        if (len(data) == 0):
            return data

        if(data[-1] == enc('\n')):
            return data
        else:
            return data + enc('\n')

    def make_reply(self, reply):
        reply = dec(reply)
        if(len(reply) == 0):
            return reply

        if(reply[-1]=='\n'):
            return reply[:-1]


    def Validate(self, request, context):
        metadata = dict(context.invocation_metadata())
        print(metadata)

        self.output_dir = self.output_dir + metadata['user_id'] + '/'
        clean_folder(self.output_dir)
        self.validator = sp.Popen([vcf_path,"-r","text","-o",self.output_dir], stdin=sp.PIPE)

        for req in request:
            if (self.validator.poll() == None): # is alive
                print("got req ",req.value)
                if(req.value == b'bye'):
                    # time.sleep(5) # time to let output code run
                    print('EOF to validator')
                    self.validator.stdin.close()
                    break
                self.validator.stdin.write(req.value)
                self.validator.stdin.flush()

            else:
                print("Process Finished")
                break

        return message.Empty()

    def Get_result(self, request, context):
        while (self.validator == None): # yet not started
            time.sleep(0.1) # time to let validator start else it will pick up old file

        while (len(get_files_in_dir(self.output_dir)) == 0):
            time.sleep(0.1) # time to let file to be created else next statement will get no file
            output_file = get_files_in_dir(self.output_dir)

        output_file = get_files_in_dir(self.output_dir)[0]
        output_file_path = self.output_dir + output_file

        output_vcf = sp.Popen(["tail -n999999 -f "+output_file_path], shell=True, stdout=sp.PIPE)
        q = queue.Queue()
        t = threading.Thread(target=self.enqueue_output, args=(output_vcf.stdout, q))
        t.start()

        # cannot terminate on validator.poll as it will exit eariler
        # while (self.validator.poll() == None): # validator alive
        while (self.validator.poll() == None or True): # validator alive or dead we will continue
            try:
                reply = q.get(timeout = 0)
            except queue.Empty: # no line yet
                pass
            else: # got line
                reply = self.make_reply(reply)
                response = message.String()
                response.value = reply
                yield response
                if(reply == end_of_report or reply == end_of_report_neg):
                    break

        print("Result completes :)")
        clean_folder(self.output_dir)
        del_folder(self.output_dir)
        response = message.String()
        response.value = "bye"
        yield response

    def enqueue_output(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    def Get_user_id(self, request, context):
        user_id = randint(1,1000)
        while (user_id in self.user_list):
            user_id = randint(1,1000)
        self.user_list[user_id] = str(user_id)
        response = message.Number()
        response.value = user_id
        return response


if (__name__=="__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port",default=default_port, help="PORT number eg:- 12321")
    parser.add_argument("-i", "--ip",default=default_ip, help="IP adress eg:- 127.0.0.1")
    args = parser.parse_args()

    ip = args.ip
    port = int(args.port)

    # Create Server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_ValidatorServicer_to_server(ValidatorServicer(), server)
    server.add_insecure_port(ip+':'+ str(port))
    print('Starting server on ' + ip + ' Listening on port ' + str(port) + '.')
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
