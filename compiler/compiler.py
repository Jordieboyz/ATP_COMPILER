from Parser import get_func_def
from tokens import Number, Variable, Is, Add, Minus, Times, Divide
from Statements import Function, MathStatement, IfStatement, \
                        ReturnFunc, ConditionsLoop, Scope, Output



class cortex:
    START_LABEL = 'start'
    
    class instructions:
        PUSH =      'push'
        POP =       'pop'
        BRANCHL =   'bl'
        BRANCH =    'b'
        MOV =       'mov'
        STORE=      'str'
        CMP=        'cmp'
        ADD=        'add'
        SUB=        'sub'
        MULS=        'muls'
        UDIV=       'udiv'
        
    class registers:
        RETURNREG = 'r0'
        R1 = 'r1'
        R2 = 'r2'
        R3 = 'r3'
        R4 = 'r4'
        R5 = 'r5'
        R6 = 'r6'
        R7 = 'r7'
        R8 = 'r8'
        LR = 'lr'
        PC = 'pc'
        

maths : dict() = {
    Add               : cortex.instructions.ADD,
    Minus        : cortex.instructions.SUB,
    Is          : cortex.instructions.MOV,
    Times           : cortex.instructions.MULS,
    Divide        : cortex.instructions.UDIV
}

spacing = lambda part, s = ' ' : part+s
imm = lambda  number: '#' + str(number)
reg = lambda reg : 'r' + str(reg)

# Produce an instruction string. f.e. add r0, r0, #0
def get_instruction_string(instr, dest, val = None):
    if instr == cortex.instructions.PUSH or instr == cortex.instructions.POP:
        return
    elif instr == cortex.instructions.ADD or instr == cortex.instructions.SUB or \
        instr == cortex.instructions.MULS or instr == cortex.instructions.UDIV:
        return spacing(instr) + spacing(dest, ', ') + spacing(dest, ', ') + spacing(val)
    
    elif instr[0] == cortex.instructions.BRANCH or instr == cortex.instructions.BRANCHL:
        return spacing(instr) + spacing(dest)
    return spacing(instr) + spacing(dest, ', ') + spacing(val)


