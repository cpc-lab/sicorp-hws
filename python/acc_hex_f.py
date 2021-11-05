import sys
import subprocess
from subprocess import PIPE
import argparse
import pandas as pd
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

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

def main() -> None:
    opt = 0
    score = pd.DataFrame(columns = benchmark_name_list)
    
    for size in [10, 20, 30, 40, 50, 60, 70, 80]:
        score.loc[str(size)+'iter'] = 0
        for benchmark_name, benchmark_label in zip(benchmark_name_list, benchmark_label_list):
            pred = []
            print(size,"",benchmark_name)
            for num in range(81, 100+1):
                #inputtxt = "./cpp_out_f/0001/f_linear_10.out linear accum d 80 a2time 81"
                inputtxt = "./cpp_out_f/{0}/{1}_{2}_f.out {3} {4} {5} {6} {7} {8}".format(lenth, args.kernel, size, args.kernel, args.type, args.mode, size, benchmark_name, num)
                proc = subprocess.run(inputtxt, shell=True, stdout=PIPE, stderr=PIPE, text=True)
                cppout = proc.stdout
                pred += [int(s) for s in cppout.split(',')[:-1]]
                #print(inputtxt)

            #print(pred)
            #print(len(pred))

            label = [benchmark_label]*len(pred)
            pred_score = accuracy_score(label, pred)
            score[benchmark_name][str(size)+'iter'] = pred_score
            #print(pred_score)

    score = score*100

    print(score.T, file=sys.stderr)
    score.T.to_csv('./log/tmp_f.csv', mode='a', header=False)
    #print(score.mean())
    #print(score.min())
    #print(score.max())

if __name__=='__main__':
    main()