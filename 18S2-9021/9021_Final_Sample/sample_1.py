'''
杰克买买提祝您阖家欢乐,万事如意.
'''
def remove_consecutive_duplicates(word):
    '''
    >>> remove_consecutive_duplicates('')
    ''
    >>> remove_consecutive_duplicates('a')
    'a'
    >>> remove_consecutive_duplicates('ab')
    'ab'
    >>> remove_consecutive_duplicates('aba')
    'aba'
    >>> remove_consecutive_duplicates('aaabbbbbaaa')
    'aba'
    >>> remove_consecutive_duplicates('abcaaabbbcccabc')
    'abcabcabc'
    >>> remove_consecutive_duplicates('aaabbbbbaaacaacdddd')
    'abacacd'
    '''
    # Insert your code here (the output is returned, not printed out)
##    from itertools import groupby
##    return ''.join([x[0] for x in groupby(word)])
##    if len(word) == 0 :
##        return ''
##    else:
##        string = word[0]
##        for i in word[1:]:
##            if i != string[-1]:
##                string = string + i
##        return string


    if len(word) == 0 :
        return ''
    if len(word) == 1:
        return word
    else:
        string = word[0]
        for i in word[1:]:
            if i != string[-1]:
                string = string + i
        return string

if __name__ == '__main__':
    import doctest
    doctest.testmod()
