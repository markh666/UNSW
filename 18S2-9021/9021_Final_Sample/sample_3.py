'''
Given a word w, a good subsequence of w is defined as a word w' such that
- all letters in w' are different;
- w' is obtained from w by deleting some letters in w.

Returns the list of all good subsequences, without duplicates, in lexicographic order
(recall that the sorted() function sorts strings in lexicographic order).

The number of good sequences grows exponentially in the number of distinct letters in w,
so the function will be tested only for cases where the latter is not too large.

'''

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
    if len(word) == 0:
        print([''])
    else:
        string = word[0]
        for i in word[1:]:
            if i != string[-1]:
                string += i
        print(sorted(set(get_com(string,''))))

def get_com(string,current):
    if len(string) == 0:
        return [current]
    if string[0] in current:
        return get_com(string[1:],current)
    else:
        return get_com(string[1:],current + string[0]) + get_com(string[1:],current)
    



    
##    if len(word) == 0:
##         print([''])
##    else:
##        string = word[0]
##        for w in word[1:]:
##            if w != string[-1]:
##                string += w
##                
##        print(sorted(set(get_com(string,''))))
##        
        
    
##        a=list(set(get_com(string,'')))
##        a.sort()
##        print(a)
    
def get_com(string,current):
    if len(string) == 0:
        return [current]

    if  string[0] in current:
        return get_com(string[1:],current)
    else:
        return get_com(string[1:],current+string[0]) + get_com(string[1:],current)
    

# good_subsequences('aaabbc')

    
# Ricky带我写
##    if len(word) == 0:
##        print([''])
##    else:
##        s = word[0]
##        for i in word[1:]:
##            if i != s[-1]:
##                s += i
##                
##        a = list(set(get_combination(s,'')))
##        a.sort()
##        print(a)
##
##def get_combination(string,current):
##    if len(string) == 0:
##        return [current]
##    if  string[0] in current :
##        return get_combination(string[1:],current)
##    return get_combination(string[1:], current + string[0]) + get_combination(string[1:],current)
##
##list(set(get_combination('abcabcab','')))

##1 step commenout the __main__
##2 去重
##3 写出所有w'
##
##def recur_find(string,current):
##    if string == '':
##        return [current]
##    if string[0] in current:
##        return recur_find(string[1:],current)
##    else:
##        return recur_find(string[1:],current+string[0]) + recur_find(string[1:],current)


##def get_combo(string,current):
##    if string == '':
##        return [current]
###general case
##    return 



if __name__ == '__main__':
    import doctest
    doctest.testmod()

