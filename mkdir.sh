#!/bin/bash

lenth_path="0001"

for dir in "record" "script" "svm" "analyze" "arrange" "arrange_delta" "arrange_accum"   
do

if [ $dir == "record" ] || [ $dir == "script" ]; then
    if [ ! -d ./data/${dir}_out ]; then
        mkdir ./data/${dir}_out
    else
        echo "dir exist -> ./data/${dir}_out"
    fi
else
    if [ ! -d ./data/${dir}_out ]; then
        mkdir ./data/${dir}_out
        mkdir ./data/${dir}_out/${lenth_path}
    else
        echo "dir exist -> ./data/${dir}_out"
        if [ ! -d ./data/${dir}_out/${lenth_path} ]; then
            mkdir ./data/${dir}_out/${lenth_path}
        fi
    fi
fi

for benchmark in "a2time" "aifftr" "aiifft" "bitmnp" "canrdr" "idctrn" "pntrch" "ttsprk"
do

if [ $dir == "record" ] || [ $dir == "script" ]; then
    if [ ! -d ./data/${dir}_out/${benchmark}01_lite ]; then
        mkdir ./data/${dir}_out/${benchmark}01_lite
    else
        echo "dir exist -> ./data/${dir}_out/${benchmark}01_lite"
    fi
else
    if [ ! -d ./data/${dir}_out/${lenth_path}/${benchmark}01_lite ]; then
        mkdir ./data/${dir}_out/${lenth_path}/${benchmark}01_lite
    else
        echo "dir exist -> ./data/${dir}_out/${lenth_path}/${benchmark}01_lite"
    fi
fi
done

done
