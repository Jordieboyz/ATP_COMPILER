from typing import List
from tokens import Token, Func, Number, Variable, ExprIfStatement, \
                   OpenFuncParam, tokendict


# This is the "main" lex function. This function creates and returns a list
# of Token(s). The String::Buff is used as a buffer f.e. variable names, and numbers
# which are usually more then one character long. 

# lex_it :: String -> List[Token] -> String -> List[Token]
def lex_it( file_string : str, tokenlist : List[Token], buff : str):
    # Return the List[Token] if you encountered all the characters in the String::file_string
    if not file_string:
        return tokenlist
    
    # Get exectly one character every recursion, continue recursion with the rest of it
    c, *rest = file_string 
    
    if c in '#_':
        return tokenlist
    
    # Ignore Spaces, Newlines and Tabs. Just add a Token based on the String::Buff 
    if c in ' \t\n':
        if buff:
            tokenlist.append(Number(buff)) if buff[0].isnumeric()     \
                else tokenlist.append(Variable(buff))
            buff = ''
    
    # Add a number or char to the String::buff
    # This is viable because every "opeartor" or "language defined character"
    # is always a symbol, not an number or char
    elif c.isnumeric() or c.isalpha():
        buff += c  
    
    # Create Token if the current character is a Language Defined Character
    elif c in r'=+-*()[]<>%$.':
        if buff:
            tokenlist.append(Number(buff)) if buff[0].isnumeric()     \
                else tokenlist.append(Variable(buff))
            buff = ''
        
        # See "tokendict" for the already mapped values
        if c in tokendict:   
            tokenlist.append(tokendict[c]())
   
    return lex_it(rest, tokenlist, buff)


# This function combines certain tokens to give their final meaning
# f.e. [ Token::Variable + Token::OpenFuncParam ] == [ Token::Func ]
# and  [ Token::ExprIfStatement ('$') + Token::Variable (eq) ] == [ Token::ExprIfStatement('$eq') ]
                   
# finish_lexing :: List[Token] -> Int -> List[Token]
def finish_lexing(tokens: List[Token], idx : int):
    if not idx < len(tokens):
        return tokens
    
    # Variable + OpenFuncParam == Func
    if isinstance(tokens[idx], OpenFuncParam):
        tokens[idx - 1] = Func(tokens[idx - 1].content)
    
    # fix the "$-exprsessions" f.e.  ($) + (eq) or ($) + (lt)        
    if isinstance(tokens[idx], ExprIfStatement):
        tokens[idx].expr = tokens[idx + 1].content
        del tokens[idx + 1]
    return finish_lexing(tokens, idx + 1)
        
# lex :: String -> Int -> List[Token]
def lex(file_str : str, start_from : int = 0):
    return finish_lexing(lex_it(file_str[start_from:], [], ''), 0)