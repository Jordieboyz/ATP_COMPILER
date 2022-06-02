import re
import sys
from functools import reduce
from lexer import lex
from Parser import Parse
from compiler import compile_as
        
# The 2 function create the "function declarations" for functions defined AFTER the '#' in the test-file.
# The output of these functions combined is a Tuple: (String, List[Token])
def make_list_for_func_declarations(func):
    def inner(func_list, function_content):
        return  list(map( lambda x: (x.group()[6:],                          \
                           lex(function_content, x.start() + len('func_'))), \
                               func(function_content)))
    return inner

# create_func_declarations :: String -> (String, List[Token])
@make_list_for_func_declarations
def create_func_declarations(function_content):
    return list( re.finditer(r'func_ (\w+)', function_content ))

# FILE_NAME = sys.argv[1]
# OUTPUT_FILE_NAME = sys.argv[2]

FILE_NAME = "test_func01.txt"
OUTPUT_FILE_NAME = "out.asm"

content = reduce(lambda x, y: x + y, open(FILE_NAME, "r").readlines())

lexed = lex(content)

_, parsed = Parse(lexed)


compile_as(parsed.statements, create_func_declarations([], content.split('#')[1]), OUTPUT_FILE_NAME)
