# Randomly fills an array of size 10x10 True and False, displayed as 1 and 0,
# and outputs the number chess knights needed to jump from 1s to 1s
# and visit all 1s (they can jump back to locations previously visited).
#
# Written by *** and Eric Martin for COMP9021


from random import seed, randrange
import sys

dim = 10

def display_grid():
    for i in range(dim):
        print('     ', end = '')
        print(' '.join(grid[i][j] and '1' or '0' for j in range(dim)))
    print()


def explore_board():
    cur_nb = 1
    g = grid
    for i in range(dim):
        for j in range(dim):
            if g[i][j] == True:
                g[i][j] = 1
            else:
                g[i][j] = 0
    for i in range(dim):
        for j in range(dim):
            if g[i][j] == 1:
                cur_nb += 1
                g[i][j] = cur_nb
                search_neighbor(i, j, cur_nb, g)
    return cur_nb - 1

def search_neighbor(a, b, cur_nb, g):
    pos_stack = []
    pos_stack.append([a, b])
    flag = False
    while len(pos_stack) != 0:
        i,j = pos_stack[-1]
        if i-2 >=0 and j-1 >=0 and g[i-2][j-1] == 1:
            g[i-2][j-1] = cur_nb
            pos_stack.append([i-2,j-1])
            flag = True
        if i+2 < dim and j-1 >=0 and g[i+2][j-1] == 1:
            g[i+2][j-1] = cur_nb
            pos_stack.append([i+2,j-1])
            flag = True
        if i-2 >=0 and j+1 < dim and g[i-2][j+1] == 1:
            g[i-2][j+1] = cur_nb
            pos_stack.append([i-2,j+1])
            flag = True
        if i+2 < dim and j+1 < dim and g[i+2][j+1] == 1:
            g[i+2][j+1] = cur_nb
            pos_stack.append([i+2,j+1])
            flag = True
        if i-1 >=0 and j-2 >=0 and g[i-1][j-2] == 1:
            g[i-1][j-2] = cur_nb
            pos_stack.append([i-1,j-2])
            flag = True
        if i+1 < dim and j-2 >=0 and g[i+1][j-2] == 1:
            g[i+1][j-2] = cur_nb
            pos_stack.append([i+1,j-2])
            flag = True
        if i-1 >=0 and j+2 < dim and g[i-1][j+2] == 1:
            g[i-1][j+2] = cur_nb
            pos_stack.append([i-1,j+2])
            flag = True
        if i+1 < dim and j+2 < dim and g[i+1][j+2] == 1:
            g[i+1][j+2] = cur_nb
            pos_stack.append([i+1,j+2])
            flag = True
        if flag == False:
            pos_stack.pop()
        if flag == True:
            flag = False

try:
    for_seed, n = (int(i) for i in input('Enter two integers: ').split())
    if not n:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
if n > 0:
    grid = [[randrange(n) > 0 for _ in range(dim)] for _ in range(dim)]
else:
    grid = [[randrange(-n) == 0 for _ in range(dim)] for _ in range(dim)]    
print('Here is the grid that has been generated:')
display_grid()
nb_of_knights = explore_board()
if not nb_of_knights:
    print('No chess knight has explored this board.')
elif nb_of_knights == 1:
    print(f'At least 1 chess knight has explored this board.')
else:
    print(f'At least {nb_of_knights} chess knights have explored this board')

