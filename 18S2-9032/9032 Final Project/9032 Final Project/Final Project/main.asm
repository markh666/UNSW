;
; Comp 9032 Final Project.asm
; Cup and Ball Game
; Created: 2018/10/23 15:35:06
; Author : hanyu
; Use AVR lab board to simulate the game: There are four stages in this project
; which are Initial Interface Stage, Shuffle Ball Stage, Make Guess Stage, and Indicate Result Stage
; for more information, please refer the user manual and design manual :)

.include "m2560def.inc"

.def temp = r16
.def temp1 = r17		
.def cup = r18			; cup number
.def lcd = r19			
.def pattern = r20		; register for pattern display
.def score = r21		; the score display on LCD
.def sign1 = r22		; sign for control motor
.def sign2 = r23		; sign for control LED & LCD
.def row = r24			; current row number
.def col = r25			; current column number
.def rmask = r29		; mask for current row during scan
.def cmask = r30		; mask for current column during scan

.equ PORTFDIR = 0xF0	; Setting PF7-4 to output and PF3-0 to input
.equ INITCOLMASK = 0xEF	; scan from the rightmost column
.equ INITROWMASK = 0x01	; scan from the top row
.equ ROWMASK = 0x0F		; for obtaining input from Port D
.equ F_CPU = 16000000
.equ DELAY_1MS = F_CPU / 4 / 1000 - 4 ; 4 cycles per iteration - setup/call-return overhead

;===============
;Marcos for LCD
;===============
.macro do_lcd_command
	ldi lcd, @0			; execute lcd command
	rcall lcd_command
	rcall lcd_wait
.endmacro
.macro do_lcd_data
	ldi lcd, @0
	rcall lcd_data		; display for word
	rcall lcd_wait
.endmacro
.macro do_lcd_rdata
	mov lcd, @0
	subi lcd, -'0'		; change ascii to decimal
	rcall lcd_data
	rcall lcd_wait
.endmacro
.macro lcd_set
	sbi PORTA, @0		; set lcd
.endmacro
.macro lcd_clr			; clear lcd set
	cbi PORTA, @0
.endmacro
;========================
.org 0
		jmp RESET
.org	INT0addr			; address of PB0
		rjmp EXT_INT0
.org	INT1addr			; adress of PB1
		jmp EXT_INT1

;===================
; Initialization
;===================
RESET:						; set portC for LED, portL for Keypad, portE for Motor
; lcd_setup:				; portF and portA for LCD
	ldi lcd, low(RAMEND)	; set stack pointer for LCD
	out SPL, lcd
	ldi lcd, high(RAMEND)
	out SPH, lcd

	ser lcd					; set lcd register
	out DDRF, lcd			
	out DDRA, lcd			
	clr lcd					; set portF and portA
	out PORTF, lcd
	out PORTA, lcd
	clr score
	ldi cup, 3				; set cup number start from 3

; keypad_setup:
	ldi temp, PORTFDIR		; load PORTFDIR into temp1
	sts DDRL, temp			; setting up direction pin A

; motor_setup:
	ser temp				; set PORTE for Motor
	out DDRE, temp

; led_setup:
	ser pattern				; set PortC as output
	out DDRC, pattern		; to display partterns
	ldi pattern, 0b00000100 ; start from the thrid cup

; interrupt_setup:
	ldi temp, (2 << ISC00) | (2 << ISC10)	; set INT0 and INT1 as falling edge sensed interrupts
	sts EICRA, temp
	ser sign1								; set sign1 for motor 
	ser sign2								; set sign2 for LED
	in temp, EIMSK							; store I/O to temp for logical OR
	ori temp, (1 << INT0) | (1 << INT1)		; logical OR operation
	out EIMSK, temp							; store temp register to I/O
	sei										; set the I bit of SREG to become 1 for enable Global interrupt, defalut I bit is 1
	jmp Stage1

EXT_INT0:					; for restart -- RDX4 PB0
	push temp				; push all the conflict register
	in temp, SREG			; save the status register value
	push temp

	clr r28
debounce0:						; debounce
	ldi r26, high(DELAY_1MS)
	ldi r27, low(DELAY_1MS)
	delayloop:				; delay
	sbiw r26:r27, 1
	brne delayloop
	inc r28
	cpi r28, 50				; loop 50 times to delay
	brne debounce0

	cpi sign2, 1			; use sign jump to different stages
	brne change				 
	ldi sign2, 0			; change sign2 from 1 to 0 means jump from stage2 to stage3
