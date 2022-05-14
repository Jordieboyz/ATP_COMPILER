from typing import List
import copy
from Parser import Parse
from tokens import Token, Func, Number, Variable, Is, ExprIfStatement, \
                   CloseFuncParam, OpenFuncParam, \
                   Add, Minus, Divide, Times, Modulo, OpenLoop, CloseLoop, \
                   StartExprLoop, EndExprLoop, Return
from Statements import st_dict, Statement, Function, MathStatement, IfStatement, \
                        ReturnFunc, ConditionsLoop, Scope, CloseScope, OpenScope

b_map = {
    "eq" : "beq",
    "neq" : "bne"
}


def start_compiling( ast, func_decl, label_name, routine_dict, last):
    if not ast:
        if routine_dict[label_name]:
            if routine_dict[label_name][-1] != "pop { pc }":
                routine_dict[label_name].append("pop { pc }") 
        return routine_dict

    
    statement, *rest = ast
        
    if label_name not in routine_dict:
        routine_dict[label_name] = []
    
    if isinstance(statement, ReturnFunc):
        if isinstance( statement.rvalue, Number):
            routine_dict[label_name].append("movs r0, #" + statement.rvalue.content)

        if isinstance(statement.rvalue, Function):
            
            if label_name not in routine_dict:
                routine_dict[label_name] = []
                routine_dict[label_name].append("push { lr }")
                
            routine_dict[label_name].append("bl " + statement.rvalue.funcname )
            
            label_name = statement.rvalue.funcname        
            f = list(filter(None, map( lambda x, y: x[1] if x[0] == y else None , func_decl, [label_name]*len(func_decl))))[0]
            
            if isinstance(f[4], OpenLoop):
                del f[4]
                if isinstance(f[-1], CloseLoop):
                    del f[-1]
            
            func_statements = Parse(f)[1]                    
            
            if label_name not in routine_dict:
                routine_dict[label_name] = []
                routine_dict[label_name].append("push { lr }")
                
                start_compiling(func_statements.statements[1:], func_decl, label_name, routine_dict,  last)

            
    if isinstance( statement, IfStatement):
        if isinstance( statement.lvalue, Variable):
            if isinstance( statement.rvalue, Number):
                if statement.operator.expr == "eq":
                    routine_dict[label_name].append("cmp r0, #" + statement.rvalue.content)
                    last = statement
    
    if isinstance( statement, MathStatement):
        if isinstance( statement.rvalue, Number):
            if isinstance( statement.operator, Minus):
                routine_dict[label_name].append("sub r0, r0, #" + statement.rvalue.content )
            if isinstance( statement.operator, Add):
                routine_dict[label_name].append("add r0, r0, #" + statement.rvalue.content )
            if isinstance( statement.operator, Is):
                routine_dict[label_name].append("movs r0, #" + statement.rvalue.content )
    
    if isinstance(statement, Scope):
          if isinstance(last, IfStatement):
                  tmp_label_name = "ret_" + str(len(routine_dict))
                  routine_dict[label_name].append(b_map[last.operator.expr] + " " + tmp_label_name)
                  start_compiling(statement.statements, func_decl, tmp_label_name, routine_dict, last)

    return start_compiling(rest, func_decl, label_name, routine_dict, last)
    
def prettyPrinter(rDict, opened_file):
    for init in rDict["init"]:
        opened_file.write(init + "\n")
    
    for item in rDict:
        if item != "init":
            opened_file.write(item + ":\n")
            for step in rDict[item]:
                opened_file.write("\t" + step + "\n")
        opened_file.write("\n")
    
    
def compile_as(ast, func_decl, filename):
    routine_dict = { "init" : [], "start" : ["push { lr }"] }

    routine_dict = start_compiling(ast, func_decl, "start", routine_dict, None)
    
    routine_dict["init"].append(".global start")
    routine_dict["init"].append(".section .text")
    routine_dict["init"].append(".cpu cortex-m0")
    routine_dict["init"].append(".align 1")
    
    FILE=open("out.asm", "w")
    prettyPrinter(routine_dict, FILE)
    FILE.close()

    
    
    
    