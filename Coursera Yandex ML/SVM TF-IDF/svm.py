import pandas as pd
import numpy as np
from sklearn import svm

data = pd.read_csv("D:/coursera/4/svm-data.csv", header = None)
y = data[0]
X = data.loc[:, 1:]

model = svm.SVC(kernel="linear", C = 100000, random_state = 241)
model.fit(X,y)

n_sv = model.support_
n_sv.sort()
print(n_sv)

