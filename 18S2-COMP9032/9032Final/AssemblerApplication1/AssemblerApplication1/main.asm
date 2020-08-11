;
; AssemblerApplication1.asm
;
; Created: 2018/11/11 14:22:16
; Author : hanyu
;

.def ah = r17
.def al = r16 ;a = 0x0123
.def bh = r19
.def bl = r18 ;b = 0x0234

//16-bit 加法
ldi ah, 0x01
ldi al, 0x23
ldi bh, 0x02
ldi al, 0x34

add al, bl
adc ah, bh ;当检测到有进位时，自动加一

//16-bit 减法
sub al, bl
sbc ah, bh ;当检测到借位，自动减一

//16-bit 乘法
mul al, bl
movw r17:r16, r1:r0
mulsu ah, bl
add r17, r0
adc r18, r1
mulsu al, bh
add r17, r0
adc r18, r1
sbci r19, 0
muls bh, bh
adc r18, r0
adc r19, r1

//在data memory中储存常量
.dseg
.org 0x200 ;可写可不写（默认就是从200开始）
a: .byte 4
b: .byte 4
c: .byte 1
d: .byte 2

//在code memory中储存变量
.cseg
b: .db "COMP9032", 0
c: .dw 9032

//Translate variables with structured data type
.set  student_ID=0
.set  name=student_ID+4 ;4
.set  WAM=name+20	;24
.set  STUDENT_RECORD_SIZE=WAM+1  ;25
.cseg
s1_value: .dw  LWRD(123456)	;123456>65536也就是low byte的极限
		  .dw  HWRD(123456) ;所以改用LWRD相当于两个low byte
		  .db  "John Smith    ", 0 ;需要用空格填补空位
		  .db  75	;因为只有两个数字，一个byte可以放下，所以用.db，否则用.dw
.dseg
s1:		.byte STUDENT_RECORD_SIZE
s2:		.byte STUDENT_RECORD_SIZE

//
.set  student_ID=0
.set  name=student_ID+4 ;4
.set  WAM=name+20	;24
.set  STUDENT_RECORD_SIZE=WAM+1  ;25
.cseg
start:	
		ldi zh, high(s1_value<<1) ;pointer to student record
		ldi zl, low(s1_value<<1) ;value in the program memory
		ldi yh, high(s1) ;pointer to student record holder
		ldi yl, low(s1) ;in the data memory
		clr r16
load:
		cpi r16, STUDENT_RECORD_SIZE
		brge end
		lpm r10, z+
		st y+, r10
		inc r16
		rjmp load
end:
		rjmp end
s1_value:
		.dw LWRD(123456)
		.dw HWRD(123456)
		.db "John Smith   ",0
		.db 75
.dseg
.org 0x200
s1:		.byte  STUDENT_RECORD_SIZE

//Convert lowercase to uppercase for a string(e.g 'hello')
.equ size=6 ;string length+1
.def counter=r17
.dseg
.org 0x200
ucase_string: .byte size ;size=6
.cseg
	ldi zl, low(lcase_string<<1)
	ldi zh, high(lcase_string<<1)
	ldi yl, low(ucase_string<<1)
	ldi yh, high(ucase_string<<1)
	clr counter
main:
	lpm r20, z+
	subi r20, 32
	st y+, r20
	inc counter
	cpi counter, size
	brlt main
end:
	rjmp end
lcase_string: .db "hello",0
//递归函数
.cseg			;code memory
	rjmp main
n: .db 12		;data in n

main:
	ldi zl, low(n<<1)	;Let Z point to n
	ldi zh, high(n<<1)
	lpm r24, z+			;Actual parameters n is stored in r24
	rcall fib			;Call fib(n)
halt:
	rjmp halt

fib:
	push r16		;Save r16 on the stack
	push yl			;Save Y on the stack
	push yh
	in yl, spl		;让Y充当一个中介，因为SP不能
	in yh, sph		;直接执行语句和数字进行操作
	sbiw y, 1		;let Y point to the top of the stack fram
	out sph, yh		;Update SP so that it points to 
	out spl, yl		;the new stack top

	std y+1, r24	;get the parameter
	cpi r24, 2		;compare n with 2
	brsh L2			;if n!=0 or 1
	ldi r24, 1		;n==0 or 1, return 1
	rjmp L1			;Jump to epilogue

L2:
	ldd r24, y+1	;n>=2, load the actual parameter n
	dec r24			;pass n-1 to the callee
	rcall fib		;call fib(n-1)
	mov r16, r24	;store the return value in r16
	ldd r24, y+1	;load the actual parameter n
	subi r24, 2		;pass n-2 to the callee
	rcall fib		;call fib(n-2)
	add r24, r16	;r24=fib(n-1)+fib(n-2)

L1:
	adiw y, 1		;Deallocate the stack fram for fib()
	out sph, yh		;Restore SP
	out spl, yl		
	pop yh			;Restore Y
	pop yl
	pop  r16		;Restore r16
	ret

//move 10 2-bit integer from program memory to data memory and change the endian type
.def counter = r16
.dseg
.org 0x200
end: .byte 10
.cseg
begin: 
	ldi zl, low(arry<<1)
	ldi zh, high(arry<<1)
	ldi yl, low(end)
	ldi yh, high(end)
	clr counter

load:
	lpm r20, z+
	rcall change
	st y+, r20
	inc counter
	cpi counter, 10
	brlt load
end:
	rjmp end
arry: .db 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

//Find max value of an integer arry
;arry a is stored in FLASH
;use at least one macro
;arry length is 10, each element is a 2-byte signed integer
.def counter = r20
.cseg
A: .dw 2000, 1, -200, 0, 3, 7777, 2, 4, 5, 6

.macro StoreStuff
mov @0, @2
mov @1, @3
.end macro

setup:
	ldi zh, high(A<<1)
	ldi zl, low(A<<1)
loop:
	lpm r18, z+
	lpm r19, z+
	cpc r19, r17
	brlt inccounter
	breq cplow

store:
	StoreStuff r16, r17, r18, r19

cplow:
	cp r18, r16
	brlt inccounter

inccounter:
	inc counter
	cpi counter, 10
	brne loop
end:
	rjmp end