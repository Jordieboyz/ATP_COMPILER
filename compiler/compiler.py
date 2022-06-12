from tokens import Number, Variable, Is, Add, Minus, Times, Divide
from Statements import Function, MathStatement, IfStatement, \
                        ReturnFunc, ConditionsLoop, Scope, Output
from Parser import get_func_def
from cortex_map import get_instruction_string, cortex, maths
from typing import List, Dict
import copy
from Statements import Statement


# These functions create a "cortex-m0" variable given a number.
# This to make teh code a lot cleaner
# imm & reg :: Integer -> String
imm = lambda  number: '#' + str(number)
reg = lambda reg : 'r' + str(reg)


# These functions return a potential start or end of a routine
# push_regs & pop_regs :: Integer -> String
push_regs = lambda r = None: "push { " + reg(r) + ", lr }" if r else "push { lr }"
pop_regs = lambda r =   None: "pop { " + reg(r) + ", pc }" if r else "pop { pc }"

# These functions return a whole or part of an eventual routine label
# This to prevent disalignment during the program in naming the newly created labels 
# returnLabel & loopLabel:: Integer -> String
returnLabel = lambda n = None: ".ret_" + str(n) if n else ".ret_"
loopLabel = lambda n = None : "loop_" + str(n) if n else "loop_"

