# Writen by Yuki Koga

import pandas as pd
import sys

#引数設定
args = sys.argv
benchmark = args[1]#ベンチマーク
num = args[2]#番号
lenth = float(args[3])#区間の大きさ 0.0001など
lenth_path = args[4]#区間の大きさを文字列で 0001など
  

#各イベント毎に下記の操作を行う
for event in ["0xC0", "0x3C", "0x81", "0x82", "0xC5"]: #, "0xD1", "0x80"
    df = pd.read_csv("../data/script_out/{0}01_lite/{1}_script_{2}.csv".format(benchmark,event,num), names=["comm", "pid", "cpu", "time", "period", "event", "addr", "sym", "bin"], sep="\t")
    df.loc[:, "time"] = df.loc[:, "time"] - df.loc[0, "time"]#0秒からの時刻に変換
    time = df.loc[:, "time"]
    max = time.max()
    min = time.min()

    result = pd.DataFrame(columns = ["time", "count"])

    offset = 0.001
    while offset <= max:
        count = df[ (df["time"] >= offset) & (df["time"] < offset+lenth) ].period.sum() #区間内のカウンタの値を合算

        #dataframeに格納
        a = pd.Series(["{:05.4f}".format(offset), "{:d}".format(count)], index = result.columns) 
        result = result.append(a, ignore_index=True)

        #次の区間に移動
        offset += lenth

    result.to_csv("../data/analyze_out/{0}/{1}01_lite/{2}_analyze_{3}.csv".format(lenth_path,benchmark,event,num), mode='w+', sep="\t")