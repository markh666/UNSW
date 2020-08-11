# Prompts the user for two numbers, say available_digits and desired_sum, and
# outputs the number of ways of selecting digits from available_digits
# that sum up to desired_sum.


import sys


def get_subsequence(input, n):
	if n == 0:
		return 1
	if len(input) == 1 :
		if int(input) != n:
			return 0
		else:
			return 1
	a = int(input[0])
	return get_subsequence(input[1:], n - a) + get_subsequence(input[1:] , n) 
	# if n == 0:
	# 	return 1
	# if len(input) == 1:
	# 	if int(input) != n:
	# 		return 0
	# if len(input) == 1 and int(input) == n:
	# 	return 1
	# a = int(input[0])
	# return get_subsequence(input[1:], n - a) + get_subsequence(input[1:],n)
# Insert your code here

input_str = input('Input a number that we will use as available digits: ')
n = input('Input a number that represents the desired sum: ')

result = get_subsequence(input_str, int(n))
if result == 0:
	print(f'There is no solution.')	
if result == 1:
	print(f'There is a unique solution.')
if result > 1:
	print(f'There are {result} solutions.')