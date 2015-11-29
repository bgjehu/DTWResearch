__author__ = 'Jieyi Hu'

from random import randint
import math
import time
import multiprocessing as mp


def rand_test_case(width, height):
    test_case = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(randint(-15,15))
        test_case.append(row)
    return test_case


def euclidean_dist(row1, row2):
    '''
    sum = 0
    for i in range(len(row1)):
        sum += math.pow(row1[i] - row2[i], 2)
    '''
    values = map(lambda x,y: math.pow(x - y, 2), row1, row2)
    return math.sqrt(reduce(lambda x,y:x+y, values))

def base_dist(idx, testcase1, testcase2):
    height = len(testcase1)
    row = idx / height
    col = idx % height
    return euclidean_dist(testcase1[row],testcase2[col])



def init_cost_table(height):
    table = []
    table.append([0] + [float("inf")] * (height))
    for i in range(height):
        row = [float("inf")] + [0] * height
        table.append(row)
    return table


def find_similarity_seq(testcase1, testcase2):
    start_time = time.time()                    #   record starting time
    height = len(testcase1)
    table = init_cost_table(height)             #   initiate cost table
    similarity = float("inf")                   #   set similarity to infinite
    for i in range(1, height + 1):              #   go through cost table cells one by one and calculate their costs
        for j in range(1, height + 1):
            row1 = testcase1[i - 1]
            row2 = testcase2[j - 1]
            table[i][j] = euclidean_dist(row1, row2) + min(table[i][j-1], table[i-1][j], table[i-1][j-1])
            if i == height or j == height:      #   find minimum cost on the fly among last column and row
                cellSimilarity = table[i][j] + abs(i - height) + abs(j - height)
                if cellSimilarity < similarity:
                    similarity = cellSimilarity
    return similarity, time.time() - start_time    #   returns similarity and run time


def find_similarity_par(testcase1, testcase2):
    start_time = time.time()                    #   record starting time
    height = len(testcase1)
    jobs_count = height * height
    processes_count = 16
    table = init_cost_table(height)             #   initiate cost table
    similarity = float("inf")                   #   set similarity to infinite
    pool = mp.Pool(processes=processes_count)   #   calculate base distances in parallel
    base_distances = [pool.apply_async(base_dist,args=(i, testcase1, testcase2)) for i in range(jobs_count)]
    pool = mp.Pool(processes=height)            #   calculate actually distance in parallel with red white algorithm
    print time.time() - start_time




tc1 = rand_test_case(3,100)
tc2 = rand_test_case(3,100)
print find_similarity_seq(tc1, tc2)
find_similarity_par(tc1, tc2)