def start_compiling( ast, funcDecl, varList, labelName, routineDict, last):

    # This function returns a new list where one or more items are replaced 
    # with another value 
    def replace(oldVal, newVal, oldList, newlist = []):
        if not oldList:
            return newlist
        
        item, *rest = oldList
        
        if item == oldVal:
            newlist.append(newVal)
        else:
            newlist.append(item)
        
        return replace(oldVal, newVal, rest, newlist)
    

    if not ast:
        if routineDict[labelName]:
            if routineDict[labelName][-1][:3] != cortex.instructions.PUSH:
                if labelName[0] != '.':
                    routineDict[labelName].append(
                            routineDict[labelName][0].replace(
                                            cortex.instructions.PUSH, 
                                            cortex.instructions.POP).replace(
                                                            cortex.registers.LR, 
                                                            cortex.registers.PC)
                                                )
                else:
                    routineDict[labelName].append(cortex.instructions.POP + " { pc }" )
        return routineDict

    
    statement, *rest = ast

    if labelName not in routineDict:
        if labelName[:3] == 'cl_':
            routineDict[labelName] = ["push { lr }"]
        else:
           routineDict[labelName] = []

    # Use r0 as return-register. at the end of a function, store the result in r0.
    if isinstance(statement, ReturnFunc):
        
        # reuturn f.e. True or false, or just a constant number in general
        if isinstance( statement.rvalue, Number):
            routineDict[labelName].append( 
                                        get_instruction_string(
                                                cortex.instructions.MOV, 
                                                cortex.registers.RETURNREG, 
                                                imm(statement.rvalue.content)
                                                )
                                        )
            
        # Return a variable, check where the variable is in the var_list 
        # and use that register to move to r0
        if isinstance( statement.rvalue, Variable):
            if statement.rvalue.content in varList:
                routineDict[labelName].append( 
                                            get_instruction_string(
                                                cortex.instructions.MOV, 
                                                cortex.registers.RETURNREG, 
                                                reg(
                                                 str(
                                                  varList.index(
                                                    statement.rvalue.content
                                                 )
                                                )
                                               )
                                              )
                                             )
        
        # return a function result, we need to declare the function first 
        if isinstance(statement.rvalue, Function):
            
            # create branch to function
            routineDict[labelName].append(
                                            get_instruction_string( 
                                                    cortex.instructions.BRANCHL, 
                                                    statement.rvalue.funcname
                                                    )
                                            )
            
            func_statements = get_func_def(funcDecl, statement.rvalue.funcname)                    
            
            # for every start of a function, we need to push the link regsiter
            if statement.rvalue.funcname not in routineDict:
                routineDict[statement.rvalue.funcname] = ["push { lr }"]
                
                # The first element in the func_statements is the "Function" Statement, so this needs to be ignored
                # We also need to replace the global variable names with the given parameters of the function in the 
                # registers.
                start_compiling( func_statements.statements[1:], funcDecl, 
                                    replace( statement.rvalue.func_params[0].content, 
                                             func_statements.statements[0].func_params[0].content, 
                                             varList
                                    ), 
                                    statement.rvalue.funcname, routineDict,  
                                    last
                                )
        
    # Output the number which is on r0 at this moment            
    elif isinstance( statement, Output):
            routineDict[labelName].append(
                                        get_instruction_string( 
                                                cortex.instructions.BRANCHL, 
                                                'put_number'
                                                )
                                        )


    # perform a comparison which will update the flags.        
    elif isinstance( statement, IfStatement):
        if isinstance( statement.lvalue, Variable):
            if isinstance( statement.rvalue, Number):
                routineDict[labelName].append(
                                get_instruction_string(
                                    cortex.instructions.CMP,
                                    reg(str(varList.index(statement.lvalue.content))),
                                    imm(statement.rvalue.content)
                                    )
                                )
                                                
            if isinstance( statement.rvalue, Variable):
                if statement.rvalue.content in varList:
                    routineDict[labelName].append(
                                                    get_instruction_string(
                                                            cortex.instructions.CMP,
                                                            reg(str(varList.index(statement.lvalue.content))),
                                                            reg(str(varList.index(statement.rvalue.content)))
                                                            )
                                                    )
            last = statement
            
            
           
    # perform a mathimatical instruction
    elif isinstance( statement, MathStatement):
        if isinstance( statement.lvalue, Variable ):
            if statement.lvalue.content in varList:
                if isinstance( statement.rvalue, Number):
                    if isinstance( statement.operator, Is):
                        routineDict[labelName].append(
                                 get_instruction_string(
                                    cortex.instructions.MOV,
                                    reg(varList.index(statement.lvalue.content)),
                                    imm(statement.rvalue.content)
                                )
                            )
                    elif isinstance( statement.operator, ( Add, Minus, Times, Divide ) ):
                        routineDict[labelName].append(
                                 get_instruction_string(
                                    maths[type(statement.operator)],
                                    reg(varList.index(statement.lvalue.content)),
                                    imm(statement.rvalue.content)
                                )
                        ) 
                        
                elif isinstance( statement.rvalue, Variable ):
                    if statement.rvalue.content in varList:
                        if isinstance( statement.operator, Is):
                            routineDict[labelName].append(
                                     get_instruction_string(
                                        cortex.instructions.MOV,
                                        reg(varList.index(statement.lvalue.content)),
                                        reg(varList.index(statement.rvalue.content)),
                                    )
                                )
                        elif isinstance( statement.operator, ( Add, Minus, Times, Divide ) ):
                            routineDict[labelName].append(
                                     get_instruction_string(
                                        maths[type(statement.operator)],
                                        reg(varList.index(statement.lvalue.content)),
                                        reg(varList.index(statement.rvalue.content))
                                    )
                            ) 
                        
            # statements.lvalue is not in varlist
            else:
                # is it a local var?
                if labelName != cortex.START_LABEL:
                    if '' in varList:
                        varList[varList[:4].index('')] = statement.lvalue.content
                    else:
                        varList.append(statement.lvalue.content)
                        
                    routineDict[labelName].append(
                                 get_instruction_string(
                                    cortex.instructions.MOV,
                                    reg(str(varList.index(statement.lvalue.content))),
                                    imm(statement.rvalue.content)
                                    )
                            )
                # it is a global var.
                else:
                    varList.append(statement.lvalue.content)
                    routineDict[labelName].append(
                                    get_instruction_string(
                                            cortex.instructions.MOV,
                                            reg(str(varList.index(statement.lvalue.content))),
                                            imm(statement.rvalue.content)
                                            )
                                    )

        
    elif isinstance( statement, ConditionsLoop):
        routineDict[labelName].append(
                                        get_instruction_string(
                                                cortex.instructions.BRANCHL,
                                                "cl_" + str(len(routineDict))
                                                )
                                        )
        start_compiling([statement.expr, statement.loop], funcDecl, varList, "cl_" + str(len(routineDict)), routineDict, statement)


        
        
    # Create a new scope and so a  new label for f.e. a subroutine
    elif isinstance(statement, Scope):
        if isinstance(last, IfStatement):
            routineDict[labelName].append(
                                            get_instruction_string(
                                                    cortex.instructions.BRANCH + last.operator.expr[:2],
                                                    ".rt_" + str(len(routineDict))
                                                    )
                                            )
            start_compiling(statement.statements, funcDecl, varList, ".rt_" + str(len(routineDict)), routineDict, last)
            rt_label = ".rt_" + str(len(routineDict)-1)
            if labelName[:3] == 'cl_':
                if routineDict[rt_label][-1] == "pop { pc }":
                    routineDict[rt_label].remove(routineDict[rt_label][-1])
                    routineDict[rt_label].append(
                                                    get_instruction_string(
                                                            cortex.instructions.BRANCH,
                                                            labelName
                                                            )
                                                    )

    
    return start_compiling(rest, funcDecl, varList, labelName, routineDict, statement)
    

