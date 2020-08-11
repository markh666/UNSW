; Reverse String
; loads a null-terminated string from program memory (lpm Rd, z+)
; pushes it onto the stack, writes out the reversed string into data memory
; st y+, Rr
.include "m2560def.inc"

.org 0x200

.dseg
Reverse: .byte 3

.cseg
String: .db "abc", 0

start:
	ldi r16, low(RAMEND)
	ldi r17, high(RAMEND)
	out SPL, r16
	out SPH, r17
	ldi ZL, low(String<<1)
	ldi ZH, high(String<<1)
	ldi YL, low(Reverse)
	ldi YH, high(Reverse)
	clr r18
	clr r19
pushZero:
	ldi r21, 0
	push r21    ; initially push a zero onto the stack for terminating byte

main:
	lpm r20, Z+ ; load from program memory (the String)
	cpi r20, 0  ; as long as z does not reach terminating byte in string
	brne move
	rjmp stack
	
move:
	push r20
	inc r18
	rjmp main

stack:
	pop r16
	st Y+,r16
	inc r19

	cp r19, r18
	brne stack
	clr r18
	st Y+, r18
	rjmp END
END:
	rjmp END
