from typing import List
from tokens import Token, Func, Number, Variable, Is, ExprIfStatement, \
                   CloseFuncParam, OpenFuncParam,  \
                   Add, Minus, Divide, Times, Modulo, OpenLoop, CloseLoop, \
                   StartExprLoop, EndExprLoop, Return, Print
from Statements import st_dict, Statement, Function, MathStatement, IfStatement, \
                        ReturnFunc, ConditionsLoop, Scope, CloseScope, OpenScope

# These 2 functions append or remove an item frmo the list. I would have done this inline IF the "append" or "remove" function
# returned itself. Unfortunately, they don't so I have to do this myself. It is kinda tricky, cause these operations always return None,
# whether it worked or not, but assuming I put the right values in these lambda functions, I'll be okay
append = lambda l, x: l if l.append(x) is None else l
remove = lambda l, x: l if l.remove(x) is None else l
    

# This function is the first step of parsing in my program.
# The function creates a List[Statement] out of a List[Token]. Statements are combined Token(s)

# parseTokensToStatements :: List[Token] -> List[Statement] -> Token -> Statement -> List[String, List[Token]] -> List[Statement]
def parseTokensToStatements(tokenlist : List[Token], statementlist : List[Statement], last_token : Token, cur_statement : Statement):
    if not tokenlist:
        return None, statementlist

    token, *rest = tokenlist
    
    # This part of the function adds fucntion parameters to a certain function and and if the current 
    # token is a Token::CloseFunParam, the completed fucntion gets added to the List[Statement] or to the Statement::Mathstatement if it needs an rvalue
    if cur_statement is not None:
        if isinstance(cur_statement, Function) and isinstance( last_token, OpenFuncParam):
            if not isinstance(token, CloseFuncParam): 
                cur_statement.func_params.append(token)
                return parseTokensToStatements(rest, statementlist, last_token, cur_statement)
            else:
                if len(statementlist) > 1:
                    if isinstance( statementlist[-1], (MathStatement, IfStatement, ReturnFunc)):
                        if statementlist[-1].rvalue is None:
                            statementlist[-1].rvalue = cur_statement
                            return parseTokensToStatements(rest, statementlist, token, None)
                return parseTokensToStatements(rest, append(statementlist, cur_statement), token, None)
  
    
  # Add the current Token::Variable or Token::Number to whatever the Statement::cur_statement is
    if isinstance( token, (Variable, Number)):
        if isinstance( cur_statement, (IfStatement, MathStatement, ReturnFunc)):
            if cur_statement.rvalue is None:
                cur_statement.rvalue = token
                return parseTokensToStatements(rest, statementlist, token, None)
        
   
    # The rest of this function is all the same but in different formats. Based on the current token, the corresponding 
    # value of the key in the st_dict wil get called and added to the List[Statement]
    elif isinstance(token, EndExprLoop):
        if isinstance( statementlist[-1], IfStatement) and isinstance(statementlist[-2], ConditionsLoop):
            statementlist[-2].expr = statementlist[-1]
            del statementlist[-1]        
        
    elif isinstance( token, (Is, Add, Minus, Times, Divide, Modulo, ExprIfStatement) ):
        return parseTokensToStatements(rest, append(statementlist, st_dict[type(token)](last_token, token, None)), token, statementlist[-1])
    
    elif isinstance( token, Print):
        return parseTokensToStatements(rest, append(statementlist, st_dict[type(token)]()), token, None)
        
    elif isinstance(token, (StartExprLoop, OpenLoop, CloseLoop)):
        return parseTokensToStatements(rest, append(statementlist, st_dict[type(token)]()), token, None)
    
    elif isinstance(token, Return):
        return parseTokensToStatements(rest, append(statementlist, st_dict[type(token)]()), token, statementlist[-1])
    
    elif isinstance(token, OpenFuncParam):
        if isinstance(last_token, Func):
            return parseTokensToStatements(rest, statementlist, token, st_dict[type(last_token)](last_token.content))
        
    return parseTokensToStatements(rest, statementlist, token, cur_statement) 


# This function is the second part of my Parse proces. In this function, The different "scopes" will be created.
# f.e. a loop, a function scope or just te scope for an if statement.
# parseInScopes :: List[Statement] -> Scope -> List[Statement]
def parseInScopes(statementlist : List[Statement], cur_scope : Scope):
    
    if not statementlist:
        return None, cur_scope

    statement, *rest = statementlist
    
    if len(cur_scope.statements) > 1:
        if isinstance(cur_scope.statements[-2], ConditionsLoop  ):
            cur_scope.statements[-2].loop = cur_scope.statements[-1]
            cur_scope.statements.remove(cur_scope.statements[-1])
            
            
    if isinstance( statement, CloseScope):
        return rest, cur_scope
    
    
    elif isinstance( statement, (IfStatement, MathStatement)):
        if isinstance( statement.rvalue, Function):
            newrest, newscope = parseInScopes(statement.rvalue.func_scope, Scope(nest=cur_scope.nestlevel + 1))
            statement.rvalue.func_scope = newscope
    
    elif isinstance( statement, Function):
        newrest, newscope = parseInScopes(statement.func_scope, Scope(nest=cur_scope.nestlevel + 1))
        statement.func_scope = newscope

    elif isinstance( statement, OpenScope ):
        newrest, newscope = parseInScopes(rest, Scope(nest=cur_scope.nestlevel + 1))
        return parseInScopes(newrest, cur_scope.add_statement(newscope))
        
    return parseInScopes(rest, cur_scope.add_statement(statement))
 
# Parse :: List[Token] -> List[Statement]
def Parse(tokenlist : List[Token]):
    return parseInScopes(parseTokensToStatements(tokenlist, [], None, None)[1], Scope())

def get_func_def(func_decl : List, func_name : str ):
    # This is absolutely not functional, I know, but I had a very hard time fixing it another way...
    # this searches for the name of the func in the List::state.func_list[Tuple(String, List[Token])] to combine them.
    # This is a very complicated line, but the function of it is pretty simple
    
    # In the "main" of this project, I "pre-compiled" my functions. I Lexed all my function declarations and combined that with a string (the name of the function) in a Tuple..
    # So I could easily search for the declaration of a certain function and just this line combined the function the runner found with one of the "pre-compiled" functions.
    f = list(filter(None, map( lambda x, y: x[1] if x[0] == y else None , func_decl, [func_name]*len(func_decl))))[0]
    
    # This is unfortunately needed...mosstly because I couldn't figure out a better way of fixing it.
    # The "pre-compiled" functions all had one scope too much and the program couldn't work with that, so I had to 
    # "manually" remove the outter loop (this is just to start the function scope).
    if isinstance(f[4], OpenLoop):
        del f[4]
        if isinstance(f[-1], CloseLoop):
            del f[-1]
    
    return Parse(f)[1]
            
            
            
            
            
            
   