#! /bin/sh 

TESTDIR=tests/
RUN_TEST_PATH=$TESTDIR/create_tests

if [ ! -f "$RUN_TEST_PATH" ]; then
	g++ -o $RUN_TEST_PATH -Wall -Werror $RUN_TEST_PATH.cpp
	./$RUN_TEST_PATH
else
	./$RUN_TEST_PATH
fi

for entry in $TESTDIR*.tst; do
	python3 main.py $entry $TESTDIR$(basename $entry .tst).asm
	echo "Created: $(basename $entry .tst).asm"
done

