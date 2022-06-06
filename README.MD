# ATP

Hello, visiter of this Repo. My name is Jort de Boer and I am a Technical Informatics student at the Hogeschool Utrecht.

This project contains my ATP (Advanced Technical Programming) project. This is part of a cource given in my third year of the study.
For this project we ahd to write an interpreter and compiler for (in my case) a complete custom language. 

The custom languague has to be Turing-complete and needed to have at least some kind of loops or GO-TO statements.
We had to write (mostly) functional style code. I wrote both the interpreter and the compiler (for the most part) in Python.


# My Custom Language, Symbolic
I don't really have a name for my custom language, but for now I'll call it "symbolic".
The language is Turing complete because it supports function calls, loops, if statements, simple operators like +, -, *, /, % and the assignment operator.

my language supports:

assigning variables and numbers 	( = ) 
using operators			( -, +, *, /, % ) 
scoping				( > < )
if-statements 			  	( $? )
"return" 			  	( . )
loops 				  	( [ $? ]> < )
functions				( func_ )
Output					( ~ )

You can write code in just one file. This file contains the "global"-code and the optional function declarations.
We seperate the functions declaration and the actual code with the "#", this ALWAYS needs to be in the file either in between teh global code and the function declaration or at the end of the global code if there are no funtions.
The program returns based on the '.' symbol. in case of the interpreter, the porgram ends here. in case of the compiler, the return value gets moved to R0.
Recursion is implemented in my custom language.
We can output somthing during the program using the "~" character.


Below, here are all the operators in my language and their syntax.
math-operators:
    Symbolic      ->   (C++) synnonym
        =         ->        =
        +         ->        +=    
        -         ->        -=    
 
f.e.:
	var = 4	->	var = 4
	var + 9 	->	var = 13
	var - 6	->	var = 7
	
	z = 3		->	var = 4 and z = 3
	var - z	->	var = 3 and z = 3
	z + 11		->	var = 3 and z = 14
	z - var	->	var = 14 and z = 11 

if-expressions:
        $eq       ->        ==
        $neq      ->        !=
        $gt       ->        >
        $get      ->        >=
        $lt       ->        < 
        $let      ->        >=

bigger-operations:
    [ <EXPR> ]> (...) <                                  This is the loop-format.
    func_ <NAME>(<PARAMS>) > (...) .<RETURNVALUE> <      This is the format for a function
    <EXPR> > (...) <                                     This is the format for an IF-statement
            
all characters and their fucntion:
    =   assign
    +   add
    -   minus
    []  expr for a loop
    ()  function parameter list
    .   return
    $   if-exppression
    <   open a new scope
    >   close a scope
    ~   Output
    #   VERY IMPORTANT! this is the actual code and function declaration separator. This needs to stand in between these 2 in the same file.
    func_ This indicates the start of a function declaration
    





