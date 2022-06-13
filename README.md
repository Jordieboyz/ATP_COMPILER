# Advanced Techinical Programming

For this course, I wrote a compiler and an interpreter for my own imaginary "programming language", named Symbolic, in python.
My custom languague has to be Turing-complete and needed to have at least some kind of loops or GO-TO statements.
For the most part, I wrote functional style code.

# My custom language, "Symbolic"

The language is Turing complete because it supports function calls, loops, if statements, simple operators like +, -, * and the assignment operator.

Symbolic supports:

	assigning variables and numbers 	( = ) 
	using operators				( -, +, *, /, % ) 
	scoping					( > < )
	if-statements 			  	( $? )
	"return" 			  	( . )
	loops 				  	( [ $? ]> < )
	functions				( func_ )
	Output					( ~ )

Symbolic symbols and it's C++ synonym:
	
	math-operators:
	    Symbolic	-> (C++) synnonym
		=	->	=
		+ 	->	+=    
		- 	->	-= 
		*	->	*=
		
	if-expressions:
		$eq	->	==
		$neq	->	!=
		$gt	->	>
		$get	->	>=
		$lt	->	< 
		$let	->	>=
 
 	bigger-operations:
		[ <EXPR> ]> (...) <                                  This is the loop-format.
		func_ <NAME>(<PARAMS>) > (...) .<RETURNVALUE> <      This is the format for a function
		<EXPR> > (...) <                                     This is the format for an IF-statement

This is a summary of all the symbols in the language and their functions:

	    =   Assign
	    +   Add
	    -   Minus
	    *	Multiply
	    $   if-exppression
	    .   return
	    ~   Output
	    > <  Scope
	    [ ]  expr for a loop
	    ( )  function parameter list
	    #   VERY IMPORTANT! this is the actual code and function declaration separator.

You can write code in just one file. This file contains the "global"-code and the optional function declarations.
We seperate the functions declaration and the actual code with the "#", this ALWAYS needs to be in the file either in between the global code and the function declaration or at the end of the global code if there are no funtions.
The declaration of a function needs te start with "func_" followed by the name of the function and the parameter list.

Every function NEEDS to return a value with the "." operator.
Functions in my language supports just one parameter.
We can output somthing during the program using the "~" character.
