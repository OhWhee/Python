import pandas as pd
from lxml import etree
import datetime

todays_date = datetime.datetime.now().date()
bablo = str(0)

code_role_types = pd.read_excel('D:/R/finmon/КодыРолейУчастников.xlsx').fillna('')
ours_or_not = pd.read_excel('D:/R/finmon/НашКонтрагент.xlsx').fillna('')
code_participant_operation = pd.read_excel('D:/R/finmon/КодыУчастниковОпераций.xlsx').fillna('')
code_status = pd.read_excel('D:/R/finmon/КодЛицаУчастников.xlsx').fillna('')
orglist = pd.read_excel('D:/R/finmon/listorgs.xlsx').fillna('')


platelshik_list = orglist[orglist['НаимЮЛ'].str.contains('ООО "КВАДРО РКЦ"')]
doljnik_list = orglist[orglist['НаимЮЛ'].str.contains('ООО УО "Квадро-3"')]
poluchatel_list = orglist[orglist['НаимЮЛ'].str.contains('ООО "РЦ ЮО"')]

def operationNumber(input_operation_number:str):
    operation_number = "2018_3444213503_344401001_"
    operation_number = operation_number + f'{input_operation_number:08}'
    return str(operation_number)

def setFileName(number):
    new_file_name = "FM01_2_3444213503344401001_"
    date = datetime.datetime.now().date().strftime('%Y%m%d')
    new_file_name = new_file_name + date + '_01' + f'{number:08}'+ '.xml'
    return str(new_file_name)

#def operationDate(date):

tree = etree.parse("D:/R/finmon/scheme.xml")

nomer_zapisi = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/НомерЗаписи')
nomer_zapisi[0].text = operationNumber(1)

data_operacii = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/ДатаОперации')
data_operacii[0].text = data #ТУТ БУДЕТ ДАТА ОПЕРАЦИИ

data_viyavleniya = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/ДатаВыявления')
data_viyavleniya[0].text = datetime.datetime.now().date().strftime('%d/%m/%Y')

sumoperacii = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/СумОперации')
sumoperacii[0].text = bablo

sumrub = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/СумРуб')
sumrub[0].text = bablo

naznachenie = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/НазнПлатеж')
naznachenie[0].text = text #ТУТ БУДЕТ ТЕКСТ

harakter = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/ХарактерОп')
harakter[0].text = text2 #ТУТ БУДЕТ ТЕКСТ

koment = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/Коммент')
koment[0].text = text3 #ТУТ ТОЖЕ

poluchatel_kod_uchastnika_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/КодУчастника')
poluchatel_kod_uchastnika_xml[0].text = text4 #aaa

naimenovanie_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/НаимЮЛ')
naimenovanie_xml[0].text = str(poluchatel_list.iloc[0]['НаимЮЛ'])# получатель
naimenovanie_xml[1].text = str(platelshik_list.iloc[0]['НаимЮЛ'])# плательщик
naimenovanie_xml[2].text = str(doljnik_list.iloc[0]['НаимЮЛ'])# должник

INN_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ИННЮЛ')
INN_xml[0].text = str(poluchatel_list.iloc[0]['ИННЮЛ'])# получатель
INN_xml[1].text = str(platelshik_list.iloc[0]['ИННЮЛ'])# плательщик
INN_xml[2].text = str(doljnik_list.iloc[0]['ИННЮЛ'])# должник

KPP_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/КППЮЛ')
KPP_xml[0].text = str(poluchatel_list.iloc[0]['КППЮЛ'])# получатель
KPP_xml[1].text = str(platelshik_list.iloc[0]['КППЮЛ'])# плательщик
KPP_xml[2].text = str(doljnik_list.iloc[0]['КППЮЛ'])# должник

OKPO_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ОКПОЮЛ')
OKPO_xml[0].text = str(poluchatel_list.iloc[0]['ОКПОЮЛ'])# получатель
OKPO_xml[1].text = str(platelshik_list.iloc[0]['ОКПОЮЛ'])# плательщик
OKPO_xml[2].text = str(doljnik_list.iloc[0]['ОКПОЮЛ'])# должник

OKVED_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ОКВЭДЮЛ')
OKVED_xml[0].text = str(poluchatel_list.iloc[0]['ОКВЭДЮЛ'])# получатель
OKVED_xml[1].text = str(platelshik_list.iloc[0]['ОКВЭДЮЛ'])# плательщик
OKVED_xml[2].text = str(doljnik_list.iloc[0]['ОКВЭДЮЛ'])# должник

