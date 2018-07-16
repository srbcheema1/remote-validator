import sys
with sys.stdin as f:
    while True:
        inp = f.read(5)
        if not inp:
            break
        print('got req',inp)
