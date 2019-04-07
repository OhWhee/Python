from lxml import etree as ET
import re
import queries
import datetime
import sqlite3

class Requisites():
    
    def __init__(self, org_name=None, type_id=None, area_post=None, area_registration=None, area_residence=None, area_ur=None, birth_date=None, birth_place_area=None, birth_place_country_id=None,
                 birth_place_locality=None, birth_place_okato_subject_id=None, corpus_post=None, corpus_registration=None, corpus_residence=None, corpus_ur=None,
                 country_citizenship_id=None, country_id_post=None, country_id_registration=None, country_id_residence=None, country_id_ur=None, department_number=None,
                 document_date=None, document_given_by=None, document_number=None, document_series=None, document_type=None, first_name=None, house_post=None,
                 house_registration=None, house_residence=None, house_ur=None, inn=None, kpp=None, last_name=None, locality_post=None, locality_registration=None,
                 locality_residence=None, locality_ur=None, middle_name=None, office_post=None, office_registration=None, office_residence=None, office_ur=None,
                 ogrn=None, okato_subject_id_post=None, okato_subject_id_registration=None, okato_subject_id_residence=None, okato_subject_id_ur=None, okpo=None,
                 okved=None, org_id=None, reg_date=None, reg_organization=None, street_post=None, street_registration=None, street_residence=None, street_ur=None, account=None, bik=None, bank_name=None):
        
        self.area_post=area_post
        self.area_registration=area_registration
        self.area_residence=area_residence
        self.area_ur=area_ur
        self.birth_date=birth_date
        self.birth_place_area=birth_place_area
        self.birth_place_country_id=birth_place_country_id
        self.birth_place_locality=birth_place_locality
        self.birth_place_okato_subject_id=birth_place_okato_subject_id
        self.corpus_post=corpus_post 
        self.corpus_registration=corpus_registration 
        self.corpus_residence=corpus_residence 
        self.corpus_ur=corpus_ur
        self.country_citizenship_id=country_citizenship_id
        self.country_id_post=country_id_post 
        self.country_id_registration=country_id_registration 
        self.country_id_residence=country_id_residence 
        self.country_id_ur=country_id_ur
        self.department_number=department_number
        self.document_date=document_date
        self.document_given_by=document_given_by 
        self.document_number=document_number
        self.document_series=document_series
        self.document_type=document_type
        self.first_name=first_name
        self.house_post=house_post
        self.house_registration=house_registration 
        self.house_residence=house_residence
        self.house_ur=house_ur 
        self.inn=inn
        self.kpp=kpp
        self.last_name=last_name
        self.locality_post=locality_post
        self.locality_registration=locality_registration
        self.locality_residence=locality_residence
        self.locality_ur=locality_ur
        self.middle_name=middle_name 
        self.office_post=office_post 
        self.office_registration=office_registration 
        self.office_residence=office_residence 
        self.office_ur=office_ur
        self.ogrn=ogrn 
        self.okato_subject_id_post=okato_subject_id_post 
        self.okato_subject_id_registration=okato_subject_id_registration 
        self.okato_subject_id_residence=okato_subject_id_residence 
        self.okato_subject_id_ur=okato_subject_id_ur 
        self.okpo=okpo
        self.okved=okved 
        self.org_name=org_name
        self.type_id=type_id
        self.org_id=org_id
        self.reg_date=reg_date
        self.reg_organization=reg_organization 
        self.street_post=street_post
        self.street_registration=street_registration
        self.street_residence=street_residence 
        self.street_ur=street_ur
        self.account=account
        self.bik=bik
        self.bank_name=bank_name

    def make_address_for_template_ul_ur(self):
        return '{} {} {} {} {}'.format(self.locality_ur, self.street_ur, self.house_ur, self.corpus_ur, self.office_ur)
    
    def make_address_for_template_ul_post(self):
        return '{} {} {} {} {}'.format(self.locality_post, self.street_post, self.house_post, self.corpus_post, self.office_post)


    def get_operation_info(self, start=None, end=None, last_number_of_operations=None):
        conn = sqlite3.connect('D:\python\FinMon\FinMon.db')
        cur = conn.cursor()   
        query = ""
        if last_number_of_operations != None:
            query = """SELECT * FROM (SELECT * FROM operations ORDER BY operations.operation_id DESC LIMIT ?) 
                                as r ORDER BY r.operation_id"""
            cur.execute(query, (last_number_of_operations,))
        else:
            query = """SELECT * FROM operations WHERE operation_id BETWEEN ? AND ?"""
            cur.execute(query, (start, end,))
        rows = cur.fetchall()
        conn.close()
        for row in rows:
            operation_object = queries.OperationObject(*row[1:14])
            payer_reqs = operation_object.get_requisites_by_type_id(participant=operation_object.payer)
            debtor_reqs = operation_object.get_requisites_by_type_id(participant=operation_object.debtor)
            receiver_reqs = operation_object.get_requisites_by_type_id(participant=operation_object.receiver)
            payer_reqs.status = '01'
            debtor_reqs.status = '08'
            receiver_reqs.status = '02'
            payer_reqs.participant_type = queries.get_participant_id_by_org_id(operation_object.payer)
            debtor_reqs.participant_type = queries.get_participant_id_by_org_id(operation_object.debtor)
            receiver_reqs.participant_type = queries.get_participant_id_by_org_id(operation_object.receiver)
            query_addition = queries.get_operation_info_with_org_names(operation_object.operation_number)
            change_operation_description(query_addition, payer_reqs, receiver_reqs, debtor_reqs)
