from multiprocessing.pool import ThreadPool
import multiprocessing
import time

def seq(count):
    print "runing seq"
    start_time = time.time()
    result = []
    for i in range(count):
        result.append(cube(i))
    print "seq --- time:{0:.4f}".format(time.time() - start_time)
    #print "seq --- time:{0:.4f}, result:{1}".format(time.time() - start_time, result)

def par(count):
    print "runing par"
    start_time = time.time()
    result = ThreadPool(processes=4).map(cube,range(count))
    #result = multiprocessing.Pool(processes=4).map(cube,range(count))
    print "par --- time:{0:.4f}".format(time.time() - start_time)
    #print "par --- time:{0:.4f}, result:{1}".format(time.time() - start_time, result)

def cube(x):
    #time.sleep(.01)
    return x*x*x

if __name__ == "__main__":    
    count = 40000000
    seq(count)
    par(count)