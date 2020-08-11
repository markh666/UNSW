import sys
import re

try:
    encoded_set = int(input('Input a nonnegative integer: '))
    if encoded_set < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

def display(L):
    print('{', end = '')
    print(', '.join(str(e) for e in L), end = '')
    print('}')

def binary(encoded_set):
    binary_set = ''
    if encoded_set:
        binary_set = binary(encoded_set // 2)
        return binary_set + str(encoded_set % 2)
    else:
        return binary_set

def decode(encoded_set):
    a = binary(encoded_set)[:]
    index_list = [i.start() for i in re.finditer('1', a[::-1])]
    code_list = []
    i = 0
    while i < len(index_list):
        if index_list[i] % 2 == 0:
            code = index_list[i] / 2
            code_list.append(int(code))
            i += 1
            continue
        else:
            code = -(index_list[i] / 2 + 1)
            code_list.append(int(code))
            i += 1
    code_list = sorted(code_list)
    return code_list

def code_derived_set(encoded_set):
    i = 0
    add_list = []
    while i < len(decode(encoded_set)):
        num = sum(decode(encoded_set)[:i+1])
        add_list.append(int(num))
        i += 1
    add_list = sorted(add_list)
    changed_list = []
    l = 0
    while l <len(add_list):
        if add_list[l] < 0:
            h = abs(add_list[l]) * 2 - 1
            changed_list.append(h)
            l += 1
            continue
        else:
            h = add_list[l] * 2
            changed_list.append(h)
            l += 1
    changed_list = sorted(changed_list)

    final_num = []
    z = 0
    while z < len(changed_list):
        r = 2 ** changed_list[z]
        final_num.append(r)
        z += 1
    derived = sum(final_num)
    return derived

print('The encoded set is: ', end = '')
display(decode(encoded_set))
code_of_derived_set = code_derived_set(encoded_set)
print('The derived set is encoded as:', code_of_derived_set)
print('It is: ', end = '')
display(decode(code_of_derived_set))
