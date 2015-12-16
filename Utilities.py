__author__ = 'Jieyi Hu'

from random import randint
import math
import time
from multiprocessing.pool import ThreadPool
import multiprocessing

testcase1 = None
testcase2 = None
height = None
cost_table = None
similarity = None
diagonal_iterator = None



def rand_test_case(width, height):
    test_case = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(randint(-15,15))
        test_case.append(row)
    return test_case


def euclidean_distance(row1, row2):
    values = map(lambda x,y: math.pow(x - y, 2), row1, row2)
    return math.sqrt(reduce(lambda x,y:x+y, values))


def init_cost_table(height):
    table = []
    table.append([0] + [float("inf")] * (height))
    for i in range(height):
        row = [float("inf")] + [0] * height
        table.append(row)
    return table


def fill_cost_table_cell(i):
    #   get global vars
    global testcase1
    global testcase2
    global height
    global cost_table
    global similarity
    global diagonal_iterator

    #   fill_cell
    x = i
    y = diagonal_iterator + 1 - x
    cost = euclidean_distance(testcase1[x - 1], testcase2[y - 1]) + min(cost_table[x - 1][y], cost_table[x][y- 1], cost_table[x-1][y-1])
    cost_table[x][y] = cost
    if x == height or y == height:
        cellSimilarity = cost + abs(x - height) + abs(y - height)
        if cellSimilarity < similarity:
            similarity = cellSimilarity



def find_similarity_in_sequential(t1, t2, dolog):
    #   set global vars
    global testcase1
    global testcase2
    global height
    global cost_table
    global similarity
    testcase1 = t1
    testcase2 = t2
    height = len(testcase1)
    cost_table = init_cost_table(height)
    similarity = float('inf')

    #   mark start time
    start_time = time.time()

    #   actually DTW
    for i in range(1, height + 1):              #   go through cost table cells one by one and calculate their costs
        for j in range(1, height + 1):
            cost_table[i][j] = euclidean_distance(testcase1[i - 1], testcase2[j - 1]) + min(cost_table[i][j - 1], cost_table[i - 1][j], cost_table[i - 1][j - 1])
            if i == height or j == height:      #   find minimum cost on the fly among last column and row
                cellSimilarity = cost_table[i][j] + abs(i - height) + abs(j - height)
                if cellSimilarity < similarity:
                    similarity = cellSimilarity

    #   mark end time
    run_time = time.time() - start_time

    #   log
    if dolog:
        print "similarity:{0:.2f}, runtime:{1:.6f}".format(similarity, run_time)

    #   return
    return similarity, run_time


def find_similarity_in_parallel(t1, t2, processes, dolog):
    #   set global vars
    global testcase1
    global testcase2
    global height
    global cost_table
    global similarity
    global diagonal_iterator
    testcase1 = t1
    testcase2 = t2
    height = len(testcase1)
    cost_table = init_cost_table(height)
    similarity = float('inf')
    diagonal_iterator = 0

    #   mark start time
    start_time = time.time()

    #   actually DTW
    for i in range(1, 2*height):
        diagonal_iterator = i
        start_index = 1
        end_index = i + 1
        if i > height:
            start_index = 1 + i - height
            end_index = 1 + height
        iterator = range(start_index, end_index)
        work = ThreadPool(processes=processes).map(fill_cost_table_cell,iterator)
        #work = multiprocessing.Pool(processes=processes).map(fill_cost_table_cell,iterator)

    #   mark end time
    run_time = time.time() - start_time

    #   log
    if dolog:
        print "similarity:{0:.2f}, runtime:{1:.6f}".format(similarity, run_time)

    #   return
    return similarity, run_time