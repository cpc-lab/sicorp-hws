import pickle
import argparse
import pandas as pd
from sklearn.svm import SVC, LinearSVC

import mkheader_hex

descri = 'このプログラムの説明'
parser = argparse.ArgumentParser(description=descri)
parser.add_argument('-k', '--kernel', help='linear or rbf')
parser.add_argument('-t', '--type', help='interval or accum or delta')
parser.add_argument('-m', '--mode', help='d(iffer) or s(imilar)')
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

#  1: 禁止プログラム
# -1: 許可プログラム
if args.mode == 'd':
    benchmark_name_list = ['aiifft01_lite', 'bitmnp01_lite', 'canrdr01_lite', 'idctrn01_lite']
    label_list = [1, 1, -1, -1]
elif args.mode == 's':
    benchmark_name_list = ['aifftr01_lite', 'aiifft01_lite', 'bitmnp01_lite', 'pntrch01_lite']
    label_list = [-1, 1, 1, -1]

def maxmin(x, df_max_mean, df_min_mean, num, opt):
    param_list = ['ins_max', 'cycle_max', 'memory_max', 'branchm_max', 'ins_min', 'cycle_min', 'memory_min', 'branchm_min']
    ins_max, cycle_max, memory_max, branchm_max = df_max_mean[0], df_max_mean[1], df_max_mean[2], df_max_mean[3]
    ins_min, cycle_min, memory_min, branchm_min = df_min_mean[0], df_min_mean[1], df_min_mean[2], df_min_mean[3]

    if opt == 1:
        fname = '../cpp/h/{}/HLS_normalize_param_'.format(lenth) + args.type + '_' + args.mode + '_{}.h'.format(num)
        with open(fname, mode='w+') as f:
            for param, param_name in zip([ins_max, cycle_max, memory_max, branchm_max, ins_min, cycle_min, memory_min, branchm_min], param_list):
                if param_name == 'ins_max':
                    header = mkheader_hex.union2header(param.reshape(-1,), 'normalize_param', 0)
                    f.write(header)
                header = mkheader_hex.unionhex2header(param.reshape(-1,), 'normalize_param', param_name, 0)
                f.write(header)

        fname = '../cpp/h_f/{}/HLS_normalize_param_'.format(lenth) + args.type + '_' + args.mode + '_{}.h'.format(num)
        with open(fname, mode='w+') as f:
            for param, param_name in zip([ins_max, cycle_max, memory_max, branchm_max, ins_min, cycle_min, memory_min, branchm_min], param_list):
                if param_name == 'ins_max':
                    header = mkheader_hex.union2header(param.reshape(-1,), 'normalize_param', 1)
                    f.write(header)
                header = mkheader_hex.unionhex2header(param.reshape(-1,), 'normalize_param', param_name, 1)
                f.write(header)
        
        fname = '../data/norm_param/{}/'.format(lenth) + 'normalize_param_' + args.type + '_' + args.mode + '_{}.csv'.format(num)
        with open(fname, mode='w+') as f:
            for param, param_name in zip([ins_max, cycle_max, memory_max, branchm_max, ins_min, cycle_min, memory_min, branchm_min], param_list):
                header = param_name + ', ' + str(mkheader_hex.double_to_hex(param)) + '\n'
                f.write(header)

        fname = '../data/norm_param_f/{}/'.format(lenth) + 'normalize_param_' + args.type + '_' + args.mode + '_{}.csv'.format(num)
        with open(fname, mode='w+') as f:
            for param, param_name in zip([ins_max, cycle_max, memory_max, branchm_max, ins_min, cycle_min, memory_min, branchm_min], param_list):
                header = param_name + ', ' + str(mkheader_hex.float_to_hex(param)) + '\n'
                f.write(header)

    y = pd.DataFrame(columns = ["ins","cycle","memory","branchm"])
    y.loc[:,"ins"] = (x.loc[:,"ins"] - ins_min) / (ins_max - ins_min)
    y.loc[:,"cycle"] = (x.loc[:,"cycle"] - cycle_min) / (cycle_max - cycle_min)
    y.loc[:,"memory"] = (x.loc[:,"memory"] - memory_min) / (memory_max - memory_min)
    y.loc[:,"branchm"] = (x.loc[:,"branchm"] - branchm_min) / (branchm_max - branchm_min)
    return y

def preprocessing(size, opt):
    feature = pd.DataFrame(columns = ["program","ins","cycle","memory","branchm"])
    df_max = pd.DataFrame(columns = ["ins","cycle","memory","branchm"])
    df_min = pd.DataFrame(columns = ["ins","cycle","memory","branchm"])

    for num in range(1, size+1):
        for benchmark_name, label in zip(benchmark_name_list, label_list):
            data = pd.read_csv('../data' + dir_name  + '_out/{}/'.format(lenth) + benchmark_name + dir_name + '_{}.csv'.format(num), usecols=ucol, sep="\t")
            # print('../data' + dir_name  + '_out/{}/'.format(lenth) + benchmark_name + dir_name + '_{}.csv'.format(num)) ###############
            # if num == 1: ###############
            #     print(benchmark_name, ',', label) ###############
            data.insert(0,'program', label)
            if args.type == 'delta':
                data = data.rename(columns={"ins_d" : "ins", "cycle_d" : "cycle", "memory_d" : "memory", "branchm_d" : "branchm"})
            feature = feature.append(data, ignore_index = True)

        max = pd.DataFrame(feature.max()).T
        min = pd.DataFrame(feature.min()).T
        df_max = df_max.append(max, ignore_index = True)
        df_min = df_min.append(min, ignore_index = True)

    label = feature.iloc[:,0].astype("int")
    feature = feature.iloc[:,1:]
    return maxmin(feature, df_max.mean().to_numpy(), df_min.mean().to_numpy(), num, opt), label, feature

def mkmodel(krnl, train_x, train_labels, size):
    if krnl == 'linear':
        #clf = SVC(C=1000000, kernel=krnl, verbose=2)
        clf = LinearSVC(C=1000000, dual=False, verbose=2)
    elif krnl == 'rbf':
        clf = SVC(C=1000000, kernel=krnl, gamma='auto', verbose=2)

    clf.fit(train_x, train_labels)
    fname = './model/{}/'.format(lenth) + krnl + '_' + args.type + '_' + args.mode + '_{}.pickle'.format(size)
    with open(fname, mode = 'wb') as fp:
        pickle.dump(clf, fp)
    
    print("size :", size)

def main() -> None:
    for size in [10, 20, 30, 40, 50, 60, 70, 80]:

        train_x, train_labels, feature = preprocessing(size, 1)
        print(size, ": pp DONE")

        mkmodel(args.kernel, train_x, train_labels, size)
        #mkmodel("linear", train_x, train_labels, size)
        #mkmodel("rbf", train_x, train_labels, size)
        print(size, ": tr DONE")
 
if __name__=='__main__':
    main()