from collections import defaultdict, deque
import sys


'''
您好，我叫杰克-买买提。是一名学IT的初中生。很高兴认识您。
现正寻找一份年底的实习项目，在国内或者澳洲都可以。数据或者写网页方向。我的目标是三十岁之前给马云那样的老板打工，请问谁能帮我？
任何信息我都要。谢谢谢谢。
WeChat : specialjack2
杰克买买提祝您阖家欢乐,万事如意.学习进步,周末愉快.
Determines whether a given sequence of words is a word ladder
from a given word word_1 to a given word word_2, that is,
a sequence of words all in the provided dictionary, of minimal length,
starting with word_1, ending in word_2, and such that two consecutive words
in the sequence differ by exactly one letter.

Assume that word_1 and word_2 are sequences of uppercase letters.

Note that a single test will examine many potential sequences at once,
so no form of hardcoding will achieve anything...

Hint to make the solution efficient enough:
- Check whether the given sequence can be a word ladder because:
   . its first word is word_1;
   . its last word is word_2;
   . any pair of consecutive words are in the dictionary and differ by exactly one letter.
- Then compute the length of some word ladder between word_1 and word_2, if any,
  giving up in case it can no longer be at most equal to the length of the given sequence,
  and check whether it is equal to the length of the given sequence.
'''


dictionary_file = 'dictionary.txt'

def get_words_and_word_relationships():
    cnt = 0
    try:
        with open(dictionary_file) as dictionary:
            lexicon = set()
            contextual_slots = defaultdict(list)
            for word in dictionary:
                word = word.rstrip()
                lexicon.add(word)
                for i in range(len(word)):
                    contextual_slots[word[: i], word[i + 1: ]].append(word)
                if cnt <5 and Test:
                    print(cnt)
                    print(word)
                    print(contextual_slots)
                    cnt+=1
            closest_words = defaultdict(set)
            for slot in contextual_slots:
                for i in range(len(contextual_slots[slot])):
                    for j in range(i + 1, len(contextual_slots[slot])):
                        closest_words[contextual_slots[slot][i]].add(contextual_slots[slot][j])
                        closest_words[contextual_slots[slot][j]].add(contextual_slots[slot][i])
            return lexicon, closest_words
    except FileNotFoundError:
        print(f'Could not open {dictionary_file}. Giving up...')
        sys.exit()

Test = False

def is_word_word_ladder(word_1, word_2, candidate_ladder):
    '''
    >>> is_word_word_ladder('AAA', 'AAA', ['AAA'])
    False
    >>> is_word_word_ladder('DAY', 'MEW', ['DAY', 'DAW', 'DEW', 'MEW'])
    False
    >>> is_word_word_ladder('COLD', 'WARM', ['COLD', 'CALD', 'CARD', 'WARD', 'WARM'])
    False
    >>> is_word_word_ladder('COLD', 'WARM', ['COLD', 'CORD', 'WORD', 'WARD', 'WARP', 'WARM'])
    False
    >>> is_word_word_ladder('TABLE', 'TABLE', ['TABLE'])
    True
    >>> is_word_word_ladder('DAY', 'MEW', ['DAY', 'HAY', 'HEY', 'HEW', 'MEW'])
    True
    >>> is_word_word_ladder('COLD', 'WARM', ['COLD', 'CORD', 'WORD', 'WARD', 'WARM'])
    True
    '''
    # Note how get_words_and_word_relationships() is called below.
    if not ( word_1 in lexicon and word_2 in lexicon and all([word in lexicon for word in candidate_ladder]) and word_1==candidate_ladder[0] and word_2==candidate_ladder[-1]):
        return False

    if not all([dif(candidate_ladder[i],candidate_ladder[i-1]) for i in range(1,len(candidate_ladder))]):
        return False
    if word_1==word_2 and len(candidate_ladder)==1:
        return True
    if  len(candidate_ladder)==2:
        return True
    for k in range(2,len(candidate_ladder)):
        if any([dif(candidate_ladder[i],candidate_ladder[i-k]) for i in range(k,len(candidate_ladder))]):
            return False
    return True

#only different in one letter
def dif(w1,w2):
    if len(w1)!=len(w2):
        return False
    return [w1[i]==w2[i] for i in range(0,len(w1))].count(False) == 1

if __name__ == '__main__':
    # lexicon is a set that records all words in the dictionary.
    # closest_words is a dictionary that maps any word w in the dictionary
    # to the set of all words that differ from w by exactly one letter.
    lexicon, closest_words = get_words_and_word_relationships()
    import doctest
    doctest.testmod()
