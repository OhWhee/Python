# -*- coding: utf-8 -*-
import pandas as pd
from lxml import etree as ET
import os
import glob

xml_path = "D:/RFM/xml monitoring/*xml"


class Operation:
    
    def __init__(self, annual_number=None, daily_number=None, operation_date=None, detection_date=None,
                 payer=None, debtor=None, receiver=None):
        
        self.annual_number = annual_number
        self.daily_number = daily_number
        self.operation_date = operation_date
        self.detection_date = detection_date
        self.payer = payer
        self.debtor = debtor
        self.receiver = receiver

        

def make_journal(xml_path):
    df = pd.DataFrame()    
    operation = Operation()
    for file in glob.glob(xml_path):
        xml_tree = ET.parse(file)
        xml_root = xml_tree.getroot()
        operation.daily_number = os.path.splitext(file)[0][-4:]
        for participants in xml_root.findall('.//УчастникОп'):
            for info in participants.getchildren():
                if info.tag == "КодРоли" and info.text == "01":
                    for n in participants.getchildren():
                        if n.tag == "СведЮЛ":
                            for m in n.getchildren():
                                if m.tag == "НаимЮЛ":
                                    operation.payer = m.text   
                if info.tag == "КодРоли" and info.text == "08":
                    for n in participants.getchildren():
                        if n.tag == "СведЮЛ":
                            for m in n.getchildren():
                                if m.tag == "НаимЮЛ":
                                    operation.debtor = m.text 
                if info.tag == "КодРоли" and info.text == "02":
                    for n in participants.getchildren():
                        if n.tag == "СведЮЛ":
                            for m in n.getchildren():
                                if m.tag == "НаимЮЛ":
                                    operation.receiver = m.text                                      
        for oper in xml_root.findall('.//Операция'):
            for info in oper.getchildren():
                if info.tag == "НомерЗаписи":
                    operation.annual_number = str(info.text)[-4:]
                if info.tag == "ДатаОперации":
                    operation.operation_date = str(info.text).replace("/", ".")
                if info.tag == "ДатаВыявления":
                    operation.detection_date = str(info.text).replace("/", ".")
        new_dict = {"Дата поступления внутреннего сообщения": operation.detection_date,
                    "ФИО лица, составившего внутреннее сообщение": "Максименко Е.В.",
                    "ФИО лица, принявшего внутреннее сообщение": "Крылов Е.А.",
                    "Краткое содержание": "Оплата {}, за {} от {}".format(operation.payer,
                                                  operation.debtor, operation.operation_date),
                    "Подпись составившего внутреннее сообщение": "",
                    "Подпись принявшего внутреннее сообщение": "",
                    "Результаты рассмотрения внутреннего сообщения": "Отправлено в РФМ №{}/{} от {}".format(operation.annual_number,
                                                                                        operation.daily_number, operation.detection_date)}
        df = df.append(new_dict, ignore_index=True)
        df = df[["Дата поступления внутреннего сообщения",
         "ФИО лица, составившего внутреннее сообщение",
         "ФИО лица, принявшего внутреннее сообщение",
         "Краткое содержание",
         "Подпись составившего внутреннее сообщение",
         "Подпись принявшего внутреннее сообщение",
         "Результаты рассмотрения внутреннего сообщения"]]
    return df.to_csv("D:/RFM/РФМ журнал/journal.csv", sep=',', encoding="utf-8")
                
df = make_journal(xml_path)
