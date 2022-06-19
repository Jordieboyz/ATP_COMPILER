from typing import List, Dict, Tuple
from tokens import Number, Variable, Is, Add, Minus, Times, Divide
from Statements import Function, MathStatement, IfStatement, \
                        ReturnFunc, ConditionsLoop, Scope, Output
from Parser import get_func_def
from Statements import Statement
from cortex_map import get_instruction_string, cortex, maths


INT_SIZE = 4

# These are all lambda functions to make the code a lot cleaner
# The function is the add the input to a constant string
# every lambda has it's own function ans producxes it's own string
# Any:: Any -> String

# These lambda functions produce a cortex-m0 using the right syntax
imm             = lambda number: '#' + str(number)
reg             = lambda reg   : 'r' + str(reg)

# This functions return a potential start of a routine
push_regs       = lambda r = None: "push { " + str(r) + ", lr }" if r else "push { lr }"

# These functions return a whole or part of an eventual routine label
# This to prevent disalignment during the program in naming the newly created labels 
scopeLabel      = lambda n = None: ".scop_"      + str(n) if n else ".scop_"
loopCondLabel   = lambda n = None: ".loop_cond_" + str(n) if n else ".loop_cond_"
endFuncLabel    = lambda n = None: ".end_"       + str(n) if n else ".end_"


