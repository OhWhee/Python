
# coding: utf-8

# In[44]:


import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.cross_validation import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score


# In[8]:


df = pd.read_csv("D:/coursera/10/abalone.csv")
df['Sex'] = df['Sex'].map(lambda x: 1 if x == 'M' else (-1 if x == 'F' else 0))


# In[28]:


X = df.iloc[: ,:-1]
y = df.iloc[: ,-1:]


# In[42]:


n_trees = np.arange(1,101,1)
param_grid = {'n_estimators': n_trees}
grid_search = GridSearchCV(RandomForestRegressor(random_state=1), param_grid)
grid_search.fit(X,y)


# In[73]:


kf = KFold(y.size, n_folds=5, random_state=1, shuffle=True)
scores = [0.0]
n_tree = range(1,51)

for n in n_tree:
    model = RandomForestRegressor(random_state=1, n_estimators=n)
    score = np.mean(cross_val_score(model, X, y, scoring='r2', cv=kf))
    scores.append(score)


# In[76]:


for n, score in enumerate(scores):
    if score > 0.52:
        print(n, score)
        break

