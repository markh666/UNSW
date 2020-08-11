import math

def nsqrt(x): # do not change the heading of the function
    import math
    if x <= 1: 
        return x
    if x == 2:
        return 1
    goal = int(x/2)

    while goal**2 > x:
        goal = int(goal/2)
    up = goal * 2
    low = goal

    while up - low > 1:
        if ((up + low)/2) **2 <= x:
            low = math.floor((up + low)/2)
        else:
            up = math.ceil((up + low)/2)
    if up ** 2 <= x:
        return up
    return low

def f(x):
    return x * math.log(x) - 16.0

def fprime(x):
    return 1.0 + math.log(x)

def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    for i in range(MAX_ITER+1):
        x_1 = x_0
        x_0 = x_0 - f(x_0) / fprime(x_0)
        if abs(x_0 - x_1) <= EPSILON:
            return x_0
    return x_0