OGRN_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ОГРНЮЛ')
OGRN_xml[0].text = str(poluchatel_list.iloc[0]['ОГРНЮЛ'])# получатель
OGRN_xml[1].text = str(platelshik_list.iloc[0]['ОГРНЮЛ'])# плательщик
OGRN_xml[2].text = str(doljnik_list.iloc[0]['ОГРНЮЛ'])# должник

RegOrgan_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/НаименРегОргана')
RegOrgan_xml[0].text = str(poluchatel_list.iloc[0]['НаименРегОргана'])# получатель
RegOrgan_xml[1].text = str(platelshik_list.iloc[0]['НаименРегОргана'])# плательщик
RegOrgan_xml[2].text = str(doljnik_list.iloc[0]['НаименРегОргана'])# должник

DataRegUl_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ДатаРегЮл')
DataRegUl_xml[0].text = str(poluchatel_list.iloc[0]['ДатаРегЮл'])# получатель
DataRegUl_xml[1].text = str(platelshik_list.iloc[0]['ДатаРегЮл'])# плательщик
DataRegUl_xml[2].text = str(doljnik_list.iloc[0]['ДатаРегЮл'])# должник

KodOKSMU_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ЮрАдр/КодОКСМ')
KodOKSMU_xml[0].text = str(poluchatel_list.iloc[0]['КодОКСМЮ'])# получатель
KodOKSMU_xml[1].text = str(platelshik_list.iloc[0]['КодОКСМЮ'])# плательщик
KodOKSMU_xml[2].text = str(doljnik_list.iloc[0]['КодОКСМЮ'])# должник

KodPoOKATOU_xml = tree.xpath ('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ЮрАдр/КодСубъектаПоОКАТО')
KodPoOKATOU_xml[0].text = str(poluchatel_list.iloc[0]['КодСубъектаПоОКАТОЮ'])# получатель
KodPoOKATOU_xml[1].text = str(platelshik_list.iloc[0]['КодСубъектаПоОКАТОЮ'])# плательщик
KodPoOKATOU_xml[2].text = str(doljnik_list.iloc[0]['КодСубъектаПоОКАТОЮ'])# должник

rayonU_xml = tree.xpath ('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ЮрАдр/Район')
rayonU_xml[0].text = str(poluchatel_list.iloc[0]['РайонЮ'])# получатель
rayonU_xml[1].text = str(platelshik_list.iloc[0]['РайонЮ'])# плательщик
rayonU_xml[2].text = str(doljnik_list.iloc[0]['РайонЮ'])# должник

punktU_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ЮрАдр/Пункт')
punktU_xml[0].text = str(poluchatel_list.iloc[0]['ПунктЮ'])# получатель
punktU_xml[1].text = str(platelshik_list.iloc[0]['ПунктЮ'])# плательщик
punktU_xml[2].text = str(doljnik_list.iloc[0]['ПунктЮ'])# должник

ulicaU_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ЮрАдр/Улица')
ulicaU_xml[0].text = str(poluchatel_list.iloc[0]['УлицаЮ'])# получатель
ulicaU_xml[1].text = str(platelshik_list.iloc[0]['УлицаЮ'])# плательщик
ulicaU_xml[2].text = str(doljnik_list.iloc[0]['УлицаЮ'])# должник

domU_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ЮрАдр/Дом')
domU_xml[0].text = str(poluchatel_list.iloc[0]['ДомЮ'])# получатель
domU_xml[1].text = str(platelshik_list.iloc[0]['ДомЮ'])# плательщик
domU_xml[2].text = str(doljnik_list.iloc[0]['ДомЮ'])# должник

korpU_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ЮрАдр/Корп')
korpU_xml[0].text = str(poluchatel_list.iloc[0]['КорпЮ'])# получатель
korpU_xml[1].text = str(platelshik_list.iloc[0]['КорпЮ'])# плательщик
korpU_xml[2].text = str(doljnik_list.iloc[0]['КорпЮ'])# должник

ofU_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ЮрАдр/Оф')
ofU_xml[0].text = str(poluchatel_list.iloc[0]['ОфЮ'])# получатель
ofU_xml[1].text = str(platelshik_list.iloc[0]['ОфЮ'])# плательщик
ofU_xml[2].text = str(doljnik_list.iloc[0]['ОфЮ'])# должник

