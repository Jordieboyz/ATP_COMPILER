#! /bin/sh 

RUN_TEST_PATH=tests/create_tests
if [ ! -f "$RUN_TEST_PATH" ]; then
	g++ -o $RUN_TEST_PATH -Wall -Werror $RUN_TEST_PATH.cpp
	./$RUN_TEST_PATH
	echo "Created test files! Run the program with again the wanted test to run."
else
	./$RUN_TEST_PATH
	echo "Created test files! Run the program with again the wanted test to run."
fi

for entry in tests/*.tst; do
	python3 main.py $entry tests/$(basename $entry .tst).asm
	echo "Created: $(basename $entry .tst).asm"
done

sudo make run