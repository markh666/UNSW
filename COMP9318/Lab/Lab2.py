## import modules here 
import pandas as pd
import numpy as np


def v_opt_dp(x, num_bins):# do not change the heading of the function

    global _x, _num_bins, dp_matrix, dp_index

    dp_matrix = [[-1 for i in range(len(x))] for j in range(num_bins)]
    dp_index = [[-1 for i in range(len(x))] for j in range(num_bins)]
    _x = x
    _num_bins = num_bins
    _v_opt_dp(0, num_bins-1) #bin is 0-3

    start = dp_index[-1][0]
    pre_start = start
    bins = [x[:start]]
    for i in range(len(dp_index)-2, 0, -1):
        start = dp_index[i][start]
        bins.append(x[pre_start:start])
        pre_start = start
    bins.append(x[pre_start:])
    return dp_matrix, bins

def _v_opt_dp(mtx_x, remain_bins): #mtx_x is the index of x, we will put
                                    #all element behind it to the reamin bin
    
    global _x, _num_bins, dp_matrix, dp_index
    
    if( _num_bins - remain_bins - mtx_x < 2) and (len(_x) - mtx_x > remain_bins):
        _v_opt_dp(mtx_x+1, remain_bins)
        if(remain_bins == 0):
            dp_matrix[remain_bins][mtx_x] = np.var(_x[mtx_x:])*len(_x[mtx_x:])
            return 

        _v_opt_dp(mtx_x, remain_bins - 1)  

        min_list = [dp_matrix[remain_bins-1][mtx_x+1]]

        for i in range(mtx_x+2, len(_x)):
            min_list.append(dp_matrix[remain_bins-1][i] + (i - mtx_x)*np.var(_x[mtx_x:i])) 

        dp_matrix[remain_bins][mtx_x] = min(min_list)
        dp_index[remain_bins][mtx_x] = min_list.index(min(min_list)) + mtx_x +1

x = [3, 1, 18, 11, 13, 17]
num_bins = 4
matrix, bins = v_opt_dp(x, num_bins)
print("Bins = {}".format(bins))
print("Matrix =")
for row in matrix:
    print(row)

LARGE_NUM = 1000000000.0
EMPTY = -1
DEBUG = False

def partition(lst):
    for i in range(1, len(lst)):
        for r in partition(lst[i:]):
            yield [lst[:i]] + r
    yield [lst]

def bin_cost(partition,cost_dict):
    cost = 0
    for part in partition:
        if part in cost_dict:
            cost += cost_dict[part]
        else:
            new_cost = sse(part)  
            cost_dict[part] = new_cost
            cost += new_cost
    return cost,cost_dict

def print_list_of_list(lol):
    for l in lol:
        print(l)


def v_opt_dp(x, num_bins):# do not change the heading of the function           
    x= tuple(x)
    suffix_len = len(x)
    result_matrix = [[-1 for x in range(suffix_len)] for y in range(num_bins)]
    cost_matrix = [[-1 for x in range(suffix_len)] for y in range(num_bins)] 
    cost_dict = {}

    # Loop for suffix then loop for bins
    for bins in range(1,num_bins + 1):
        for i in reversed(range(suffix_len)):
            prefix = x[0 : i ]
            suffix = x[i  : ]

            # Check if quesiton is valid
            if bins > len(suffix):
                continue
            # Don't call function for one bin
            elif bins == 1:
                cost = sse(suffix)
                cost_dict[suffix] = cost
                optimal = suffix
            else:

                # Build partitions
                partitions = [part for part in partition(suffix) if len(part) == bins]
                partition_costs = []

                # Calculate costs
                for part in partitions:
                    cost,cost_dict = bin_cost(part, cost_dict)
                    partition_costs.append(cost)
                
                # Get minimums
                cost = min(partition_costs)
                optimal = partitions[partition_costs.index(min(partition_costs))]

            # Insert cost and solution
            cost_matrix[bins-1][i] = cost
            result_matrix[bins-1][i] = optimal

    return cost_matrix,result_matrix[bins-1][0]


def sse(arr):
    if len(arr) == 0: # deal with arr == []
        return 0.0

    avg = np.average(arr)
    val = sum([(x-avg)*(x-avg) for x in arr] )

    return val

def calc_depth(b):
    return 5 - b

#x = [3, 1, 18, 11, 13,4,5,5,7,7, 17]
#y = [7,9,13,5]
#num_bins = 7
#parts = [part for part in parts if len(part) == 3]


#matrix,bins=v_opt_dp(x,num_bins)
#print(matrix)
#print(bins)