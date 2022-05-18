# makefile which links to a makefile with some arduino specific settings

# SOURCES and HEADERS are used to build and compile the whole project
# SEARCH are folders/paths where to find files
# CLEAN is just for the cleanup 

SOURCES += UART_due.cpp 

HEADERS := UART_due.h 
HEADERS += waitable.h 

# paths to look for additional files in the project
SEARCH  := UART 
SEARCH += include

# Clean these annoying folder automaticly created by python and vscode
CLEAN += .vscode
CLEAN += __pycache__

RELATIVE	      ?= ../
include           $(RELATIVE)Makefile.ardue
