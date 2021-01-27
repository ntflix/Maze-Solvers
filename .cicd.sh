#!/bin/sh
export PYTHONPATH=`pwd`

for file in `find .`
do
    if [[ $file == *.unittest.py ]]
    then
        echo $file
        python3 $file
        echo
    fi
done
