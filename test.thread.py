import time
import multiprocessing
from threading import Thread

print multiprocessing.cpu_count()
def myfunc(i):
    print "sleeping 5 sec from thread %d" % i
    time.sleep(5)
    print "finished sleeping from thread %d" % i

for i in range(multiprocessing.cpu_count()):
    t = Thread(target=myfunc, args=(i,))
    t.start()