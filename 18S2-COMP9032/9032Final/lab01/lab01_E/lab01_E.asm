; Array sort
.include "m2560def.inc"

.equ SIZE = 8
.def COUNTER = r24
.def COUNTCORRECT = r25

clr r24
clr r25

ldi r16, 7
ldi r17, 4
ldi r18, 5
ldi r19, 1
ldi r20, 6
ldi r21, 3
ldi r22, 2

	ldi ZL, low(arr) ;ZH+ZL=Z
	ldi ZH, high(arr)

	st Z+, r16
	st Z+, r17
	st Z+, r18
	st Z+, r19
	st Z+, r20
	st Z+, r21
	st Z+, r22

restart:
	ldi ZL, low(arr) ;ZH+ZL=Z
	ldi ZH, high(arr)
	clr r24
	clr r25
	rjmp compareLoop

compareLoop:
	inc COUNTER
	ld r26,Z+ 
	ld r27,Z
	cp r26, r27
	brlo lowerSwap
	brge higherCorrect

lowerSwap:
	st -Z, r27 
	adiw Z, 1
	st Z, r26
	cpi COUNTER, SIZE
	breq restart
	brlt compareLoop
	
higherCorrect:
	inc COUNTCORRECT
	cpi COUNTCORRECT, SIZE
	breq end
	brlt compareLoop


end:
	rjmp end

.dseg
arr: .byte SIZE
