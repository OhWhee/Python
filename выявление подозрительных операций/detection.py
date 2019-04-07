import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import KFold
import glob
import os
import pickle



path = "D:/python/TableFormat/все выписки банка/обработанные выписки/*.xlsx"
def gather_xlsx(path):
    all_data = pd.DataFrame()

    for f in glob.glob(path):
        df = pd.read_excel(f)
        all_data = all_data.append(df, ignore_index=True)
    
    writer = pd.ExcelWriter("D:/python/TableFormat/все выписки банка/обработанные выписки/объединенные.xlsx", engine='xlsxwriter')
    all_data.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()

data = pd.DataFrame()
data = pd.read_excel("D:/python/TableFormat/все выписки банка/обработанные выписки/объединенные.xlsx", ignore_index=True)
data = data.dropna()

 
    
X = data.drop(['Статус'], axis=1)
X = X.dropna()    
X['ИНН_дебитора'] = X['ИНН_дебитора'].apply(int)
X['ИНН_дебитора'] = X['ИНН_дебитора'].apply(str)
X['ИНН_кредитора'] = X['ИНН_кредитора'].apply(int)
X['ИНН_кредитора'] = X['ИНН_кредитора'].apply(str)

X = data.drop(['Третья сторона'], axis=1)
X = X.dropna() 
X['ИНН_дебитора'] = X['ИНН_дебитора'].apply(int)
X['ИНН_дебитора'] = X['ИНН_дебитора'].apply(str)
X['ИНН_кредитора'] = X['ИНН_кредитора'].apply(int)
X['ИНН_кредитора'] = X['ИНН_кредитора'].apply(str)

X = data.drop(['Статус третьего лица'], axis=1)
X = X.dropna() 
X['ИНН_дебитора'] = X['ИНН_дебитора'].apply(int)
X['ИНН_дебитора'] = X['ИНН_дебитора'].apply(str)
X['ИНН_кредитора'] = X['ИНН_кредитора'].apply(int)
X['ИНН_кредитора'] = X['ИНН_кредитора'].apply(str)




X = X['Назначение_платежа'] + X['Наименование_дебитора'] + X['ИНН_дебитора'] + X['Наименование_кредитора'] + X['ИНН_кредитора']
y = data['Статус']
X = X['Назначение_платежа']
y = data['Третья сторона']
X = X['Назначение_платежа'] + X['Наименование_дебитора'] + X['ИНН_дебитора'] + X['Наименование_кредитора'] + X['ИНН_кредитора']
y = data['Статус третьего лица']

 
vectorizer = TfidfVectorizer()
vectorizer.fit_transform(X)


#grid = {'C': np.power(10.0, np.arange(-5, 6))}
grid = {'n_estimators': range(1, 300, 50)}
cv = KFold(y.size, n_folds=5, shuffle=True, random_state=241)
clf = RandomForestClassifier()
gs = GridSearchCV(clf, grid, scoring='accuracy', cv=cv)
gs.fit(vectorizer.transform(X), y)

score = 0
n_estimators = 0
for attempt in gs.grid_scores_:
    if attempt.mean_validation_score > score:
        score = attempt.mean_validation_score
        n_estimators = attempt.parameters['n_estimators']

model = RandomForestClassifier(n_estimators=n_estimators)
model.fit(vectorizer.transform(X), y)

modelpickle = 'D:/python/TableFormat/terTree.sav'
vectorizerpickle = 'D:/python/TableFormat/vectorizer.sav'
pickle.dump(model, open(modelpickle, 'wb'))
pickle.dump(vectorizer, open(vectorizerpickle, 'wb'))



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

modelpickle = 'D:/python/TableFormat/orgdetector.sav'
vectorizerpickle = 'D:/python/TableFormat/vectorizer_org.sav'
pickle.dump(model, open(modelpickle, 'wb'))
pickle.dump(vectorizer, open(vectorizerpickle, 'wb'))


words = vectorizer.get_feature_names()
coef = pd.DataFrame(model.coef_.data, model.coef_.indices)
top_words = coef[0].map(lambda w: abs(w)).sort_values(ascending=False).head(10).index.map(lambda i: words[i])
print(', '.join(sorted(top_words)))   

text_to_predict = ['''6164318594 ОАО "ЕИРЦ" 3444213503 ООО "Расчетный центр южного округа" Оплата населения ООО УПРАВЛЯЮЩАЯ ОРГАНИЗАЦИЯ ЖКХ за тепло из ср-в. РТС согл. дог. 5376 от 27.09.16  В том числе НДС 18 % - 1372.88''']


#Прогноз является ли операци подозрительной
model.predict(vectorizer.transform(text_to_predict))
