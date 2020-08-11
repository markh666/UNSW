## import modules here 

################# Question 0 #################

def add(a, b): # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x): # do not change the heading of the function
    x = abs(x)
    high = x
    low = 0.0
    mid = x / 2
    while abs(mid * mid - x) > 0.0001:
        if (mid * mid > x):
            high = mid
            mid = low + (mid - low) / 2
        else:
            low = mid
            mid = high - (high - mid) / 2
    if mid - int(mid)>=0.9999:
        result = int(mid)+1
    else:
        result = int(mid)
    return result


################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

## NOTE: you must use the default values of the above parameters, do not change them

def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    for i in range(MAX_ITER+1):
        x_1 = x_0
        x_0 = x_0 - f(x_0) / fprime(x_0)
        if abs(x_0 - x_1) <= EPSILON:
            return x_0
    return x_0


################# Question 3 #################

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

def make_tree(tokens): # do not change the heading of the function
    parent_list = []
    for i in range(0, len(tokens)):
        if i == 0:
            parent = child = root = Tree(tokens[0])
        
        elif tokens[i] == '[':
            parent_list.append(parent)
            parent = child

        elif tokens[i] == ']':
            parent = parent_list.pop()

        else:
            child = Tree(tokens[i])
            parent.add_child(child)

    return root

def max_depth(root): # do not change the heading of the function
    if root == None:
        return 0
    
    if len(root.children) == 0:
        return 1
    
    result = []
    for i in root.children:
        result.append(max_depth(i))
    
    return max(result)+1
