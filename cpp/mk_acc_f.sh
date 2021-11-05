#!/bin/bash

lenth_path="0001"

for kernel in "rbf" #"rbf" "linear"
do

for size in `seq 10 10 80`
do
cp ./h_f/${lenth_path}/HLS_svm_param_${kernel}_accum_d_${size}.h ./tmp/HLS_svm_param_${kernel}_accum_d.h
cp ./h_f/${lenth_path}/HLS_normalize_param_accum_d_${size}.h ./tmp/HLS_normalize_param_accum_d.h

echo $kernel $size

g++ -O2 acc_to_py_f.cpp ${kernel}_prediction_f.cpp -o ../python/cpp_out_f/${lenth_path}/${kernel}_${size}_f.out
echo "g++ svm_check_f.cpp "$kernel"_prediction_f.cpp -o ../python/cpp_out_f/${lenth_path}/"$kernel"_"$size"_f.out"

done

done