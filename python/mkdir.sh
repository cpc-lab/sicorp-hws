#!/bin/bash

lenth_path="0001"

for dir in "img" "log"
do
if [ ! -d ./${dir} ]; then
    mkdir ./${dir}
else
    echo "dir exist -> ./${dir}"
fi
done


for dir in "model" "cpp_out" "cpp_out_f"
do
if [ ! -d ./${dir} ]; then
    mkdir ./${dir}
    mkdir ./${dir}/${lenth_path}
else
    echo "dir exist -> ./${dir}"
    if [ ! -d ./${dir}/${lenth_path} ]; then
        mkdir ./${dir}/${lenth_path}
    fi
fi
done


for dir in "svm_input" "svm_output" "svm_output_f" "norm_param" "norm_param_f"
do

if [ ! -d ../data/${dir} ]; then
    mkdir ../data/${dir}
    mkdir ../data/${dir}/${lenth_path}
else
    echo "dir exist -> ../data/${dir}"
    if [ ! -d ../data/${dir}/${lenth_path} ]; then
        mkdir ../data/${dir}/${lenth_path}
    fi
fi

if [ $dir == "svm_input" ] || [ $dir == "svm_output" ] || [ $dir == "svm_output_f" ]; then
    for benchmark in "a2time" "aifftr" "aiifft" "bitmnp" "canrdr" "idctrn" "pntrch" "ttsprk"
    do

    if [ ! -d ../data/${dir}/${lenth_path}/${benchmark}01_lite ]; then
            mkdir ../data/${dir}/${lenth_path}/${benchmark}01_lite
        else
            echo "dir exist -> ../data/${dir}/${lenth_path}/${benchmark}01_lite"
    fi
    done
fi

done