#            insert_participants(payer_reqs, receiver_reqs, debtor_reqs)
#            print(debtor_reqs.__class__.__name__ == 'ParticipantUL')
            


class ParticipantFL(Requisites):
    
    def __init__(self, org_name, type_id, first_name, middle_name, last_name, inn, country_citizenship_id, birth_date, birth_place_country_id, birth_place_okato_subject_id,
                 birth_place_area, birth_place_locality, document_type, document_series, document_number, document_date, document_given_by, department_number,
                 country_id_registration, okato_subject_id_registration, area_registration, locality_registration, street_registration, house_registration, corpus_registration,
                 office_registration, country_id_residence, okato_subject_id_residence, area_residence, locality_residence, street_residence, house_residence, corpus_residence,
                 office_residence, account, bik, bank_name):
        
        self.org_name = org_name
        self.type_id = type_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.inn = inn
        self.country_citizenship_id = country_citizenship_id
        self.birth_date = birth_date
        self.birth_place_country_id = birth_place_country_id
        self.birth_place_okato_subject_id = birth_place_okato_subject_id
        self.birth_place_area = birth_place_area
        self.birth_place_locality = birth_place_locality
        self.document_type = document_type
        self.document_series = document_series
        self.document_number = document_number
        self.document_date = document_date
        self.document_given_by  = document_given_by
        self.department_number = department_number
        self.country_id_registration = country_id_registration
        self.okato_subject_id_registration  = okato_subject_id_registration
        self.area_registration = area_registration
        self.locality_registration = locality_registration
        self.street_registration = street_registration
        self.house_registration = house_registration
        self.corpus_registration = corpus_registration
        self.office_registration = office_registration
        self.country_id_residence = country_id_residence
        self.okato_subject_id_residence = okato_subject_id_residence
        self.area_residence = area_residence
        self.locality_residence = locality_residence
        self.street_residence  = street_residence
        self.house_residence = house_residence
        self.corpus_residence = corpus_residence
        self.office_residence = office_residence
        self.account = account
        self.bik = bik
        self.bank_name = bank_name
        
        
        
        
