# import modules here
import pandas as pd
import numpy as np

def SSE (l):
    mean = np.average(l)
    sse = sum([(i-mean)**2 for i in l])
    return sse

def v_opt_dp(x, b):# do not change the heading of the function
    matrix = [[-1 for j in range(len(x))] for i in range(b)]
    _matrix = [[-1 for j in range(len(x))] for i in range(b)]
    cost = 0
    for i in  range(b):
        for j in reversed(range(len(x))):
            if j < len(x)-i and j >= b-(i+1):
                if i == 0 :
                    cost = SSE(x[j:])
                else:
                    temp = []
                    for n in range(j+1,len(x)):
                        if matrix[i-1][n] != -1:
                            temp.append(SSE(x[j:n]) + matrix[i-1][n])
                    cost = min(temp)
                    _matrix[i][j] = temp.index(min(temp)) + j+1
                
                if cost == 0.0:
                    cost = 0
                matrix[i][j] = cost
    end = 0     
    result = []   
    for i in reversed(range(b)):
        start = end
        end = _matrix[i][end]
        if len(x[start:end]) != 0:
            result.append(x[start:end])
    result.append(x[end:])

    return matrix, result

# test
x = [3, 1, 18, 11, 13, 17]
num_bins = 4
matrix, bins = v_opt_dp(x, num_bins)
print("Bins = {}".format(bins))
print("Matrix =")
for row in matrix:
    print(row)