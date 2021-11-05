#!/bin/bash

lenth_path="0001"

if [ ! -d ./tmp ]; then
    mkdir ./tmp
else
    echo "dir exist -> ./tmp"
fi


for dir in "h" "h_f"
do

if [ ! -d ./${dir} ]; then
    mkdir ./${dir}
    mkdir ./${dir}/${lenth_path}
else
    echo "dir exist -> ./data/${dir}_out"
    if [ ! -d ./${dir}/${lenth_path} ]; then
        mkdir ./${dir}/${lenth_path}
    fi
fi

done