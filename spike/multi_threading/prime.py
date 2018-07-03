import threading


class PrimeNumber(threading.Thread):
  def __init__(self, number):
    threading.Thread.__init__(self)
    self.Number = int(number)

  def run(self):
    counter = 2
    while counter*counter <= self.Number:
        if self.Number % counter == 0:
            promptLock.acquire()
            if(prompt):print()
            print( "%d is not prime number" % ( self.Number) )
            if(prompt):print("number: ",end="")
            promptLock.release()
            return
        counter += 1
    promptLock.acquire()
    if(prompt): print()
    print ("%d is a prime number" % self.Number)

    #strange line
    debug_line = 1
    if(debug_line==1):
        if(prompt):print("number: ",end="")
    if(debug_line==2):
        if(prompt):print("number: ")

    promptLock.release()

threads = []
prompt=False
promptLock = threading.Lock()

def promptlocker():
    global prompt
    promptLock.acquire()
    prompt = not prompt
    promptLock.release()


while True:
    promptlocker()
    print("number: ",end="")
    input1 = int(input())
    promptlocker()
    if input1 < 1:
        break
    thread = PrimeNumber(input1)
    threads += [thread]
    thread.start()

for x in threads:
    x.join()