continue:
	pop temp				; pop all conflict register
	out SREG, temp			; recover the status register
	pop temp				
	sbi EIFR, INT0
	reti					; return from interrupt to main

change:
	ldi sign2, 1			; change sign2 from 0 to 1 means 
	jmp continue			; jump from stage1 to stage2


EXT_INT1:					; for stop and start -- RDX3 PB1
	push temp				; save register
	in temp, SREG			; save SREG
	push temp
	
	clr r28
debounce1:						; debounce
	ldi r26, high(DELAY_1MS)
	ldi r27, low(DELAY_1MS)
	delayloop1:				; delay
	sbiw r26:r27, 1
	brne delayloop1
	inc r28
	cpi r28, 50				; loop 50 times to delay
	brne debounce1

	ldi sign2, 2			; for restart the game
	pop temp				; for SREG
	out SREG, temp
	pop temp				; for register
	sbi EIFR, INT1
	reti					; return



;================================
;Stage1: Initial Interface
;================================
Stage1:
;display_ready:
	do_lcd_command 0b00111000	; 2x5x7
	do_lcd_command 0b00000001	; clear display
	do_lcd_command 0b00000110	; increment, no display shift
	do_lcd_command 0b00001110	; Cursor on, bar, no blink
		do_lcd_data 'R'
		do_lcd_data 'e'
		do_lcd_data 'a'
		do_lcd_data 'd'			; display the word "Ready..."
		do_lcd_data 'y'
		do_lcd_data '.'
		do_lcd_data '.'
		do_lcd_data '.'
		do_lcd_data ' '
		do_lcd_data 'S'
		do_lcd_data 'c'
		do_lcd_data 'o'			; display the word "Score:"
		do_lcd_data 'r'
		do_lcd_data 'e'
		do_lcd_data ':'
		do_lcd_rdata score		; display the score number
; display on LED
		cpi pattern, 0b1111000	; set the start pattern same like last result
		brlo led_loop			; if last reult is flashing pattern
		subi pattern, 0b11110000 ; minus last four indicator pattern
	led_loop:	 
		out PORTC, pattern
		cpi sign2, 1			; if sign2 is 1, start stage2
		breq Stage2
		rjmp led_loop
;================================
;Stage2: Shuffle Ball
;================================
Stage2:
;display_start:
	ldi sign1, 0xff				; turn on the swich of the motor
	out PORTE, sign1
	do_lcd_command 0b00000001	; clear display
		do_lcd_data 'S'
		do_lcd_data 't'
		do_lcd_data 'a'
		do_lcd_data 'r'			; display the word "Start..."
		do_lcd_data 't'
		do_lcd_data '.'
		do_lcd_data '.'
		do_lcd_data '.'
		do_lcd_data ' '
		do_lcd_data 'S'
		do_lcd_data 'c'
		do_lcd_data 'o'
		do_lcd_data 'r'			; display the word "Score:"
		do_lcd_data 'e'
		do_lcd_data ':'
		do_lcd_rdata score		; display the socre number
;======================================
;Start Shuffle with Dimmed Light
;======================================
shuffle_loop:
	ldi pattern, 0b00000111	; three cups turn on
	out PORTC, pattern
	ldi pattern, 0b00000000	; all lights turn off immediately
	out PORTC, pattern		; use delay to show the dimmed light		
	cpi cup, 3
	breq clear_cup
	inc cup
	nop						; use nop to show the dimmed light
	nop
	nop						; more nop cause darker
	nop
	nop						; less nop cause lighter
	nop		
	cpi sign2, 0			; first time press PB0
	breq Stage3				; stop shuffle and jump to stage3 to make a guess				
	rjmp shuffle_loop

clear_cup:
	ldi cup, 1
	jmp shuffle_loop

;===================================
; Stage3: Scan Keypad, Make a Guess
;===================================
Stage3:
	ldi sign1, 0x00
	out PORTE, sign1
	ldi pattern, 0b00000111	; three cups turn on
	out PORTC, pattern
	ldi pattern, 0b00000000	; all lights turn off immediately
	out PORTC, pattern		; use delay to show the dimmed light	
; scan keypad
	ldi cmask, INITCOLMASK	; initial column mask
	clr col					; initial column
	rjmp colloop			; scan input

