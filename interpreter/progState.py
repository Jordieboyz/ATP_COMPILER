from Parser import MathStatement
from tokens import Is, Number, Variable, Add, Minus ,Times, Divide, Modulo, CloseLoop, OpenLoop
from Parser import Parse, ConditionsLoop, IfStatement, ReturnFunc, Function, Scope


exec_dict = {
    Add : "+=",
    Minus : "-=",
    Times : "*=",
    Divide : "/=",
    Modulo : "%",
    'eq' : lambda l, r: l == r ,
    'neq' : lambda l, r: l != r,
    'gt' : lambda l, r: l > r,
    'get' : lambda l, r: l >= r,
    'lt' : lambda l, r: l < r,
    'let' : lambda l, r: l <= r,
}


class ProgramState:
    def __init__(self, func_list  = None):
        self.cells = dict()
        self.cur_loop = None
        self.cur_func = None
        self.last_statement = None
        self.scope_vars = []
        self.returned = False
        self.func_list = func_list
        
        
    def __str__(self) -> str:
        return self.cells.__str__()

    def __repr__(self) -> str:
        return self.__str__()
    
    def add_to_mem(self, name, value = 0):
        if not self.returned:
            if name:
                if isinstance(name, Variable) and isinstance( value, Number):
                    self.cells[name.content] = int(value.content)
                
                elif value == 0:
                    self.cells[name.content] = 0
                    
                elif isinstance(name, Function):
                    if isinstance(value , Number):
                        self.cells[name.funcname] = int(value.content)
                    else:
                        self.cells[name.funcname] = int(value)
                elif isinstance( name, Variable) and isinstance( value, Variable):
                    self.cells[name.content] = self.cells[value.content]
                
                elif isinstance(name, Variable):
                    if isinstance(value, Variable):
                        self.cells[name.content] = self.cells[value.content]
        return self
                           
                            
    def op_on_var(self, name : str, operator, value : int):
        make_exec = lambda l, o, r: l.__str__() + o.__str__() + r.__str__()          
        
        if isinstance( operator, Is):
            if not self.returned:
                self.add_to_mem(name, value)
        
        if name and isinstance( name, Variable):            
            if not self.returned:
                if isinstance( value, Number ):
                    if name.content in self.cells:
                        if type(operator) in exec_dict: 
                            exec(make_exec('self.cells[name.content]', exec_dict[type(operator)] , 'int(value.content)'))
                        
                elif isinstance(value, Variable):
                    if value.content in self.cells:
                        if name.content in self.cells:
                            if type(operator) in exec_dict:
                                exec(make_exec('self.cells[name.content]', exec_dict[type(operator)] , 'self.cells[value.content]'))
        return self
        
    def evaluate_expr(self, expr):
        if not self.returned:
            if isinstance(expr.lvalue, Variable):
                if expr.lvalue.content in self.cells:
                    if isinstance( expr.rvalue, Number ):
                        if expr.operator.expr in exec_dict:
                            return exec_dict[expr.operator.expr](self.cells[expr.lvalue.content], int(expr.rvalue.content))


# This function creates and runs the scope. until this point, the Lexer and Parser both don't no anything about
# the declaration of the function. This is what this function does and immediately "runs"  this scope
# runFunction :: ProgramState -> Int -> (ProgramState, Int)
def runFunction( state: ProgramState, output : int):
    if isinstance(state.cur_func, Function):
        if len(state.cur_func.func_scope.statements) == 0:
            
            # This is absolutely not functional, I know, but I had a very hard time fixing it another way...
            # this searches for the name of the func in the List::state.func_list[Tuple(String, List[Token])] to combine them.
            # This is a very complicated line, but the function of it is pretty simple
            
            # In the "main" of this project, I "pre-compiled" my functions. I Lexed all my function declarations and combined that with a string (the name of the function) in a Tuple..
            # So I could easily search for the declaration of a certain function and just this line combined the function the runner found with one of the "pre-compiled" functions.
            f = list(filter(None, map( lambda x, y: x[1] if x[0] == y else None , state.func_list, [state.cur_func.funcname]*len(state.func_list))))[0]
            
            # This is unfortunately needed...mosstly because I couldn't figure out a better way of fixing it.
            # The "pre-compiled" functions all had one scope too much and the program couldn't work with that, so I had to 
            # "manually" remove the outter loop (this is just to start the function scope).
            if isinstance(f[4], OpenLoop):
                del f[4]
                if isinstance(f[-1], CloseLoop):
                    del f[-1]

            tokens = Parse(f)[1]
            state.cur_func.func_scope.statements = tokens.statements[1:]
            # print(tokens.statements[1:])
            state.add_to_mem(tokens.statements[0].func_params[0], state.cur_func.func_params[0])
            state.last_statement = None
            state.cur_loop = None
            
    if state.cur_func.returned is True:
        return state, output
    
    else:
        state_, output_ = runScope(state.cur_func.func_scope, state, None)
        state.cur_func.ret_val = output_
        state.add_to_mem(Variable(state.cur_func.funcname), Number(output_))
        if output_ is not None:
            state.cur_func.returned = True
            
        return runCode(state.cur_func.func_scope, 0, state_, output_)

