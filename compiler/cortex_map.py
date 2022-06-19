from tokens import Is, Add, Minus, Times


class cortex:
    START_LABEL = 'start'
    
    class instructions:
        PUSH    = 'push'
        POP     = 'pop'
        BRANCHL = 'bl'
        BRANCH  = 'b'
        MOV     = 'mov'
        STORE   = 'str'
        LOAD    = 'ldr'
        CMP     = 'cmp'
        ADD     = 'add'
        SUB     = 'sub'
        MUL     = 'mul'
      
    class registers:
        RETURNREG   = 'r0'
        R1          = 'r1'
        R2          = 'r2'
        R3          = 'r3'
        R4          = 'r4'
        R5          = 'r5'
        R6          = 'r6'
        FP          = 'r7'
        SP          = 'sp'
        LR          = 'lr'
        PC          = 'pc'
        
        

maths : dict() = {
    Add     : cortex.instructions.ADD,
    Minus   : cortex.instructions.SUB,
    Is      : cortex.instructions.MOV,
    Times   : cortex.instructions.MUL,
}


spacing = lambda part, s = ' ' : part+s
mem_adr = lambda offset, fp = cortex.registers.FP : '[ ' + spacing(fp, ', ') + offset +' ]'
  
# Produce an instruction string. f.e. add r0, r0, #0
def get_instruction_string(instr, dest, val = None):
    if instr == cortex.instructions.PUSH or instr == cortex.instructions.POP:
        return
    
    elif instr == cortex.instructions.ADD or instr == cortex.instructions.SUB or  instr == cortex.instructions.MUL:
        return spacing(instr) + spacing(dest, ', ') + spacing(dest, ', ') + spacing(val)
    
    elif instr == cortex.instructions.STORE or instr == cortex.instructions.LOAD:
        return spacing(instr) + spacing(dest, ', ') + mem_adr(val) 
    
    elif instr[0] == cortex.instructions.BRANCH or instr == cortex.instructions.BRANCHL:
        return spacing(instr) + spacing(dest)
    
    return spacing(instr) + spacing(dest, ', ') + spacing(val)