class ParticipantIP(Requisites):
    
    def __init__(self, org_name, type_id, first_name, middle_name, last_name, inn, ogrn, reg_organization, reg_date, country_citizenship_id, birth_date, birth_place_country_id, birth_place_okato_subject_id,
                 birth_place_area, birth_place_locality, document_type, document_series, document_number, document_date, document_given_by, department_number,
                 country_id_registration, okato_subject_id_registration, area_registration, locality_registration, street_registration, house_registration, corpus_registration,
                 office_registration, country_id_residence, okato_subject_id_residence, area_residence, locality_residence, street_residence, house_residence, corpus_residence,
                 office_residence, account, bik, bank_name):
        
        self.org_name = org_name
        self.type_id = type_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.inn = inn
        self.ogrn = ogrn
        self.reg_organization = reg_organization
        self.reg_date = reg_date
        self.country_citizenship_id = country_citizenship_id
        self.birth_date = birth_date
        self.birth_place_country_id = birth_place_country_id
        self.birth_place_okato_subject_id = birth_place_okato_subject_id
        self.birth_place_area = birth_place_area
        self.birth_place_locality = birth_place_locality
        self.document_type = document_type
        self.document_series = document_series
        self.document_number = document_number
        self.document_date = document_date
        self.document_given_by  = document_given_by
        self.department_number = department_number
        self.country_id_registration = country_id_registration
        self.okato_subject_id_registration  = okato_subject_id_registration
        self.area_registration = area_registration
        self.locality_registration = locality_registration
        self.street_registration = street_registration
        self.house_registration = house_registration
        self.corpus_registration = corpus_registration
        self.office_registration = office_registration
        self.country_id_residence = country_id_residence
        self.okato_subject_id_residence = okato_subject_id_residence
        self.area_residence = area_residence
        self.locality_residence = locality_residence
        self.street_residence  = street_residence
        self.house_residence = house_residence
        self.corpus_residence = corpus_residence
        self.office_residence = office_residence
        self.account = account
        self.bik = bik
        self.bank_name = bank_name
        
        
        
class ParticipantUL(Requisites):
    
    def __init__(self, org_name, type_id, inn, kpp, okpo, okved,  ogrn, reg_organization, reg_date, country_id_ur, okato_subject_id_ur, area_ur, locality_ur, street_ur, house_ur,
                 corpus_ur, office_ur, country_id_post, okato_subject_id_post, area_post, locality_post, street_post, house_post, corpus_post, office_post, account, bik, bank_name):
        
        self.org_name = org_name
        self.type_id = type_id
        self.inn = inn
        self.kpp = kpp
        self.okpo = okpo
        self.okved = okved
        self.ogrn = ogrn
        self.reg_organization = reg_organization
        self.reg_date = reg_date
        self.country_id_ur = country_id_ur
        self.okato_subject_id_ur = okato_subject_id_ur
        self.area_ur = area_ur
        self.locality_ur = locality_ur
        self.street_ur = street_ur
        self.house_ur = house_ur
        self.corpus_ur = corpus_ur
        self.office_ur = office_ur
        self.country_id_post = country_id_post
        self.okato_subject_id_post = okato_subject_id_post
        self.area_post = area_post
        self.locality_post = locality_post
        self.street_post = street_post
        self.house_post = house_post
        self.corpus_post = corpus_post
        self.office_post = office_post
        self.account = account
        self.bik = bik
        self.bank_name = bank_name
        
#        super().__init__(org_name, type_id, inn, kpp, okpo, okved, ogrn, reg_organization, reg_date, country_id_ur, okato_subject_id_ur, area_ur, locality_ur, street_ur, house_ur,
#                 corpus_ur, office_ur, country_id_post, okato_subject_id_post, area_post, locality_post, street_post, house_post, corpus_post, office_post, account, bik, bank_name)             
class ToXML():
    
    def __init__(self, participant):
        pass
    pass

def change_operation_description(query_addition, *args):   
    print("вызывали?")
    testfile = r'D:\python\FinMon\test.xml'  
    operation_object = queries.OperationObject(*query_addition[1:14])
    old_date = datetime.datetime.strptime(operation_object.detection_date, '%d.%m.%Y')
    new_date = old_date.strftime('%Y%m%d')  
    operation_description = """<Операция>
          <НомерЗаписи>{}</НомерЗаписи>
          <ТипЗаписи>1</ТипЗаписи>
          <ПризнФТр>0</ПризнФТр>
          <ДатаОперации>{}</ДатаОперации>
          <ДатаВыявления>{}</ДатаВыявления>
          <КодОперации>6001</КодОперации>
          <ПризнНеобОперации>1194</ПризнНеобОперации>
          <КодВал>643</КодВал>
          <СумОперации>{}</СумОперации>
          <СумРуб>{}</СумРуб>
          <ОснованиеОп>
            <КодДок>32</КодДок>
            <ДатаДок>{}</ДатаДок>
            <НомДок>{}</НомДок>
            <СодДок>{}</СодДок>
          </ОснованиеОп>
          <НазнПлатеж>{}</НазнПлатеж>
          <КодПризнОперации>0</КодПризнОперации>
          <КодДенежСредств>2</КодДенежСредств>
          <ХарактерОп>{}</ХарактерОп>
          <Коммент>{}</Коммент>
          </Операция>""".format(operation_object.operation_number, str(operation_object.operation_date).replace(".", "/"), str(operation_object.detection_date).replace(".", "/"),
          operation_object.amount, operation_object.amount, str(query_addition[14]).replace(".", "/"), operation_object.contract, query_addition[15], operation_object.payment_purpose,
          operation_object.payment_purpose, operation_object.payment_number)   
      
    xmlfile = ET.parse(testfile)
    root = xmlfile.getroot()
    root.find('.//ДатаСообщения').text = str(operation_object.detection_date).replace(".", "/")
    starting_tag = root.find('.//ИнфЛицо')
    root_to_add = ET.fromstring(operation_description, parser=ET.XMLParser(encoding='utf-8'))
    starting_tag.addnext(root_to_add)
              
