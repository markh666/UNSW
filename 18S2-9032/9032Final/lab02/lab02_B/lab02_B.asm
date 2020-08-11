; Recursive linked-list search
; write a recursive function to find the address of the longest string in the list


.include "m2560def.inc"

.def length = r16
.def nextAddressL = r18
.def nextAddressH = r19
.def currString = r20
.def currLength = r21
.def currAddressL = r22
.def currAddressH = r23
.def largeAddressL = r24
.def largeAddressH = r25

.set NEXT_STRING = 0x0000
.macro defstring ; str
      .set T = PC
      .dw NEXT_STRING << 1
      .set NEXT_STRING = T
      .if strlen(@0) & 1 ; odd length + null byte
            .db @0, 0
	   .else ; even length + null byte, add padding byte 
			.db @0, 0, 0
      .endif
.endmacro

.cseg
rjmp main
defstring "let's"
defstring "try"
defstring "this"
defstring "really"
defstring "long"
defstring "string"
main:
	ldi zl, low(NEXT_STRING<<1)
	ldi zh, high(NEXT_STRING<<1)
	cpi zl,0 
	cpc zh, r0
	breq end
init:
	ldi r28, low(RAMEND)
	ldi r29, high(RAMEND)
	out SPH, r29
	out SPL, r28
	lpm nextAddressL, z+
	lpm nextAddressH, z+
	mov currAddressL, zl
	mov currAddressH, zh
	cpi nextAddressL, 0		; last string in linked list
	cpc nextAddressH, r0
	breq L3					; handle final string in list
	rcall findLargest
end:
	rjmp end
findLargest:
	in r28, SPL
	in r29, SPH
	inc currLength
	lpm currString, z+
	cpi currString, 0
	brne L3
	dec currLength
	rcall isLonger
	rcall init
L3:
	inc currLength
	lpm currString, z+
	cpi currString, 0
	brne L3
	dec currLength
	rcall isLonger
	cpi nextAddressL, 0
	cpc nextAddressH, r0
	brne init
	movw zh:zl, largeAddressH:largeAddressL
	rjmp end
isLonger:
	cp length, currLength
	brge L5
	mov length, currLength
	movw largeAddressH:largeAddressL, currAddressH:currAddressL
	movw zh:zl, nextAddressH:nextAddressL
	clr currLength
	clr currString
	ret
L5:
	movw zh:zl, nextAddressH:nextAddressL
	clr currLength
	clr currString
	ret
