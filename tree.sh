tree(){
    n=$3
    if (( $n < 6)); then
        for entry in $2/*; do
            tmp=''
            for i in $(seq 0 $n); do
                tmp+='\t'
            done
        
            tmp+='|_ '$(basename $entry)
            

            if [ -d  $entry ]; then
                echo -e $tmp/ >> $1

                n=$((n+2))
                tree $1 $entry $n  
                n=$((n-2))  
            else
                echo -e $tmp >> $1
            fi
        done
    else
        return
    fi  
}

OUTPUT_FILE=tree_comp.txt
rm -f $OUTPUT_FILE
touch $OUTPUT_FILE
echo "../ATP_COMPILER/" >> $OUTPUT_FILE
tree $OUTPUT_FILE ../ATP_COMPILER 1