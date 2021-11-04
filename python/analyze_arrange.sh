#!/bin/bash

# Writen by Yuki Koga

lenth="0.0001"
lenth_path="0001" 

for num in `seq 1 1 100`
do
echo "${num} :"

for benchmark in "a2time" "aifftr" "aiifft" "bitmnp" "canrdr" "idctrn" "pntrch" "ttsprk"
do

python analyze.py ${benchmark} ${num} ${lenth} ${lenth_path}
python arrange.py ${benchmark} ${num} ${lenth_path}

echo "${num} : ${benchmark} done"
done

done
