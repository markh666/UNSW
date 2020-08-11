; String search
.include "m2560def.inc" 

//.dseg 					; Define a data segment
//.org 0x100 				; Set the starting address of data segment to 0x100
//Cap_string: .byte 5 		; Allocate 5 bytes of data memory (SRAM) to store the string of
							; upper-case letters.


.equ size = 5 				; Define size to be 5
.def counter = r17 			; Define counter to be r17




ldi zl, low(Array<<1) 		; Get the low byte of the address of the array
ldi zh, high(Array<<1) 		; Get the high byte of the address of the array

clr counter 				; counter = 0
ldi r16, 255

loop:	
	lpm r20, z+ 

	cpi r20, 0
	breq end
		
	cpi r20, 'l'			; compare
	breq Equal				; breq if equal

	inc counter
	cpi counter, size
	rjmp loop

Equal: 
	mov r16, r17
	rjmp end			

end:
	rjmp end


.cseg 						; Define a code segment
Array: .db "hello"			; Define the string "hello" which is stored in the program
							; (Flash) memory.
