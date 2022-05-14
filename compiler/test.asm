.global start
.section .text
.cpu cortex-m0
.align 1

start:
	push { lr }
	movs r0, #7
	bl odd

odd:
	push { lr }
	cmp r0, #0
	beq ret_3
	sub r0, r0, #1
	bl even
	pop { pc }

ret_3:
	movs r0, #0
	pop { pc }

even:
	push { lr }
	cmp r0, #0
	beq ret_5
	sub r0, r0, #1
	bl odd
	pop { pc }

ret_5:
	movs r0, #1
	pop { pc }

