# makefile which links to a makefile with some arduino specific settings

# SOURCES and HEADERS are used to build and compile the whole project
# SEARCH are folders/paths where to find files
# CLEAN is just for the cleanup 

SOURCES += UART_due.cpp 

# header files in this project
HEADERS := UART_due.h 
HEADERS += waitable.h 

# other places to lookzz for files for this project
SEARCH  := UART 
SEARCH += include

CLEAN += .vscode
CLEAN += __pycache__

RELATIVE	      ?= ../
include           $(RELATIVE)Makefile.ardue
