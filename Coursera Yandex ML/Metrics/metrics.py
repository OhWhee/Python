from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import sklearn
import numpy as np
import pandas as pd
from sklearn.datasets import load_boston

df = load_boston()
df_pd = pd.DataFrame(df.data)
df_pd.columns = df.feature_names
df_pd["PRICE"] = df.target

df_sized = pd.DataFrame(sklearn.preprocessing.scale(df_pd))
df_sized.columns = df_pd.columns

Y = df_sized["PRICE"]
X = df_sized.drop("PRICE", axis=1)



def accuracy_test(X, Y, kf):
    scores = list()
    p_range = np.linspace(1, 10, num = 200)
    for p in p_range:
     model = sklearn.neighbors.KNeighborsRegressor(p=p, n_neighbors=5, weights="distance")
     scores.append(cross_val_score(model, X, Y, cv=kf, scoring='mean_squared_error')) 
    return pd.DataFrame(scores, p_range).max(axis=1).sort_values(ascending = False)

kf = KFold(n_splits=5, shuffle=True, random_state=42)    
accuracy = accuracy_test(X, Y, kf)
top_accuracy = accuracy.head(1)
print(1, top_accuracy.index[0])


















