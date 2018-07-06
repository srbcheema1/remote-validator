import subprocess as sp

b = sp.Popen(["tail -f my_file.txt"], shell=True, stdout=sp.PIPE)

while (True):
    if (b.poll() == None):
        print(b.stdout.readline())
    else:
        print("validation completes :)")
        break

