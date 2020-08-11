from random import seed, randrange
import sys
dim = 10
def display_grid():
    for i in range(dim):
        print('     ', end = '')
        print(' '.join(f'{int(e)}' for e in grid[i]))
    print()

#给定一个 row 第 i 行,可以返回一个 list of start point(一段连续1中 第一个1的index 位置)
def find_row_start(i):
    start=0
    end=0
    start_list=[]
    #for i in range(len(grid)-1,-1,-1):
        #print('i=',i)
    for j in range(0,10):
        if (j ==0 and grid[i][j]==1) or (grid[i][j] == 1 and grid[i][j-1]==0) :
            start=j
            start_list.append(start)
    result = list(set(start_list))
    #print('Starts:',result)
    return result

def size_of_largest_construction():
    area = 0
    for i in range(9,-1,-1):
        start_list = find_row_start(i)
        #给每个 start point 都找到对应的结束的那个1的 index
        #print('start_list =',start_list)
        for start in start_list:
            #print('start =',start)
            if start != 9:
                tail =start
                #print(f'X01 start = {start}, tail = {tail}')
                #print('i,tail',i,tail)
                while grid[i][tail]==1:
                    tail+=1
                    if tail == 10:
                        break
                tail-=1
            else:
                if grid[i][9]==1:
                    tail = 9
            #print(f'i = {i},start={start},tail={tail}')

            start_tail_size = construction_size(i,start,tail)
            #print(start_tail_size)
            if start_tail_size > area:
                area = start_tail_size

            tail=start

    return area

# If j1 <= j2 and the grid has a 1 at the intersection of row i and column j
# for all j in {j1, ..., j2}, then returns the number of blocks in the construction
# built over this line of blocks.
#这道题其实就是把0当做空气, 把1看成块板砖,问你能砌多大 size 的墙
#(空气上面不能垒砖头,只有1上面才可以垒上去另一个1)
#让你分别计算每一行中如果有一段连续的砖头(1),这段砖头往上面垒可以垒多少块(size)
#然后输出您能砌出来 size 最大的墙 的 size
# 给定一个 row 第 i 行, start point 就是j1, 即那一段连续1中,起始1的 index
# j2 就是 tail, 就是第 irow 中,这一段1中最后那个1的 index 位置
#返回的是 在第 i row 中这一段连续的1可以垒起来的1的个数(size)
#我的思路是暴力搜索, 从左往右,从下往上数. 先从最后一行开始,
#每一行都从 j1那一列往上面数有多少个1,这一列数到0了就从他右边一列最下面开始往上面数,一直数到 j2那一列的最顶
def construction_size(i, j1, j2):
    original = i
    size = 0
    while j1 <= j2 :
        if grid[i][j1] == 1:
            #print('(i,j) =',i,j1)
            size += 1
            i -= 1
        if grid[i][j1]!=1 or i==-1:
            j1 = j1 + 1
            i = original

    return size

try:
    for_seed, n = input('Enter two integers, the second one being strictly positive: ').split()
    for_seed = int(for_seed)
    n = int(n)
    # for_seed = 0
    # n = 3
    if n <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[bool(randrange(n)) for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()
size = size_of_largest_construction()
if not size:
    print(f'The largest block construction has no block.')
elif size == 1:
    print(f'The largest block construction has 1 block.')
else:
    print(f'The largest block construction has {size_of_largest_construction()} blocks.')
