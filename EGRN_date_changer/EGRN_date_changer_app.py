from PyQt5 import QtCore, QtGui, QtWidgets
from lxml import etree as ET



class Ui_Dialog(object):
    files = []
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(485, 198)
        self.OpenString = QtWidgets.QLineEdit(Dialog)
        self.OpenString.setGeometry(QtCore.QRect(120, 50, 351, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OpenString.sizePolicy().hasHeightForWidth())
        self.OpenString.setSizePolicy(sizePolicy)
        self.OpenString.setText("")
        self.OpenString.setObjectName("OpenString")
        self.SaveString = QtWidgets.QLineEdit(Dialog)
        self.SaveString.setGeometry(QtCore.QRect(120, 90, 351, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SaveString.sizePolicy().hasHeightForWidth())
        self.SaveString.setSizePolicy(sizePolicy)
        self.SaveString.setObjectName("SaveString")
        self.OpenBtn = QtWidgets.QPushButton(Dialog)
        self.OpenBtn.setGeometry(QtCore.QRect(10, 50, 75, 23))
        self.OpenBtn.clicked.connect(self.openButton)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OpenBtn.sizePolicy().hasHeightForWidth())
        self.OpenBtn.setSizePolicy(sizePolicy)
        self.OpenBtn.setObjectName("OpenBtn")
        self.SaveBtn = QtWidgets.QPushButton(Dialog)
        self.SaveBtn.setGeometry(QtCore.QRect(10, 90, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SaveBtn.sizePolicy().hasHeightForWidth())
        self.SaveBtn.setSizePolicy(sizePolicy)
        self.SaveBtn.setObjectName("SaveBtn")
        self.SaveBtn.clicked.connect(self.saveButton)
        self.DateString = QtWidgets.QLineEdit(Dialog)
        self.DateString.setGeometry(QtCore.QRect(10, 130, 75, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DateString.sizePolicy().hasHeightForWidth())
        self.DateString.setSizePolicy(sizePolicy)
        self.DateString.setObjectName("DateString")
        self.ResultBtn = QtWidgets.QPushButton(Dialog)
        self.ResultBtn.setGeometry(QtCore.QRect(120, 130, 351, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResultBtn.sizePolicy().hasHeightForWidth())
        self.ResultBtn.setSizePolicy(sizePolicy)
        self.ResultBtn.setObjectName("ResultBtn")
        self.ResultBtn.clicked.connect(self.changeDateButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Изменятор дат"))
        self.OpenBtn.setText(_translate("Dialog", "Открыть"))
        self.SaveBtn.setText(_translate("Dialog", "Сохранить"))
        self.ResultBtn.setText(_translate("Dialog", "Сделать хорошо"))
        
    def read_xml(path):
        """Возваращает объект типа xml.etree.ElementTree"""
        tree = ET.parse(path)
        root = tree.getroot()
        return root
    
    def replaceDate(root, date):
        for t in root.findall(".//{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}ReestrExtract"):
            for i in t.getchildren():
                if i.tag == '{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}DeclarAttribute':
                    i.attrib['ExtractDate'] = date
                    i.attrib['RequeryDate'] = date
        for t in root.findall(".//{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}ReestrExtract"):
            for i in t.getchildren():
                if i.tag == '{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}Sender':
                    i.attrib["Date_Upload"] = date.replace('.','-')
        for t in root.findall(".//{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}HeadContent"):
            for i in t.getchildren():
                if i.tag == '{urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1}Content':
                    i.text = 'На основании запроса от {} г., поступившего на рассмотрение {} г., сообщаем, что согласно записям Единого государственного реестра недвижимости:'.format(date, date)
                    
        
    def openButton(self):
        filenames = QtWidgets.QFileDialog.getOpenFileNames(None, filter = "XML (*.xml)")
        for file in filenames[0]:
            self.files.append(file)
            
    def saveButton(self):
        self.SaveString.setText(QtWidgets.QFileDialog.getExistingDirectory())
        
    def changeDateButton(self):
        new_counter = 1
        for file in self.files:
            file_counter = len(self.files)
            print('Обрабатываемый файл: '+str(file))
            #ET.register_namespace('', 'urn://x-artefacts-rosreestr-ru/outgoing/kpoks/4.0.1')
            ET.register_namespace('smev', 'urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1')
            ET.register_namespace('num', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/numbers/1.0')
            ET.register_namespace('adrs', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1')
            ET.register_namespace('spa', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/5.0.1')
            ET.register_namespace('param', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/parameters-oks/2.0.1')
            ET.register_namespace('cer', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0')
            ET.register_namespace('doc', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/document-output/4.0.1')
            ET.register_namespace('flat', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/assignation-flat/1.0.1')
            ET.register_namespace('ch', 'urn://x-artefacts-rosreestr-ru/commons/complex-types/cultural-heritage/2.0.1')
            try:
                tree = ET.parse(file)
                root = tree.getroot()
            except:
                print('Беда с файлом: '+str(file))
            try:
                Ui_Dialog.replaceDate(root, self.DateString.text())
                tree.write(str(file), encoding='UTF-8', xml_declaration=True)
            except:
                print("Беда с тегами в файле: "+str(file))            
            print('Обработано файлов: '+ str(new_counter) + '/'+str(file_counter))
            new_counter+=1
        return print("Все файлы обработаны")
        
        
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
sys.exit(app.exec_())