import subprocess as sp
import queue
import threading

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

out_path = "hello.txt"
output_vcf = sp.Popen(["tail -f "+out_path], shell=True, stdout=sp.PIPE)
q = queue.Queue()
t = threading.Thread(target=enqueue_output, args=(output_vcf.stdout, q))

t.daemon = True # thread dies with the program
t.start()

while (True):
    try:
        line = q.get(timeout = 2)
    except queue.Empty:
        print('no output yet')
    else: # got line
        print(line)

