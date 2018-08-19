import xml.etree.ElementTree as ET
import re

def read_xml(path):
    """Возваращает объект типа xml.etree.ElementTree"""
    tree = ET.parse(path)
    root = tree.getroot()
    return root
    
def get_operation_info(xml_root):
    """Создает класс с параметрами операции"""
    record_number = xml_root.findall(".//НомерЗаписи")[0].text
    operation_date = xml_root.findall(".//ДатаОперации")[0].text
    detection_date = xml_root.findall(".//ДатаВыявления")[0].text
    sum_operation = xml_root.findall(".//СумОперации")[0].text
    purpose = xml_root.findall(".//НазнПлатеж")[0].text
    pay_number = xml_root.findall(".//Коммент")[0].text
    operation_info_object = OperationInfo(record_number, operation_date,
                                             detection_date, sum_operation,
                                             purpose, pay_number)
    return operation_info_object


class OperationInfo:
    
    def __init__(self, record_number, operation_date, detection_date,
                 sum_operation, purpose, pay_number):
        self.record_number = record_number
        self.operation_date = operation_date
        self.detection_date = detection_date
        self.sum_operation = sum_operation
        self.purpose = purpose
        self.pay_number = pay_number

class ParticipantUl():
    
    def __init__(self, org_name, org_inn, org_kpp, org_ogrn, org_okpo,
                 org_okved, org_rs, bik, bank_name, register_name, 
                 register_date, ur_adress, post_adress):
        self.org_name = org_name
        self.org_inn = org_inn
        self.org_kpp = org_kpp
        self.org_ogrn = org_ogrn
        self.org_okpo = org_okpo
        self.org_okved = org_okved
        self.org_rs = org_rs
        self.bik = bik
        self.bank_name = bank_name
        self.register_name = register_name
        self.register_date = register_date
        self.ur_adress = ur_adress
        self.post_adress = post_adress


class ParticipantFl():
    
    def __init__(self, second_name, first_name, patronimic, inn, birth_date,
                 adress_reg, adress_preb, bik, bank_name, rs, passport_data):
        self.second_name = second_name
        self.first_name = first_name
        self.patronimic = patronimic
        self.inn = inn
        self.birth_date = birth_date
        self.adress_reg = adress_reg
        self.adress_preb = adress_preb
        self.bik = bik
        self.bank_name = bank_name
        self.rs = rs
        self.passport_data = passport_data




def get_requisites(root, role):
    """Роли: Recipient - получатель
             Debtor - должник
             Payer - плательщик"""
    role_dict = {"Payer": "01", "Recipient": "02", "Debtor": "08"}
    role_code = role_dict.get(role)
    data = []
    for tags in root.findall(".//УчастникОп"):
        for tag in tags.getchildren():
            if tag.tag == "КодРоли" and tag.text == role_code:
                for tag in tags.getchildren():
                    if tag.tag == "СведЮЛ":
                        for i in tag:
                            #if i.text != re.match("\\n+\s+", str(i.text)) is None:
                            #print(tag.tag, i.tag, i.text)
                            #if i.text == None:
                            if i.text != re.match("\\n+\s+", str(i.text)):
                                i.text == ""
                            elif i.text == None:
                                i.text = ""
                            data.append({tags.tag + i.tag: i.text})
                    if tag.tag == "СведенияКО":
                        for k in tag:
                            #if k.text != re.match("\\n+\s+", str(k.text)) is None:
                            #print(tag.tag, k.tag, k.text)
                            #if k.text == None:
                            if k.text == re.match("\\n+\s+", str(k.text)):
                                k.text = ""
                            elif k.text == None:
                                k.text = ""
                            data.append({tags.tag + k.tag: k.text})
                    for t in tag.getchildren():
                        if t.tag == "ЮрАдр":
                            for x in t.getchildren():
                                #print(t.tag, x.tag)
                                if x.text == None:
                                    x.text = ""
                                data.append({t.tag + x.tag: x.text})
                        if t.tag == "ФактАдр":
                            for x in t.getchildren():
                                #print(t.tag, x.tag)
                                if x.text == None:
                                    x.text = ""
                                data.append({t.tag + x.tag: x.text})
    obj = combine_reqs_to_object(data)
    return obj

def combine_reqs_to_object(data):
    req_list = ['УчастникОпНаимЮЛ', 'УчастникОпИННЮЛ', 'УчастникОпКППЮЛ', 
                'УчастникОпОКПОЮЛ', 'УчастникОпОКВЭДЮЛ', 'УчастникОпОГРНЮЛ',
                'УчастникОпНаименРегОргана', 'УчастникОпДатаРегЮл', 'ЮрАдрПункт',
                'ЮрАдрУлица', 'ЮрАдрДом', 'ЮрАдрКорп', 'ЮрАдрОф', 'ФактАдрПункт',
                'ФактАдрУлица', 'ФактАдрДом', 'ФактАдрКорп', 'ФактАдрОф',
                'УчастникОпБИККО', 'УчастникОпНомерСчета', 'УчастникОпНаимКО']
    requisites = []
    req_list_index = 0
    for req in data:
        for key in req.keys():
            if key == req_list[req_list_index]:
                print(req_list_index)
                requisites.append(req.get(req_list[req_list_index]))
                if (req_list_index + 1) < (len(req_list)):
                    req_list_index = req_list_index + 1
    print(requisites)
    org_name = requisites[0]
    org_inn = requisites[1]
    org_kpp = requisites[2]
    org_ogrn = requisites[5]
    org_okpo = requisites[3]
    org_okved = requisites[4]
    org_rs = requisites[19]
    bik = requisites[18]
    bank_name = requisites[20]
    register_name = requisites[6]
    register_date = requisites[7].replace('/', '.')
    ur_adress = re.sub(" +", " ",'{} {} {} {} {}'.format(requisites[8], requisites[9], requisites[10],
                     requisites[11], requisites[12]))
    post_adress = re.sub(" +", " ", '{} {} {} {} {}'.format(requisites[13], requisites[14], requisites[15],
                     requisites[16], requisites[17]))
    participant = ParticipantUl(org_name, org_inn, org_kpp, org_ogrn, org_okpo,
                     org_okved, org_rs, bik, bank_name, register_name, 
                     register_date, ur_adress, post_adress)
    return participant