colloop:
	cpi col, 3				; only need first 3 column in this project
	breq Stage3				; if all keys are scanned, repeat
	sts PORTL, cmask		; otherwise scan a column
	ldi temp1, 0xFF			; for slowing down the scan operation
	
delay: 
	ldi pattern, 0b00000111	; three cups turn on
	out PORTC, pattern
	ldi pattern, 0b00000000	; all lights turn off immediately
	out PORTC, pattern		; use delay to show the dimmed light
	dec temp1
	brne delay

	lds temp1, PINL			
	andi temp1, ROWMASK		; Get the keypad output value
	cpi temp1, 0xF			; check if any row is low
	breq nextcol			

	ldi rmask, INITROWMASK	; initialise for row check
	clr row
rowloop:
	ldi pattern, 0b00000111	; three cups turn on
	out PORTC, pattern
	ldi pattern, 0b00000000	; all lights turn off immediately
	out PORTC, pattern		; use delay to show the dimmed light

	cpi row, 1				; only need first row in this project
	breq nextcol			; the row scan is over, start scan next column
	mov temp, temp1
	and temp, rmask		    ; check un-masked bit
	breq Stage4				; if bit is clear, the key is pressed

	inc row					; else move to the next row
	lsl rmask
	jmp rowloop

nextcol:
	ldi pattern, 0b00000111	; three cups turn on
	out PORTC, pattern
	ldi pattern, 0b00000000	; all lights turn off immediately
	out PORTC, pattern		; use delay to show the dimmed light
	lsl cmask				; increase column number
	inc col					; start scan next column
	jmp colloop

;=====================================
; Stage4: Compare and Indicate Result
;=====================================
Stage4:
;record_guess:
	clr temp1			; clear guess to 0
	mov temp1, col		; input the guess number but column number
	inc temp1			; needs add 1 to real guess number
	
checkresult:
	cp temp1, cup		; check result is correct or wrong 
	brne wrong
	subi score, -1		; if correct, add 1 score
do_lcd_command 0b00000001; clear display
	do_lcd_data 'S'
	do_lcd_data 't'
	do_lcd_data 'a'
	do_lcd_data 'r'		; display the word "Start..."
	do_lcd_data 't'
	do_lcd_data '.'
	do_lcd_data '.'
	do_lcd_data '.'
	do_lcd_data ' '
	do_lcd_data 'S'
	do_lcd_data 'c'
	do_lcd_data 'o'
	do_lcd_data 'r'		; display the word "Score:"
	do_lcd_data 'e'
	do_lcd_data ':'
	do_lcd_rdata score	; display the socre number
	
	cpi cup, 1			; if correct
	breq flashing1
	cpi cup, 2			; check the ball poisition and display it
	breq flashing2
	cpi cup, 3
	breq flashing3

wrong:					; jump to wrong result part
	jmp guesswrong
;==============================
;LED Flashing if Guess Correct
;==============================
flashing1:
	cpi sign2, 2				; if pressed restart botton
	breq End					; restart the game
	ldi pattern, 0b00000001		; the result pattern
	out PORTC, pattern
	rcall sleep_500ms			; dispaly half second
	ldi pattern, 0b11110001		; flashing
	out PORTC, pattern
	rcall sleep_500ms
	rjmp flashing1

flashing2:
	cpi sign2, 2				; if pressed restart botton
	breq End					; restart the game
	ldi pattern, 0b00000010		; the result pattern
	out PORTC, pattern
	rcall sleep_500ms			; dispaly half second
	ldi pattern, 0b11110010		; flashing
	out PORTC, pattern
	rcall sleep_500ms
	rjmp flashing2

flashing3:
	cpi sign2, 2				; if pressed restart botton
	breq End					; restart the game
	ldi pattern, 0b00000100		; the result pattern
	out PORTC, pattern
	rcall sleep_500ms			; dispaly half second
	ldi pattern, 0b11110100		; flashing
	out PORTC, pattern
	rcall sleep_500ms
	rjmp flashing3

End:
	ser sign1					; reset the sign
	ser sign2					; for LED and Motor
	jmp Stage1					; return to stage1