# This is the main compile function. It loops (recursively) through the ast and creates cortex-m0 instructions.
# The instructions get "saved" in the routineDict. The varList keeps track of all the excisting variables. either local or global.
# start_compiling :: List[Statement] -> List[Statement] -> List[String] -> String -> dict[String, List[String]] -> Statement -> dict[String, List[String]]
def start_compiling( ast : List[Statement], funcDecl : List[Statement], varList : List[str], labelName : str, routineDict : Dict[str, List[str]], last: Statement ) -> Dict[str, List[str]]: 
    # We return the routineDict if we looped through all the statements (in a scope)
    if not ast:
        return routineDict

    # head, tail structure
    statement, *rest = ast

    # If we are working on a new label we need a place to store the instructions.
    if labelName not in routineDict:
        routineDict[labelName] = []

    
    # Here we create the implementation of a function wether it does or doesnt already excists
    # in the routineDict. Our function NEED to return for it to work
    # so there is no point using it as an 'void' function aka without expression.
    if isinstance(last, (MathStatement, ReturnFunc)):
        if isinstance(last.rvalue, Function):
            
            # creating the label for the function to prevent duplication
            func_label = last.rvalue.funcname
            
            # we can pass up to one parameter in a function. This can either be 
            # a number or variable. We need to put this on r0 for the function
            # so we kinda follow the way a C++ program passes parameters to asm.
            if isinstance(last.rvalue.func_params[0], Number):
                # A raw number gets moved in r0
                routineDict[labelName].append(
                            get_instruction_string(
                                cortex.instructions.MOV,
                                cortex.registers.RETURNREG,
                                imm(last.rvalue.func_params[0].content)
                            ))
              
            elif isinstance(last.rvalue.func_params[0], Variable):                        
                # A variable gets moved in r0
                routineDict[labelName].append(
                            get_instruction_string(
                                cortex.instructions.MOV,
                                cortex.registers.RETURNREG,
                                reg(varList.index(last.rvalue.func_params[0].content))
                            ))
            
            # Create a branchLink to the function label
            routineDict[labelName].append(
                        get_instruction_string(
                            cortex.instructions.BRANCHL,
                            func_label
                        )) 

            # here we specify if the function is already created.
            # because if it already excists, we dont need to create it again.
            if func_label not in routineDict:  
                # Get the function declaration and the amount of DIRECT new 
                # variables. We dont look in the extra scopes. 
                # (so we cant declare new variables in the sub-scopes)
                # Based on this amount, we create a 'local' stack for the function
                # assuming we only use integers with a size of 4 bytes, 32 bits.
                # We give a 8 bytes extra spaces just in case.
                func_statements = get_func_def(funcDecl, last.rvalue.funcname)
                func_parameter = func_statements.statements[0].func_params[0].content
                n_stack_integers = get_n_variables_in_scope(func_statements.statements[1:]) + 2
                
                
                # Here we start setting up the 'local' stack.
                # we push the framepointer and the linkregister
                # substract the stackpointer (to create space for variables)
                # We move the framepointer along
                if last.rvalue.funcname not in routineDict:
                    routineDict[func_label] = [push_regs(cortex.registers.FP)]
                    
                    routineDict[func_label].append(
                                get_instruction_string(
                                    cortex.instructions.SUB,
                                    cortex.registers.SP,
                                    imm(n_stack_integers * INT_SIZE)
                                )) 
                
                    routineDict[func_label].append(
                                get_instruction_string(
                                    cortex.instructions.MOV,
                                    cortex.registers.FP,
                                    cortex.registers.SP,
                                ))
                    
                    
                    # We're entering a function and it needs a clean local scope.
                    # The function parameter gets put on the r0.
                    newList = [func_parameter]

                    # The function parameter (on r0 upon entering the function) 
                    # gets pushed on the stack
                    routineDict[func_label].append(
                                get_instruction_string(
                                    cortex.instructions.STORE,
                                    reg(newList.index(func_parameter)),
                                    imm((newList.index(func_parameter) + 1) * INT_SIZE)
                                ))
                        
                # Here we start creating instructions for the declaration of ther function
                # The first element in the func_statements is the "Function" 
                # Statement, so this needs to be ignored.
                start_compiling( func_statements.statements[1:], funcDecl, 
                                    newList,
                                    func_label, routineDict,  
                                    None
                                )
                
                # Move the result of the function (usually stored in r0) in te right register
                if isinstance( last, MathStatement):
                    routineDict[labelName].append(
                                get_instruction_string(
                                    cortex.instructions.MOV,
                                    reg(varList.index(last.lvalue.content)),
                                    cortex.registers.RETURNREG
                                ))
                    
                    
    # The next section implement the 'return', 'if-statements' and 'mathematical operators'
    # A quick side-note is the difference between a 'global' and 'local' scope.
    # if we enter a function for example, we create a new list for it: [<func_param>]
    # If we are working in the global scope, we dont put any variables in the 
    # first 3 registers: ['', '', '', '', <var1>, <var2>, etc...]
    # Which means, We can differnciate a global and local scope by checking if 
    # there is a '' in the list. If there is, we know we can use basic, simple instruction
    # Otherwise, we need to use the stack to store, load and move variables.
    # This is the simple implementation I came up with but the downside is,
    # In the global scope, we have a very limited amount of variables to work with
    # just the r4, r5, r6 and r7.in functions, we can use as many as there 
    # is space on the stack. (also not really true, if we have to much variables, we lose em)
    
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
                # Local scope?
                if '' not in varList:
                    # before branching to the end of a fucntion, load 
                    # the value on the stack to be returned in r0
                    routineDict[labelName].append( 
                                get_instruction_string(
                                    cortex.instructions.LOAD, 
                                    cortex.registers.RETURNREG, 
                                    imm((varList.index(statement.rvalue.content)+1) * INT_SIZE)
                                ))
                    
                    # create a somewhat fixed end_function label
                    endFLabel = endFuncLabel(labelName)
                    
                    # If this function doesn't excist yet, we create it.
                    if endFLabel not in routineDict:
                        routineDict[endFLabel] = []
                    
                        # we pretty much remove the stack and restore everything
                        # we stated in the beginning of the function
                        routineDict[endFLabel].append(
                                    get_instruction_string(
                                        cortex.instructions.MOV,
                                        cortex.registers.SP,
                                        cortex.registers.FP
                                    ))
                        
                        routineDict[endFLabel].append(
                                    get_instruction_string(
                                        cortex.instructions.ADD,
                                        cortex.registers.SP,
                                        routineDict[labelName][1][routineDict[labelName][1].index('#'):]
                                    ))
                
                        routineDict[endFLabel].append(
                                routineDict[labelName][0].replace(
                                                cortex.instructions.PUSH,
                                                cortex.instructions.POP).replace(
                                                                cortex.registers.LR,
                                                                cortex.registers.PC)
                                                    )
                    # We make sure we branch to the end_function label
                    routineDict[labelName].append( 
                                get_instruction_string(
                                    cortex.instructions.BRANCH, 
                                    endFLabel
                                ))
                else:
                    # nope. global scope. simple instruction
                    routineDict[labelName].append( 
                                get_instruction_string(
                                    cortex.instructions.MOV, 
                                    cortex.registers.RETURNREG,
                                    reg(varList.index(statement.rvalue.content))
                                ))
                
        # Move a function result to r0, we need to declare the function first 
        if isinstance(statement.rvalue, Function):
            start_compiling([None], funcDecl, varList, labelName, routineDict, statement)
            # Local scope?
            if '' not in varList:

                # create a somewhat fixed end_function label
                endFLabel = endFuncLabel(labelName)

                # If this function doesn't excist yet, we create it.
                if endFLabel not in routineDict:
                    routineDict[endFLabel] = []
                
                    # we pretty much remove the stack and restore everything
                    # we stated in the beginning of the function
                    routineDict[endFLabel].append(
                                get_instruction_string(
                                    cortex.instructions.MOV,
                                    cortex.registers.SP,
                                    cortex.registers.FP
                                ))
                    
                    routineDict[endFLabel].append(
                                get_instruction_string(
                                    cortex.instructions.ADD,
                                    cortex.registers.SP,
                                    routineDict[labelName][1][routineDict[labelName][1].index('#'):]
                                ))
                
                    routineDict[endFLabel].append(
                            routineDict[labelName][0].replace(
                                            cortex.instructions.PUSH,
                                            cortex.instructions.POP).replace(
                                                            cortex.registers.LR,
                                                            cortex.registers.PC)
                                                )
                # We make sure we branch to the end_function label
                routineDict[labelName].append( 
                            get_instruction_string(
                                cortex.instructions.BRANCH, 
                                endFLabel
                            ))

    # Put a branchl instruction in the routineDict so the program can 
    # output the value in r0            
    elif isinstance( statement, Output):
            routineDict[labelName].append(
                            get_instruction_string( 
                                cortex.instructions.BRANCHL, 
                                'put_number'
                            ))


    # Perform a comparison between either vars or vars and number
    # This results in a cmp instruction being added to the routine        
    elif isinstance( statement, IfStatement):
        if isinstance( statement.lvalue, Variable):
            if isinstance( statement.rvalue, Number):
                if statement.lvalue.content in varList:
                    # before comparison, we need to load the value from the stack
                    routineDict[labelName].append(
                                get_instruction_string(
                                    cortex.instructions.LOAD,
                                    cortex.registers.RETURNREG,
                                    imm((varList.index(statement.lvalue.content)+1) * INT_SIZE)
                                ))
                    
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
                                        cortex.instructions.LOAD,
                                        cortex.registers.RETURNREG,
                                        imm((varList.index(statement.lvalue.content)+1) * INT_SIZE)
                                    ))
                        
                        routineDict[labelName].append(
                                    get_instruction_string(
                                        cortex.instructions.CMP,
                                        reg(varList.index(statement.lvalue.content)),
                                        reg(varList.index(statement.rvalue.content))
                                    ))
                else:
                    None
                    # this is a clause we get to isf we use an undefined variable in an ifstatement
                    # I could implement this.
            
            
           
    # Create a mathematical instruction between vars or vars and numbers
    # This results in a add, sub, muls or mov instruction being added to the routine
    elif isinstance(statement, MathStatement):
        if isinstance(statement.lvalue, Variable):
            if statement.lvalue.content in varList:
                # lvalue already initialized
                if isinstance(statement.rvalue, Number):
                    # rvalue is a number
                    if isinstance(statement.operator, Is):
                        routineDict[labelName].append(
                                 get_instruction_string(
                                    cortex.instructions.MOV,
                                    reg(varList.index(statement.lvalue.content)),
                                    imm(statement.rvalue.content)
                                 ))
                        # If we are in a local scope of (f.e.) a function
                        # We need to store this variable on the stack
                        if '' not in varList:
                            routineDict[labelName].append( 
                                        get_instruction_string(
                                            cortex.instructions.STORE, 
                                            reg(varList.index(statement.lvalue.content)), 
                                            imm((varList.index(statement.lvalue.content)+1) * INT_SIZE)
                                        ))
                
                    elif isinstance(statement.operator, (Add,Minus,Times,Divide)):
                        # Check wether we are working in the 'global' or a local scope
                        # local scope?
                        if '' not in varList:
                            routineDict[labelName].append( 
                                        get_instruction_string(
                                            cortex.instructions.LOAD, 
                                            reg(varList.index(statement.lvalue.content)), 
                                            imm((varList.index(statement.lvalue.content)+1) * INT_SIZE)
                                        ))                        
                            routineDict[labelName].append(
                                        get_instruction_string(
                                            maths[type(statement.operator)],
                                            reg(varList.index(statement.lvalue.content)),
                                            imm(statement.rvalue.content)
                                        )) 
                            routineDict[labelName].append( 
                                        get_instruction_string(
                                            cortex.instructions.STORE, 
                                            reg(varList.index(statement.lvalue.content)), 
                                            imm((varList.index(statement.lvalue.content)+1) * INT_SIZE)
                                        )) 
                        # global scope. simple instruction  
                        else:
                            routineDict[labelName].append(
                                get_instruction_string(
                                    maths[type(statement.operator)],
                                    reg(varList.index(statement.lvalue.content)),
                                    imm(statement.rvalue.content)
                                ))
                        
                elif isinstance(statement.rvalue, Variable):
                    # rvalue is a variable
                    if statement.rvalue.content in varList:
                        # This is an already initialized variable
                        if isinstance(statement.operator, Is):
                            # local scope?
                            if '' not in varList:
                                # Move value of the rvalue in the register of the lvalue
                                routineDict[labelName].append(
                                            get_instruction_string(
                                                cortex.instructions.MOV,
                                                reg(varList.index(statement.lvalue.content)),
                                                reg(varList.index(statement.rvalue.content)),
                                            ))
                                # store the 'moved' on the stack 
                                routineDict[labelName].append(
                                            get_instruction_string(
                                                cortex.instructions.STORE,
                                                reg(varList.index(statement.lvalue.content)),
                                                reg(varList.index(statement.rvalue.content)),
                                            ))
                            # global scope. simple instruction.
                            else:
                                routineDict[labelName].append(
                                    get_instruction_string(
                                        cortex.instructions.MOV,
                                        reg(varList.index(statement.lvalue.content)),
                                        reg(varList.index(statement.rvalue.content)),
                                    ))          

                        elif isinstance(statement.operator, ( Add,Minus,Times,Divide)):
                            # local scope?
                            if '' not in varList:
                                # we need to load the lvalue from the stack in a register before operating with it
                                routineDict[labelName].append( 
                                            get_instruction_string(
                                                cortex.instructions.LOAD, 
                                                reg(varList.index(statement.lvalue.content)), 
                                                imm((varList.index(statement.lvalue.content)+1) * INT_SIZE)
                                            ))
                                # we need to load the rvalue from the stack in a register before operating with it
                                routineDict[labelName].append( 
                                            get_instruction_string(
                                                cortex.instructions.LOAD, 
                                                reg(varList.index(statement.rvalue.content)), 
                                                imm((varList.index(statement.rvalue.content)+1) * INT_SIZE)
                                            ))
                                # 'perform' the maths on the already loaded registers
                                routineDict[labelName].append(
                                            get_instruction_string(
                                                maths[type(statement.operator)],
                                                reg(varList.index(statement.lvalue.content)),
                                                reg(varList.index(statement.rvalue.content))
                                            )) 
                                # Store the result of the operation back on the stack
                                routineDict[labelName].append( 
                                            get_instruction_string(
                                                cortex.instructions.STORE, 
                                                reg(varList.index(statement.lvalue.content)), 
                                                imm((varList.index(statement.lvalue.content)+1) * INT_SIZE)
                                            ))

                            # global scope, simple instruction
                            else:
                                routineDict[labelName].append(
                                            get_instruction_string(
                                                maths[type(statement.operator)],
                                                reg(varList.index(statement.lvalue.content)),
                                                reg(varList.index(statement.rvalue.content))
                                            )) 
                elif isinstance(statement.rvalue, Function):
                    # rvalue is a Function which needs to be implemented
                    start_compiling([None], funcDecl, varList, labelName, routineDict, statement)
                    statement = None
                            
                        
            # This an undefined variable
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

                    # move value in chosen register    
                    routineDict[labelName].append(
                                 get_instruction_string(
                                    cortex.instructions.MOV,
                                    reg(varList.index(statement.lvalue.content)),
                                    imm(statement.rvalue.content)
                                 ))
                    # store the value on the stack
                    routineDict[labelName].append(
                                get_instruction_string(
                                    cortex.instructions.STORE,
                                    reg(varList.index(statement.lvalue.content)),
                                    imm((varList.index(statement.lvalue.content) + 1) * INT_SIZE)
                                ))
                # nope. global scope.
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
        loopClabel = loopCondLabel(len(routineDict))
        routineDict[labelName].append(
                    get_instruction_string(
                        cortex.instructions.BRANCHL,
                        loopClabel
                    ))
        

        start_compiling([statement.expr, statement.loop], funcDecl, varList,  \
                                            loopClabel, routineDict, statement)
 
    
    # Create a new scope and so a new label
    elif isinstance(statement, Scope):
        
        if isinstance(last, IfStatement):
            retLabel = scopeLabel(len(routineDict))
            routineDict[labelName].append(
                        get_instruction_string(
                            cortex.instructions.BRANCH + last.operator.expr[:2],
                            retLabel
                        ))

            start_compiling(statement.statements, funcDecl, varList, 
                                                  retLabel, routineDict, last)
            
            if isinstance(statement.statements[0], ReturnFunc):
                routineDict[retLabel].append(
                            get_instruction_string(
                                cortex.instructions.BRANCH,
                                endFuncLabel( labelName)
                            ))


    return start_compiling(rest, funcDecl, varList, labelName, routineDict, 
                                                                    statement)

