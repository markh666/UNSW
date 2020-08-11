
def merge_two(first, second, large):

	if not first:
		if second == large:
			return True
		else:
			return False
	if not second:
		if first == large:
			return True
		else:
			return False
	if first[0] == large[0] and second[0] == large[0]:
		return merge_two(first[1:], second, large[1:]) or merge_two(first, second[1:], large[1:])
	if first[0] == large[0]:
		return merge_two(first[1:], second, large[1:])
	if second[0] == large[0]:
		return merge_two(first, second[1:], large[1:])
	return False

ranks = 'first', 'second', 'third'
strings = [input(f'Please input the {rank} string: ') for rank in ranks]

largest_string = strings[0]

largest = 0
for i in range(len(strings)):
	if len(strings[i]) > len(largest_string):
		largest_string = strings[i]
		largest = i

strings.remove(largest_string)

first = strings[0]
second = strings[1]

if len(largest_string) != len(first) + len(second):
	print('No solution')
else:
	if merge_two(first,second, largest_string):
		print(f'The {ranks[largest]} string can be obtained by merging the other two.') 
	else:
		print('No solution')