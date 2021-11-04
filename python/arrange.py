# Writen by Yuki Koga

import pandas as pd
import sys

#引数の設定
args = sys.argv
benchmark = args[1] #ベンチマーク
num = args[2] #番号
lenth_path = args[3] #区間の大きさを文字列で 0001など

#イベント毎にデータを取得
ins = pd.read_csv("../data/analyze_out/{0}/{1}01_lite/0xC0_analyze_{2}.csv".format(lenth_path,benchmark,num), usecols=["time","count"], sep="\t")
cycle = pd.read_csv("../data/analyze_out/{0}/{1}01_lite/0x3C_analyze_{2}.csv".format(lenth_path,benchmark,num), usecols=["count"], sep="\t")
load = pd.read_csv("../data/analyze_out/{0}/{1}01_lite/0x81_analyze_{2}.csv".format(lenth_path,benchmark,num), usecols=["count"], sep="\t")
store = pd.read_csv("../data/analyze_out/{0}/{1}01_lite/0x82_analyze_{2}.csv".format(lenth_path,benchmark,num), usecols=["count"], sep="\t")
branchm = pd.read_csv("../data/analyze_out/{0}/{1}01_lite/0xC5_analyze_{2}.csv".format(lenth_path,benchmark,num), usecols=["count"], sep="\t")

#1つに結合
#loadとstoreを合算
feature = pd.concat([ins, cycle, load+store, branchm], axis = 1).dropna()
feature.columns = ["time", "ins", "cycle", "memory", "branchm"]
feature.to_csv("../data/arrange_out/{0}/{1}01_lite/arrange_{2}.csv".format(lenth_path,benchmark,num), mode='w+', sep="\t")