guesswrong:
	subi score, 1				; if guess wrong, decrease score
	cpi score, 1				; if the score is less or equal 0
	brlt zero					; reset to the initial start status
	do_lcd_command 0b00000001	; clear display
	do_lcd_data 'S'
	do_lcd_data 't'
	do_lcd_data 'a'
	do_lcd_data 'r'				; display the word "Start..."
	do_lcd_data 't'
	do_lcd_data '.'
	do_lcd_data '.'
	do_lcd_data '.'
	do_lcd_data ' '
	do_lcd_data 'S'
	do_lcd_data 'c'
	do_lcd_data 'o'
	do_lcd_data 'r'				; display the word "Score:"
	do_lcd_data 'e'
	do_lcd_data ':'
	do_lcd_rdata score			; display the socre number
	cpi cup, 1					; if wrong,
	breq result1
	cpi cup, 2					; check the ball poisition and display it
	breq result2
	cpi cup, 3
	breq result3

zero:
	jmp RESET					; if the score less or equal than zero
								; jump to reset part clear the score
;=======================================
;LED Only Display Result if Guess Wrong
;=======================================
result1:
	cpi sign2, 2				; if pressed restart botton
	breq Over					; restart the game
	ldi pattern, 0b00000001		; the result pattern
	out PORTC, pattern
	rjmp result1

result2:
	cpi sign2, 2				; if pressed restart botton
	breq Over					; restart the game
	ldi pattern, 0b00000010		; the result pattern
	out PORTC, pattern
	rjmp result2

result3:
	cpi sign2, 2				; if pressed restart botton
	breq Over					; restart the game
	ldi pattern, 0b00000100		; the result pattern
	out PORTC, pattern
	rjmp result3

Over:
	ser sign1					; reset the sign
	ser sign2					; for LED and Motor
	jmp Stage1					; return to stage1


;=================================
; Send a command to the LCD (lcd)
;=================================
lcd_command:			
	out PORTF, lcd
	rcall sleep_1ms
	lcd_set LCD_E		; commond for LCD
	rcall sleep_1ms
	lcd_clr LCD_E
	rcall sleep_1ms		; rcall sleep function between the gap
	ret
lcd_data:
	out PORTF, lcd
	lcd_set LCD_RS
	rcall sleep_1ms
	lcd_set LCD_E		; load data to LCD
	rcall sleep_1ms
	lcd_clr LCD_E
	rcall sleep_1ms		; rcall sleep function between the gap
	lcd_clr LCD_RS
	ret
lcd_wait:
	push lcd			; wait function for lcd
	clr lcd				; to make sure everything can display on lcd
	out DDRF, lcd
	out PORTF, lcd
	lcd_set LCD_RW
lcd_wait_loop:			; enter the wait loop
	rcall sleep_1ms
	lcd_set LCD_E		
	rcall sleep_1ms		; rcall sleep function between the gap
	in lcd, PINF
	lcd_clr LCD_E		
	sbrc lcd, 7
	rjmp lcd_wait_loop
	lcd_clr LCD_RW
	ser lcd
	out DDRF, lcd
	pop lcd
	ret
.equ LCD_RS = 7
.equ LCD_E = 6		; set each pin of LCD Contrl
.equ LCD_RW = 5
.equ LCD_BE = 4

;================
;Sleep Functions
;================
sleep_1ms:
	push r24					; sleep functions
	push r25
	ldi r25, high(DELAY_1MS)
	ldi r24, low(DELAY_1MS)
delayloop_1ms:					; decrese until 1ms pass
	sbiw r25:r24, 1
	brne delayloop_1ms
	pop r25
	pop r24
	ret

sleep_5ms:						; sleep for 5ms
	rcall sleep_1ms
	rcall sleep_1ms
	rcall sleep_1ms				; recall sleep 1ms functions 5 times
	rcall sleep_1ms
	rcall sleep_1ms
	ret

sleep_25ms:						; sleep for 25ms
	rcall sleep_5ms
	rcall sleep_5ms
	rcall sleep_5ms				; recall sleep 5ms functions 5 times
	rcall sleep_5ms
	rcall sleep_5ms
	ret

sleep_100ms:					; sleep for 100ms
	rcall sleep_25ms
	rcall sleep_25ms
	rcall sleep_25ms			; recall sleep 25ms functions 4 times
	rcall sleep_25ms
	ret

sleep_500ms:					; sleep for 500ms
		rcall sleep_100ms
		rcall sleep_100ms
		rcall sleep_100ms		; recall sleep 100ms functions 5 times
		rcall sleep_100ms
		rcall sleep_100ms
		ret