#    args = tuple(args) 
    reqs = ''
#    payer_reqs, receiver_reqs, debtor_reqs 
    starting_tag = root.find('.//Коммент')
    
    for arg in args:
        if arg.__class__.__name__ == 'ParticipantUL':
            reqs = """
                      <УчастникОп>
                        <КодРоли>{}</КодРоли>
                        <КодУчастника>{}</КодУчастника>
                        <ТипУчастника>1</ТипУчастника>
                        <ПризнУчастника>1</ПризнУчастника>
                        <Клиент>0</Клиент>
                        <ПризнакИдентификации>0</ПризнакИдентификации>
                        <СведЮЛ>
                          <НаимЮЛ>{}</НаимЮЛ>
                          <ИННЮЛ>{}</ИННЮЛ>
                          <КППЮЛ>{}</КППЮЛ>
                          <ОКПОЮЛ>{}</ОКПОЮЛ>
                          <ОКВЭДЮЛ>{}</ОКВЭДЮЛ>
                          <ОГРНЮЛ>{}</ОГРНЮЛ>
                          <НаименРегОргана>{}</НаименРегОргана>
                          <ДатаРегЮл>{}</ДатаРегЮл>
                          <ЮрАдр>
                            <КодОКСМ>{}</КодОКСМ>
                            <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                            <Район>{}</Район>
                            <Пункт>{}</Пункт>
                            <Улица>{}</Улица>
                            <Дом>{}</Дом>
                            <Корп>{}</Корп>
                            <Оф>{}</Оф>
                          </ЮрАдр>
                          <ФактАдр>
                            <КодОКСМ>{}</КодОКСМ>
                            <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                            <Район>{}</Район>
                            <Пункт>{}</Пункт>
                            <Улица>{}</Улица>
                            <Дом>{}</Дом>
                            <Корп>{}</Корп>
                            <Оф>{}</Оф>
                          </ФактАдр>
                        </СведЮЛ>
                        <СведенияКО>
                          <БИККО>{}</БИККО>
                          <НомерСчета>{}</НомерСчета>
                          <НаимКО>{}</НаимКО>
                        </СведенияКО>
                      </УчастникОп>""".format(arg.status, arg.participant_type, arg.org_name, arg.inn, arg.kpp, arg.okpo, arg.okved, arg.ogrn, arg.reg_organization, 
                      str(arg.reg_date).replace(".", "/"), arg.country_id_ur, arg.okato_subject_id_ur, arg.area_ur, arg.locality_ur, arg.street_ur, arg.house_ur,
                      arg.corpus_ur, arg.office_ur, arg.country_id_post, arg.okato_subject_id_post, arg.area_post, arg.locality_post,
                      arg.street_post, arg.house_post, arg.corpus_post, arg.office_post, arg.bik, arg.account, arg.bank_name).replace("None", "")

                      
        if arg.__class__.__name__ == 'ParticipantFL':
            reqs = """<УчастникОп>
                    <КодРоли>{}</КодРоли>
                    <КодУчастника>{}</КодУчастника>
                    <ТипУчастника>2</ТипУчастника>
                    <ПризнУчастника>1</ПризнУчастника>
                    <Клиент>0</Клиент>
                    <ПризнакИдентификации>0</ПризнакИдентификации>
                    <СведФЛИП>
                      <ФИОФЛИП>
                        <Фам>{}</Фам>
                        <Имя>{}</Имя>
                        <Отч>{}</Отч>
                      </ФИОФЛИП>
                      <ИННФЛИП>{}</ИННФЛИП>
                      <СведДокУдЛичн>
                        <ВидДокКод>21</ВидДокКод>
                        <СерияДок>{}</СерияДок>
                        <НомДок>{}</НомДок>
                        <ДатВыдачиДок>{}</ДатВыдачиДок>
                        <КемВыданДок>{}</КемВыданДок>
                        <КодПодр>{}</КодПодр>
                      </СведДокУдЛичн>
                      <ДатаРождения>{}</ДатаРождения>
                      <МестоРожд>
                        <КодОКСМ>{}</КодОКСМ>
                        <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                        <Район>{}</Район>
                      </МестоРожд>
                      <КодОКСМ>{}</КодОКСМ>
                      <ПризнакПубЛицо>0</ПризнакПубЛицо>
                      <АдрРег>
                        <КодОКСМ>{}</КодОКСМ>
                        <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                        <Район>{}</Район>
                        <Пункт>{}</Пункт>
                        <Улица>{}</Улица>
                        <Дом>{}</Дом>
                        <Корп>{}</Корп>
                        <Оф>{}</Оф>
                      </АдрРег>
                      <АдрПреб>
                        <КодОКСМ>{}</КодОКСМ>
                        <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                        <Район>{}</Район>
                        <Пункт>{}</Пункт>
                        <Улица>{}</Улица>
                        <Дом>{}</Дом>
                        <Корп>{}</Корп>
                        <Оф>{}</Оф>
                      </АдрПреб>
                    </СведФЛИП>
                    <СведенияКО>
                      <БИККО>{}</БИККО>
                      <НомерСчета>{}</НомерСчета>
                      <НаимКО>{}</НаимКО>
                    </СведенияКО>
                  </УчастникОп>""".format(arg.status,
                  arg.participant_type,
                  arg.first_name,
                  arg.middle_name,
                  arg.last_name, 
                  arg.inn,
                  arg.document_series, 
                  arg.document_number,
                  str(arg.document_date).replace(".", "/"),
                  arg.document_given_by,
                  arg.department_number, 
                  str(arg.birth_date).replace(".", "/"),
                  arg.birth_place_country_id,
                  arg.birth_place_okato_subject_id,
                  arg.birth_place_area,
                  arg.country_citizenship_id, 
                  arg.country_id_registration,
                  arg.okato_subject_id_registration,
                  arg.area_registration, 
                  arg.locality_registration,
                  arg.street_registration,
                  arg.house_registration, 
                  arg.corpus_registration, 
                  arg.office_registration, 
                  arg.country_id_residence, 
                  arg.okato_subject_id_residence,
                  arg.area_residence, 
                  arg.locality_residence,
                  arg.house_residence, 
                  arg.street_residence,
                  arg.corpus_residence, 
                  arg.office_residence, 
                  arg.bik,
                  arg.account, 
                  arg.bank_name).replace("None", "")
        
        if arg.__class__.__name__ == 'ParticipantIP':  
            reqs = """<УчастникОп>
            <КодРоли>{}</КодРоли>
            <КодУчастника>{}</КодУчастника>
            <ТипУчастника>3</ТипУчастника>
            <ПризнУчастника>1</ПризнУчастника>
            <Клиент>1</Клиент>
            <ПризнакИдентификации>0</ПризнакИдентификации>
            <СведФЛИП>
              <ФИОФЛИП>
                <Фам>{}</Фам>
                <Имя>{}</Имя>
                <Отч>{}</Отч>
              </ФИОФЛИП>
              <ИННФЛИП>{}</ИННФЛИП>
              <ОКВЭДФЛИП>{}</ОКВЭДФЛИП>
              <ОГРНФЛИП>{}</ОГРНФЛИП>
              <НаименРегОргана>{}</НаименРегОргана>
              <ДатаРегИП>{}</ДатаРегИП>
              <СведДокУдЛичн>
                <ВидДокКод>21</ВидДокКод>
                <СерияДок>{}</СерияДок>
                <НомДок>{}</НомДок>
                <ДатВыдачиДок>{}</ДатВыдачиДок>
                <КемВыданДок>{}</КемВыданДок>
                <КодПодр>{}</КодПодр>
              </СведДокУдЛичн>
              <ДатаРождения>{}</ДатаРождения>
              <МестоРожд>
                <КодОКСМ>{}</КодОКСМ>
                <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                <Район>{}</Район>
                <Пункт>{}</Пункт>
              </МестоРожд>
              <КодОКСМ>{}</КодОКСМ>
              <ПризнакПубЛицо>0</ПризнакПубЛицо>
              <АдрРег>
                <КодОКСМ>{}</КодОКСМ>
                <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                <Район>{}</Район>
                <Пункт>{}</Пункт>
                <Улица>{}</Улица>
                <Дом>{}</Дом>
                <Корп>{}</Корп>
                <Оф>{}</Оф>
              </АдрРег>
              <АдрПреб>
                <КодОКСМ>{}</КодОКСМ>
                <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                <Район>{}</Район>
                <Пункт>{}</Пункт>
                <Улица>{}</Улица>
                <Дом>{}</Дом>
                <Корп>{}</Корп>
                <Оф>{}</Оф>
              </АдрПреб>
            </СведФЛИП>
            <СведенияКО>
              <БИККО>{}</БИККО>
              <НомерСчета>{}</НомерСчета>
              <НаимКО>{}</НаимКО>
            </СведенияКО>
          </УчастникОп>""".format(arg.status, arg.participant_type, arg.first_name, arg.middle_name, arg.last_name, arg.inn, arg.okved, arg.ogrn, arg.reg_organization, str(arg.reg_date).replace(".", "/"),
          arg.document_series, arg.document_number, str(arg.document_date).replace(".", "/"), arg.department_number, str(arg.birth_date).replace(".", "/"), arg.birth_place_country_id, arg.birth_place_okato_subject_id, arg.birth_place_area, arg.birth_place_locality, 
          arg.country_citizenship_id, arg.country_id_registration,
          arg.okato_subject_id_registration, arg.area_registration, arg.locality_registration, arg.street_registration, arg.house_registration, arg.corpus_registration,
          arg.office_registration, arg.country_id_residence, arg.okato_subject_id_residence, arg.area_residence, arg.locality_residence, arg.street_residence,
          arg.house_residence, arg.corpus_residence, arg.office_residence, arg.bik, arg.account, arg.bank_name).replace("None", "")
          
        root_to_add = ET.fromstring(reqs)
        starting_tag.addnext(root_to_add)
        starting_tag = root.find('.//УчастникОп')      
          
