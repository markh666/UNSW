'''
您好，我叫杰克-买买提。是一名学IT的初中生。很高兴认识您。
现正寻找一份年底的实习项目，在国内或者澳洲都可以。数据或者写网页方向。我的目标是三十岁之前给马云那样的老板打工，请问谁能帮我？
任何信息我都要。谢谢谢谢。
WeChat : specialjack2
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

    # approach 1
    # return '' if len(word) == 0 else ''.join([word[0]] + [ word[i] if word[i] != word[i-1] else '' for i in range(1, len(word))])
    # approach 2

    # if len(word) == 0:
    #     return word
    # new = word[0]
    # for i in range(len(word)-1):
    #     if word[i] != word[i+1]:
    #         new += word[i+1]
    # retuen new
    if len(word) == 0:
        return ''
    string = word[0]
    for i in word[1:]:
        if i != string[-1]:
            string += i

    return string

# remove_consecutive_duplicates('aba')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
