import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import os
import pickle
import sys
import inspect
import queries
import datetime


model_status = pickle.load(open('D:/python/TableFormat/model_status_detector.sav', 'rb'))
vectorizer_status = pickle.load(open('D:/python/TableFormat/status_vectorizer.sav', 'rb'))
model_org_detector = pickle.load(open('D:/python/TableFormat/model_3rd_party_name_detector.sav', 'rb'))
vectorizer_org_detector = pickle.load(open('D:/python/TableFormat/3rd_party_name_vectorizer.sav', 'rb'))
model_terdetector = pickle.load(open('D:/python/TableFormat/model_3rd_party_status_detector.sav', 'rb'))
vectorizer_terdetector = pickle.load(open('D:/python/TableFormat/3rd_party_status_vectorizer.sav', 'rb'))

def apply_classifier_to_df(path):
    model_status = pickle.load(open('D:/python/TableFormat/model_status_detector.sav', 'rb'))
    vectorizer_status = pickle.load(open('D:/python/TableFormat/status_vectorizer.sav', 'rb'))
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
    
    return recognize_organization(df, path)
    
def recognize_organization(df, path):
    df['Статус третьего лица'] = df['Статус третьего лица'].astype('str')
    df = df[df['Статус третьего лица'] == '[1]']
    df = df.reset_index()
    
    df["Орг"] = ""
    
    index = 0
    for i in range(0, len(df)):
        text_to_predict = df['Текст'][i]
        df['Орг'][index] = model_org_detector.predict(vectorizer_org_detector.transform([text_to_predict]))[0]
        index += 1
        
#    df['Орг'] = df['Орг'].str.replace("""[""", "")
#    df['Орг'] = df['Орг'].str.replace("""]""", "")
#    df['Орг'] = df['Орг'].str.replace("""'""", "")
        
    writer = pd.ExcelWriter("D:/python/TableFormat/[CLASSIFIED] {} [CLASSIFIED].xlsx".format(os.path.splitext(os.path.split(path)[1])[0]), engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()



def detect_ter_for_bd(path):
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
    
    return recognize_organization_for_bd(df)

def recognize_organization_for_bd(df):
    now = datetime.datetime.now()
    df['Статус третьего лица'] = df['Статус третьего лица'].astype('str')
    df = df[df['Статус третьего лица'] == '[1]']
    df = df.reset_index()
    
    df["Орг"] = ""
    
    index = 0
    for i in range(0, len(df)):
        text_to_predict = df['Текст'][i]
        df['Орг'][index] = model_org_detector.predict(vectorizer_org_detector.transform([text_to_predict]))[0]
        index += 1
    
    for row in df.iterrows():
        date = datetime.datetime.strptime(str(row[1]["Дата_проводки"]), "%Y-%m-%d %H:%M:%S")
        new_date = date.strftime("%d.%m.%Y")
        operation_object = queries.OperationObjectFactory().create_last_operation_object()
        payer = str(queries.get_org_id_by_inn(inn=str(row[1]["ИНН_кредитора"])))
        receiver = str(queries.get_org_id_by_inn(inn=str(row[1]["ИНН_дебитора"])))
        debtor = str(queries.get_org_id_by_short_name(row[1]["Орг"]))
        
        operation_data = {"operation_date": new_date,
                          "detection_date": str(now.strftime("%d.%m.%Y")),
                          "daily_number": int(operation_object.make_new_daily_number()),
                          "annual_number": int(operation_object.make_next_annual_number()),
                          "operation_number": str(operation_object.make_next_operation_number()),
                          "amount": float(row[1]["Сумма_по_кредиту"]) if float(row[1]["Сумма_по_дебету"]) == 0 else float(row[1]["Сумма_по_дебету"]),
                          "payment_purpose": str(row[1]["Назначение_платежа"]),
                          "payment_class": str(row[1]["Назначение_платежа"]),
                          "payer": payer,
                          "receiver": receiver,
                          "debtor": debtor,
                          "contract": queries.get_first_contract_depending_on_sides_ID(payer,
                                                                                    debtor,
                                                                                    receiver),
                          "payment_number": str(row[1]["№_документа"])}
        
        for k, v in operation_data.items():
            print(k, v)
        
        queries.insert_operation(operation_date=operation_data["operation_date"],
                                 detection_date=operation_data["detection_date"],
                                 daily_number=operation_data["daily_number"],
                                 annual_number=operation_data["annual_number"],
                                 operation_number=operation_data["operation_number"],
                                 amount=operation_data["amount"],
                                 payment_purpose=operation_data["payment_purpose"],
                                 payment_class=operation_data["payment_class"],
                                 payer=operation_data["payer"],
                                 receiver=operation_data["receiver"],
                                 debtor=operation_data["debtor"],
                                 contract=operation_data["contract"],
                                 payment_number=operation_data["payment_number"])

#path = 'D:\python\TableFormat\все выписки банка\обработанные выписки\Выписка за 2019-02-28 20-22-35.xlsx'
#
#
#
#
#apply_classifier_to_df(path)
#df = detect_ter(path)
#
#filename = inspect.getframeinfo(inspect.currentframe()).filename
#path = os.path.dirname(os.path.abspath(filename))
        
