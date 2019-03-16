import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import os
import pickle
import sys
import inspect


#model_status = pickle.load(open('D:/python/TableFormat/terTree.sav', 'rb'))
#vectorizer_status = pickle.load(open('D:/python/TableFormat/vectorizer.sav', 'rb'))
#model_org_detector = pickle.load(open('D:/python/TableFormat/orgdetector.sav', 'rb'))
#vectorizer_org_detector = pickle.load(open('D:/python/TableFormat/vectorizer_org.sav', 'rb'))
#model_terdetector = pickle.load(open('D:/python/TableFormat/terdetector.sav', 'rb'))
#vectorizer_terdetector = pickle.load(open('D:/python/TableFormat/vectorizer_ter.sav', 'rb'))

def apply_classifier_to_df(path):
    model_status = pickle.load(open('D:/python/TableFormat/terTree.sav', 'rb'))
    vectorizer_status = pickle.load(open('D:/python/TableFormat/vectorizer.sav', 'rb'))
    df = pd.read_excel(path, skiprows=0)
    df["Статус"] = ""
    
    index = 0
    for i in df['Назначение_платежа']:
        text_to_predict = i
        df["Статус"][index] = model_status.predict(vectorizer_status.transform([text_to_predict]))
        index += 1
       
    writer = pd.ExcelWriter("D:/python/TableFormat/[CLASSIFIED] {} [CLASSIFIED].xlsx".format(os.path.splitext(os.path.split(path)[1])[0]), engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    
def apply_classifier_to_df_tableformat(vipiska):
    model_status = pickle.load(open('P:/Obmen/MaksimenkoEV/terTree.sav', 'rb'))
    vectorizer_status = pickle.load(open('P:/Obmen/MaksimenkoEV/vectorizer.sav', 'rb'))
    vipiska["Статус"] = ""
    
    index = 0
    for i in vipiska['Назначение_платежа']:
        text_to_predict = i
        vipiska["Статус"][index] = model_status.predict(vectorizer_status.transform([text_to_predict]))
        index += 1
       
    return vipiska


def detect_ter(path):
    df = pd.read_excel(path, skiprows=0)
    df = df.dropna()
    df = df.reset_index()
    df['ИНН_дебитора'] = df['ИНН_дебитора'].apply(int)
    df['ИНН_дебитора'] = df['ИНН_дебитора'].apply(str)
    df['ИНН_кредитора'] = df['ИНН_кредитора'].apply(int)
    df['ИНН_кредитора'] = df['ИНН_кредитора'].apply(str)
#    df["Текст"] = df['Назначение_платежа'] + df['Наименование_дебитора'] + df['ИНН_дебитора'] + df['Наименование_кредитора'] + df['ИНН_кредитора']
    df["Текст"] = df['Назначение_платежа']
    df["Статус третьего лица"] = ""
    
    index = 0
    for i in range(0, len(df)):
        text_to_predict = df['Текст'][i]
        df['Статус третьего лица'][index] = model_terdetector.predict(vectorizer_terdetector.transform([text_to_predict]))
        index += 1
    
    return recognize_organization(df)
    
def recognize_organization(df):
    df['Статус третьего лица'] = df['Статус третьего лица'].astype('str')
    df = df[df['Статус третьего лица'] == '[1]']
    df = df.reset_index()
    
    df["Орг"] = ""
    
    index = 0
    for i in range(0, len(df)):
        text_to_predict = df['Текст'][i]
        df['Орг'][index] = model_org_detector.predict(vectorizer_org_detector.transform([text_to_predict]))
        index += 1
        
    writer = pd.ExcelWriter("D:/python/TableFormat/[CLASSIFIED] {} [CLASSIFIED].xlsx".format(os.path.splitext(os.path.split(path)[1])[0]), engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    
#path = 'D:\python\TableFormat\все выписки банка\обработанные выписки\Выписка за 2019-02-28 20-22-35.xlsx'
#
#
#
#
#apply_classifier_to_df(path)
#detect_ter(path)
#
#filename = inspect.getframeinfo(inspect.currentframe()).filename
#path = os.path.dirname(os.path.abspath(filename))