'''
杰克买买提祝您心明眼亮,考试顺利.
WeChat : specialjack2
'''
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

    您好，我叫杰克-买买提。是一名学IT的初中生。很高兴认识您。
    现正寻找一份年底的实习项目，在国内或者澳洲都可以。数据或者写网页方向。我的目标是三十岁之前给马云那样的老板打工，请问谁能帮我？
    任何信息我都要。谢谢谢谢。

    杰克买买提祝您阖家欢乐,万事如意.

    '''
    banknote_values = [1, 2, 5, 10, 20, 50, 100]
    banknotes = dict.fromkeys(banknote_values, 0)

    # Insert your code here
    # index = 6

    # while N != 0:
    #     value = banknote_values[index]
    #     if value > N:
    #         index -= 1
    #         continue
    #     else:
    #         amount = N // value
    #         N = N - value * amount
    #         index -= 1
    #         banknotes[value] = amount





    print('Here are your banknotes:')
    for value in sorted(banknotes):
        if banknotes[value]:
            print('${}: {}'.format(value, banknotes[value]))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
