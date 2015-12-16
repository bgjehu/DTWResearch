__author__ = 'Jieyi Hu'


from Utilities import rand_test_case
from Utilities import find_similarity_in_sequential
from Utilities import find_similarity_in_parallel
import time
import multiprocessing

width = None
height = None
workload = None
captured = None
predefined = None

def find_similarity(i):
    find_similarity_in_sequential(captured, predefined[i],False)
    #time.sleep(.01)

def dtw_among_n_testcases(w, h, n, iteration, log):
    global width
    global height
    global workload
    global captured
    global predefined

    width = w
    height = h
    workload = n
    ts = 0
    tp = 0
    for i in range(iteration):
        captured = rand_test_case(width, height)
        predefined = [rand_test_case(width, height) for i in range(workload)]

        if log:
            print '----------------------'
        start_t = time.time()
        if log:
            print 'running sequential DTWs...'
        for i in range(workload):
             find_similarity(i)
        run_t = time.time() - start_t
        ts += run_t
        if log:
            print 'run in sequential for {0:.4f} seconds'.format(run_t)

        start_t = time.time()
        if log:
            print 'running parallel DTWs...'
        result = multiprocessing.Pool(processes=4).map(find_similarity, range(workload))
        run_t = time.time() - start_t
        tp += run_t
        if log:
            print 'run in parallel for {0:.4f} seconds'.format(run_t)
            print '----------------------'
            print
    #print 'sequential:{0:.4f}'.format(ts/iteration)
    #print 'parallel:{0:.4f}'.format(tp/iteration)
    print "{0},{1:.4f},{2:.4f}".format(n,ts/iteration,tp/iteration)

def batch_dtw(w,h,iteration,log,iterator):
    for i in iterator:
        #print "width:{0}, height:{1}, n_cases:{2}".format(w,h,i)
        dtw_among_n_testcases(w,h,i,iteration,log)
        #print

def dtw_between_two_testcases(width, height, iteration):
    ts_sum = 0
    tp_sum = 0
    for i in range(iteration):
        a = rand_test_case(width, height)
        b = rand_test_case(width, height)
        cs, ts = find_similarity_in_sequential(a,b,True)
        cp, tp =find_similarity_in_parallel(a,b,2,True)
        ts_sum += ts
        tp_sum += tp
    ts_avg = ts_sum / iteration
    tp_avg = tp_sum / iteration
    print
    print 'sequential: {0:.4f}'.format(ts_avg)
    print 'parallel: {0:.4f}'.format(tp_avg)

if __name__ == "__main__":
    dtw_among_n_testcases(3,100,4,10,True)