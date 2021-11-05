import pickle
import argparse
import numpy as np
import struct
import binascii

descri = 'このプログラムの説明'
parser = argparse.ArgumentParser(description=descri)
parser.add_argument('-k', '--kernel', help='linear or rbf')
parser.add_argument('-t', '--type', help='interval or accum or delta')
parser.add_argument('-m', '--mode', help='d(iffer) or s(imilar)')
args = parser.parse_args()

lenth="0001"

def num2header(num, type, header='dummy'):
    ret = "%s %s[1] = {" % (type,header)
    ret += ' , '.join(['{: .9f}'.format(num)])
    ret += ',};\n\n'
    return ret

def shape2header(ary, header='dummy'):
    n = len(ary)
    ret = "int %s[%d] = {" % (header,n)
    for i, x in enumerate(ary):
        if i != 0:
            ret += ' '
        ret += ', '.join(['{: d}'.format(x)])
        ret += ','
    ret += '};\n\n'
    return ret

def array2header(ary, type, header='dummy'):
    n = len(ary)
    ret = "%s %s[%d] = {" % (type,header,n)
    for i, x in enumerate(ary):
        if i != 0:
            ret += ' '
        ret += ', '.join(['{: .9f}'.format(x)])
        ret += ','
    ret += '};\n\n'
    return ret

def double_to_hex(f):
    return hex(struct.unpack('>Q', struct.pack('>d', f))[0])

def hex_to_double(s):
    if s.startswith('0x'):
        s = s[2:]
    s = s.replace(' ', '')
    return struct.unpack('>d', binascii.unhexlify(s))[0] if s != '0' else 0.0

def float_to_hex(f):
    return hex(struct.unpack('>I', struct.pack('>f', f))[0])

def hex_to_float(s):
    if s.startswith('0x'):
        s = s[2:]
    s = s.replace(' ', '')
    return struct.unpack('>f', binascii.unhexlify(s))[0] if s != '0' else 0.0

def union2header(ary, header, opt):
    (dtype1, dtype2) = ('long', 'double') if opt == 0 else ('int', 'float')
    n = len(ary)
    ret = "union %s {\n" % (header)
    ret += "    %s %s_param[%s];\n" % (dtype1, dtype1 ,n)
    ret += "    %s %s_param[%s];\n" % (dtype2, dtype2 ,n)
    ret += '};\n\n'
    return ret

def unionhex2header(ary, header, name, opt):
    dtype = 'long' if opt == 0 else 'int'
    n = len(ary)
    ret = "union %s %s = " % (header, name)
    if n == 1:
        ret += "{"
    else:
        ret += "\n{"
    for i, x in enumerate(ary):
        if i != 0:
            ret += ' '
        s = double_to_hex(x) if opt == 0 else float_to_hex(x)
        #print(s)
        ret += '(%s)' % dtype
        ret += ', '.join(['{:}'.format(s)])
        ret += ','
        if (i != n-1) and (i % 4 == 3):
            ret += '\n'
    ret += '};\n\n'
    return ret

def opmodel(size):
    fname = './model/{0}/{1}_{2}_{3}_{4}.pickle'.format(lenth, args.kernel, args.type, args.mode, size)
    with open(fname, mode = 'rb') as fp:
        clf = pickle.load(fp)
    return clf

def saveparam(clf, size, opt):
    dir_name = 'h' if opt == 0 else 'h_f'

    if args.kernel == 'rbf':
        fname = '../cpp/{0}/{1}/HLS_svm_param_rbf_{2}_{3}_{4}.h'.format(dir_name, lenth, args.type, args.mode, size)
        with open(fname, mode='w+') as f:
            support_vectors_shape = shape2header(clf.support_vectors_.shape, 'support_vectors_shape')
            f.write(support_vectors_shape)
            support_vectors = union2header(clf.support_vectors_.reshape(-1,), 'svm_param_svectors', opt)
            f.write(support_vectors)
            support_vectors = unionhex2header(clf.support_vectors_.reshape(-1,), 'svm_param_svectors', 'support_vectors', opt)
            f.write(support_vectors)

            dual_coef_shape = shape2header(clf.dual_coef_.shape, 'dual_coef_shape')
            f.write(dual_coef_shape)
            dual_coef = union2header(clf.dual_coef_.reshape(-1,), 'svm_param_dcoef', opt)
            f.write(dual_coef)
            dual_coef = unionhex2header(clf.dual_coef_.reshape(-1,), 'svm_param_dcoef', 'dual_coef', opt)
            f.write(dual_coef)

            scalar = union2header(clf.intercept_.reshape(-1,), 'svm_param_scalar', opt)
            f.write(scalar)
            bias = unionhex2header(clf.intercept_.reshape(-1,), 'svm_param_scalar', 'bias', opt)
            f.write(bias)
            rbf_gamma = unionhex2header(np.array([clf._gamma]), 'svm_param_scalar', 'rbf_gamma', opt) # 'gamma' is previous declaration in C++
            f.write(rbf_gamma)

    if args.kernel == 'linear':
        fname = '../cpp/{0}/{1}/HLS_svm_param_linear_{2}_{3}_{4}.h'.format(dir_name, lenth, args.type, args.mode, size)
        with open(fname, mode='w+') as f:
            coef_shape = shape2header(clf.coef_.shape, 'coef_shape')
            f.write(coef_shape)
            coef = union2header(clf.coef_.reshape(-1,), 'svm_param_coef', opt)
            f.write(coef)
            coef = unionhex2header(clf.coef_.reshape(-1,), 'svm_param_coef', 'coef', opt)
            f.write(coef)

            bias = union2header(clf.intercept_.reshape(-1,), 'svm_param_bias', opt)
            f.write(bias)
            bias = unionhex2header(clf.intercept_.reshape(-1,), 'svm_param_bias', 'bias', opt)
            f.write(bias)

def main() -> None:
    for size in [10, 20, 30, 40, 50, 60, 70, 80]:
        clf = opmodel(size)
        saveparam(clf, size, 0) #'double'
        saveparam(clf, size, 1) #'float'
        
if __name__=='__main__':
    main()