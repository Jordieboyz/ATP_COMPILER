FILE="test_dirs"
if [ -f "$FILE" ]; then
    rm "$FILE"
fi

touch "$FILE"
PATH=../examples

for entry in "$PATH"/*
do
    echo "$entry" >> test_dirs
done