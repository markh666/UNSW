from copy import deepcopy

print('''Input pairs of the form \'value : number\' \n to indicate that you have \' number \' many banknotes of face \'value\'.\nInput these pairs one per line, with a blank line to indicate end of input.''')

notes = dict()

line = input()
banknotes = []
while line != '':
	note,value = int(line.split(':')[0]), int(line.split(':')[1])
	notes[note] = value
	banknotes.append(note)
	line = input()
banknotes.sort()
amount = input('Input the desired amount:')
amount = int(amount)

fill_in = [[] for i in range(amount + 1)]

for i in range(len(fill_in)):

	# check value greater than one note.
	if any(i - banknotes[a] >= 0 for a in range(len(banknotes))):
		for a in banknotes:
			if i == a:
				fill_in[i] = [{a:1}]
				break
			if {} not in fill_in[i-a]:
				for solution in fill_in[i-a]:
					if a in solution and solution[a] + 1 <= notes[a]:
						new_solution = deepcopy(solution)
						new_solution[a] += 1
						if new_solution not in fill_in[i]:
							fill_in[i].append(new_solution)

					if a not in solution:
						if notes[a] >= 1:
							new_solution = deepcopy(solution)
							new_solution[a] = 1
							if new_solution not in fill_in[i]:
								fill_in[i].append(new_solution)
		
		min_value  = min([sum(x.values()) for x in fill_in[i]])
		sol = []
		for x in fill_in[i]:
			if sum(x.values()) == min_value:
				sol.append(x)
		fill_in[i] = solu
		#fill_in[i] = [a for a in fill_in[i] if sum(a.values()) == min([sum(b.values()) for b in fill_in[i]])]

for i in range(len(fill_in)):
	print(i, fill_in[i])

if not fill_in[-1]:
	print('There is no solution.')

if len(fill_in[-1]) == 1:
	print('There is a unique solution:')
	solution = fill_in[-1][0]
	for i in banknotes:
		if i in solution:
			print(f'${i}: {solution[i]}')

if len(fill_in[-1]) > 1:
	print('There are {len(fill_in[-1])} solutions:')
	for solution in fill_in[-1]:
		for i in banknotes:
			if i in solution:
				print(f'${i}: {solution[i]}')
		print()		






