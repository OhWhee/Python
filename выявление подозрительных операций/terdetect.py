import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import KFold

vipiska = pd.read_excel("D:/R/vipiska/terbase.xlsx")

X = vipiska.drop(["status"], axis=1)
X = vipiska["Счет_дебет"] + vipiska["Счет_кредит"] + vipiska["Назначение_платежа"]
y = vipiska["status"]

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

model = SVC(kernel='linear', random_state=241, C=C)s
model.fit(vectorizer.transform(X), y)

words = vectorizer.get_feature_names()
coef = pd.DataFrame(model.coef_.data, model.coef_.indices)
top_words = coef[0].map(lambda w: abs(w)).sort_values(ascending=False).head(10).index.map(lambda i: words[i])
print(','.join(sorted(top_words)))

text_to_predict = ['''''']

#Прогноз является ли операци подозрительной
model.predict(vectorizer.transform(text_to_predict))

for i in [X]:
    text_to_predict = i
    vipiska["model_predict"] = model.predict(vectorizer.transform(text_to_predict))
