from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

df_train = pd.read_csv("D:/coursera/5/perceptron-train.csv", header =None)
df_test = pd.read_csv("D:/coursera/5/perceptron-test.csv", header=None)
X_train = np.array(df_train.iloc[:,1:3])
y_train = np.array(df_train.iloc[:,0:1])
X_test = np.array(df_test.iloc[:,1:3])
y_test = np.array(df_test.iloc[:,0:1])
clf = Perceptron(random_state=241)
clf.fit(X_train, y_train)
predicted_train = clf.predict(X_test)
no_scale = accuracy_score(y_test, predicted_train) #0.655
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
clf = Perceptron(random_state=241)
clf.fit(X_train_scaled, y_train)
predicted_train_scaled = clf.predict(X_test_scaled)
scaled = accuracy_score(y_test, predicted_train_scaled) #0.845
