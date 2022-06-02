.global _start
.text
.cpu cortex-m0
.align 2

_start:
	push {  r4,  lr }
	mov r4, #8
	bl even
	bl putCharacter
	pop {  r4,  pc }

even:
	push { lr }
	mov r0, r4
	cmp r0, #0
	beq .ret_3
	sub  r4,  r4,  #1
	bl odd
	pop { pc }

.ret_3:
	mov r0, #1
	pop { pc }

odd:
	push { lr }
	mov r0, r4
	cmp r0, #0
	beq .ret_5
	sub  r4,  r4,  #1
	bl even
	pop { pc }

.ret_5:
	mov r0, #0
	pop { pc }

