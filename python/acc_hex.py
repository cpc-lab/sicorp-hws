import sys
import argparse
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

import mkheader_hex

descri = 'このプログラムの説明'
parser = argparse.ArgumentParser(description=descri)
parser.add_argument('-k', '--kernel', help='linear or rbf')
parser.add_argument('-t', '--type', help='interval or accum or delta or all')
parser.add_argument('-m', '--mode', help='d(iffer) or s(imilar)')
#parser.add_argument('-s', '--size', help='INT representing the size of the model')
args = parser.parse_args()

lenth="0001"

if args.type == 'interval':
    dir_name = '/arrange'
elif args.type == 'accum':
    dir_name = '/arrange_' + args.type
elif args.type == 'delta':
    dir_name = '/arrange_' + args.type

if args.type == 'interval':
    ucol = ["ins","cycle","memory","branchm"]
elif args.type == 'accum':
    ucol = ["ins","cycle","memory","branchm"]
elif args.type == 'delta':
    ucol = ["ins_d","cycle_d","memory_d","branchm_d"]

benchmark_name_list = ['a2time', 'aifftr', 'aiifft', 'bitmnp', 'canrdr', 'idctrn', 'pntrch', 'ttsprk']

#  1: 禁止プログラム
# -1: 許可プログラム
if args.mode == 'd':
    benchmark_label_list = [1, 1, 1, 1, -1, -1, 1, 1]
elif args.mode == 's':
    benchmark_label_list = [1, -1, 1, 1, 1, 1, -1, 1]

def maxmin(x, df_max_mean, df_min_mean):
    ins_max, cycle_max, memory_max, branchm_max = df_max_mean[0], df_max_mean[1], df_max_mean[2], df_max_mean[3]
    ins_min, cycle_min, memory_min, branchm_min = df_min_mean[0], df_min_mean[1], df_min_mean[2], df_min_mean[3]

    y = pd.DataFrame(columns = ["ins","cycle","memory","branchm"])
    y.loc[:,"ins"] = (x.loc[:,"ins"] - ins_min) / (ins_max - ins_min)
    y.loc[:,"cycle"] = (x.loc[:,"cycle"] - cycle_min) / (cycle_max - cycle_min)
    y.loc[:,"memory"] = (x.loc[:,"memory"] - memory_min) / (memory_max - memory_min)
    y.loc[:,"branchm"] = (x.loc[:,"branchm"] - branchm_min) / (branchm_max - branchm_min)
    return y

def svmtestall(clf, feature, norm_param):
    df_max = np.ndarray(shape=[4])
    df_min = np.ndarray(shape=[4])
    if norm_param.dtype == '<U18':
        for i in range(4):
            df_max[i] = float(mkheader_hex.hex_to_double(str(norm_param[i])))
            df_min[i] = float(mkheader_hex.hex_to_double(str(norm_param[i+4])))

    elif norm_param.dtype == '<U10':
        for i in range(4):
            df_max[i] = float(mkheader_hex.hex_to_float(str(norm_param[i])))
            df_min[i] = float(mkheader_hex.hex_to_float(str(norm_param[i+4])))

    test_x = maxmin(feature, df_max, df_min)
    pred = clf.predict(test_x)
    return pred

def preprocessing(benchmark_name, benchmark_label):
    feature = pd.DataFrame(columns = ["program","ins","cycle","memory","branchm"])

    for num in range(81, 100+1):
        fname = '../data' + dir_name  + '_out/{}/'.format(lenth) + benchmark_name + '01_lite' + dir_name + '_{}.csv'.format(num)
        data = pd.read_csv(fname, usecols=ucol, sep="\t")
        data.insert(0,'program', benchmark_label)
        if args.type == 'delta':
            data = data.rename(columns={"ins_d" : "ins", "cycle_d" : "cycle", "memory_d" : "memory", "branchm_d" : "branchm"})
        feature = feature.append(data, ignore_index = True)

    label = feature.iloc[:,0].astype("int")
    feature = feature.iloc[:,1:]
    #print(feature)
    return label, feature

def main() -> None:
    opt = 0
    score = pd.DataFrame(columns = benchmark_name_list)
    
    for size in [10, 20, 30, 40, 50, 60, 70, 80]:
        clf = mkheader_hex.opmodel(size) #clf_linear = opmodel(args.size) #clf_rbf = opmodel(args.size)
        if opt == 0:
            fname = '../data/norm_param/{0}/normalize_param_{1}_{2}_{3}.csv'.format(lenth, args.type, args.mode, size)
            norm_param = np.loadtxt(fname, dtype='str', usecols=1)
        elif opt == 1:
            fname = '../data/norm_param_f/{0}/normalize_param_{1}_{2}_{3}.csv'.format(lenth, args.type, args.mode, size)
            norm_param = np.loadtxt(fname, dtype='str', usecols=1)

        score.loc[str(size)+'iter'] = 0
        for benchmark_name, benchmark_label in zip(benchmark_name_list, benchmark_label_list):
            print(size,"",benchmark_name)
            label, feature = preprocessing(benchmark_name, benchmark_label)
            pred = svmtestall(clf, feature, norm_param)
            pred_score = accuracy_score(label, pred)
            score[benchmark_name][str(size)+'iter'] = pred_score
            #print(pred_score)

    score = score*100

    print(score.T, file=sys.stderr)
    score.T.to_csv('./log/tmp.csv', mode='a', header=False)
    #print(score.mean())
    #print(score.min())
    #print(score.max())

if __name__=='__main__':
    main()