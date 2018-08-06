from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import math
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

df = pd.read_csv("D:/coursera/6/data-logistic.csv", header =None)

y = df[0]
X = df.loc[:, 1:]



def fw1(w1, w2, y, X, k, C):
    l = len(y)
    S = 0
    for i in range(0, l):
        S += y[i] * X[1][i] * (1.0 - 1.0 / (1.0 + math.exp(-y[i] * (w1*X[1][i] + w2*X[2][i]))))
    return w1 + (k * (1.0 / l) * S) - k * C * w1


def fw2(w1, w2, y, X, k, C):
    l =len(y)
    S = 0
    for i in range(0, l):
        S += y[i] * X[2][i] * (1.0 - 1.0 / (1.0 + math.exp(-y[i] * (w1*X[1][i] + w2*X[2][i]))))
    return w2 + (k * (1.0 / l) * S) - k * C * w2


def gradient_descent(y, X, C=0.0, w1=0.0, w2=0.0, k=0.1, error=1e-5):
    iterations = 10000
    i = 0
    w1_new, w2_new = w1, w2
    while True:
            i += 1
            w1_new, w2_new = fw1(w1, w2, y, X, k, C), fw2(w1, w2, y, X, k, C)
            e = math.sqrt((w1_new - w1) ** 2 + (w2_new - w2) ** 2)
            if i >= iterations or e <= error:
                break
            else:
                w1, w2 = w1_new, w2_new
                print(i, w1, w2)
    return [w1_new, w2_new]


def a(X, w1, w2):
    return 1.0 / (1.0 + math.exp(-w1 * X[1] - w2 * X[2]))


w1, w2 = gradient_descent(y, X, C=0.0)
rw1, rw2 = gradient_descent(y, X, C=10.0)

y_score = X.apply(lambda x: a(x, w1, w2), axis=1)
y_rscore = X.apply(lambda x: a(x, rw1, rw2), axis=1)

auc = roc_auc_score(y, y_score)
rauc = roc_auc_score(y, y_rscore)

print("{:0.3f} {:0.3f}".format(auc, rauc))