import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import KFold

newsgroups = datasets.fetch_20newsgroups(
                    subset='all',
                    categories=['alt.atheism', 'sci.space']
             )

X = newsgroups.data
y = newsgroups.target

vectorizer = TfidfVectorizer()
vectorizer.fit_transform(X)


grid = {'C': np.power(10.0, np.arange(-5, 6))}
cv = KFold(y.size, n_folds=5, shuffle=True, random_state=241)
clf = SVC(kernel='linear', random_state=241)
gs = GridSearchCV(clf, grid, scoring='accuracy', cv=cv)
gs.fit(vectorizer.transform(X), y)

score = 0
C = 0
for attempt in gs.grid_scores_:
    if attempt.mean_validation_score > score:
        score = attempt.mean_validation_score
        C = attempt.parameters['C']

model = SVC(kernel='linear', random_state=241, C=C)
model.fit(vectorizer.transform(X), y)

words = vectorizer.get_feature_names()
coef = pd.DataFrame(model.coef_.data, model.coef_.indices)
top_words = coef[0].map(lambda w: abs(w)).sort_values(ascending=False).head(10).index.map(lambda i: words[i])
print(','.join(sorted(top_words)))
