.global start
.text
.align 4

start:
   push { r5, lr }
   ldr r0, =msg
   mov  r5, r0
loop: 
   ldrb r0, [ r5 ]
   add  r0, r0, #0
   beq  done
   bl putCharacter
   add  r5, r5, #1
   b    loop
done: 
   pop  { r5, pc }

.data 
msg: 
.asciz "hELLO WORLD, THE answeerefeawfdf2134325r IS 42! @[]`{}~\n"
