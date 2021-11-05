#!/bin/bash

lenth_path="0001"

for kernel in "rbf" #"rbf" "linear"
do

for size in `seq 10 10 80`
do
cp ./h/${lenth_path}/HLS_svm_param_${kernel}_accum_d_${size}.h ./tmp/HLS_svm_param_${kernel}_accum_d.h
cp ./h/${lenth_path}/HLS_normalize_param_accum_d_${size}.h ./tmp/HLS_normalize_param_accum_d.h

echo $kernel $size

g++ -O2 acc_to_py.cpp ${kernel}_prediction.cpp -o ../python/cpp_out/${lenth_path}/${kernel}_${size}.out
echo "g++ svm_check.cpp "$kernel"_prediction.cpp -o ../python/cpp_out/${lenth_path}/"$kernel"_"$size".out"

done

done