//PART B - ARRAY ADDITION
.include "m2560def.inc"
.dseg
.org 0x200
array_3: .byte 5 //reserve space for array_3 in data memory

.cseg

.def array1_1 = r16
.def array1_2 = r17
.def array1_3 = r18
.def array1_4 = r19
.def array1_5 = r20

.def array2_1 = r21
.def array2_2 = r22
.def array2_3 = r23
.def array2_4 = r24
.def array2_5 = r25

ldi array1_1, 1
ldi array1_2, 2
ldi array1_3, 3
ldi array1_4, 4
ldi array1_5, 5

ldi array2_1, 5
ldi array2_2, 4
ldi array2_3, 3
ldi array2_4, 2
ldi array2_5, 1	


ldi xl, low(array_3)
ldi xl, high(array_3)

main:
	add array1_1, array2_1
	add array1_2, array2_2
	add array1_3, array2_3
	add array1_4, array2_4
	add array1_5, array2_5

	st x+, array1_1
	st x+, array1_2
	st x+, array1_3
	st x+, array1_4
	st x+, array1_5

	rjmp end

end: 
	jmp end


