#!/bin/bash

# Writen by Yuki Koga

#測定したいベンチマークを設定
benchmark="a2time01_lite" #"a2time01_lite" "aifftr01_lite" "aiifft01_lite" "bitmnp01_lite" "canrdr01_lite" "idctrn01_lite" "pntrch01_lite" "ttsprk01_lite"

for num in `seq 1 1 100`
do

sleep 3;

#-Fのあとにパフォーマンスカウンタを測定する頻度を設定
#-eのあとに測定するアーキテクチャイベントを設定
sudo perf timechart record perf record -a -F 10000 \
-e cpu/event=0xC0,umask=0x00/u \
-e cpu/event=0x3C,umask=0x00/u \
-e cpu/event=0xD0,umask=0x81/u \
-e cpu/event=0xD0,umask=0x82/u \
-e cpu/event=0xC5,umask=0x00/u \
./benchmark/autobench/${benchmark}

#測定したデータをdata形式ファイルを生成し，record_outディレクトリに移動
sudo mv perf.data ./data/record_out/${benchmark}/record_${num}

#データをcsvファイルに変換
sudo perf script -i ./data/record_out/${benchmark}/record_${num} > ./data/script_out/${benchmark}/script_${num}.csv 

#取得したcsvファイルをイベント毎に分ける
#それぞれのイベントで要素をtab毎に区切ってscript_outディレクトリにcsv形式で保存
for event in 0xC0 0x3C 0x81 0x82 0xC5 #0xD1 0x80 
do
grep ${benchmark} ./data/script_out/${benchmark}/script_${num}.csv | grep ${event} | \
  sed "s/^ \+//g" | sed "s/:\? \+/;/g" | sed "s/;/\t/g" > ./data/script_out/${benchmark}/${event}_script_${num}.csv 
done

done