#!/bin/bash

lenth_path="0001"

for kernel in "rbf" #"rbf" "linear" 
do

for type in "accum" #"accum" "delta" "interval"
do

for mode in "d" #"d" "s"
do
echo $kernel $type $mode

python mkmodel.py --kernel $kernel --type $type --mode $mode
python mkheader.py --kernel $kernel --type $type --mode $mode
python mktest.py --kernel $kernel --type $type --mode $mode

done

done

done
