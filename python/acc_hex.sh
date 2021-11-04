#!/bin/bash

lenth_path="0001"

cp /dev/null ./log/acc.log
cp /dev/null ./log/tmp.csv

for kernel in "rbf" #"rbf" "linear"
do

for type in "accum" #"accum" "delta" "interval"
do

for mode in "d" #"d" "s"
do
echo $kernel $type $mode

echo "${kernel} ${type} ${mode} 64bit(double)" >> ./log/acc.log
echo "${kernel} ${type} ${mode}" >> ./log/tmp.csv
python acc_hex.py --kernel $kernel --type $type --mode $mode 2>> ./log/acc.log
echo "" ./log/acc.log

done

done

done