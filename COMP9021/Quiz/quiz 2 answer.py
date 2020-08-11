import sys
from random import seed, randint
from math import gcd


try:
    arg_for_seed, length, max_value = input('Enter three strictly positive integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, length, max_value = int(arg_for_seed), int(length), int(max_value)
    if arg_for_seed < 1 or length < 1 or max_value < 1:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randint(1, max_value) for _ in range(length)]
print('Here is L:')
print(L)
print()

size_of_simplest_fraction = None
simplest_fractions = []
size_of_most_complex_fraction = None
most_complex_fractions = []
multiplicity_of_largest_prime_factor = 0
largest_prime_factors = []

from fractions import Fraction
fraction_list=[]

for n in L:
    for d in L:
        f = Fraction(n,d)
        if f == 1:
            fraction_list.append("1/1")
        if f < 1:
            fraction_list.append(str(f))
fraction_list = set(fraction_list)
#print(fraction_list)

len_list = []
for i in fraction_list:
    f = Fraction(i)
#    print(f.numerator)
#    print(f.denominator)
    lenth = len(str(i))-1
    len_list.append(lenth)
size_of_simplest_fraction = min(len_list)
size_of_most_complex_fraction = max(len_list)
#print(size_of_simplest_fraction)
#print(size_of_most_complex_fraction)

for i in fraction_list:
    if len(str(i))-1 == size_of_simplest_fraction:
        simplest_fractions.append(i)
    if len(str(i))-1 == size_of_most_complex_fraction:
        most_complex_fractions.append(i)

simplest_fractions = sorted(simplest_fractions, key=Fraction)
most_complex_fractions = sorted(most_complex_fractions, key=Fraction, reverse=True)
#print(simplest_fractions)
#print(most_complex_fractions)

a = []
b = []
for i in simplest_fractions:
    numerator = int(i.split('/')[0])
    denominator = int(i.split('/')[1])
    a.append((numerator,denominator))

for i in most_complex_fractions:
    numerator = int(i.split('/')[0])
    denominator = int(i.split('/')[1])
    b.append((numerator,denominator))
    
simplest_fractions = a
most_complex_fractions = b

#print(simplest_fractions)
#print(most_complex_fractions)

max_Arr = []
def prime_factors(n):
    if n == 0 | n == 1: 
        return []
    prime_list= []
    i = 2
    while i <= n:
        if n % i == 0:
            prime_list.append(i)
            n = n / i
            i = 2
            continue
        i += 1
    set_list = set(prime_list)
    max_count = 0
    for item in prime_list:
        if prime_list.count(item) > max_count:
            max_count = prime_list.count(item)
    for item in set_list:
        if prime_list.count(item) == max_count:
            max_Arr.append([item,max_count])
    return max_Arr

latter_denominators = []
for n in most_complex_fractions:
    latter_denominators.append(n[1])
#print(latter_denominators)

max_Arr = []
for i in latter_denominators:
    prime_factors(i)
    #print(max_Arr)
highest_multiplicity_of_prime_factors = max_Arr
#print(highest_multiplicity_of_prime_factors)

primes = []
times = 0
for item in max_Arr:
    if item[1] > times:
        times = item[1]
for item in max_Arr:
    if item[1] == times:
        primes.append(item[0])
largest_prime_factors = set(primes)
multiplicity_of_largest_prime_factor = times
#print(multiplicity_of_largest_prime_factor)
#print(largest_prime_factors)
largest_prime_factors = sorted(largest_prime_factors)
#print(largest_prime_factors)
# REPLACE THIS COMMENT WITH YOUR CODE

print('The size of the simplest fraction <= 1 built from members of L is:',
      size_of_simplest_fraction
     )
print('From smallest to largest, those simplest fractions are:')
print('\n'.join(f'    {x}/{y}' for (x, y) in simplest_fractions))
print('The size of the most complex fraction <= 1 built from members of L is:',
      size_of_most_complex_fraction
     )
print('From largest to smallest, those most complex fractions are:')
print('\n'.join(f'    {x}/{y}' for (x, y) in most_complex_fractions))
print("The highest multiplicity of prime factors of the latter's denominators is:",
      multiplicity_of_largest_prime_factor
     )
print('These prime factors of highest multiplicity are, from smallest to largest:')
print('   ', largest_prime_factors)
        
        
