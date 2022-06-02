.global _start
.text
.cpu cortex-m0
.align 2

_start:
	push { r4, lr }
	mov r4, #6
	bl sommig 
	bl print_int
	pop { r4, pc }

sommig:
	push { lr } 
	mov r0, #0
	bl cond
	mov r0, r0
	pop { pc } 

cond:	
	push { lr } 
	cmp r4, #1
	bgt scope
	pop { pc } 

scope:
	add r0, r0, r4
	sub r4, r4, #1
	b loop
	
	
	
