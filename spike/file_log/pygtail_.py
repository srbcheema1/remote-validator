from pygtail import Pygtail

while True:
    for line in Pygtail("my_file.txt"):
        print(line)
