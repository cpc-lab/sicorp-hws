import argparse
import numpy as np
import pandas as pd

import mkmodel_hex
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

benchmark_name_list = ['a2time01_lite', 'aifftr01_lite', 'aiifft01_lite', 'bitmnp01_lite', 'canrdr01_lite', 'idctrn01_lite', 'pntrch01_lite', 'ttsprk01_lite']
   
#  1: 禁止プログラム
# -1: 許可プログラム
if args.mode == 'd':
    label_list = [1, 1, 1, 1, -1, -1, 1, 1]
elif args.mode == 's':
    label_list = [1, -1, 1, 1, 1, 1, -1, 1]
    
def mktestinput(benchmark_name, benchmark_label, size, num):
    fname = '../data' + dir_name  + '_out/{}/'.format(lenth) + benchmark_name + dir_name + '_{}.csv'.format(num)
    benchmark = pd.read_csv(fname, usecols=ucol, sep="\t")
    feature = benchmark[ucol]
    if size == 10:
        fname = '../data/svm_input/{0}/{1}/svm_input_{2}_{3}.txt'.format(lenth, benchmark_name, args.type, num)
        np.savetxt(fname, feature, fmt="%d")
        
    return feature

def mktestoutput(benchmark_name, clf, feature, norm_param, size, num):
    df_max = np.ndarray(shape=[4])
    df_min = np.ndarray(shape=[4])
    if norm_param.dtype == '<U18':
        fname = '../data/svm_output/{0}/{1}/svm_output_{2}_{3}_{4}_{5}_{6}.txt'.format(lenth, benchmark_name, args.kernel, args.type, args.mode, size, num)
        for i in range(4):
            df_max[i] = float(mkheader_hex.hex_to_double(str(norm_param[i])))
            df_min[i] = float(mkheader_hex.hex_to_double(str(norm_param[i+4])))

    elif norm_param.dtype == '<U10':
        fname = '../data/svm_output_f/{0}/{1}/svm_output_{2}_{3}_{4}_{5}_{6}.txt'.format(lenth, benchmark_name, args.kernel, args.type, args.mode, size, num)
        for i in range(4):
            df_max[i] = float(mkheader_hex.hex_to_float(str(norm_param[i])))
            df_min[i] = float(mkheader_hex.hex_to_float(str(norm_param[i+4])))

    test_x = mkmodel_hex.maxmin(feature, df_max, df_min, num, 0)
    pred = clf.predict(test_x)
    np.savetxt(fname, pred, fmt="%d")

def main() -> None:
    opt = 0
    for size in [10, 20, 30, 40, 50, 60, 70, 80]:
        clf = mkheader_hex.opmodel(size)
        if opt == 0:
            fname = '../data/norm_param/{0}/normalize_param_{1}_{2}_{3}.csv'.format(lenth, args.type, args.mode, size)
            norm_param = np.loadtxt(fname, dtype='str', usecols=1)
        elif opt == 1:
            fname = '../data/norm_param_f/{0}/normalize_param_{1}_{2}_{3}.csv'.format(lenth, args.type, args.mode, size)
            norm_param = np.loadtxt(fname, dtype='str', usecols=1)

        for benchmark_name, benchmark_label in zip(benchmark_name_list, label_list):
            for num in range(81, 101):
                print('model size:', size, ' -> ', benchmark_name, ':', num, ':')
                feature = mktestinput(benchmark_name, benchmark_label, size, num)
                mktestoutput(benchmark_name, clf, feature, norm_param, size, num)

if __name__=='__main__':
    main()