#    return xmlfile.write_c14n(r'D:\python\FinMon\{}.xml'.format(operation_object.make_filename(new_date)))
      
    return xmlfile.write(r'D:\RFM\xml monitoring\{}.xml'.format(operation_object.make_filename(new_date)), method="c14n",  pretty_print=False)




 

def insert_participants(*args):
    args = tuple(args)
    testfile = r'D:\python\FinMon\test2.xml'
    xmlfile = ET.parse(testfile)
    root = xmlfile.getroot() 
    reqs = ''
#    payer_reqs, receiver_reqs, debtor_reqs 
    starting_tag = root.find('.//Коммент')
    
    for arg in args:
        if arg.__class__.__name__ == 'ParticipantUL':
            reqs = """
                      <УчастникОп>
                        <КодРоли>{}</КодРоли>
                        <КодУчастника></КодУчастника>
                        <ТипУчастника>1</ТипУчастника>
                        <ПризнУчастника>1</ПризнУчастника>
                        <Клиент>0</Клиент>
                        <ПризнакИдентификации>0</ПризнакИдентификации>
                        <СведЮЛ>
                          <НаимЮЛ>{}</НаимЮЛ>
                          <КодЛица></КодЛица>
                          <ИННЮЛ>{}</ИННЮЛ>
                          <КППЮЛ>{}</КППЮЛ>
                          <ОКПОЮЛ>{}</ОКПОЮЛ>
                          <ОКВЭДЮЛ>{}</ОКВЭДЮЛ>
                          <ОГРНЮЛ>{}</ОГРНЮЛ>
                          <НаименРегОргана>{}</НаименРегОргана>
                          <ДатаРегЮл>{}</ДатаРегЮл>
                          <ЮрАдр>
                            <КодОКСМ>{}</КодОКСМ>
                            <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                            <Район>{}</Район>
                            <Пункт>{}</Пункт>
                            <Улица>{}</Улица>
                            <Дом>{}</Дом>
                            <Корп>{}</Корп>
                            <Оф>{}</Оф>
                          </ЮрАдр>
                          <ФактАдр>
                            <КодОКСМ>{}</КодОКСМ>
                            <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                            <Район>{}</Район>
                            <Пункт>{}</Пункт>
                            <Улица>{}</Улица>
                            <Дом>{}</Дом>
                            <Корп>{}</Корп>
                            <Оф>{}</Оф>
                          </ФактАдр>
                        </СведЮЛ>
                        <СведенияКО>
                          <БИККО>{}</БИККО>
                          <НомерСчета>{}</НомерСчета>
                          <НаимКО>{}</НаимКО>
                        </СведенияКО>
                      </УчастникОп>""".format(arg.status, arg.org_name, arg.inn, arg.kpp, arg.okpo, arg.okved, arg.ogrn, arg.reg_organization, 
                      str(arg.reg_date).replace(".", "/"), arg.country_id_ur, arg.okato_subject_id_ur, arg.area_ur, arg.locality_ur, arg.street_ur, arg.house_ur,
                      arg.corpus_ur, arg.office_ur, arg.country_id_post, arg.okato_subject_id_post, arg.area_post, arg.locality_post,
                      arg.street_post, arg.house_post, arg.corpus_post, arg.office_post, arg.bik, arg.account, arg.bank_name).replace({'None':' ', '':' '})
            print(reqs)
                      
        if arg.__class__.__name__ == 'ParticipantFL':
            reqs = """<УчастникОп>
                    <КодРоли>{}</КодРоли>
                    <КодУчастника></КодУчастника>
                    <ТипУчастника>2</ТипУчастника>
                    <ПризнУчастника>1</ПризнУчастника>
                    <Клиент>0</Клиент>
                    <ПризнакИдентификации>0</ПризнакИдентификации>
                    <СведФЛИП>
                      <ФИОФЛИП>
                        <Фам>{}</Фам>
                        <Имя>{}</Имя>
                        <Отч>{}</Отч>
                      </ФИОФЛИП>
                      <ИННФЛИП>{}</ИННФЛИП>
                      <СведДокУдЛичн>
                        <ВидДокКод>21</ВидДокКод>
                        <СерияДок>{}</СерияДок>
                        <НомДок>{}</НомДок>
                        <ДатВыдачиДок>{}</ДатВыдачиДок>
                        <КемВыданДок>{}</КемВыданДок>
                        <КодПодр>{}</КодПодр>
                      </СведДокУдЛичн>
                      <ДатаРождения>{}</ДатаРождения>
                      <МестоРожд>
                        <КодОКСМ>{}</КодОКСМ>
                        <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                        <Район>{}</Район>
                      </МестоРожд>
                      <КодОКСМ>{}</КодОКСМ>
                      <ПризнакПубЛицо>0</ПризнакПубЛицо>
                      <АдрРег>
                        <КодОКСМ>{}</КодОКСМ>
                        <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                        <Район>{}</Район>
                        <Пункт>{}</Пункт>
                        <Улица>{}</Улица>
                        <Дом>{}</Дом>
                        <Корп>{}</Корп>
                        <Оф>{}</Оф>
                      </АдрРег>
                      <АдрПреб>
                        <КодОКСМ>{}</КодОКСМ>
                        <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                        <Район>{}</Район>
                        <Пункт>{}</Пункт>
                        <Улица>{}</Улица>
                        <Дом>{}</Дом>
                        <Корп>{}</Корп>
                        <Оф>{}</Оф>
                      </АдрПреб>
                    </СведФЛИП>
                    <СведенияКО>
                      <БИККО>{}</БИККО>
                      <НомерСчета>{}</НомерСчета>
                      <НаимКО>{}</НаимКО>
                    </СведенияКО>
                  </УчастникОп>""".format(arg.status, arg.first_name, arg.middle_name, arg.last_name, arg.inn, arg.document_series, arg.document_number,
                  str(arg.document_date).replace(".", "/"), arg.document_given_by, arg.department_number, str(arg.birth_date).replace(".", "/"), arg.birth_place_country_id, arg.birth_place_okato_subject_id,
                  arg.birth_place_area, arg.country_id_registration, arg.okato_subject_id_registration, arg.area_registration, arg.locality_registration,
                  arg.street_registration, arg.house_registration, arg.corpus_registration, arg.office_registration, arg.country_id_residence, arg.okato_subject_id_residence,
                  arg.area_residence, arg.locality_residence, arg.house_residence, arg.corpus_residence, arg.office_residence, arg.bik, arg.account, arg.bank_name).replace({'None':' ', '':' '})
        
        if arg.__class__.__name__ == 'ParticipantIP':  
            reqs = """<УчастникОп>
            <КодРоли>{}</КодРоли>
            <КодУчастника></КодУчастника>
            <ТипУчастника>3</ТипУчастника>
            <ПризнУчастника>1</ПризнУчастника>
            <Клиент>1</Клиент>
            <ПризнакИдентификации>0</ПризнакИдентификации>
            <СведФЛИП>
              <ФИОФЛИП>
                <Фам>{}</Фам>
                <Имя>{}</Имя>
                <Отч>{}</Отч>
              </ФИОФЛИП>
              <КодЛица></КодЛица>
              <ИННФЛИП>{}</ИННФЛИП>
              <ОКВЭДФЛИП>{}</ОКВЭДФЛИП>
              <ОГРНФЛИП>{}</ОГРНФЛИП>
              <НаименРегОргана>{}</НаименРегОргана>
              <ДатаРегИП>{}</ДатаРегИП>
              <СведДокУдЛичн>
                <ВидДокКод>21</ВидДокКод>
                <СерияДок>{}</СерияДок>
                <НомДок>{}</НомДок>
                <ДатВыдачиДок>{}</ДатВыдачиДок>
                <КемВыданДок>{}</КемВыданДок>
                <КодПодр>{}</КодПодр>
              </СведДокУдЛичн>
              <ДатаРождения>{}</ДатаРождения>
              <МестоРожд>
                <КодОКСМ>{}</КодОКСМ>
                <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                <Район>{}</Район>
                <Пункт>{}</Пункт>
              </МестоРожд>
              <КодОКСМ>{}</КодОКСМ>
              <ПризнакПубЛицо>0</ПризнакПубЛицо>
              <АдрРег>
                <КодОКСМ>{}</КодОКСМ>
                <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                <Район>{}</Район>
                <Пункт>{}</Пункт>
                <Улица>{}</Улица>
                <Дом>{}</Дом>
                <Корп>{}</Корп>
                <Оф>{}</Оф>
              </АдрРег>
              <АдрПреб>
                <КодОКСМ>{}</КодОКСМ>
                <КодСубъектаПоОКАТО>{}</КодСубъектаПоОКАТО>
                <Район>{}</Район>
                <Пункт>{}</Пункт>
                <Улица>{}</Улица>
                <Дом>{}</Дом>
                <Корп>{}</Корп>
                <Оф>{}</Оф>
              </АдрПреб>
            </СведФЛИП>
            <СведенияКО>
              <БИККО>{}</БИККО>
              <НомерСчета>{}</НомерСчета>
              <НаимКО>{}</НаимКО>
            </СведенияКО>
          </УчастникОп>""".format(arg.status, arg.first_name, arg.middle_name, arg.last_name, arg.inn, arg.okved, arg.ogrn, arg.reg_organization, str(arg.reg_date).replace(".", "/"),
          arg.document_series, arg.document_number, str(arg.document_date).replace(".", "/"), arg.department_number, str(arg.birth_date).replace(".", "/"), arg.birth_place_country_id, arg.country_id_registration,
          arg.okato_subject_id_registration, arg.area_registration, arg.locality_registration, arg.street_registration, arg.house_registration, arg.corpus_registration,
          arg.office_registration, arg.country_id_residence, arg.okato_subject_id_residence, arg.area_residence, arg.locality_residence, arg.street_residence,
          arg.house_residence, arg.corpus_residence, arg.office_residence, arg.bik, arg.account, arg.bank_name).replace({'None':' ', '':' '})
          
        root_to_add = ET.fromstring(reqs)
        starting_tag.addnext(root_to_add)
        starting_tag = root.find('.//УчастникОп')
    
    return xmlfile.write(r'D:\python\FinMon\tttttt.xml', encoding='UTF-8', xml_declaration=True)
    




def read_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return root

def get_tree(path):
    tree = ET.parse(path)
    return tree