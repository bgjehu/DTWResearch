__author__ = 'Jieyi Hu'

from Utilities import rand_test_case
from Utilities import euclidean_distance
from Utilities import init_cost_table
import threading
import math
import time
import multiprocessing

def fill_cost_table_cell(data, coordinate):
    x = coordinate[0]
    y = coordinate[1]
    cost = data.base_distance(x - 1, y - 1) + min(data.cost_table[x - 1][y], data.cost_table[x][y- 1], data.cost_table[x-1][y-1])
    data.cost_table[x][y] = cost
    if x == data.height or y == data.height:
        cellSimilarity = cost + abs(x - data.height) + abs(y - data.height)
        if cellSimilarity < data.similarity:
            data.similarity = cellSimilarity



def fill_cost_table_cell_mul(data, coordinates):
    for coordinate in coordinates:
        fill_cost_table_cell(data, coordinate)


class DTWData:


    def __init__(self, identical_testcases, width, height):
        self.identical_testcases = identical_testcases
        self.width = width
        self.height = height
        self.cell_count = height * height
        self.testcase1 = rand_test_case(width, height)
        self.testcase2 = None
        if identical_testcases:
            self.testcase2 = self.testcase1
        else:
            self.testcase2 = rand_test_case(width, height)
        self.cost_table = init_cost_table(height)
        self.similarity = float("inf")


    def reset_cost_table(self):
        self.cost_table = init_cost_table(self.height)
        self.similarity = float("inf")



    def base_distance(self, row, col):
        return euclidean_distance(self.testcase1[row], self.testcase2[col])

    '''
    def fill_base_distance_MPPool(self, processes_count):
        pool = multiprocessing.Pool(processes=processes_count)
        base_distances = [pool.apply(func=fill_base_distance, args=(self,i)) for i in range(self.cell_count)]

    def fill_base_distance_THPool(self, threads_count):
        work_count = self.height * self.height
        pool = ThreadPool(threads_count)
        result = [pool.apply(func=fill_base_distance, args=(self,i)) for i in range(self.cell_count)]
        pool.close()
        pool.join()

    def fill_base_distance_sequential(self):
        for i in range(self.cell_count):              #   go through cost table cells one by one and calculate their costs
            fill_base_distance(self, i)



    def fill_base_distance_parallel(self, threads_count):
        work_count_per_thread = self.cell_count / threads_count
        threads = []
        for i in range(threads_count):
            indices = [ work_count_per_thread * i + x for x in range(work_count_per_thread)]
            t = threading.Thread(target=fill_base_distance_mul, args=(self,indices))
            threads.append(t)
            t.start()
    '''


    def find_similarity_sequentially(self):
        self.reset_cost_table()
        start_time = time.time()
        for i in range(1, self.height + 1):              #   go through cost table cells one by one and calculate their costs
            for j in range(1, self.height + 1):
                self.cost_table[i][j] = self.base_distance(i - 1, j - 1) + min(self.cost_table[i][j - 1], self.cost_table[i - 1][j], self.cost_table[i - 1][j - 1])
                if i == self.height or j == self.height:      #   find minimum cost on the fly among last column and row
                    cellSimilarity = self.cost_table[i][j] + abs(i - self.height) + abs(j - self.height)
                    if cellSimilarity < self.similarity:
                        self.similarity = cellSimilarity
        run_time = time.time() - start_time
        return self.similarity, run_time


    def find_similarity_parallel(self, threads_count):

        def get_target_cell_coordinates(iteration):     #   iteration goes from 1 to (2 * height) + 1
            coordinates = []
            const = iteration + 1
            for i in range(iteration):
                x = i + 1
                y = const - x
                if x < self.height + 1 and y < self.height + 1:
                    coordinates.append((x,y))
            return coordinates

        def fill_cost_table_cell_in_parallel(threads_count, coordinates_pool):
            '''
            work_count = len(coordinates_pool)
            threads = []
            if threads_count <= work_count:
                work_count_per_thread = int(math.ceil(float(work_count) / threads_count))
                for i in range(threads_count):
                    left_element = work_count - work_count_per_thread * i
                    if left_element <= work_count_per_thread:      #   last iteration
                        indices = [ x for x in range(work_count_per_thread * i, work_count)]
                    else:
                        indices = [ work_count_per_thread * i + x for x in range(work_count_per_thread)]
                    coordinates = map(lambda x:coordinates_pool[x], indices)
                    t = threading.Thread(target=fill_cost_table_cell_mul, args=(self,coordinates))
                    threads.append(t)
                    t.start()
                    t.join()
                    if left_element <= work_count_per_thread:
                        break;
            else:
                for i in range(work_count):
                    t = threading.Thread(target=fill_cost_table_cell, args=(self,coordinates_pool[i]))
                    threads.append(t)
                    t.start()
                    t.join()
            '''


        self.reset_cost_table()
        start_time = time.time()

        for i in range(1, 2 * self.height):     #   for every diagonal starting from 1 to 2 * height - 1
            coordinates = get_target_cell_coordinates(i)
            if len(coordinates) > 1:
                fill_cost_table_cell_in_parallel(threads_count, coordinates)
            else:
                fill_cost_table_cell(self,coordinates[0])


        run_time = time.time() - start_time
        return self.similarity, run_time