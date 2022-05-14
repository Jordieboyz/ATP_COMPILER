tokendict : dict() = {
    '=' : lambda: Is(), 
    '+' : lambda: Add(),
    '-' : lambda: Minus(),
    '*' : lambda: Times(),
    '/' : lambda: Divide(),
    '%' : lambda: Modulo(),
    ',' : lambda: Comma(),
    '>' : lambda: OpenLoop(),
    '<' : lambda: CloseLoop(),
    '(' : lambda: OpenFuncParam(),
    ')' : lambda: CloseFuncParam(),
    '$' : lambda: ExprIfStatement(),
    '[' : lambda: StartExprLoop(),
    ']' : lambda: EndExprLoop(),
    '?' : lambda: StartIfStatement(),
    '.' : lambda: Return()
   }

class Token:
    def __init__(self, content : str = ''):
        self.content = content

    def __str__(self):
        return "undefined"
            
    def __repr__(self):
        return self.__str__()

class Func(Token):
    def __init__(self, content : str):
        self.content = content
    
    def __str__(self):
        return "{}('{}')".\
            format(type(self).__name__, self.content)
    
    def __repr__(self):
        return self.__str__()
    
    
class Number(Token):
    def __init__(self, content : str):
        self.content = content
    
    def __str__(self):
        return "{}('{}')".\
            format(type(self).__name__, self.content)
    
    def __repr__(self):
        return self.__str__()
    
    
class Variable(Token):
    def __init__(self, content : str):
        self.content = content
    
    def __str__(self):
        return "{}('{}')".\
            format(type(self).__name__, self.content)
    
    def __repr__(self):
        return self.__str__()
    
class Is(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class If(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()

class ExprIfStatement(Token):
    def __init__(self):
        self.expr = ''
        
    def __str__(self):
        return "${}".format(self.expr)
    
    def __repr__(self):
        return self.__str__()
    
class StartIfStatement(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()

class CloseFuncParam(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()

class OpenFuncParam(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()

class Add(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class Comma(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class Minus(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class Return(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class Divide(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class Times(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()

class Modulo(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class OpenLoop(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class CloseLoop(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()

class StartExprLoop(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()
    
class EndExprLoop(Token):
    def __str__(self):
        return type(self).__name__
    
    def __repr__(self):
        return self.__str__()