'''
您好，我叫杰克-买买提。是一名学IT的初中生。很高兴认识您。
现正寻找一份年底的实习项目，在国内或者澳洲都可以。数据或者写网页方向。我的目标是三十岁之前给马云那样的老板打工，请问谁能帮我？
任何信息我都要。谢谢谢谢.
WeChat : specialjack2
杰克买买提祝您阖家欢乐,万事如意.
Tries and find a word in a text file that represents a grid of words, all of the same length.
There is only one word per line in the file.
The letters that make up a word can possibly be separated by an arbitrary number of spaces,
and there can also be spaces at the beginning or at the end of a word,
and there can be lines consisting of nothing but spaces anywhere in the file.
Assume that the file stores data as expected.

A word can be read horizontally from left to right,
or vertically from top to bottom,
or diagonally from top left to bottom right
(this is more limited than the lab exercise).
The locations are represented as a pair (line number, column number),
starting the numbering with 1 (not 0).
'''


def find_word(filename, word):
    '''
    >>> find_word('word_search_1.txt', 'PLATINUM')
    PLATINUM was found horizontally (left to right) at position (10, 4)
    >>> find_word('word_search_1.txt', 'MANGANESE')
    MANGANESE was found horizontally (left to right) at position (11, 4)
    >>> find_word('word_search_1.txt', 'LITHIUM')
    LITHIUM was found vertically (top to bottom) at position (2, 14)
    >>> find_word('word_search_1.txt', 'SILVER')
    SILVER was found vertically (top to bottom) at position (2, 13)
    >>> find_word('word_search_1.txt', 'SODIUM')
    SODIUM was not found
    >>> find_word('word_search_1.txt', 'TITANIUM')
    TITANIUM was not found
    >>> find_word('word_search_2.txt', 'PAPAYA')
    PAPAYA was found diagonally (top left to bottom right) at position (1, 9)
    >>> find_word('word_search_2.txt', 'RASPBERRY')
    RASPBERRY was found vertically (top to bottom) at position (5, 14)
    >>> find_word('word_search_2.txt', 'BLUEBERRY')
    BLUEBERRY was found horizontally (left to right) at position (13, 5)
    >>> find_word('word_search_2.txt', 'LEMON')
    LEMON was not found
    '''
    with open(filename) as file:
        grid = []
        lines = file.readlines()

        for line in lines:
            l = [x for x in line if x != ' ' and x !='\n']
            if l:
                grid.append(l)

        # Insert your code here
        # A one liner that sets grid to the appropriate value is enough.
        location = find_word_horizontally(grid, word)
        found = False
        if location:
            found = True
            print(word, 'was found horizontally (left to right) at position', location)
        location = find_word_vertically(grid, word)
        if location:
            found = True
            print(word, 'was found vertically (top to bottom) at position', location)
        location = find_word_diagonally(grid, word)
        if location:
            found = True
            print(word, 'was found diagonally (top left to bottom right) at position', location)
        if not found:
            print(word, 'was not found')


def find_word_horizontally(grid, word):
    l = len(word)
    for i in range(len(grid)):
        for j in range(0,len(grid[i])-len(word)+1):
            if word == ''.join(grid[i][j:j+l]):
                return i+1,j+1
    # Replace pass above with your code


def find_word_vertically(grid, word):
    l = len(word)
    trans = [[None]*len(grid) for j in range(len(grid[1]))]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            trans[j][i] = grid[i][j]
    for i in range(len(trans)):
        for j in range(0,len(trans[i])-len(word)+1):
            if word == ''.join(trans[i][j:j+l]):
                return j+1,i+1
    # Replace pass above with your code


def find_word_diagonally(grid, word):
    l = len(word)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            diag = find_diagonal_word(grid,i,j,l)
            if diag ==word:
                return i+1,j+1


def find_diagonal_word(grid, i,j, l):
    wordlist = []
    while True:
        try:
            wordlist.append(grid[i][j])
            i+=1
            j+=1
            if len(wordlist)==l:
                return ''.join(wordlist)
        except Exception:
            return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()
