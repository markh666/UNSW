'''
您好，我叫杰克-买买提。是一名学IT的初中生。很高兴认识您。
现正寻找一份年底的实习项目，在国内或者澳洲都可以。数据或者写网页方向。我的目标是三十岁之前给马云那样的老板打工，请问谁能帮我？
任何信息我都要。谢谢谢谢。
is_valid_prefix_expression(expression) checks whether the string expression
represents a correct infix expression (where arguments follow operators).

evaluate_prefix_expression(expression) returns the result of evaluating expression.

For expression to be syntactically correct:
- arguments have to represent integers, that is, tokens that can be converted to an integer
  thanks to int();
- operators have to be any of +, -, * and /;
- at least one space has to separate two consecutive tokens.

Assume that evaluate_prefix_expression() is only called on syntactically correct expressions,
and that / (true division) is applied to a denominator that is not 0.

You might find the reversed() function, the split() string method,
and the pop() and append() list methods useful.
'''

from operator import add, sub, mul, truediv
from collections import deque

class ListNonEmpty(Exception):
    pass


def is_valid_prefix_expression(expression):
    '''
    >>> is_valid_prefix_expression('12')
    Correct prefix expression
    >>> is_valid_prefix_expression('+ 12 4')
    Correct prefix expression
    >>> is_valid_prefix_expression('- + 12 4 10')
    Correct prefix expression
    >>> is_valid_prefix_expression('+ - + 12 4 10 * 11 4')
    Correct prefix expression
    >>> is_valid_prefix_expression('/ + - + 12 4 10 * 11 4 5')
    Correct prefix expression
    >>> is_valid_prefix_expression('+ / + - + 12 4 10 * 11 4 5 - 80 82 ')
    Correct prefix expression
    >>> is_valid_prefix_expression('twelve')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('2 3')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+ + 2 3')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+1 2')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+ / 1 2 *3 4')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+1 2')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+ +1 2')
    Correct prefix expression
    >>> is_valid_prefix_expression('++1 2')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+ +1 -2')
    Correct prefix expression
    '''

    stack = []
    try:
        evals = list(reversed(expression.strip().split()))
        if not evals:
            raise IndexError

        operators = {'+':add,'-':sub,'*':mul,'/':truediv}
        top_number = False

        while len(stack)>1 or evals:
            if len(stack)>2 and \
               (type(stack[-1])==int or type(stack[-1])==float) \
               and (type(stack[-2])==int or type(stack[-2])==float):
                b = stack.pop()
                a = stack.pop()
                oper= stack.pop()
                c = oper(a,b)
                stack.append(c)

            else:
                item = evals.pop()
                if item in operators:
                    stack.append(operators[item])
                else:
                    try:
                        stack.append(int(item))
                    except:
                        stack.append(float(item))

        if type(stack[0])!=int and type(stack[0])!=float:
            raise ListNonEmpty
    except (IndexError, ValueError, ListNonEmpty):
        print('Incorrect prefix expression')
    else:
        print('Correct prefix expression')


def evaluate_prefix_expression(expression):
    '''
    >>> evaluate_prefix_expression('12')
    12
    >>> evaluate_prefix_expression('+ 12 4')
    16
    >>> evaluate_prefix_expression('- + 12 4 10')
    6
    >>> evaluate_prefix_expression('+ - + 12 4 10 * 11 4')
    50
    >>> evaluate_prefix_expression('/ + - + 12 4 10 * 11 4 5')
    10.0
    >>> evaluate_prefix_expression('+ / + - + 12 4 10 * 11 4 5 - 80 82 ')
    8.0
    >>> evaluate_prefix_expression('+ +1 2')
    3
    >>> evaluate_prefix_expression('+ +1 -2')
    -1
    杰克买买提祝您学习进步,考试顺利.
    WeChat : specialjack2
    '''
    stack = []
    try:
        evals = list(reversed(expression.strip().split()))
        if not evals:
            raise IndexError

        operators = {'+':add,'-':sub,'*':mul,'/':truediv}

        while len(stack)>1 or evals:
            if len(stack)>2 and \
               (type(stack[-1])==int or type(stack[-1])==float) \
               and (type(stack[-2])==int or type(stack[-2])==float):
                b = stack.pop()
                a = stack.pop()
                oper= stack.pop()
                c = oper(a,b)
                stack.append(c)
            else:
                item = evals.pop()
                if item in operators:
                    stack.append(operators[item])
                else:
                    try:
                        stack.append(int(item))
                    except:
                        stack.append(float(item))
        print(stack.pop())

    except (IndexError, ValueError, ListNonEmpty):
        print('Incorrect prefix expression')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
