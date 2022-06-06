#! /bin/sh

INPUT_FILE=$1

if [ -z "$1" ]
then
    echo "No input file given!"
    exit
fi

python3 main.py $INPUT_FILE
