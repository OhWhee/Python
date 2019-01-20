from PyQt5 import QtCore, QtGui, QtWidgets
from lxml import etree as ET
import csv
import datetime
import os
import math


class Ui_Dialog(object):
    now = datetime.datetime.now()
    files = []
    initial_step = 0
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(485, 198)
       # self.OpenString = QtWidgets.QLineEdit(Dialog)
       # self.OpenString.setGeometry(QtCore.QRect(120, 50, 351, 20))
       # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
       # sizePolicy.setHorizontalStretch(0)
       # sizePolicy.setVerticalStretch(0)
       # sizePolicy.setHeightForWidth(self.OpenString.sizePolicy().hasHeightForWidth())
       # self.OpenString.setSizePolicy(sizePolicy)
       # self.OpenString.setText("")
       # self.OpenString.setObjectName("OpenString")
        self.SaveString = QtWidgets.QLineEdit(Dialog)
        self.SaveString.setGeometry(QtCore.QRect(120, 40, 351, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SaveString.sizePolicy().hasHeightForWidth())
        self.SaveString.setSizePolicy(sizePolicy)
        self.SaveString.setObjectName("SaveString")
        self.OpenBtn = QtWidgets.QPushButton(Dialog)
        self.OpenBtn.setGeometry(QtCore.QRect(10, 10, 75, 20))
        self.OpenBtn.clicked.connect(self.openButton)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OpenBtn.sizePolicy().hasHeightForWidth())
        self.OpenBtn.setSizePolicy(sizePolicy)
        self.OpenBtn.setObjectName("OpenBtn")
        self.SaveBtn = QtWidgets.QPushButton(Dialog)
        self.SaveBtn.setGeometry(QtCore.QRect(10, 40, 75, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SaveBtn.sizePolicy().hasHeightForWidth())
        self.SaveBtn.setSizePolicy(sizePolicy)
        self.SaveBtn.setObjectName("SaveBtn")
        self.SaveBtn.clicked.connect(self.saveButton)
        self.DateString = QtWidgets.QLineEdit(Dialog)
        self.DateString.setGeometry(QtCore.QRect(10, 70, 75, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DateString.sizePolicy().hasHeightForWidth())
        self.DateString.setSizePolicy(sizePolicy)
        self.DateString.setObjectName("DateString")
        self.ResultBtn = QtWidgets.QPushButton(Dialog)
        self.ResultBtn.setGeometry(QtCore.QRect(120, 70, 173, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResultBtn.sizePolicy().hasHeightForWidth())
        self.ResultBtn.setSizePolicy(sizePolicy)
        self.ResultBtn.setObjectName("ResultBtn")
        self.ResultBtn.clicked.connect(self.changeDateButton)
        self.OwnersBtn = QtWidgets.QPushButton(Dialog)
        self.OwnersBtn.setGeometry(QtCore.QRect(300, 70, 173, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OwnersBtn.sizePolicy().hasHeightForWidth())
        self.OwnersBtn.setSizePolicy(sizePolicy)
        self.OwnersBtn.setObjectName("OwnersBtn")
        self.OwnersBtn.clicked.connect(self.saveToCSV)
        self.ChangeBtn = QtWidgets.QPushButton(Dialog)
        self.ChangeBtn.setGeometry(QtCore.QRect(300, 100, 173, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ChangeBtn.sizePolicy().hasHeightForWidth())
        self.ChangeBtn.setSizePolicy(sizePolicy)
        self.ChangeBtn.setObjectName("ChangeBtn")
        self.ChangeBtn.clicked.connect(self.changeFileNames)
        self.ProgressBar = QtWidgets.QProgressBar(Dialog)
        self.ProgressBar.setSizePolicy(sizePolicy)
        self.ProgressBar.setGeometry(QtCore.QRect(10, 150, 450, 20))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Изменятор дат"))
        self.OpenBtn.setText(_translate("Dialog", "Открыть"))
        self.SaveBtn.setText(_translate("Dialog", "Сохранить"))
        self.ResultBtn.setText(_translate("Dialog", "Изменить дату"))
        self.OwnersBtn.setText(_translate("Dialog", "Выгрузить собственников"))
        self.ChangeBtn.setText(_translate("Dialog", "Переименовать файлы"))
        
    def read_xml(path):
        """Возваращает объект типа xml.etree.ElementTree"""
        tree = ET.parse(path)
        root = tree.getroot()
        return root
               
        
    def openButton(self):
        self.ProgressBar.setValue(0)
        self.files = []
        self.now = datetime.datetime.now()
        filenames = QtWidgets.QFileDialog.getOpenFileNames(None, filter = "XML (*.xml)")
        for file in filenames[0]:
            self.files.append(file)
            
    def saveButton(self):
        self.SaveString.setText(QtWidgets.QFileDialog.getExistingDirectory())
        
    def changeDateButton(self):
        new_counter = 1
        file_counter = len(self.files)
        step = 100 / file_counter
        for file in self.files:
            print('Обрабатываемый файл: '+str(file))
            try:
                obj = OwnerList(file)
            except:
                print('Беда с файлом: '+str(file))
            try:    
                tree = obj.tree
                obj.replaceDate(obj.root, self.DateString.text())
                tree.write(str(file), encoding='UTF-8', xml_declaration=True)
                #obj.saveFile(str(file))
            except:
                print("Беда с тегами в файле: "+str(file))            
            print('Обработано файлов: '+ str(new_counter) + '/'+str(file_counter))
            new_counter+=1
            self.initial_step += step
            self.ProgressBar.setValue(math.ceil(self.initial_step))
        return print("Все файлы обработаны")
    
    def changeFileNames(self):
        new_counter = 1
        file_counter = len(self.files)
        step = 100 / file_counter
        for file in self.files:
            print('Обрабатываемый файл: '+str(file))
            try:
                obj = OwnerList(file)
                if not os.path.exists('{}/{}'.format(self.SaveString.text(), obj.folderName)):
                    os.mkdir('{}/{}'.format(self.SaveString.text(), obj.folderName))
                else:
                    save_string = '{}/{}/{}'.format(self.SaveString.text(), obj.folderName, obj.address.replace("/", "-"))
                    tree = obj.tree
                    print(save_string)
                    filenumber = ""
                    index = 1
                    new_string = ''
                    while os.path.exists(save_string + "{}.xml".format(filenumber)):
                        filenumber = ' ({})'.format(index)
                        index += 1               
                        print(new_string)
                    new_string = save_string + '{}.xml'.format(filenumber)
                    tree.write(new_string, encoding='UTF-8', xml_declaration=True)
                    print('Обработано файлов: '+ str(new_counter) + '/'+str(file_counter))
                    new_counter+=1
            except:
                print("Возможно ошибка в тэегах. Файл {} не обработан".format(str(file)))
            self.initial_step += step
            self.ProgressBar.setValue(math.ceil(self.initial_step))
            print(self.initial_step, step)
        return print("Все файлы обработаны")    
    
    def saveToCSV(self):
        new_counter = 1
        file_counter = len(self.files)
        step = 100 / file_counter
        save_string = '{}/{}.csv'.format(self.SaveString.text(), self.now.strftime('%d.%m.%Y %H-%M-%S'))
        for file in self.files:
            try:
                obj = OwnerList(file)
                string_to_csv = []
                string_to_csv.append(obj.address)
            except:
                print('Беда с файлом: '+str(file))
            for string in obj.owners:
                string_to_csv.append(string)
            with open(save_string, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow(string_to_csv) 
            new_counter += 1
            self.initial_step += step
            self.ProgressBar.setValue(math.ceil(self.initial_step))
      
        
class OwnerList:
    
    savePath = r'D:\EGRN_date_changer\test.csv'
    
    def __init__(self, path):
        self.path = path
        self.root = self.read_xml(self.path)
        self.address = self.get_address(self.root)
        self.owners = self.get_owners(self.root)
        self.tree = self.get_tree(self.path)
        self.folderName = self.make_folder(self.root)
        
            
    def read_xml(self, path):
        """Возваращает объект типа xml.etree.ElementTree"""
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
    
    def get_tree(self, path):
        ET.register_namespace('smev', 'urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1')
        ET.register_namespace('num', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/numbers/1.0')
        ET.register_namespace('adrs', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1')
        ET.register_namespace('spa', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/5.0.1')
        ET.register_namespace('param', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/parameters-oks/2.0.1')
        ET.register_namespace('cer', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0')
        ET.register_namespace('doc', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/document-output/4.0.1')
        ET.register_namespace('flat', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/assignation-flat/1.0.1')
        ET.register_namespace('ch', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/cultural-heritage/2.0.1')
        tree = ET.ElementTree(self.root)
        return tree


    def get_address(self, root):
        street = ""
        street_type = ""
        house_type = ""
        house_number = ""
        flat_type = ""
        flat_number = ""
        
        try:
            for t in root.findall('.//{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}Address'):
                for i in t.getchildren():
                    if i.tag == "{urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1}Street":
                        street, street_type = i.attrib["Name"], i.attrib["Type"]
                    if i.tag == "{urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1}Level1":
                        house_type, house_number = i.attrib["Type"], i.attrib["Value"]
                    if i.tag == "{urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1}Apartment":
                        flat_type, flat_number = i.attrib["Type"], i.attrib["Value"]
                return r'{}. {}, {}. {}, {}. {}'.format(street_type, street, house_type, house_number, flat_type, flat_number)
        except:
            print("Возможно ошибка в тэгах")


    def replaceDate(self, root, date):
        try:
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
                            print(i.text)
        except:
            print("Возможно ошибка в тэгах")

    def get_owners(self, root):
        owners = []
        try:
            for t in root.findall(".//{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}Person"):
                for i in t.getchildren():
                    if i.tag == '{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}Content':
                        owners.append(i.text)
            return owners
        except:
            owners.append("Отсутствует в выписке")
            
    def make_folder(self, root):
        street = ""
        house_number = ""
        try:
            for t in root.findall('.//{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}Address'):
                for i in t.getchildren():
                    if i.tag == "{urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1}Street":
                        street = i.attrib["Name"]
                    if i.tag == "{urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1}Level1":
                        house_number = i.attrib["Value"]
                return r'{} {}'.format(street, house_number.replace("/", "-"))
        except:
            print("Возможно ошибка в тэгах")
 
           
    



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
sys.exit(app.exec_())