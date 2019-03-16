from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from applyTree import apply_classifier_to_df_tableformat



class Ui_Dialog(object):
    files = []
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 135)
        self.OpenBtn = QtWidgets.QPushButton(Dialog)
        self.OpenBtn.setGeometry(QtCore.QRect(10, 30, 75, 23))
        self.OpenBtn.setObjectName("OpenBtn")
        self.OpenBtn.clicked.connect(self.openButton)
        self.SaveBtn = QtWidgets.QPushButton(Dialog)
        self.SaveBtn.setGeometry(QtCore.QRect(10, 60, 75, 23))
        self.SaveBtn.setObjectName("SaveBtn")
        self.SaveBtn.clicked.connect(self.saveButton)
        self.StrOpen = QtWidgets.QLineEdit(Dialog)
        self.StrOpen.setGeometry(QtCore.QRect(100, 30, 281, 20))
        self.StrOpen.setObjectName("StrOpen")
        self.StrSave = QtWidgets.QLineEdit(Dialog)
        self.StrSave.setGeometry(QtCore.QRect(100, 60, 281, 20))
        self.StrSave.setObjectName("StrSave")
        self.ConvertTable = QtWidgets.QPushButton(Dialog)
        self.ConvertTable.setGeometry(QtCore.QRect(100, 90, 281, 23))
        self.ConvertTable.setObjectName("ConvertTable")
        self.ConvertTable.clicked.connect(self.makeCool)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.OpenBtn.setText(_translate("Dialog", "Открыть"))
        self.SaveBtn.setText(_translate("Dialog", "Сохранить"))
        self.ConvertTable.setText(_translate("Dialog", "Сделать хорошо"))


    def openButton(self):
        self.files = []
        filenames = QtWidgets.QFileDialog.getOpenFileNames(None, filter = "XML (*.xlsx)")
        for file in filenames[0]:
            self.files.append(file)

    def saveButton(self):
        self.StrSave.setText(QtWidgets.QFileDialog.getExistingDirectory())

    def makeCool(self):
        filepathSave = self.StrSave.text()
        filepathOpen = self.StrOpen.text()
        import pandas as pd
        for file in self.files:
            print(file)
            df = pd.read_excel(file, skiprows=0, header=None, sheet_name='40702810852090005784')
            for index, row in df.iterrows():
                text_in_rows = row.tolist()
                if "Дата проводки" not in text_in_rows:
                    pass#df.drop(df.iloc[0:index], inplace=True, axis=1)
                else:
                    df = pd.read_excel(file, skiprows=index, header=None, sheet_name='40702810852090005784')
                    break

                
    
            for col in df.columns:
                indexer = []
                indexer = df[col]#.str.contains("б/с 40702")):
                for index, item in enumerate(indexer):
                    if item == "б/с" or item == "б/с 40702":
                        df = df.drop(df.index[index:])
    
    
            df = pd.DataFrame(df).dropna(axis='columns', how='all')
            df.columns = range(1, df.shape[1]+1)
            vipiska = df.iloc[:,0:df.shape[1]]
    
            if vipiska.shape[1] > 9:
                vipiska = vipiska.iloc[:, 0:9]
    
            
            vipiska.columns = ("Дата_проводки",
                                  "Счет_дебет",
                                  "Счет_кредит",
                                  "Сумма_по_дебету",
                                  "Сумма_по_кредиту",
                                  "№_документа",
                                  "ВО",
                                  "Банк_(БИК_и_наименование)",
                                  "Назначение_платежа")
            
            vipiska_updated = pd.DataFrame()
            for i in vipiska.iterrows():
                if i[1]["Счет_дебет"] != "Дебет" and i[1]["Счет_дебет"] != "Счет" and i[1]["Дата_проводки"] != "Дата проводки":
                    vipiska_updated = vipiska_updated.append(i[1])
    
    #vipiska = pd.DataFrame(vipiska).dropna(axis='columns', how='all')
            vipiska = pd.DataFrame(vipiska).dropna(axis='rows', how='all')
    
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
    
            vipiska.reset_index(drop=True, inplace=True)
            
            apply_classifier_to_df_tableformat(vipiska)      

            
            filename = "/Выписка за "
            filedate = str(vipiska['Дата_проводки'].reset_index(drop="True")[0]).replace(":", "-")
            tblformat = ".xlsx"
            filepathSave1 = "".join((filepathSave, filename, filedate, tblformat))
            writer = pd.ExcelWriter(filepathSave1, engine='xlsxwriter')
            vipiska.to_excel(writer, sheet_name='Sheet1', index=False)
            writer.save()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
sys.exit(app.exec_())