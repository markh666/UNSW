import sys
from random import seed, randrange


try:
    arg_for_seed = int(input('Enter an integer: '))
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
x = randrange(10 ** 10)
sum_of_digits_in_x = 0
L = [randrange(10 ** 8) for _ in range(10)]
first_digit_greater_than_last = 0
same_first_and_last_digits = 0
last_digit_greater_than_first = 0
distinct_digits = [0] * 9
min_gap = 10
max_gap = -1
first_and_last = set()

# REPLACE THIS COMMENT WITH YOUR CODE
sum = int(0);
for i in str(x):
    sum = sum + int(i);
    sum_of_digits_in_x = sum;
#print(sum_of_digits_in_x);

first_digit_greater_than_last = int(0)
for item in L:
    greater = str(item);
    if greater[0] > greater[len(greater)-1]:
        first_digit_greater_than_last += 1;
#print(first_digit_greater_than_last)

last_digit_greater_than_first = int(0)
for item in L:
    smaller = str(item);
    if smaller[0] < smaller[len(smaller)-1]:
        last_digit_greater_than_first += 1;
#print(last_digit_greater_than_first)

same_first_and_last_digits = int(0)
for item in L:
    same = str(item);
    if same[0] == same[len(same)-1]:
        same_first_and_last_digits += 1;
#print(same_first_and_last_digits)

for number in L:
    new_L = [];
    obj = str(number)
    for s in obj:
        if s not in new_L:
            new_L.append(s)
    i = len(new_L)
    distinct_digits[i] += 1
    #print(distinct_digits)
	
fl_list=[]
for item in L:
    myStr = str(item);
    f = myStr[0]
    l = myStr[len(myStr)-1];
    fl = (int(f),int(l))
    fl_list.append(fl)
    if abs(int(f)-int(l)) < min_gap:
        min_gap = abs(int(f)-int(l));
    if abs(int(f)-int(l)) > max_gap:
        max_gap = abs(int(f)-int(l))
#print(fl_list)

max_num = 0
from collections import Counter
fl_count = Counter(fl_list)
for item in fl_list:
    if fl_count[item] >= max_num:
        max_num = fl_count[item]
for item in fl_list:
    if fl_list.count(item) == max_num:
        first_and_last.add(item)
#print(max_num)
#print(first_and_last)


print()
print('x is:', x)
print('L is:', L)
print()
print(f'The sum of all digits in x is equal to {sum_of_digits_in_x}.')
print()
print(f'There are {first_digit_greater_than_last}, {same_first_and_last_digits} '
      f'and {last_digit_greater_than_first} elements in L with a first digit that is\n'
      '  greater than the last digit, equal to the last digit,\n'
      '  and smaller than the last digit, respectively.'
     )
print()
for i in range(1, 9):
    if distinct_digits[i]:
        print(f'The number of members of L with {i} distinct digits is {distinct_digits[i]}.')
print()
print('The minimal gap (in absolute value) between first and last digits\n'
      f'  of a member of L is {min_gap}.'
     )
print('The maximal gap (in absolute value) between first and last digits\n'
      f'  of a member of L is {max_gap}.')
print()
print('The number of pairs (f, l) such that f and l are the first and last digits\n'
      f'of members of L is maximal for (f, l) one of {sorted(first_and_last)}.'
     )
        
