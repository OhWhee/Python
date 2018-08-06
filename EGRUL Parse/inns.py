import json
import requests
import pandas as pd

inns = pd.read_excel("D:/R/inns/инн_лист.xlsx")


API_KEY = 'API_KEY'
BASE_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party'

def suggest(query):
    url = BASE_URL
    headers = {
        'Authorization': 'Token %s' % API_KEY,
        'Content-Type': 'application/json'}
    data = {'query': query}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()

df = pd.DataFrame()
for i in inns["ИНН"]:
    inn_find = suggest(i)
    cols = {}
    try:
        cols["Полное наименование организации"] = str(inn_find["suggestions"][0]["data"]["name"]["full_with_opf"])
    except Exception:
        pass
    try:
        cols["Короткое наименование организации"] = str(inn_find["suggestions"][0]["data"]["name"]["short"])
    except Exception:
        pass
    try:
        cols["ФИО руководителя"] = str(inn_find["suggestions"][0]["data"]["management"]["name"])
    except Exception:
        pass
    try:
        cols["Должность руководителя"] = str(inn_find["suggestions"][0]["data"]["management"]["post"])
    except Exception:
        pass
    try:
        cols["Адрес организации"] = str(inn_find["suggestions"][0]["data"]["address"]["value"])
    except Exception:
        pass
    try:
        cols["ИНН организации"] = str(inn_find["suggestions"][0]["data"]["inn"])
    except Exception:
        pass
    try:
        cols["КПП организации"] = str(inn_find["suggestions"][0]["data"]["kpp"])
    except Exception:
        pass
    try:
        cols["ОГРН организации"] = str(inn_find["suggestions"][0]["data"]["ogrn"])
    except Exception:
        pass
    try:
        cols["ОКПО организации"] = str(inn_find["suggestions"][0]["data"]["okpo"])
    except Exception:
        pass
    try:
        cols["ОКВЭД организации"] = str(inn_find["suggestions"][0]["data"]["okved"])
    except Exception:
        pass
    try:
        cols["Статус организации"] = str(inn_find["suggestions"][0]["data"]["state"]["status"])
    except Exception:
        pass
    try:
        cols["Тип лица"] = str(inn_find["suggestions"][0]["data"]["type"])
    except Exception:
        pass
    try:
        cols["ФИАС"] = str(inn_find["suggestions"][0]["data"]["address"]["data"]["fias_id"])
    except Exception:
        pass
    try:
        df1 = pd.DataFrame.from_records([cols])
    except Exception:
        df1 = pd.DataFrame.from_dict([cols])
    df = df.append(df1)


df.to_excel("D:\R\egrul.xlsx")

