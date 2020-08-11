
def f(N):
    '''
    >>> f(20)
    Here are your banknotes:
    $20: 1
    >>> f(40)
    Here are your banknotes:
    $20: 2
    >>> f(42)
    Here are your banknotes:
    $2: 1
    $20: 2
    >>> f(43)
    Here are your banknotes:
    $1: 1
    $2: 1
    $20: 2
    >>> f(45)
    Here are your banknotes:
    $5: 1
    $20: 2
    >>> f(2537)
    Here are your banknotes:
    $2: 1
    $5: 1
    $10: 1
    $20: 1
    $100: 25
    '''
    banknote_values = [1, 2, 5, 10, 20, 50, 100]
    banknotes = dict.fromkeys(banknote_values, 0)

    for v in reversed(banknote_values):
        if N// v :
            banknotes[v] = N//v
            N = N % v
    print('Here are your banknotes:')
    for k in banknotes:
        if banknotes[k] != 0 :
            print('${}: {}'.format(k,banknotes[k]))






##    for v in reversed(banknote_values):
##        if N//v:
##            banknotes[v] = N//v
##            N = N % v
##    print('Here are your banknotes:')
##    for k in banknotes:
##        if banknotes[k] != 0:
##            print(f'${k}: {banknotes[k]}')
##        
    

##    for v in reversed(banknote_values):
##        if N//v:
##            banknotes[v] = N//v
##            N = N%v
##    print('Here are your banknotes:')
##    for k in banknotes:
##        if banknotes[k] != 0:
##            print(f'${k}: {banknotes[k]}')


    

##    if N//100:
##        banknotes[100] = N//100
##        N = N%100
##    if N//50:
##        banknotes[50] = N//50
##        N = N%50
##    if N//20:
##        banknotes[20] = N//20
##        N = N%20
##    if N//10:
##        banknotes[10] = N//10
##        N = N%10
##    if N//5:
##        banknotes[5] = N//5
##        N = N%5
##    if N//2:
##        banknotes[2] = N//2
##        N = N%2
##    if N//1:
##        banknotes[1] = N//1
##    print('Here are your banknotes:')
##    for k in banknotes:
##        if banknotes[k] != 0:
##            print(f'${k}: {banknotes[k]}')



##    if N // 100:
##        banknotes[100] = N // 100
##        N = N % 100
##    if N // 20 :
##        banknotes[20] =  N // 20
##        N = N % 20
##    if N // 10 :
##        banknotes[10] = N // 10
##        N =  N % 10
##    if N // 5 :
##        banknotes[5] = N // 5
##        N = N % 5
##    if N // 2 :
##        banknotes[2] = N // 2
##        N = N % 2
##    if N // 1:
##        banknotes[1] = N//1
##    print('Here are your banknotes:')
##    for k in banknotes:
##        if banknotes[k]:
##            print(f'${k}: {banknotes[k]}')
####    banknotes[100] = N//100
##    N = N - 100*banknotes[100]
##    
##    if N//50 != 0:
##        banknotes[50] = N//50
##        N = N - 50*banknotes[50]
##    if N//20 != 0:
##        banknotes[20] = N//20
##        N = N - 20*banknotes[20]
##    if N//10 != 0:
##        banknotes[10] = N//10
##        N = N - 10*banknotes[10]
##    if N//5 != 0:
##        banknotes[5] = N//5
##        N = N - 5*banknotes[5]
##    if N // 2 != 0:
##        banknotes[2] = N//2
##        N = N - 2*banknotes[2]
##    banknotes[1] = N//1
##    for i in reversed(banknote_values):
##        if N//i != 0 :
##            banknotes[i] = N//i
##            N -= i*banknotes[i]
##    print('Here are your banknotes:')
##    for value in sorted(banknotes):
##        if banknotes[value]:
##            print('${}: {}'.format(value, banknotes[value]))
##
##    index = 6
##    while N != 0:
##        notes =  banknote_values[index]
##        if N >= notes:
##            amount = N// notes
##            N -+ amount * notes
##            banknotes[notes] = amount
##            index -= 1
##        else:
##            index -= 1

   
if __name__ == '__main__':
    import doctest
    doctest.testmod()
