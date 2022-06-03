from tokens import Token, Func, Number, Variable, Is, ExprIfStatement, \
                   OpenFuncParam, Print, \
                   Add, Minus, Divide, Times, Modulo, OpenLoop, CloseLoop, \
                   StartExprLoop, Return
    

st_dict : dict() = {
    Is              : lambda l, op, r: MathStatement(l, op, r),
    Add               : lambda l, op, r: MathStatement(l, op, r),
    Minus             : lambda l, op, r: MathStatement(l, op, r),
    Times             : lambda l, op, r: MathStatement(l, op, r),
    Divide            : lambda l, op, r: MathStatement(l, op, r),
    Modulo            : lambda l, op, r: MathStatement(l, op, r),
    ExprIfStatement   : lambda l, op, r: IfStatement(l, op, r),
    OpenLoop          : lambda : OpenScope(),
    CloseLoop         : lambda : CloseScope(),
    StartExprLoop     : lambda : ConditionsLoop(),
    Func              : lambda n : Function(n),
    Return            : lambda : ReturnFunc(),
    OpenFuncParam     : lambda n : Function(n),
    Print             : lambda : Output()
}
    
class Statement():
    def __str__(self):
        return "undefined statement"

class Scope:
    def __init__(self, nest : int = 1):
        self.statements = []
        self.nestlevel = nest
    
    def add_statement(self, statement : Statement):
        self.statements.append(statement)
        return self
    
    def __str__(self):
        return self.statements.__str__()
    
    def __repr__(self):
        return self.__str__()


class MathStatement(Statement):
    def __init__(self, lvalue : Variable, operator : Token, rvalue : Number):
        self.lvalue = lvalue
        self.operator = operator
        self.rvalue = rvalue
        
    def __str__(self):
        return "{} with: {} {} {}". \
            format(type(self).__name__, self.lvalue, self.operator, self.rvalue)
    
    def __repr__(self):
        return self.__str__()
    
    
class IfStatement(Statement):
    def __init__(self, lvalue, operator, rvalue):
        self.lvalue = lvalue
        self.operator = operator
        self.rvalue = rvalue
        
    def __str__(self):
        return "{} with: {} {} {}". \
            format(type(self).__name__, self.lvalue, self.operator, self.rvalue)
    
    def __repr__(self):
        return self.__str__()
        
class Function(Statement):
    def __init__(self, funcname : str):
        self.funcname = funcname
        self.func_params = []
        self.func_scope = []
        self.ret_val = None
        self.returned = False
        
    def __str__(self):
        return "{} {} with {} \t{}".format(type(self).__name__, self.funcname, self.func_params, self.func_scope.__str__())
    
    def __repr__(self):
        return self.__str__()

    
class ConditionsLoop(Statement):
    def __init__(self):
        self.expr = None
        self.loop = []
        
    def __str__(self):
        return "{} with: {} with scope:  {}". \
            format(type(self).__name__, self.expr, self.loop)
    
    def __repr__(self):
        return self.__str__()
    
class OpenScope(Statement):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class CloseScope(Statement):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class ReturnFunc(Statement):
    def __init__(self):
        self.rvalue = None
        
    def __str__(self):
        return "{} with: {}". \
            format(type(self).__name__, self.rvalue)
    
    def __repr__(self):
        return self.__str__()

class Output(Statement):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()