# TESTING
test = read_xml('D:/FM01_2_3444213503344401001_20180803_0100000001.xml')
operation_info = get_operation_info(test)
recipient_reqs = get_requisites(test, role="Recipient")
debtor_reqs = get_requisites(test, role="Debtor")
payer_reqs = get_requisites(test, role="Payer")

tree = ET.parse('D:/FM01_2_3444213503344401001_20180801_0100000003.xml')
root = tree.getroot()




test1 = []
for tags in root.findall(".//УчастникОп"):
    for tag in tags.getchildren():
        #print(tag.tag)
        if tag.tag != "ТипУчастника" and tag.text != "2":
            if tag.tag == "КодРоли" and tag.text == "02":
                for tag in tags.getchildren():
                    if tag.tag == "СведЮЛ":
                        for i in tag:
                            if i.text != re.match("\\n+\s+", str(i.text)):
                                i.text == ""
                            elif i.text == None:
                                i.text = ""
                            test1.append({tags.tag + i.tag: i.text})
                    if tag.tag == "СведенияКО":
                        for k in tag:
                            if k.text == re.match("\\n+\s+", str(k.text)):
                                k.text = ""
                            elif k.text == None:
                                k.text = ""
                            test1.append({tags.tag + k.tag: k.text})
                    for t in tag.getchildren():
                        if t.tag == "ЮрАдр":
                            for x in t.getchildren():
                                #print(t.tag, x.tag)
                                if x.text == None:
                                    x.text = ""
                                test1.append({t.tag + x.tag: x.text})
                        if t.tag == "ФактАдр":
                            for x in t.getchildren():
                                #print(t.tag, x.tag)
                                if x.text == None:
                                    x.text = ""
                                test1.append({t.tag + x.tag: x.text})
        else:
            for tag in tags.getchildren():
                if tag.tag == "КодРоли" and tag.text == "02":
                    for tag in tags.getchildren():
                        if tag.tag == "СведФЛИП":
                            for n in tag.iter():
                                print(n.tag)
                                if n.text != re.match("\\n+\s+", str(n.text)):
                                    n.text == ""
                                elif n.text == None:
                                    n.text = ""
                                test1.append({tags.tag + n.tag: n.text})
                        if tag.tag == "СведенияКО":
                            for s in tag:
                                if s.text == re.match("\\n+\s+", str(s.text)):
                                    s.text = ""
                                elif s.text == None:
                                    s.text = ""
                                test1.append({tags.tag + s.tag: s.text})





try:
    req_list_ul = ['УчастникОпНаимЮЛ', 'УчастникОпИННЮЛ', 'УчастникОпКППЮЛ', 
                    'УчастникОпОКПОЮЛ', 'УчастникОпОКВЭДЮЛ', 'УчастникОпОГРНЮЛ',
                    'УчастникОпНаименРегОргана', 'УчастникОпДатаРегЮл', 'ЮрАдрПункт',
                    'ЮрАдрУлица', 'ЮрАдрДом', 'ЮрАдрКорп', 'ЮрАдрОф', 'ФактАдрПункт',
                    'ФактАдрУлица', 'ФактАдрДом', 'ФактАдрКорп', 'ФактАдрОф',
                    'УчастникОпБИККО', 'УчастникОпНомерСчета', 'УчастникОпНаимКО']
    requisites = []
    req_list_index = 0
    for req in test1:
        for key in req.keys():
            if key == req_list_ul[req_list_index]:
                print(req_list_index)
                requisites.append(req.get(req_list_ul[req_list_index]))
                if (req_list_index + 1) < (len(req_list_ul)):
                    req_list_index = req_list_index + 1
    print(requisites)
    org_name = requisites[0]
    org_inn = requisites[1]
    org_kpp = requisites[2]
    org_ogrn = requisites[5]
    org_okpo = requisites[3]
    org_okved = requisites[4]
    org_rs = requisites[19]
    bik = requisites[18]
    bank_name = requisites[20]
    register_name = requisites[6]
    register_date = requisites[7].replace('/', '.')
    ur_adress = re.sub(" +", "", '{} {} {} {} {}'.format(requisites[8], requisites[9], requisites[10],
                         requisites[11], requisites[12]))
    post_adress = '{} {} {} {} {}'.format(requisites[13], requisites[14], requisites[15],
                         requisites[16], requisites[17])
except Exception:
    
                            
                            