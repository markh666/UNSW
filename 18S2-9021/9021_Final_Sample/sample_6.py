'''
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
    op = ['+','-','*','/']
##    try:
##        expression = expression.split()
##        # print(expression)
##        for i in expression:
##            if i in op or int(i):
##                stack.append(i)
##            while len(stack) >= 3 and stack[-1] not in op and stack[-2] not in op and stack[-3] in op:
##                right = stack.pop()
##                left = stack.pop()
##                opp = stack.pop()
##                result =  eval(left + opp + right)
##                stack.append(str(result))
##                # print(stack)
##        if len(stack) > 1 or len(stack) == 0 :
##            raise ValueError
            
    # - IndexError is raised in particular when trying to pop from an empty list
    # - ValueError is raised in particular when trying to convert to an int
    #   a string that cannot be converted to an int
    # - ListNonEmpty is expected to be raised when a list is found out not to be empty
    except (IndexError, ValueError, ListNonEmpty):
        print('Incorrect prefix expression')
    else:
        print('Correct prefix expression')

# is_valid_prefix_expression('+ 12 4')
# is_valid_prefix_expression('/ + - + 12 4 10 * 11 4 5')
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
    '''
    # Insert your code here
##    stack = []
##    op = ['+','-','*','/']
##    
##    expression = expression.split()
##    for i in expression:
##        if i in op or int(i):
##            stack.append(i)
##            
##        while len(stack) >= 3 and stack[-1] not in op and stack[-2] not in op and stack[-3] in op:
##            right = stack.pop()
##            left = stack.pop()
##            opp = stack.pop()
##            result =  eval(left + opp + right)
##            stack.append(str(result))
##    if '.' in stack[0]:
##        return float(stack[0])
##    return int(stack[0])
##

    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
##
##
### expression = '12 + 4'
### eval(expression)
### >> 16
##
##- + 12 4 10
##== - (+ 12 4 ) 10
##==  12+4-10
