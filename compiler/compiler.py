from Parser import get_func_def
from tokens import Number, Variable, Is, Add, Minus
from Statements import Function, MathStatement, IfStatement, \
                        ReturnFunc, ConditionsLoop, Scope, Output

class cortex:
    START_LABEL = 'start'
    
    class instructions:
        PUSH =      'push'
        POP =       'pop'
        BRANCHL =   'bl'
        BRANCH =    lambda expr = None : str('b' + expr) if expr is not None else 'b'
        MOV =      'mov'
        STORE=      'str'
        CMP=        'cmp'
        ADD=        'add'
        SUB=        'sub'
        
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
        

spacing = lambda part, s = ' ' : part+s
imm = lambda  number: '#' + number
reg = lambda reg : 'r' + reg

def get_instruction_string(instr, dest, val = None):
    if instr == cortex.instructions.PUSH or instr == cortex.instructions.POP:
        return
    elif instr == cortex.instructions.ADD or instr == cortex.instructions.SUB:
        return spacing(instr) + spacing(dest, ', ') + spacing(dest, ', ') + spacing(val)
    
    elif instr[0] == 'b' or instr == cortex.instructions.BRANCHL:
        return spacing(instr) + spacing(dest)
    return spacing(instr) + spacing(dest, ', ') + spacing(val)


def start_compiling( ast, func_decl, var_list, label_name, routine_dict, last):

    # this function returns a new list where one or more items are replaced with another value (new becomes old) 
    def repl(old, new, iList, new_list = []):
        if not iList:
            return new_list
        
        item, *rest = iList
        
        if item == old:
            new_list.append(new)
        else:
            new_list.append(item)
        
        return repl(old, new, rest, new_list)
    

    if not ast:
        if routine_dict[label_name]:
            if routine_dict[label_name][-1][:3] != cortex.instructions.PUSH:
                if label_name[0] != '.':
                    routine_dict[label_name].append(
                            routine_dict[label_name][0].replace(
                                            cortex.instructions.PUSH, 
                                            cortex.instructions.POP).replace(
                                                            cortex.registers.LR, 
                                                            cortex.registers.PC)
                                                )
                else:
                    routine_dict[label_name].append("pop { pc }" )
        return routine_dict

    
    statement, *rest = ast

    if label_name not in routine_dict:
        if label_name[:3] == 'cl_':
            routine_dict[label_name] = ["push { lr }"]
        else:
           routine_dict[label_name] = []

    # Use r0 as return-register. at the end of a fucntion, store the result in r0.
    if isinstance(statement, ReturnFunc):
        
        # reuturn f.e. True or false, or just a constant noumber in general
        if isinstance( statement.rvalue, Number):
            routine_dict[label_name].append( 
                                        get_instruction_string(
                                                cortex.instructions.MOV, 
                                                cortex.registers.RETURNREG, 
                                                imm(statement.rvalue.content)
                                                )
                                        )
            
        # return a variable, check where the variable is in the var_list and use that register to move to r0
        if isinstance( statement.rvalue, Variable):
            if statement.rvalue.content in var_list:
                routine_dict[label_name].append( 
                                            get_instruction_string(
                                                    cortex.instructions.MOV, 
                                                    cortex.registers.RETURNREG, 
                                                    reg(str((var_list.index(statement.rvalue.content))))
                                                    )
                                            )
        
        # return a fucntion result, we need to declare teh function first 
        if isinstance(statement.rvalue, Function):
            
            # create branch to function
            routine_dict[label_name].append(
                                            get_instruction_string( 
                                                    cortex.instructions.BRANCHL, 
                                                    statement.rvalue.funcname
                                                    )
                                            )
            
            func_statements = get_func_def(func_decl, statement.rvalue.funcname)                    
            
            # for every start of a function, we need to push the link regsiter (and after pop the program counter)
            if statement.rvalue.funcname not in routine_dict:
                routine_dict[statement.rvalue.funcname] = ["push { lr }"]
                
       
                start_compiling(func_statements.statements[1:], func_decl, repl(statement.rvalue.func_params[0].content, func_statements.statements[0].func_params[0].content, var_list), statement.rvalue.funcname, routine_dict,  last)
    
    

        
        
    # output the number which is on r0 at this moment            
    elif isinstance( statement, Output):
            routine_dict[label_name].append(
                                            get_instruction_string( 
                                                    cortex.instructions.BRANCHL, 
                                                    'putNumber'
                                                    )
                                            )


    # perform an comparisson which will update the flags.        
    elif isinstance( statement, IfStatement):
        if isinstance( statement.lvalue, Variable):
            if isinstance( statement.rvalue, Number):
                routine_dict[label_name].append(
                                                get_instruction_string(
                                                        cortex.instructions.CMP,
                                                        reg(str(var_list.index(statement.lvalue.content))),
                                                        imm(statement.rvalue.content)
                                                        )
                                                )
                last = statement
           
    # perform a mathimatical instruction
    elif isinstance( statement, MathStatement):
        if isinstance( statement.rvalue, Number):
            if isinstance( statement.operator, Minus):
                if statement.lvalue.content in var_list:

                    routine_dict[label_name].append(
                                                    get_instruction_string(
                                                            cortex.instructions.SUB,
                                                            reg(str((var_list.index(statement.lvalue.content)))),
                                                            imm(statement.rvalue.content)
                                                            )
                                                    )
            if isinstance( statement.operator, Add):
                    routine_dict[label_name].append(
                                                    get_instruction_string(
                                                            cortex.instructions.ADD,
                                                            reg(str((var_list.index(statement.lvalue.content)))),
                                                            imm(statement.rvalue.content)
                                                            )
                                                    )
            if isinstance( statement.operator, Is):
                if statement.lvalue.content in var_list:
                    routine_dict[label_name].append(
                                                    get_instruction_string(
                                                            cortex.instructions.MOV,
                                                            reg(str((var_list.index(statement.lvalue.content)) + 3)),
                                                            imm(statement.rvalue.content)
                                                            )
                                                    )
                else:
                    # is it a local or global value?
                    if label_name != cortex.START_LABEL:
                        if '' in var_list:
                            var_list[var_list[:4].index('')] = statement.lvalue.content
                        else:
                            var_list.append(statement.lvalue.content)
                            
                        routine_dict[label_name].append(
                                                        get_instruction_string(
                                                                cortex.instructions.MOV,
                                                                reg(str((var_list.index(statement.lvalue.content)))),
                                                                imm(statement.rvalue.content)
                                                                )
                                                        )
                    else:
                        var_list.append(statement.lvalue.content)
                        routine_dict[label_name].append(
                                                        get_instruction_string(
                                                                cortex.instructions.MOV,
                                                                reg(str(len(var_list)-1)),
                                                                imm(statement.rvalue.content)
                                                                )
                                                        )
                        
        elif isinstance(statement.rvalue, Variable ):
            if isinstance( statement.operator, Add):
                    routine_dict[label_name].append(
                                                get_instruction_string(
                                                        cortex.instructions.ADD,
                                                        reg(str((var_list.index(statement.lvalue.content)))),
                                                        reg(str((var_list.index(statement.rvalue.content))))
                                                )
                                        )
            elif isinstance( statement.operator, Minus):
                    routine_dict[label_name].append(
                                                get_instruction_string(
                                                        cortex.instructions.SUB,
                                                        reg(str((var_list.index(statement.lvalue.content)))),
                                                        reg(str((var_list.index(statement.rvalue.content))))
                                                )
                                        )
        
        
    elif isinstance( statement, ConditionsLoop):
        routine_dict[label_name].append(
                                        get_instruction_string(
                                                cortex.instructions.BRANCHL,
                                                "cl_" + str(len(routine_dict))
                                                )
                                        )
        start_compiling([statement.expr, statement.loop], func_decl, var_list, "cl_" + str(len(routine_dict)), routine_dict, statement)


        
        
    # Create a new scope and so a  new label for f.e. a subroutine
    elif isinstance(statement, Scope):
        if isinstance(last, IfStatement):
            routine_dict[label_name].append(
                                            get_instruction_string(
                                                    cortex.instructions.BRANCH(last.operator.expr[:2]),
                                                    ".rt_" + str(len(routine_dict))
                                                    )
                                            )
            start_compiling(statement.statements, func_decl, var_list, ".rt_" + str(len(routine_dict)), routine_dict, last)
            rt_label = ".rt_" + str(len(routine_dict)-1)
            if label_name[:3] == 'cl_':
                if routine_dict[rt_label][-1] == "pop { pc }":
                    routine_dict[rt_label].remove(routine_dict[rt_label][-1])
                    routine_dict[rt_label].append(
                                                    get_instruction_string(
                                                            cortex.instructions.BRANCH(),
                                                            label_name
                                                            )
                                                    )

    
    return start_compiling(rest, func_decl, var_list, label_name, routine_dict, statement)
    

