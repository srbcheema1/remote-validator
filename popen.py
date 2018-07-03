#!/usr/bin/env python3

import subprocess as sp

from util.enc_dec import enc, dec
from util.string_constants import vcf_path

def get_input():
    inp = input() + "\n"
    return enc(inp)

b = sp.Popen([vcf_path], stdin=sp.PIPE, stdout=sp.PIPE)

while (True):
    if (b.poll() == None):
        data = get_input()
        b.stdin.write(data)
        b.stdin.flush()
    else:
        print("validation completes :)")
        break
