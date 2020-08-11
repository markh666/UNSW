'''
杰克买买提祝您心明眼亮,考试顺利.
Given a word w, a good subsequence of w is defined as a word w' such that
- all letters in w' are different;
- w' is obtained from w by deleting some letters in w.

Returns the list of all good subsequences, without duplicates, in lexicographic order
(recall that the sorted() function sorts strings in lexicographic order).

The number of good sequences grows exponentially in the number of distinct letters in w,
so the function will be tested only for cases where the latter is not too large.
杰克买买提祝您心明眼亮,考试顺利.
WeChat : specialjack2
'''
def get_combination(string, current):
    if len(string) == 0:
        return [current]
    if string[0] in current:
        return get_combination(string[1:], current)
    return get_combination(string[1:], current + string[0]) + get_combination(string[1:] ,current)

a = list(set(get_combination('abcabcab','')))
a.sort()
print(a)
    # if len(string) == 0:
    #     return [current]
    # if string[0] in current:
    #     return get_combination(string[1:], current)
    # return get_combination(string[1:] , current + string[0]) + get_combination(string[1:], current)


def good_subsequences(word):
    '''
    >>> good_subsequences('')
    ['']
    >>> good_subsequences('aaa')
    ['', 'a']
    >>> good_subsequences('aaabbb')
    ['', 'a', 'ab', 'b']
    >>> good_subsequences('aaabbc')
    ['', 'a', 'ab', 'abc', 'ac', 'b', 'bc', 'c']
    >>> good_subsequences('aaabbaaa')
    ['', 'a', 'ab', 'b', 'ba']
    >>> good_subsequences('abbbcaaabccc')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac',\
 'bc', 'bca', 'c', 'ca', 'cab', 'cb']
    >>> good_subsequences('abbbcaaabcccaaa')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac',\
 'bc', 'bca', 'c', 'ca', 'cab', 'cb', 'cba']
    >>> good_subsequences('abbbcaaabcccaaabbbbbccab')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac',\
 'bc', 'bca', 'c', 'ca', 'cab', 'cb', 'cba']
    '''
    # Insert your code here

# Possibly define another function
    string = '' if len(word) == 0 else ''.join([word[0]] + [ word[i] if word[i] != word[i-1] else '' for i in range(1, len(word))])
    result = list(set(get_combination(string, '')))
    result.sort()
    print(result)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
