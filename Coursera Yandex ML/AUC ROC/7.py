import pandas as pd
from sklearn import metrics
import numpy as np

df = pd.read_csv("D:/coursera/7/classification.csv")

clf_table = {"tp": (1, 1), "fp": (0, 1), "fn": (1, 0), "tn": (0,0)}

#Заполнение таблицы ошибок классификации
for name, res in clf_table.items():
    clf_table[name] = len(df[(df["true"] == res[0]) & (df["pred"] == res[1])])
    
print(clf_table)

#Расчет метрик качества

#Доля правильных ответов
accuracy = metrics.accuracy_score(y_true = df["true"], y_pred = df["pred"])

#Точность ответов
precision = metrics.precision_score(y_true = df["true"], y_pred = df["pred"])

#Полнота ответов
recall = metrics.recall_score(y_true = df["true"], y_pred = df["pred"])

#Гармоническое среднее
harmonic_mean = metrics.f1_score(y_true = df["true"], y_pred = df["pred"])

df2 = pd.read_csv("D:/coursera/7/scores.csv")


#Площадь под ROC кривой
roc_square = {"score_logreg":0, "score_svm":0, "score_knn":0, "score_tree":0}
for name in df2.columns[1:]:
    roc_square[name] = metrics.roc_auc_score(y_true = df2["true"], y_score = df2[name])


#Найти максимальное значание точности при полноте >= 70%
prc_scores = {}

for name in df2.columns[1:]:
    prc_square = metrics.precision_recall_curve(y_true = df2["true"], probas_pred = df2[name])
    prc_square_df = pd.DataFrame({'precision': prc_square[0], 'recall': prc_square[1]})
    prc_scores[name] = prc_square_df[prc_square_df["recall"] >= 0.7]["precision"].max()

