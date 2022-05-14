SOURCES 	+= main.cpp
SOURCES 	:= $(strip $(SOURCES))
SOURCES         += bmptk_cortex.c

# arduino specific folders
SEARCH		+= include/cortex
SEARCH		+= include/cortex/atmel
SEARCH		+= include/cortex/atmel/sam3xa/include

# assuming only the .c, .cpp or .asm extensions are used
OBJECTS      += $(patsubst %.c,%.o,$(patsubst %.cpp,%.o,$(patsubst %.asm,%.o,$(SOURCES))))

DEPENDENCIES += $(HEADERS) $(MAKEFILE)
$(OBJECTS): $(DEPENDENCIES)


# find non-local files
vpath %.h    $(SEARCH)
vpath %.hpp  $(SEARCH)
vpath %.asm  $(SEARCH)
vpath %.c    $(SEARCH)
vpath %.cpp  $(SEARCH)

#============================================================================
#
# LANGUAGE FLAGS
#
#============================================================================

COMMON        :=
COMMON        += -mcpu=cortex-m3 -mthumb -fomit-frame-pointer -march=armv7-m
COMMON        += -Wall -Werror
COMMON        += -Wno-maybe-uninitialized -Wno-unused-local-typedefs -Wno-unused-but-set-variable -Wno-unused-function -Wno-attributes
COMMON        += -Os
COMMON        += -fdata-sections -ffunction-sections
COMMON        += $(foreach x, $(SEARCH), -I$(x))

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
%.o:$(DEPENDENCIES)

# How to make an object file from an assembler file
%.o: %.asm
	@echo 'Assembling (.asm) file: $<'
	@echo $(COMMON) > _common_flags
	"arm-none-eabi-gcc" @_common_flags -x assembler-with-cpp -c -o $@ $<
	@echo ' '

# How to make an object file from a C file
%.o: %.c
	@echo 'Compiling C (.c) file: $<'
	@echo $(COMMON) > _common_flags
	"arm-none-eabi-gcc" @_common_flags -std=c11 -c -o $@ $<
	@echo ' '

# How to make an object file from a C++ file (.cpp)
%.o: %.cpp
	@echo 'Compiling C++ (.cpp) file: $<'
	@echo $(COMMON) > _common_flags
	@echo $(CPP_FLAGS) > _cpp_flags
	"arm-none-eabi-g++" @_common_flags @_cpp_flags -c -o $@ $<
	@echo ' '


#=========================================================================
#
# create the linkerscript from the template
#
#=========================================================================

LD_CONFIG    += -DROM_START=0x00000000 -DROM_SIZE=512k 
LD_CONFIG    += -DRAM_START=0x20070000 -DRAM_SIZE=96k

# How to make a linkerscipt by preprocessing a .c linkerfile template
main.ld: bmptk_linkerscript_cortex.c
	@echo 'Creating the linkerscript'
	"arm-none-eabi-gcc" $(LD_CONFIG) -E -P -C $< -o $@
	@echo ' '

#=========================================================================
#
# .elf processing
#
#=========================================================================

# make .elf by linking all objects
main.elf: $(addprefix ./,$(OBJECTS)) main.ld
	@echo 'Linking ELF target: main.elf'
	@echo $(COMMON) > _common_flags
	@echo $(LN_FLAGS) > _linker_flags
	"arm-none-eabi-g++" @_common_flags @_linker_flags -o $@ $(OBJECTS)  -nostdlib -nodefaultlibs -nostartfiles -lm -lgcc -lc -T main.ld -Iinclude/cortex/atmel/sam3xa/source/as_gcc
	@echo ' '
	
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
CLEAN        	+= $(OBJECTS)

#============================================================================
#
# RUN OR SOMETHING
#
#============================================================================

SERIAL_PORT	?= $(shell ls /dev/ttyACM?)
LPC21ISP_EXE	?= include/tools/lpc21isp_197/lpc21isp_hr_linux.exe
BOSSAC 	?= include/tools/BOSSA-Arduino/bin/bossac
BOSSAC_FLAGS	?= 
RUN            := $(SUDO) $(BOSSAC) --port=$(subst /dev/,,$(SERIAL_PORT)) --force_usb_port=false -e -w -v -b main.bin -R


.PHONY: main run clean
	
main: main.bin
run: main $(LPC21ISP_EXE) $(BOSSAC) 
	$(SUDO) stty -F $(SERIAL_PORT) speed 1200 cs8 -cstopb -parenb; sleep 1.0
	-$(RUN)
	$(SUDO) $(LPC21ISP_EXE) -termonly -term main.hex $(SERIAL_PORT) 115200 12000

clean:
	rm -rfd $(CLEAN)
	@echo ' '
