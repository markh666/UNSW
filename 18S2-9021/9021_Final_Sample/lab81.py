

def encode(n):

	digit, start = get_number_digit(n)
	raw_digit = ['0'] * (digit-2) + ['1','1']
	if start == n:
		return ''.join(raw_digit)
	maxi = digit - 3
	while n - start != 0:
		diff = n - start
		print(diff)
		if diff <= maxi:
			raw_digit[diff-1] = '1'
			return ''.join(raw_digit)
		else:
			raw_digit[maxi - 1] = '1'
			start += digit - 4
			maxi -= 2
	return ''.join(raw_digit)

def decode(code):
	if len(code) < 2 or code[-2: ] != '11':
		return 0

	first = 1
	second = 1
	sequence = False
	result = 0
	for c in code[:-1]:
		if c == '1':
			if sequence:
				return 0
			else:
				sequence = True
			result += second
		else:
			sequence = False
		first,second = second , first + second
	return result



def get_number_digit(n):
	first = 1
	second = 1
	digit = 2
	while second <= n:
		digit += 1
		first, second = second, first + second
	return digit - 1, first

# print(get_number_digit(15))
print(encode(8))
print(decode('1000011'))