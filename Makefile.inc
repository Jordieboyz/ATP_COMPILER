# This makefile builds, compiles, link and even runs the project

# find non-local files
vpath %.h    $(SEARCH)
vpath %.hpp  $(SEARCH)
vpath %.asm  $(SEARCH)
vpath %.c    $(SEARCH)
vpath %.cpp  $(SEARCH)


TESTDEF += $(addprefix '-D_', $(basename $(subst $(TESTSDIR)/,,$(shell find tests -name "*.asm")) .asm ))
EXTERNS=  $(foreach name,$(basename $(subst $(TESTSDIR)/,,$(shell find tests -name "*.asm")) .asm ), $(subst @, $(name), extern "C" uint8_t@(); ) ) 
	

#============================================================================
#
# LANGUAGE FLAGS
#
#============================================================================

COMMON        += -Wall -Werror
COMMON        += -Wno-maybe-uninitialized -Wno-unused-local-typedefs -Wno-unused-but-set-variable -Wno-unused-function -Wno-attributes
COMMON        += -Os
COMMON        += -fdata-sections -ffunction-sections
COMMON        += $(foreach x, $(SEARCH), -I$(x))
COMMON 		  += $(TESTDEF) 
	
# add C++-specific flags
CPP_FLAGS     := -std=c++17
CPP_FLAGS     += -fno-rtti 
CPP_FLAGS     += -fno-exceptions -fno-asynchronous-unwind-tables
CPP_FLAGS     += -fno-threadsafe-statics
CPP_FLAGS     += -fno-use-cxa-get-exception-ptr -fno-use-cxa-atexit
CPP_FLAGS     += -nostdlib -nodefaultlibs

# add linker-specific flags
LN_FLAGS      := -lgcc -Wl,--gc-sections -Wl,-fatal-warnings


#=========================================================================
#
# Compile
#
#=========================================================================

#the input *.asm file
SOURCES 	+= $(PROJECT)

SOURCES 	+= main.cpp
SOURCES 	:= $(strip $(SOURCES))

# assuming there are only .c, .cpp or .asm files
OBJECTS      += $(patsubst %.c,%.o,$(patsubst %.cpp,%.o,$(patsubst %.asm,%.o,$(SOURCES))))

DEPENDENCIES += $(HEADERS)
$(OBJECTS): $(DEPENDENCIES)

%.o:$(DEPENDENCIES)

# How to make an object file from an assembler file
%.o: %.asm
	@echo '$(EXTERNS)' > include_tests.h  
	@echo $(COMMON) > _common_flags
	"arm-none-eabi-gcc" @_common_flags -x assembler-with-cpp -c -o $@ $<

# How to make an object file from a C file
%.o: %.c
	@echo $(COMMON) > _common_flags
	"arm-none-eabi-gcc" @_common_flags -std=c11 -c -o $@ $<


# How to make an object file from a C++ file (.cpp)
%.o: %.cpp
	@echo $(COMMON) > _common_flags
	@echo $(CPP_FLAGS) > _cpp_flags
	"arm-none-eabi-g++" @_common_flags @_cpp_flags -c -o $@ $<



#=========================================================================
#
# create the linkerscript from the template
#
#=========================================================================

LD_CONFIG    += -DROM_START=0x00000000 -DROM_SIZE=512k 
LD_CONFIG    += -DRAM_START=0x20070000 -DRAM_SIZE=96k

# How to make a linkerscipt by preprocessing a .c linkerfile template
main.ld: $(CORTEX_LD)
	"arm-none-eabi-gcc" $(LD_CONFIG) -E -P -C $< -o $@
	

# make .elf by linking all objects
main.elf: $(addprefix ./,$(OBJECTS)) main.ld 
	@echo $(LN_FLAGS) > _linker_flags
	"arm-none-eabi-g++" @_common_flags @_linker_flags -o $@ $(OBJECTS)  -nostdlib -nodefaultlibs -nostartfiles -lm -lgcc -lc -T main.ld -Iinclude/cortex/atmel/sam3xa/source/as_gcc
	
# How to make a .bin file from an .elf file
main.bin: main.elf
	"arm-none-eabi-objcopy" -O binary -R .bss $< $@


#============================================================================
#
# cleanup
#
#============================================================================

CLEAN		+= _common_flags _linker_flags _cpp_flags
CLEAN   	+= main.ld main.bin main.elf
CLEAN       += $(OBJECTS)
CLEAN 		+= .vscode
CLEAN 		+= __pycache__

#============================================================================
#
# RUN OR SOMETHING
#
#============================================================================

SERIAL_PORT		?= $(shell ls /dev/ttyACM?)
LPC21ISP_EXE	?= include/tools/lpc21isp_197/lpc21isp_hr_linux.exe
BOSSAC 			?= include/tools/BOSSA-Arduino/bin/bossac

.PHONY: main run clean info
	
main: main.bin
run: main $(LPC21ISP_EXE) $(BOSSAC)
	$(SUDO) stty -F $(SERIAL_PORT) speed 1200 cs8 -cstopb -parenb; sleep 1.0
	-$(SUDO) $(BOSSAC) --port=$(subst /dev/,,$(SERIAL_PORT)) --force_usb_port=false -e -w -v -b main.bin -R
	$(SUDO) $(LPC21ISP_EXE) -termonly -term main.hex $(SERIAL_PORT) 115200 12000

cleanall:
	rm -rfd *.o tests/*.asm tests/create_tests *.asm $(CLEAN) tests/*.tst include_tests.h

clean:
	rm -rfd $(CLEAN)