# This is the main compile function. It loops (recursively) through the ast and creates cortex-m0 instructions.
# The instructions get "saved" in the routineDict. The varList keeps track of all the excisting variables. either local or global.
# start_compiling :: List[Statement] -> List[Statement] -> List[String] -> String -> dict[String, List[String]] -> Statement -> dict[String, List[String]]
def start_compiling( ast : List[Statement], funcDecl : List[Statement], varList : List[str], labelName : str, routineDict : Dict[str, List[str]], last: Statement ):

    # This function replaces the newVal with the oldVal in the oldList and puts them in the newList
    # it essentially creates a new list with repalces values. We can use this to convert
    # global variables (like a function parameter) to their "local" placeholder.
    # replace :: String -> String -> List[String] -> List[String] -> List[String]
    def replace(oldVal : str, newVal : str, oldList : List[str], newlist : List[str] = [] ):
        if not oldList:
            return newlist
        
        item, *rest = oldList
        
        if item == oldVal:
            newlist.append(newVal)  
        else:
            newlist.append(item)
            
        return replace(oldVal, newVal, rest, newlist)

    # We need to make sure we add the line "pop { ??? }" at the end of certain routines
    # However, we need to make sure it matches the push "{ ??? }".
    # Therefore, we can just replace 'push'with 'pop' and 'lr and 'pc'.
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

        return routineDict

    statement, *rest = ast

    # If we are working on a new label we need a place to store the instructions.
    # If we have a loop, we need to add the 'push { lr } line.
    # Else we can just add an empty list
    if labelName not in routineDict:
        # make sure it is a loop label
        if labelName[:5] == loopLabel():
            routineDict[labelName] = [push_regs()]
        else:
           routineDict[labelName] = []

    if isinstance(last, (MathStatement, ReturnFunc)):
        if isinstance(last.rvalue, Function):
            func_label = last.rvalue.funcname + last.rvalue.func_params[0].content
            
            routineDict[labelName].append(
                        get_instruction_string(
                            cortex.instructions.BRANCHL,
                            func_label
                        )) 
            if func_label not in routineDict:    
                func_statements = get_func_def(funcDecl, last.rvalue.funcname)
                
                # if we enter a raw number in the function, wqe need to give it a space in the varlist
                # but because it is not a global variable, we dont need to push extra registers
                # we also have to move the raw number in the wanted register, because it doesnt excist other wise
                if isinstance(last.rvalue.func_params[0], Number):
                    # For every start of a function, we need to push the link regsiter
                    if last.rvalue.funcname not in routineDict:
                        routineDict[func_label] = [push_regs()]
                    
                    newList = copy.deepcopy(varList)
                    if '' in newList:
                        newList[newList[:4].index('')] = func_statements.statements[0].func_params[0].content
                    else:
                        newList.append(func_statements.statements[0].func_params[0].content)
                    
                    routineDict[func_label].append(
                                     get_instruction_string(
                                                 cortex.instructions.MOV,
                                                 reg(newList.index(func_statements.statements[0].func_params[0].content)),
                                                 imm(last.rvalue.func_params[0].content)
                                                 )  
                                     )
                elif isinstance(last.rvalue.func_params[0], Variable):
                    if last.rvalue.func_params[0].content in varList:
                        
                        if last.rvalue.funcname not in routineDict:
                            routineDict[func_label] = [push_regs(varList.index(last.rvalue.func_params[0].content))]
                            
    
                            newList = replace(last.rvalue.func_params[0].content, 
                                                 func_statements.statements[0].func_params[0].content, 
                                                 varList
                                        )

                # The first element in the func_statements is the "Function" 
                # Statement, so this needs to be ignored.
                # We also need to replace the global variable names with
                # the given parameters of the function in the registers.
                start_compiling( func_statements.statements[1:], funcDecl, 
                                    newList,
                                    func_label, routineDict,  
                                    None
                                )
                   
                
                if isinstance( last, ReturnFunc):
                # make sure the result of the function (stored in r0) gets put in r0
                    routineDict[labelName].append(
                                get_instruction_string(
                                    cortex.instructions.MOV,
                                    cortex.registers.RETURNREG,
                                    cortex.registers.RETURNREG
                                ))
                else:
                    routineDict[labelName].append(
                                get_instruction_string(
                                    cortex.instructions.MOV,
                                    reg(varList.index(last.lvalue.content)),
                                    cortex.registers.RETURNREG
                                ))
                
    # Use r0 as return-register. Store the result in r0.
    if isinstance(statement, ReturnFunc):
        
        # Move a number in r0
        if isinstance( statement.rvalue, Number):
            routineDict[labelName].append( 
                        get_instruction_string(
                            cortex.instructions.MOV, 
                            cortex.registers.RETURNREG, 
                            imm(statement.rvalue.content) 
                        ))
            
        # Return a variable, check where the variable is in the var_list 
        # If it is, we can move this regsiter in r0
        if isinstance( statement.rvalue, Variable):
            if statement.rvalue.content in varList:
                routineDict[labelName].append( 
                            get_instruction_string(
                                cortex.instructions.MOV, 
                                cortex.registers.RETURNREG, 
                                reg(varList.index(statement.rvalue.content))
                            ))
                
        # Move a function result to r0, we need to declare the function first 
        if isinstance(statement.rvalue, Function):
            start_compiling([None], funcDecl, varList, labelName, routineDict, statement)
            statement = None
                
        
    # Put a branchl instruction in the routineDict so the program can 
    # output the value in r0            
    elif isinstance( statement, Output):
            routineDict[labelName].append(
                                        get_instruction_string( 
                                                cortex.instructions.BRANCHL, 
                                                'put_number'
                                                )
                                        )


    # Perform a comparison between either vars or vars and number
    # This results in a cmp instruction being added to the routine        
    elif isinstance( statement, IfStatement):
        if isinstance( statement.lvalue, Variable):
            if isinstance( statement.rvalue, Number):
                routineDict[labelName].append(
                            get_instruction_string(
                                cortex.instructions.CMP,
                                reg(varList.index(statement.lvalue.content)),
                                imm(statement.rvalue.content)
                            ))
                                                
            elif isinstance( statement.rvalue, Variable):
                if statement.rvalue.content in varList:
                    routineDict[labelName].append(
                                get_instruction_string(
                                    cortex.instructions.CMP,
                                    reg(varList.index(statement.lvalue.content)),
                                    reg(varList.index(statement.rvalue.content))
                                ))
            last = statement
            
            
           
    # Create a mathematical instruction between vars or vars and numbers
    # This results in a add, sub, muls udiv or mov instruction being added to the routine
    elif isinstance(statement, MathStatement):
        if isinstance(statement.lvalue, Variable):
            if statement.lvalue.content in varList:
                if isinstance(statement.rvalue, Number):
                    if isinstance(statement.operator, Is):
                        routineDict[labelName].append(
                                 get_instruction_string(
                                    cortex.instructions.MOV,
                                    reg(varList.index(statement.lvalue.content)),
                                    imm(statement.rvalue.content)
                                )
                            )
                    elif isinstance(statement.operator, (Add,Minus,Times,Divide)):
                        routineDict[labelName].append(
                                    get_instruction_string(
                                        maths[type(statement.operator)],
                                        reg(varList.index(statement.lvalue.content)),
                                        imm(statement.rvalue.content)
                                    )) 
                        
                elif isinstance(statement.rvalue, Variable):
                    if statement.rvalue.content in varList:
                        if isinstance(statement.operator, Is):
                            routineDict[labelName].append(
                                        get_instruction_string(
                                            cortex.instructions.MOV,
                                            reg(varList.index(statement.lvalue.content)),
                                            reg(varList.index(statement.rvalue.content)),
                                        ))
                            
                        elif isinstance(statement.operator, ( Add,Minus,Times,Divide)):
                            routineDict[labelName].append(
                                        get_instruction_string(
                                            maths[type(statement.operator)],
                                            reg(varList.index(statement.lvalue.content)),
                                            reg(varList.index(statement.rvalue.content))
                                        )) 
                            
                elif isinstance(statement.rvalue, Function):
                    start_compiling([None], funcDecl, varList, labelName, routineDict, statement)
                    statement = None
                            
                        
                        
            # If the lvalue of statement is not yet declared in the routine.
            # we need to add it to the varList (so it can be used).
            # We need to figure out wether it is a local or global variable
            else:
                # is it a local var?
                if labelName != cortex.START_LABEL:
                    # We add this variable to the 'scratch' registers (if there is place)
                    if '' in varList:
                        varList[varList[:4].index('')] = statement.lvalue.content
                    else:
                        varList.append(statement.lvalue.content)
                        
                    routineDict[labelName].append(
                                 get_instruction_string(
                                    cortex.instructions.MOV,
                                    reg(varList.index(statement.lvalue.content)),
                                    imm(statement.rvalue.content)
                                 ))
                # it is a global var.
                else:
                    varList.append(statement.lvalue.content)
                    
                    if isinstance(statement.rvalue, Function):
                        start_compiling([None], funcDecl, varList, labelName, routineDict, statement)
                        statement = None
                        
                    else:
                        routineDict[labelName].append(
                                    get_instruction_string(
                                        cortex.instructions.MOV,
                                        reg(varList.index(statement.lvalue.content)),
                                        imm(statement.rvalue.content)
                                    ))



    # This is a bit of a tricky one.
    # We need to check the condition and based on the result we need to branch
    # to another scope.
    elif isinstance( statement, ConditionsLoop):
        looplabel = loopLabel(len(routineDict))
        routineDict[labelName].append(
                    get_instruction_string(
                        cortex.instructions.BRANCHL,
                        looplabel
                    ))
        
        routineDict[looplabel] = [routineDict[labelName][0]]
        start_compiling([statement.expr, statement.loop], funcDecl, varList,  \
                                            looplabel, routineDict, statement)
 
    
    # Create a new scope and so a new label
    elif isinstance(statement, Scope):
        
        if isinstance(last, IfStatement):
            retLabel = returnLabel(len(routineDict))
            routineDict[labelName].append(
                        get_instruction_string(
                            cortex.instructions.BRANCH + last.operator.expr[:2],
                            retLabel
                        ))

            start_compiling(statement.statements, funcDecl, varList, 
                                                  retLabel, routineDict, last)
                
            
            routineDict[retLabel].append(
                    routineDict[labelName][0].replace(
                                    cortex.instructions.PUSH,
                                    cortex.instructions.POP).replace(
                                                    cortex.registers.LR,
                                                    cortex.registers.PC)
                                        )
            

            # a loop should be a loop, so we need to branch back to the start of the loop
            # if there is automaticaly added a "pop { pc } to the routine, remove it.
            if labelName[:5] == loopLabel():
                if routineDict[retLabel][-1][:3] == cortex.instructions.POP:
                    routineDict[retLabel].remove(routineDict[retLabel][-1])
                
                # add the instruction to loop back to the start of the loop.
                routineDict[retLabel].append(
                            get_instruction_string(
                                cortex.instructions.BRANCH,
                                labelName
                            ))

    return start_compiling(rest, funcDecl, varList, labelName, routineDict, 
                                                                    statement)
    

