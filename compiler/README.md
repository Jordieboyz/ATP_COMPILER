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