# Return the amount of initialized variables in this ast aka this direct scope
# get_n_variables_in_scope :: List[Statement] -> Integer -> Integer
def get_n_variables_in_scope(ast : List[Statement], n : int = 0) -> int:
    if not ast:
        return n
    
    statement, *rest = ast
    
    if isinstance(statement, MathStatement):
        if isinstance(statement.operator, Is):
            n += 1
    
    return get_n_variables_in_scope(rest, n)
    
import copy
# This works, but is functional-wise terrible...
# It kinda fixes the problem with wrong order of routines and adds the last 'pop' instruction
# finish_compiling_simple :: Dict[Statement] -> Dict[Statement] -> Dict[Statement]
def finish_compiling_simple(rDict : Dict[str, List[str]], nDict : Dict[str, List[str]] = dict()) -> Dict[str, List[str]]:
    def get_name(instruction): return instruction[(instruction.index(' ')):].replace(" ", "")
    listt = list(rDict.keys())
    fresh_list = [listt[0], listt[1]]
    
    for label in list(rDict.keys())[2:]:
        if label not in fresh_list:
            if label[0] != '.':
                fresh_list.append(label)
                fresh_list.append(endFuncLabel(label))
            else:
                fresh_list.append(label)
        if fresh_list[-1][:6] == scopeLabel() and fresh_list[-2][:11] == loopCondLabel():
            fresh_list[-1], fresh_list[-2] = fresh_list[-2], fresh_list[-1]
        

    for label in fresh_list:
        if label == cortex.START_LABEL:
            if rDict[label][0][:4] == cortex.instructions.PUSH:
                if rDict[label][-1][:3] != cortex.instructions.POP:
                    rDict[label].append(
                            rDict[label][0].replace(
                                            cortex.instructions.PUSH,
                                            cortex.instructions.POP).replace(
                                                            cortex.registers.LR,
                                                            cortex.registers.PC)
                                                )
                                                
        nDict[label] = rDict[label]

    return nDict

        
