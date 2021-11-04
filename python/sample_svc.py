import pickle
import argparse
import math
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
from sklearn.svm import SVC

descri = 'このプログラムの説明'
parser = argparse.ArgumentParser(description=descri)
parser.add_argument('-k', '--kernel', help='linear or rbf')
args = parser.parse_args()

class MyPredSVC():
    def __init__(self, kernel=2, gamma=0.1):
        if kernel not in self.__kernel_dict:
            print(kernel + " kernel does not exist!\nUse rbf kernel.")
            kernel = 2
        if kernel == 2:
            def kernel_func(x, y):
                return self.__kernel_dict[kernel](x, y, gamma=gamma)
        else:
            kernel_func = self.__kernel_dict[kernel]
        self.kernel = kernel_func

    def __mylinear_kernel(x, y):
        return np.dot(x, y)

    def __myrbf_kernel(x, y, gamma):
        diff = x - y
        return np.exp(-gamma * np.dot(diff, diff))

    __kernel_dict = {1: __mylinear_kernel, 2: __myrbf_kernel}

    def mydecision_function(self, Xsv, X, dual_coef_, bias, kernel):
        y_score = []
        if kernel == 1:
            for test_x in X:
                y_buff = sum(np.dot(dual_coef_, self.kernel(Xsv, test_x))) + bias
                y_score.append(y_buff)

        elif kernel == 2:
            for test_x in X:
                y_buff = 0
                for i in range(Xsv.shape[0]):
                    y_buff += np.dot(dual_coef_[0][i], self.kernel(Xsv[i], test_x))
                y_buff += bias
                y_score.append(y_buff)

        return np.array(y_score)

    def mypredict(self, Xsv, X, dual_coef_, bias, kernel):
        y_score = self.mydecision_function(Xsv, X, dual_coef_, bias, kernel)
        predict = map(lambda s: 1 if s >= 0. else -1, y_score)
        return list(predict)

def main() -> None:
    kernel_func = 1 if args.kernel == "linear" else 2
        
    train_x = np.array([[3, 4], [1, 4], [2, 3], [6, -1], [7, -1], [5, -3]])
    train_labels = np.array([-1, -1, -1, 1, 1, 1])
    
    clf = SVC(C=1e5, kernel="linear")
    clf.fit(train_x, train_labels)

    i = 8
    x = np.linspace(0, i, 2*i+1)
    a = - (clf.coef_[0,0] / clf.coef_[0,1])
    b = - (clf.intercept_[0] / clf.coef_[0,1])
    y = x * a + b

    t1 = abs(y[0])
    t2 = abs(y[-1])
    t = t1 if t1 < t2 else t2
    u = y[0] if y[0] < y[-1] else y[-1]
    dx = (clf.support_vectors_[0,0] + clf.support_vectors_[1,0])/2
    dy = (clf.support_vectors_[0,1] + clf.support_vectors_[1,1])/2
    test_x = 2*t*np.random.rand(50, 2) - t+np.array([dx, dy])

    if kernel_func == 2:
        clf = SVC(C=1e5, kernel="rbf", gamma=0.1)
        clf.fit(train_x, train_labels)

    for k,v in clf.__dict__.items():
        print(k, ':', v)

    pred = clf.predict(test_x)

    myclf = MyPredSVC(kernel_func, clf.gamma)
    mypred = myclf.mypredict(clf.support_vectors_, test_x, clf.dual_coef_, clf.intercept_, kernel_func)

    print()
    print(list(pred))
    print(mypred)

if __name__=='__main__':
    main()