# Essentially we just return the amount of global variables 
# So we know what registers to safen
# get_reg_init_string :: List[Statement] -> List[String] -> String -> List[String]
def get_reg_init_string( ast, reg_list = ["", "", "", ""], push_str = " " ):
    if not ast:
        return cortex.instructions.PUSH + " {" + push_str + " lr }"
    
    statement, *rest = ast

    if isinstance( statement, MathStatement):
        if isinstance( statement.operator, Is):
            if isinstance( statement.lvalue, Variable):
                if statement.lvalue.content not in reg_list:
                    reg_list.append(statement.lvalue.content)
                    push_str += reg(str(len(reg_list)-1)) + ', '
                
    return get_reg_init_string(rest, reg_list, push_str)
        
# This function jsut formats the created dictionary during the compilation
# and writes it to the openedFile
def format_write_file(rDict, openedFile, initLabel = "init"):
    for init in rDict[initLabel]:
        openedFile.write(init + "\n")
    
    for item in rDict:
        if item != initLabel:
            openedFile.write(item + ":\n")
            for step in rDict[item]:
                openedFile.write("\t" + step + "\n")
        openedFile.write("\n")
        
        
# yes, ugly, need to remove, but cant
def remove_extra_pop(routinedict):
    for routine in routinedict:
        for index, elem in enumerate(routinedict[routine]):
            if elem[:3] == 'pop':
                if index != len(routinedict[routine]):
                   del  routinedict[routine][index]
    return routinedict
        
    
    
# parseInScopes :: List[Statement] -> List[Statement] -> String -> Dict[String, [String]]
def compile_asm_(ast, funcDecl, filename):
    initLabel = "init"
    cortex.START_LABEL = filename
    
    # We dont use the 'scratch registers to store 'global' variables
    # So, we need to make sure they won't be used until needed
    return remove_extra_pop(start_compiling(
                            ast, 
                            funcDecl,
                            ["", "", "", ""],
                            filename,
                            { initLabel : [  ".global " + filename,
                                             ".text",
                                             ".cpu cortex-m0",
                                             ".align 2"],
                             filename : [ get_reg_init_string(ast) ] },
                            None )
        )