KodOKSMP_xml = tree.xpath ('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ФактАдр/КодОКСМ')
KodOKSMP_xml[0].text = str(poluchatel_list.iloc[0]['КодОКСМП'])# получатель
KodOKSMP_xml[1].text = str(platelshik_list.iloc[0]['КодОКСМП'])# плательщик
KodOKSMP_xml[2].text = str(doljnik_list.iloc[0]['КодОКСМП'])# должник

KodPoOKATOP_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ФактАдр/КодСубъектаПоОКАТО')
KodPoOKATOP_xml[0].text = str(poluchatel_list.iloc[0]['КодСубъектаПоОКАТОП'])# получатель
KodPoOKATOP_xml[1].text = str(platelshik_list.iloc[0]['КодСубъектаПоОКАТОП'])# плательщик
KodPoOKATOP_xml[2].text = str(doljnik_list.iloc[0]['КодСубъектаПоОКАТОП'])# должник

rayonP_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ФактАдр/Район')
rayonP_xml[0].text = str(poluchatel_list.iloc[0]['РайонП'])# получатель
rayonP_xml[1].text = str(platelshik_list.iloc[0]['РайонП'])# плательщик
rayonP_xml[2].text = str(doljnik_list.iloc[0]['РайонП'])# должник

punktP_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ФактАдр/Пункт')
punktP_xml[0].text = str(poluchatel_list.iloc[0]['ПунктП'])# получатель
punktP_xml[1].text = str(platelshik_list.iloc[0]['ПунктП'])# плательщик
punktP_xml[2].text = str(doljnik_list.iloc[0]['ПунктП'])# должник

ulicaP_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ФактАдр/Улица')
ulicaP_xml[0].text = str(poluchatel_list.iloc[0]['УлицаП'])# получатель
ulicaP_xml[1].text = str(platelshik_list.iloc[0]['УлицаП'])# плательщик
ulicaP_xml[2].text = str(doljnik_list.iloc[0]['УлицаП'])# должник

domP_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ФактАдр/Дом')
domP_xml[0].text = str(poluchatel_list.iloc[0]['ДомП'])# получатель
domP_xml[1].text = str(platelshik_list.iloc[0]['ДомП'])# плательщик
domP_xml[2].text = str(doljnik_list.iloc[0]['ДомП'])# должник

korpP_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ФактАдр/Корп')
korpP_xml[0].text = str(poluchatel_list.iloc[0]['КорпП'])# получатель
korpP_xml[1].text = str(platelshik_list.iloc[0]['КорпП'])# плательщик
korpP_xml[2].text = str(doljnik_list.iloc[0]['КорпП'])# должник

ofP_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведЮЛ/ФактАдр/Оф')
ofP_xml[0].text = str(poluchatel_list.iloc[0]['ОфП'])# получатель
ofP_xml[1].text = str(platelshik_list.iloc[0]['ОфП'])# плательщик
ofP_xml[2].text = str(doljnik_list.iloc[0]['ОфП'])# должник

bikko_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведенияКО/БИККО')
bikko_xml[0].text = str(poluchatel_list.iloc[0]['БИККО'])# получатель
bikko_xml[1].text = str(platelshik_list.iloc[0]['БИККО'])# плательщик
bikko_xml[2].text = str(doljnik_list.iloc[0]['БИККО'])# должник

nomerscheta_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведенияКО/НомерСчета')
nomerscheta_xml[0].text = str(poluchatel_list.iloc[0]['НомерСчета'])# получатель
nomerscheta_xml[1].text = str(platelshik_list.iloc[0]['НомерСчета'])# плательщик
nomerscheta_xml[2].text = str(doljnik_list.iloc[0]['НомерСчета'])# должник

naimko_xml = tree.xpath('/Сбщ110Операции/ИнформЧасть/Операция/УчастникОп/СведенияКО/НаимКО')
naimko_xml[0].text = str(poluchatel_list.iloc[0]['НаимКО'])# получатель
naimko_xml[1].text = str(platelshik_list.iloc[0]['НаимКО'])# плательщик
naimko_xml[2].text = str(doljnik_list.iloc[0]['НаимКО'])# должник

tree.write('D:/R/finmon/out.xml', pretty_print=True, xml_declaration=True,   encoding="utf-8")
