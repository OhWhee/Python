import xml.etree.ElementTree as ET

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

class Participant():
    
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




def get_requisites(root):
    requisites = []
    for tags in root.findall(".//УчастникОп"):
        for tag in tags.getchildren():
            if tag.tag == "КодРоли" and tag.text == "02":
                for tag in tags.getchildren():
                    if tag.tag == "СведЮЛ":
                        for i in tag.iter():
                            requisites.append(i.text)
                    if tag.tag == "СведенияКО":
                        for k in tag.iter():
                            requisites.append(k.text)
    obj = combine_reqs_to_object(requisites)
    return obj

def combine_reqs_to_object(requisites):
    org_name = requisites[1]
    org_inn = requisites[3]
    org_kpp = requisites[4]
    org_ogrn = requisites[7]
    org_okpo = requisites[5]
    org_okved = requisites[6]
    org_rs = requisites[7]
    bik = requisites[29]
    bank_name = requisites[31]
    register_name = requisites[8]
    register_date = requisites[9].replace('/', '.')
    ur_adress = '{} {} {} {} {}'.format(requisites[14], requisites[15], requisites[16],
                 requisites[17], requisites[18])
    post_adress = '{} {} {} {} {}'.format(requisites[23], requisites[24], requisites[25],
                 requisites[26], requisites[27])
    participant = Participant(org_name, org_inn, org_kpp, org_ogrn, org_okpo,
                 org_okved, org_rs, bik, bank_name, register_name, 
                 register_date, ur_adress, post_adress)
    return participant



# TESTING
test = read_xml('D:/FM01_2_3444213503344401001_20180803_0100000003.xml')
operation_info = get_operation_info(test)
reqs = get_requisites(test)

tree = ET.parse('D:/FM01_2_3444213503344401001_20180803_0100000003.xml')
root = tree.getroot()




test = []
for movie in root.findall(".//УчастникОп"):
    if root.findall(".//КодРоли").iter().getchildren().text == "08":
        #print(movie.getchildren())
        for text in movie.getchildren():
            print(text.text, text.tag)
            if text.text != "\n            ":
                test.append({text.tag: text.text})



test = []
for tags in root.findall(".//УчастникОп"):
    for tag in tags.getchildren():
        if tag.tag == "КодРоли" and tag.text == "02":
            for tag in tags.getchildren():
                if tag.tag == "СведЮЛ":
                    for i in tag.iter():
                        test.append(i.text)
                if tag.tag == "СведенияКО":
                    for k in tag.iter():
                        test.append(k.text)

    
    
    
    
    
    
    
    
    
    
    
    

    