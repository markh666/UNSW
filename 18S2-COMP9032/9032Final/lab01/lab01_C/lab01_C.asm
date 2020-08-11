; Upper case
.include "m2560def.inc"

.equ size =5 				; Define size to be 5
.def counter = r17 			; Define counter to be r17



ldi zl, low(Low_string<<1) 	; Get the low byte of the address of "h"
ldi zh, high(Low_string<<1) ; Get the high byte of the address of "h"
ldi yl, low(Cap_string)
ldi yh, high(Cap_string)
clr counter 				; counter = 0


main:
	
	lpm r20, z+ 			; Load a letter from flash memory
	cpi r20, 123
	brlt branchLOW
	inc counter
	cpi counter, size
	brlt main

branchLOW:
	cpi r20, 97
	brge success
ret

success:
	subi r20, 32 			; Convert it to the capital letter
							; In ASCII, low case letter - 32 = upper case letter
	st y+, r20 				; Store the capital letter in SRAM
ret



loop: nop
	rjmp loop

; tutor asked to leave all the .dseg and .cseg to the end of the program
.dseg 						; Define a data segment
.org 0x200					; Set the starting address of data segment to 0x200
Cap_string: .byte 5 		; Allocate 5 bytes of data memory (SRAM) to store the string of
							; upper-case letters.
.cseg 						; Define a code segment
Low_string: .db "hello"		; Define the string "hello" which is stored in the program
							; (Flash) memory.
							; .db for define constant bytes
