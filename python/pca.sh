#!/bin/bash

lenth_path="0001"

for type in "accum" "delta" "interval"
do

python pca.py --type $type --mode all

done