# parseInScopes :: List[Statement] -> List[Statement] -> String -> Dict[String, List[String]]
def compile_asm_(ast : List[Statement], funcDecl : List[Tuple[str, List[Statement]]], filename : str) -> Dict[str, List[str]]:
    initLabel = "init"
    cortex.START_LABEL = filename
    
    # We dont use the 'scratch registers to store 'global' variables
    # So, we need to make sure they won't be used until needed
    return finish_compiling_simple(
                        start_compiling(
                                        ast, 
                                        funcDecl,
                                        ["", "", "", ""],
                                        filename,
                                        { initLabel : [  ".global " + filename,
                                                         ".text",
                                                         ".cpu cortex-m0",
                                                         ".align 4"],
                                        filename : [ 'push {r4-r7, lr}' ] },
                                        None 
                        ))

        
# This function jsut formats the created dictionary during the compilation
# and writes it to the openedFile
def format_write_file(rDict : Dict[str, List[str]], openedFile : str, initLabel : str = "init") -> None:
    for init in rDict[initLabel]:
        openedFile.write(init + "\n")
    
    for item in rDict:
        if item != initLabel:
            openedFile.write(item + ":\n")
            for step in rDict[item]:
                openedFile.write("\t" + step + "\n")
        openedFile.write("\n")
        
    