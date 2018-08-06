import pandas as pd
import os

filepathOpen = "D:/R/vipiska/160218.xlsx"
df = pd.read_excel(filepathOpen, skiprows=0, header=None)


def reopen_with_correct_skiprows(df):
    for index, row in df.iterrows():
        text_in_rows = row.tolist()
        if "Дата проводки" not in text_in_rows:
            pass#df.drop(df.iloc[0:index], inplace=True, axis=1)
        else:
            df = pd.read_excel(filepathOpen, skiprows=index, header=None)
            break
    return df

df = reopen_with_correct_skiprows(df)



def check_for_exact_string(df):
    for col in df.columns:
        indexer = []
        indexer = df[col]#.str.contains("б/с 40702")):
        for index, item in enumerate(indexer):
            if item == "б/с 40702":
                df = df.drop(df.index[index:])
    return df
df = check_for_exact_string(df)
df = pd.DataFrame(df).dropna(axis='columns', how='all')
df.columns = range(1, df.shape[1]+1)
vipiska = df.iloc[:,0:df.shape[1]]

def check_col_numbers(vipiska):
    if vipiska.shape[1] > 9:
        vipiska = vipiska.iloc[:, 0:9]
        #for col in vipiska.columns:
            #if sum(vipiska[col].isna()) == vipiska.shape[0]:
                #del vipiska[col]
    return vipiska

vipiska = check_col_numbers(vipiska)

vipiska.columns = ("Дата_проводки",
                      "Счет_дебет",
                      "Счет_кредит",
                      "Сумма_по_дебету",
                      "Сумма_по_кредиту",
                      "№_документа",
                      "ВО",
                      "Банк_(БИК_и_наименование)",
                      "Назначение_платежа")


def delete_strings(vipiska):
    vipiska_updated = pd.DataFrame()
    for i in vipiska.iterrows():
        if i[1]["Счет_дебет"] != "Дебет" and i[1]["Счет_дебет"] != "Счет" and i[1]["Дата_проводки"] != "Дата проводки":
            vipiska_updated = vipiska_updated.append(i[1])
    return vipiska_updated

vipiska_updated = delete_strings(vipiska)

#vipiska = vipiska.drop(vipiska.index[:1])

#vipiska = pd.DataFrame(vipiska).dropna(axis='columns', how='all')
vipiska_updated = pd.DataFrame(vipiska_updated).dropna(axis='rows', how='all')

#for index, string in enumerate(list(vipiska["Сумма_по_дебету"])):
    #if pd.isna(string):
        #vipiska["Сумма_по_дебету"][index] = 0

if pd.isna(vipiska_updated["Сумма_по_дебету"]).any():
    vipiska_updated["Сумма_по_дебету"].fillna(0, inplace=True)
if pd.isna(vipiska_updated["Сумма_по_кредиту"]).any():
    vipiska_updated["Сумма_по_кредиту"].fillna(0, inplace=True)

vipiska = vipiska[vipiska['Дата_проводки'].notnull() & (vipiska['Дата_проводки'] != "Дата проводки")]
vipiska['Счет_дебет'] = vipiska['Счет_дебет'].replace({'\\n':' '}, regex=True)
vipiska['Счет_кредит'] = vipiska['Счет_кредит'].replace({'\\n':' '}, regex=True)
vipiska['Банк_(БИК_и_наименование)'] = vipiska['Банк_(БИК_и_наименование)'].replace({'\\n':' '}, regex=True)
vipiska['Сумма_по_дебету'] = vipiska['Сумма_по_дебету'].fillna("0")
vipiska['Сумма_по_кредиту'] = vipiska['Сумма_по_кредиту'].fillna("0")

try:
    vipiska['Сумма_по_кредиту'] = vipiska['Сумма_по_кредиту'].replace({'\\s':'', ',':'.'}, regex=True)
    vipiska['Сумма_по_дебету'] = vipiska['Сумма_по_дебету'].replace({'\\s':'', ',':'.'}, regex=True)
except Exception:
    pass

vipiska['Сумма_по_кредиту'] = pd.to_numeric(vipiska['Сумма_по_кредиту'], errors='coerce')
vipiska['Сумма_по_дебету'] = pd.to_numeric(vipiska['Сумма_по_дебету'], errors='coerce')

vipiska['ИНН_дебитора'] = vipiska['Счет_дебет'].str.extract('(\\s[0-9]{10,12})', expand=False).str.strip()
vipiska['Р/С_дебитора'] = vipiska['Счет_дебет'].str.extract('(^[0-9]{20})', expand=False).str.strip()
vipiska['Наименование_дебитора'] = vipiska['Счет_дебет'].str.extract('(\\s+\\D.*)', expand=False).str.strip()
vipiska['ИНН_кредитора'] = vipiska['Счет_кредит'].str.extract('(\\s[0-9]{10,12})', expand=False).str.strip()
vipiska['Р/С_кредитора'] = vipiska['Счет_кредит'].str.extract('(^[0-9]{20})', expand=False).str.strip()
vipiska['Наименование_кредитора'] = vipiska['Счет_кредит'].str.extract('(\\s+\\D.*)', expand=False).str.strip()


vipiska.reset_index(drop=True)
writer = pd.ExcelWriter('D:/test.xlsx', engine='xlsxwriter')
vipiska.to_excel(writer, sheet_name='Sheet1', index=False, append=True)
writer.save()

for filename in os.walk('D:/R/vipiska/Выписки банка/красиво'):
    print(i[2])

#united = pd.DataFrame(columns=("Дата_проводки",
#                     # "Счет_дебет",
#                      "Счет_кредит",
#                      "Сумма_по_дебету",
#                      "Сумма_по_кредиту",
#                      "№_документа",
#                      "ВО",
#                      "Банк_(БИК_и_наименование)",
#                      "Назначение_платежа"))
#for i in filename[2]:
#    df = pd.read_excel("D:/R/vipiska/Выписки банка/красиво" + "/" + i, skiprows=0, header=None)
#    united.append(i)