# essentially we just return the amount of global variables so we know what registers to safen
def get_reg_init_string( ast, reg_list, push_str = " " ):
    if not ast:
        return "push {" + push_str + " lr }"
    
    statement, *rest = ast
    
    if isinstance( statement, MathStatement):
        if isinstance( statement.operator, Is):
            if isinstance( statement.lvalue, Variable):
                if statement.lvalue.content not in reg_list:
                    reg_list.append(statement.lvalue.content)
                    push_str += spacing(reg(str(len(reg_list)-1)), ', ')
                
    return get_reg_init_string(rest, reg_list, push_str)
        
    
def format_file(rDict, opened_file):
    for init in rDict["init"]:
        opened_file.write(init + "\n")
    
    for item in rDict:
        if item != "init":
            opened_file.write(item + ":\n")
            for step in rDict[item]:
                opened_file.write("\t" + step + "\n")
        opened_file.write("\n")
        
def compile_as(ast, func_decl, filename):  
    routine_dict = start_compiling(
                        ast, 
                        func_decl,          \
                        ["", "", "", ""],             \
                        filename[filename.index('/')+1:-4],                                           \
                        { "init" : [],                                       \
                             filename[filename.index('/')+1:-4] : [get_reg_init_string(ast, ["", "", "", ""])] }, \
                        None)
    
    routine_dict["init"].append(".global " + filename[filename.index('/')+1:-4])
    routine_dict["init"].append(".text")
    routine_dict["init"].append(".cpu cortex-m0")
    routine_dict["init"].append(".align 2")
    

    FILE=open(filename, "w")
    format_file(routine_dict, FILE)
    FILE.close()
