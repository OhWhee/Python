from lxml import etree as ET

def read_xml(path):
    """Возваращает объект типа xml.etree.ElementTree"""
    #ET.register_namespace("", 'urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1')
    ET.register_namespace('smev', 'urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1')
    ET.register_namespace('num', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/numbers/1.0')
    ET.register_namespace('adrs', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1')
    ET.register_namespace('spa', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/5.0.1')
    ET.register_namespace('param', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/parameters-oks/2.0.1')
    ET.register_namespace('cer', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0')
    ET.register_namespace('doc', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/document-output/4.0.1')
    ET.register_namespace('flat', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/assignation-flat/1.0.1')
    ET.register_namespace('ch', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/cultural-heritage/2.0.1')
    tree = ET.parse(path)
    root = tree.getroot()
    return root


root = read_xml(r'D:\EGRN_date_changer\б-р. Комарова, д. 20, кв. 59 (2).xml')

def get_address(root):
    street = ""
    street_type = ""
    house_type = ""
    house_number = ""
    flat_type = ""
    flat_number = ""
     
    for t in root.findall('.//{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}Address'):
        for i in t.getchildren():
            if i.tag == "{urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1}Street":
                street, street_type = i.attrib["Name"], i.attrib["Type"]
            if i.tag == "{urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1}Level1":
                house_type, house_number = i.attrib["Type"], i.attrib["Value"]
            if i.tag == "{urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1}Apartment":
                flat_type, flat_number = i.attrib["Type"], i.attrib["Value"]
        return r'{}. {}, {}. {}, {}. {}'.format(street_type, street, house_type, house_number, flat_type, flat_number)
 
get_address(root)

def replaceDate(root, date):
    for t in root.findall(".//{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}ReestrExtract"):
        for i in t.getchildren():
            if i.tag == '{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}DeclarAttribute':
                print(i.attrib['ExtractDate'], i.attrib['RequeryDate'])
                i.attrib['ExtractDate'] = date
                i.attrib['RequeryDate'] = date
                print(i.attrib['ExtractDate'], i.attrib['RequeryDate'])
    for t in root.findall(".//{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}HeadContent"):
            for i in t.getchildren():
                if i.tag == '{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}Content':
                    i.text = 'На основании запроса от {} г., поступившего на рассмотрение {} г., сообщаем, что согласно записям Единого государственного реестра недвижимости:'.format(date, date)
    

addr = 'D:/EGRN_date_changer/б-р. Комарова, д. 20, кв. 59 (2).xml'
date = '15.12.2018'

def getInfo(addr, date):
    ET.register_namespace('smev', 'urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1')
    ET.register_namespace('num', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/numbers/1.0')
    ET.register_namespace('adrs', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1')
    ET.register_namespace('spa', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/5.0.1')
    ET.register_namespace('param', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/parameters-oks/2.0.1')
    ET.register_namespace('cer', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0')
    ET.register_namespace('doc', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/document-output/4.0.1')
    ET.register_namespace('flat', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/assignation-flat/1.0.1')
    ET.register_namespace('ch', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/cultural-heritage/2.0.1')
    tree = ET.parse(addr)
    root = tree.getroot()
    replaceDate(root, date)
    tree.write(addr, encoding='UTF-8', xml_declaration=True)
    
getInfo(addr, date)
replaceDate(root, '15.12.2018')
