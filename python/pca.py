import argparse
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

descri = 'このプログラムの説明'
parser = argparse.ArgumentParser(description=descri)
parser.add_argument('-k', '--kernel', help='linear or rbf')
parser.add_argument('-t', '--type', help='interval or accum or delta')
parser.add_argument('-m', '--mode', help='d(iffer) or s(imilar) or all')
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
#benchmark_label_list = [0, 1, 3, 5, 7, 8, 11, 15]

#  1: 禁止プログラム
# -1: 許可プログラム
#if args.mode == 'd':
#    benchmark_label_list = [1, 1, 1, 1, -1, -1, 1, 1]
#elif args.mode == 's':
#    benchmark_label_list = [1, -1, 1, 1, 1, 1, -1, 1]

if args.mode == 'd':
    #benchmark_name_list = ['aiifft01_lite', 'bitmnp01_lite', 'canrdr01_lite', 'idctrn01_lite']
    benchmark_label_list = [0, 0, 1, 1, -1, -1, 0, 0]
    print('d')
elif args.mode == 's':
    #benchmark_name_list = ['aifftr01_lite', 'aiifft01_lite', 'bitmnp01_lite', 'pntrch01_lite']
    benchmark_label_list = [0, -1, 1, 1, 0, 0, -1, 0]
    print('s')
elif args.mode == 'all':
    benchmark_label_list = [0, 1, 3, 5, 7, 8, 11, 15]

def maxmin(x, df_max_mean, df_min_mean):
    ins_max, cycle_max, memory_max, branchm_max = df_max_mean[0], df_max_mean[1], df_max_mean[2], df_max_mean[3]
    ins_min, cycle_min, memory_min, branchm_min = df_min_mean[0], df_min_mean[1], df_min_mean[2], df_min_mean[3]

    y = pd.DataFrame(columns = ["ins","cycle","memory","branchm"])
    y.loc[:,"ins"] = (x.loc[:,"ins"] - ins_min) / (ins_max - ins_min)
    y.loc[:,"cycle"] = (x.loc[:,"cycle"] - cycle_min) / (cycle_max - cycle_min)
    y.loc[:,"memory"] = (x.loc[:,"memory"] - memory_min) / (memory_max - memory_min)
    y.loc[:,"branchm"] = (x.loc[:,"branchm"] - branchm_min) / (branchm_max - branchm_min)
    return y

def preprocessing(size):
    feature = pd.DataFrame(columns = ["program","ins","cycle","memory","branchm"])
    df_max = pd.DataFrame(columns = ["ins","cycle","memory","branchm"])
    df_min = pd.DataFrame(columns = ["ins","cycle","memory","branchm"])

    for num in range(1, size+1):
        for benchmark_name, label in zip(benchmark_name_list, benchmark_label_list):
            fname = '../data' + dir_name  + '_out/{}/'.format(lenth) + benchmark_name + dir_name + '_{}.csv'.format(num)
            data = pd.read_csv(fname, usecols=ucol, sep="\t")
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
    print(feature)
    return label, maxmin(feature, df_max.mean().to_numpy(), df_min.mean().to_numpy())

def plot2d(X, y):
    marksize = 1
    plt.scatter(X[:,0][y==0], X[:,1][y==0], s=marksize, label = 'a2time01_lite')
    plt.scatter(X[:,0][y==1], X[:,1][y==1], s=marksize, label = 'aifftr01_lite')
    plt.scatter(X[:,0][y==3], X[:,1][y==3], s=marksize, label = 'aiifft01_lite')
    plt.scatter(X[:,0][y==5], X[:,1][y==5], s=marksize, label = 'bitmnp01_lite')
    plt.scatter(X[:,0][y==7], X[:,1][y==7], s=marksize, label = 'canrdr01_lite')
    plt.scatter(X[:,0][y==8], X[:,1][y==8], s=marksize, label = 'idctrn01_lite')
    plt.scatter(X[:,0][y==11], X[:,1][y==11], s=marksize, label = 'pntrch01_lite')
    plt.scatter(X[:,0][y==15], X[:,1][y==15], s=marksize, label = 'ttsprk01_lite')
    plt.xlabel("PC1",fontsize=18)
    plt.ylabel("PC2",fontsize=18)
    plt.tick_params(labelsize=18)

def plot1d(X, y, n):
    plt.plot(X[:,n-1][y==0], linestyle="solid", linewidth="1.0", label = 'a2time01_lite')
    plt.plot(X[:,n-1][y==1], linestyle="solid", linewidth="1.0", label = 'aifftr01_lite')
    plt.plot(X[:,n-1][y==3], linestyle="solid", linewidth="1.0", label = 'aiifft01_lite')
    plt.plot(X[:,n-1][y==5], linestyle="solid", linewidth="1.0", label = 'bitmnp01_lite')
    plt.plot(X[:,n-1][y==7], linestyle="solid", linewidth="1.0", label = 'canrdr01_lite')
    plt.plot(X[:,n-1][y==8], linestyle="solid", linewidth="1.0", label = 'idctrn01_lite')
    plt.plot(X[:,n-1][y==11], linestyle="solid", linewidth="1.0", label = 'pntrch01_lite')
    plt.plot(X[:,n-1][y==15], linestyle="solid", linewidth="1.0", label = 'ttsprk01_lite')
    plt.xlabel("none",fontsize=18)
    plt.ylabel("PC1",fontsize=18)
    plt.tick_params(labelsize=18)

def plot2d3color(X, y):
    marksize = 1
    plt.scatter(X[:,0][y==1], X[:,1][y==1], s=marksize, label = 'train --')
    plt.scatter(X[:,0][y==-1], X[:,1][y==-1], s=marksize, label = 'train ++')
    plt.scatter(X[:,0][y==0], X[:,1][y==0], s=marksize, label = 'test')
    plt.xlabel("PC1",fontsize=18)
    plt.ylabel("PC2",fontsize=18)
    plt.tick_params(labelsize=18)

def main() -> None:
    ulist = ["ins","cycle","memory","branchm"]
    for size in [1]: #[10, 20, 30, 40, 50, 60, 70, 80]: 
        program, feature = preprocessing(size)

        feature = feature[ulist]
        #print(feature)
        print(size, ": pp DONE\n")

        pca = PCA(n_components = 2)
        feature_pca = pca.fit_transform(feature)
        #print(feature_pca)

        '''
        #固有ベクトル
        feature_pca_vec = pd.DataFrame(pca.components_.T, columns = ['PC1', 'PC2'])
        print(feature_pca_vec, "\n")

        #固有値
        feature_pca_eig = pd.DataFrame(pca.explained_variance_, index=['PC1','PC2'], columns=['固有値']).T
        print(feature_pca_eig, "\n")

        #寄与率
        feature_pca_contribution = pd.DataFrame(pca.explained_variance_ratio_, index = ['PC1', 'PC2'], columns=['寄与率']).T
        print(feature_pca_contribution, "\n")
        '''

        fig = plt.figure(figsize=(12,8))
        ax = fig.add_subplot(111)

        #plot1d(feature_pca, program, 1)
        if args.mode == 'all':
            #print("OK")
            plot2d(feature_pca, program)
            ax.legend(loc='upper right', fontsize=12)
            fig.savefig("./img/PCA_{0}_{1}".format(lenth, args.type))
        else:
            plot2d3color(feature_pca, program)
            ax.legend(loc='upper right', fontsize=12)
            fig.savefig("./img/PCA_{0}_{1}_{2}".format(lenth, args.type, args.mode))

if __name__=='__main__':
    main()