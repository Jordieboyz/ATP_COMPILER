# The Compiler

Everything we need is in this directory except for the templates for the unit_tests. These can be found in the root of this repo (/templates).

# What does the Compiler Support
This compiler supports these operators and operands in my custom language, Symbolic:
	
	Assign:
		var = number
		var = var
		var = func_
		
	Math:
		var + number
		var + var
		var + func_ (not tested!)
		
		var - number
		var - var
		var - func_ (not tested!)
		
		var * number
		var * var
		var * func_ (not tested!)
		
	If-statement:
		- var $expr var
		- var $expr number
		- var $expr func_ (not tested!)
		
	Return:
		- number
		- var
		- func_
		
	functions:
		- func_(var)
		- func_(number)

# How to run the Compiler

You can run a script which creates all the unit tests, builds the .asm files, flashes everything to the arduino_due and runs the program.
The script file is called: "run.sh"

So run this command and it will build and execute everything: 

	./run.sh


# The proces of the compiler

The compiler is all in all 2 seperate programs combined. We have a part which we run native and a part we can flash and run on the arduino. Let's start talking about the native part. 

![overview_compiler drawio](https://user-images.githubusercontent.com/60455414/173268001-cb037b8a-6261-49be-be0b-f46570bc6872.png)

For this part of the course, we had to write unit tests (preferably in C++).
To make these unit tests. I made some templates to create actual testable files out of. (see ../templates). The files "tests/create_tests.cpp" does exactly that.

This is a native program, so we can use the C++ libraries for an input and output stream. The program uses one simple function; create_test. This function opens, reads, replaces '?' with actual variables and writes everything to the output (.tst) file based on the info which we already got from the struct which is filled with information for specific tests and are created in the main function.

Before we can run these unit tests (or .tst files at this point), we need to turn these .tst files into .asm files (so we can flash and run them on the ardunio_due). Here come all the pytthon files in handy. in essention, this part of the program turns the .tst files into .asm files. I'm not gonna explain all of the indepths of this, because evything is also commented in the (.py) files itself.

At this point we have: .asm files based on the .tst files which were created based on the templates in the root foler. The only thing left to do is compiling and flashing all the .asm files to the arduino so we can run the unit tests on the arduino_due.

Here we're finally gonna use the main.cpp, waitable.h and the (self-written) UART-driver.
To start off, the main.cpp contains all the unit tests. these tests are C-peprocessor based and are based on the filenames of the already created test.
The waitable.h is a simple delay, wait, stop of the program, I only needed this to give lpc21isp time to start the console. I wrote a timer based on the SysTick.
Then at last, my own UART-driver. it is not a big part of this whole program, but it was a bit of a stretch to figure out what I had to do to make it work.

Ater all of these steps, we (or run.sh) flashes and run the main.cp with all the .asm files and we get to know what unit tests passed or failed.

# Libraries
I opted to NOT use complete bmptk or hwlib library to get my compiler to work. The reason why is because I wanted it to be
independent, a project on its own, without the need of those big libraries. So that is what I did. I ofcourse used third party software, their licences are in the "licence.txt" in the root directory.
 
Some third party fortware I used is BOSSA.
I used BOSSA (Basic Open Source SAM-BA Application) to flash the code (by that point already converted in a main.bin file) to my arduino due. 
"BOSSA is a flash programming utility for Atmel's SAM family of flash-based ARM microcontrollers."

I also used lpc21isp as a third party software and get the console used it to get the console working in paralel with the arduino_due.

I also used a couple files from BMPTK for creating a linkerscript which were needed to make the main.ld.
these are the cortex.c and the linkerscript_cortex.c.

## The makefiles 
I used a chain of makefiles to make the "C++" part of the compiler (compiling the .asm file and flashing it to the arduino) work.

It starts with the makefile in the directory itself (/compiler/Makefile). This makefile adds local (self inputted) files to the SOURCES, HEADERS and SEARCH variables (which will we'll be using later in the makefile.inc). 

After, this makefile wil link to the makefile.ardue.
In this makefile there are some specific arduino settings which are set in this makefile and the last makefile before linking, compiling and finishing the build.

Now we arrive at the makefile.inc
This makefile will build, compile, link, create the needed files and eventually flashes and even runs the project.

So:
	
	Makefile -> Makefile.ardue -> Makefile.inc
