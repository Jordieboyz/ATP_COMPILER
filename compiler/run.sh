#! /bin/sh

INPUT_FILE=$1
OUTPUT_FILE=$2

if [ -z "$1" ]
then
    echo "No input file given!"
    exit
fi

if [ -z "$2" ]
then
	echo "No output file name given... using $(basename $INPUT_FILE .txt).asm"
	OUTPUT_FILE=$(basename $INPUT_FILE .txt).asm
fi	

# make tests out of C++




python3 main.py $INPUT_FILE $OUTPUT_FILE

if [ -s $(readlink -f $OUTPUT_FILE) ]; then
	echo ""$OUTPUT_FILE" succesfully created!"
else
	echo "Something went wrong. No output file created!"
	exit
fi

# g++ -o output -Wall -Werror create_tests.cpp


sudo make run PROJECT=$OUTPUT_FILE TESTDEF=-D$(basename $INPUT_FILE .txt)
make clean PROJECT=$OUTPUT_FILE