# Essentially we just return the amount of global variables 
# So we know what registers to safen
def get_reg_init_string( ast, reg_list = ["", "", "", ""], push_str = " " ):
    if not ast:
        return cortex.instructions.PUSH + " {" + push_str + " lr }"
    
    statement, *rest = ast
    
    if isinstance( statement, MathStatement):
        if isinstance( statement.operator, Is):
            if isinstance( statement.lvalue, Variable):
                if statement.lvalue.content not in reg_list:
                    reg_list.append(statement.lvalue.content)
                    push_str += spacing(reg(str(len(reg_list)-1)), ', ')
                
    return get_reg_init_string(rest, reg_list, push_str)
        
    
def format_file(rDict, openedFile, initLabel = "init"):
    for init in rDict[initLabel]:
        openedFile.write(init + "\n")
    
    for item in rDict:
        if item != initLabel:
            openedFile.write(item + ":\n")
            for step in rDict[item]:
                openedFile.write("\t" + step + "\n")
        openedFile.write("\n")
        
def compile_as(ast, funcDecl, filename):
    # We dont use the 'scratch registers to store 'global' variables
    # So, we need to make sure they won't be used until needed
    startRegs = ["", "", "", ""]
    initLabel = "init"
    fileNameWithoutExtention = filename[filename.index('/')+1:-4]
    cortex.START_LABEL = filename[filename.index('/')+1:-4]
    
    routineDict = start_compiling(
                        ast, 
                        funcDecl,                                            \
                        startRegs,                                           \
                        fileNameWithoutExtention,                          \
                        { initLabel : [],                                    \
                             fileNameWithoutExtention : 
                                    [get_reg_init_string(ast)] }, \
                        None)
    
    routineDict[initLabel].append(".global " +                              \
                                        fileNameWithoutExtention )         
    routineDict[initLabel].append(".text")
    routineDict[initLabel].append(".cpu cortex-m0")
    routineDict[initLabel].append(".align 2")
    

    FILE=open(filename, "w")
    format_file(routineDict, FILE, initLabel)
    FILE.close()