# This function functions like a while loop in c++. You have a condidion and constantly checked every cycle. 
# So, we check if the condition is True other wise we continue in the loop

# runLoop :: Scope -> ProgramState -> Int -> (ProgramState, Int)
def runLoop( scope : Scope, state : ProgramState, output : int ):
    if state.cur_loop is not None:
        if not state.evaluate_expr(state.cur_loop) or output is not None:
            return state, output
        else:
            state_, output_ = runCode(scope, 0, state, output)
            return runLoop(scope, state_, output_)


# This function just runs one loop. f.e. an if-statement. An if-statement always had a scope.
# To run just that one scope, you use this function. It is very similar to the function above, but for clearance purpose, I separated them.

# runLoop :: Scope -> ProgramState -> Int -> (ProgramState, Int)        
def runScope( scope : Scope, state : ProgramState, output  : int):
    if state.last_statement is not None:
        if not state.evaluate_expr(state.last_statement) or output is not None:
            return state, output
        else:
            return runCode(scope, 0, state, output)
    else:
        return runCode(scope, 0, state, output)

# This is the runner. The runner loops through the list the parser created and tries to execute the statements.

# runLoop :: Scope -> Int -> ProgramState -> Int -> (ProgramState, Int)
def runCode(code : Scope, ptr : int, state : ProgramState,  output : int):
    if(ptr >= len(code.statements)):
        return state, output
    
    if state.cur_func is not None:
        if state.cur_func.returned:
            return state, output
        
    cur = code.statements[ptr]

    
    # A MathStatement is just a statement with the =, -, +, *, % or / operator.    
    if isinstance( cur, MathStatement):
        
        # here, We check if the rvalue of the statement is a Function.
        if isinstance(cur.rvalue, Function):
            state.cur_func = cur.rvalue
            state_, output_ = runFunction(state, output)
            if output_ is not None:
                state_.add_to_mem(cur.lvalue, Number(output_))
                state_.cur_func = None
                return runCode( code, ptr + 1, state_, output_)
        else:  
            state.op_on_var(cur.lvalue, cur.operator, cur.rvalue)
        return runCode( code, ptr + 1, state, output)
    
    # Here, if the current statement is a fucntion statement, we run the "runfunction" and run the scope of the current function
    elif isinstance( cur, Function):
        state.add_to_mem(Variable(cur.funcname))
        state.cur_func = cur

        state_, output_ = runFunction(state, output)

        state.cur_func = None
        return runCode(code, ptr + 1, state_, None)
        
    
    # The '.'-symbol symbolizes a return out of a function f.e.. There are different return values. just a Number, a Variable, but also a Function (recursion f.e.)
    # We need to handle at least all of these.
    elif isinstance( cur, ReturnFunc):
        if isinstance(cur.rvalue , Function):
            state.add_to_mem(Variable(cur.rvalue.funcname))
            state.cur_func = cur.rvalue
            state.cur_func.func_scope = Scope()
    
            state_, output_ = runFunction(state, output)
            return runCode(code, ptr + 1, state_, output_)
        elif state.cur_func is not None:
            if isinstance(state.cur_func, Function):
                state.cur_func.returned = True
                state.cur_func.ret_val = cur.rvalue
   
                if state.cur_func.ret_val is not None:
                    if isinstance( cur.rvalue, Number):
                        state.cur_func.ret_val = int(cur.rvalue.content)
                        return runCode(code, ptr + 1, state, state.cur_func.ret_val)
                    else:
                        state.cur_func.ret_val = state.cells[cur.rvalue.content]
                        return runCode(code, ptr + 1, state, state.cells[cur.rvalue.content])
        elif isinstance(cur.rvalue, Number):
            state.returned = True
            return runCode(code, ptr + 1, state, int(cur.rvalue.content))
        elif isinstance(cur.rvalue, Variable):
            state.returned = True
            return runCode(code, ptr + 1, state, state.cells[cur.rvalue.content])
    
    # If the current statement is an ifstatement, we evaluate it and based on the result we continue or skip the next statement.
    elif isinstance( cur, IfStatement):
        if state.evaluate_expr( cur ) :
            state.last_statement = cur
            return runCode(code, ptr + 1, state, output)
        else:
            return runCode(code, ptr + 2, state, output)

    # This is de indication of the "c++ while loop".
    elif isinstance( cur, ConditionsLoop):
        if state.evaluate_expr( cur.expr ) :
            state.cur_loop = cur.expr
            return runCode(code , ptr + 1, state, output)
        else:
            return runCode(code, ptr + 2, state, output)
    
    # Here, we run a scope based on the statement which indicates the start of a scope.
    elif isinstance( cur, Scope):
        if isinstance( code.statements[ptr - 1], IfStatement):
            state_, output_ = runScope(cur, state, None)
            return runCode(code, ptr + 1, state_, output_)
        elif isinstance( code.statements[ptr -1], ConditionsLoop):
            state_, output_ = runLoop(cur, state, None)
            return runCode(code, ptr + 1, state_, output_)
    else:    
        return runCode(code, ptr + 1, state, output)    