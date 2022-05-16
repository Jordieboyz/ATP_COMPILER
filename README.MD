# ATP

Hello, visiter of this Repo. My name is Jort de Boer and I am a Technical Informatics student at the Hogeschool Utrecht.

This project contains my ATP (Advanced Technical Programming) project. This is part of a cource given in my third year of the study.
For this project we ahd to write an interpreter and compiler for (in my case) a complete custom language. 

The custom languague has to be Turing-complete and needed to have at least some kind of loops or GO-TO statements.
We had to write (mostly) functional style code. I wrote both the interpreter and the compiler(for the most part) in Python.


# My Custom Language, Symbolic
I don't really have a name for my custom language, but for now I'll call it "symbolic".
The language is Turing complete because it supports function calls, loops, if statements, simple operators like +, -, *, /, % and the assignment operator.

my language supports:

assigning variables and numbers 
using operators( -, +, *, /, %) 
loops
if-statements
"return"
scoping

The code supports 1 file where the code and all the function declaration are in.
Function-params are just passed in the parantheses, like a c++ function.
Function could call other function (recursion supported)
Function result doesn't imediately printed. The whole program needs to end and if it returned somewhere in the middle, after the return, no operations get executed anymore.
You return based on the '.' operator. you call it with the rvalue you like and that gets "printed" at the end of the whole interpret.

Below, here are all the operators in my language and their syntax.

math-operators:
    myLanguage           (C++) synnonym
    
        =         ->        =
            -> a = 3
            -> a = b
            -> a = func(n)
        
        +         ->        +=    
            -> a + 1
            -> a + b
            -> a + func(n)

        -         ->        -=    
            -> a - 1
            -> a - b
            -> a - func(n)
            
        *        ->        *=    
            -> a * 1
            -> a * b
            -> a * func(n)
            
        /         ->        /=    
            -> a / 1
            -> a / b
            -> a / func(n)

if-expressions:

        $eq       ->        ==
        $neq      ->        !=
        $gt       ->        >
        $get      ->        >=
        $lt       ->        < 
        $let      ->        >=

bigger-operations:

    [ <EXPR> ]> (...) <                                   this is the loop-format.
    
    func_ <NAME>(<PARAMS>) > (...) .<RETURNVALUE> <      this is the format for a function
    
    <EXPR> > (...) <                                     this is the format for an IF-statement
            
all characters and their fucntion:

    =   assign
    +   add
    -   minus
    *   times
    /   divide
    %   modulo
    []  expr for a loop
    ()  function parameter list
    .   return
    $   if-exppression
    <   open a new scope
    >   close a scope
    #   VERY IMPORTANT! this is the actual code and function declaration separator. This needs to stand in betweend these 2 in the same file.
    func_ This indicates the start of a function declaration
    
    
# The Interpreter

You can find the interpereter and its files in the "/interpreter" directory.

You can run is by executing the "main.py" <INPUT_FILE>
f.e. [ python3 main.py test_func00.txt ]

the "INPUT_FILE" is essentially a file where an example of my custom language is written.

for the exercise, I had to use the next features and higher orde functions in my code.

Classes with inheritance        -> yes (tokens.py, parser.py)
Object-printing for every class -> yes
Type-annotation                 -> yes

3 Higher orde Functions:
Map    -> main.py      ; line 3   and ProgState.py ; line 103 
Filter -> ProgState.py ; line 103
Reduce -> main.py      ; line 13

P.S. the lines ending on '3' is just a coincedence lmao

link to explaining: https://youtu.be/fgYMcvStBdg

# The Compiler

You can find everything neeeded for the compiler to run in the "/compiler" directory

You can run the compiler by executing the run.sh <INPUT_FILE> <OUTPUT_FILE>
f.e. [ ./run.sh test_func00.txt out.asm ]

run.sh is a bash script I quickly wrote to combine the output of the python code (the compilation)
with the makefile where I flash the output to the arduino due.

the "INPUT_FILE" is essentially a file where an example of my custom language is written.
the "OUTPUT_FILE" is the ASM (yes it has to be an .asm file) file where the compiler will write the output to.
This will also be the file which will be compiled to binary and later flashed to the arduino to run it.

The compiler took me a lot of time to get it to work. 

I opted to NOT use complete bmptk or hwlib library to get my compiler to work. The reason why is because I wanted it to be
independent, a project on its own, without the need of those libraries. So that is what I did. I ofcourse used third party software, there licence are in the "3th_licence.txt"
 
I used BOSSA (Basic Open Source SAM-BA Application) to flash the code (by that point already converted in a main.bin file) to my arduino due. 
"BOSSA is a flash programming utility for Atmel's SAM family of flash-based ARM microcontrollers."

I used lpc21isp pretty much for the working of the console.

I also distributed a couple files from BMPTK for creating a linkerscript which were needed to make the main.ld.
these are the cortex.c and the linkerscript_cortex.c.

## The makefiles 
I used a chain of makefiles to make the "C++" part of the compiler (compiling the .asm file and flashing it to the arduino) work.

I starts with the makefile in the directory itself (/compiler/Makefile). This makefile adds local (self inputted) files to the SOURCES, HEADERS and SEARCH variables (which will we'll be using later in the makefile.inc). 

After, this makefile wil link to the makefile.ardue.
In this makefile there are some specific arduino settings which are set in this makefile and the last makefile before linking, compiling and finishing the build.

Now we arrive at the makefile.inc
This makefile will build, compile, link, create the needed files and eventually even run the project.

So     Makefile -> Makefile.ardue -> Makefile.inc


## Explanation for the compiler itself when I'm done writing the thing...







