#! /bin/sh

INPUT_FILE=$1
OUTPUT_FILE=$2

if [ -z "$1" ]
then
    echo "No input file given!"
    set -e
fi

if [ -z "$2" ]
then 
    echo "No output file name given... using out.asm"
    OUTPUT_FILE=out.asm
fi

python3 main.py $INPUT_FILE $OUTPUT_FILE
sudo make run PROJECT=$OUTPUT_FILE
make clean PROJECT=$OUTPUT_FILE
