//PART A - 16 BIT ADDITION

ldi r16, low(40960)		; r16 <- low(40960)
ldi r17, high(40960)	; r17 <- high(40960)

ldi r18, low(2730)		; r18 <- low(2730)
ldi r19, high(2730)		; r19 <- high(2730)

add r16, r18			; r16 <- low(40960) + low(2730)
mov r20, r16			; r20 <- r16
adc r17, r19			; r17 <- high(40960) + high(2730)
mov r21, r17			; r21 <- r17				;
