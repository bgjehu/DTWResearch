__author__ = 'fullstackpug'
import multiprocessing as mp
import time

def seq(count):
    start_time = time.time()
    result = []
    for i in range(count):
        result.append(cube(i))
    print "seq --- time:{0:.4f}, result:{1}".format(time.time() - start_time, result)

def par(count):
    start_time = time.time()
    result = mp.Pool(processes=2).map(cube,range(count))
    print "par --- time:{0:.4f}, result:{1}".format(time.time() - start_time, result)

def cube(x):
    return x*x*x


count = 20
seq(count)
par(count)