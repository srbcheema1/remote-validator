import subprocess as sp

from util.enc_dec import enc, dec
def get_input():
    inp = input() + "\n"
    return enc(inp)


b = sp.Popen(["./even.out"], stdin=sp.PIPE,stdout=sp.PIPE)

while (True):
    if (b.poll() == None):
        data = get_input()
        b.stdin.write(data)
        b.stdin.flush()
        print(b.stdout.readline())
    else:
        print("validation completes :)")
        break

# a = b.communicate('3\n3\n4\n3\n'.encode('UTF-8'))[0]
# print(a)
