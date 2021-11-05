#!/bin/bash

lenth_path="0001"

cp /dev/null ./log/acc_f.log
cp /dev/null ./log/tmp_f.csv

for kernel in "rbf" #"rbf" "linear" 
do

for type in "accum" #"accum" "delta" "interval"
do

for mode in "d" #"d" "s"
do
echo $kernel $type $mode

echo "${kernel} ${type} ${mode} 32bit(float)" >> ./log/acc_f.log
echo "${kernel} ${type} ${mode}" >> ./log/tmp_f.csv
python acc_hex_f.py --kernel $kernel --type $type --mode $mode 2>> ./log/acc_f.log
echo "" ./log/acc.log

done

done

done