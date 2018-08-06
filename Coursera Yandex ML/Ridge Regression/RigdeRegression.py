
# coding: utf-8

# In[55]:


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Ridge
from scipy.sparse import hstack
import numpy as np


# In[34]:


train = pd.read_csv('D:\coursera\8\salary-train.csv')
train.columns


# In[35]:


train['FullDescription'] = train['FullDescription'].str.lower()
train['FullDescription'] = train['FullDescription'].replace('[^a-zA-Z0-9]', ' ', regex = True)


# In[46]:


vectorizer = TfidfVectorizer(min_df=5)
X_train_text = vectorizer.fit_transform(train['FullDescription'])


# In[37]:


train['LocationNormalized'].fillna('nan', inplace=True)
train['ContractTime'].fillna('nan', inplace=True)
enc = DictVectorizer()
X_train_categ = enc.fit_transform(train[['LocationNormalized', 'ContractTime']].to_dict('records'))


# In[53]:


X_train = hstack([X_train_text, X_train_categ])


# In[58]:


Y_train = train['SalaryNormalized']
model = Ridge(alpha=0.1, random_state=241)
model.fit(X_train, Y_train)


# In[73]:


test = pd.read_csv('D:\coursera\8\salary-test-mini.csv')
test['FullDescription'] = test['FullDescription'].str.lower()
test['FullDescription'] = test['FullDescription'].replace('[^a-zA-Z0-9]', ' ', regex = True)
vectorizer1 = TfidfVectorizer()
X_test_categ = enc.transform(test[['LocationNormalized', 'ContractTime']].to_dict('records'))
X_test_text = vectorizer.transform(test['FullDescription'])
X_test = hstack([X_test_text, X_test_categ])


# In[78]:


Y_test = model.predict(X_test)
print('{:0.2f} {:0.2f}'.format(Y_test[0], Y_test[1]))

