try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import os
import numpy as np
import re
from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
from datetime import datetime
import glob
from sys import argv

script, fullpath, filename, directory = argv
os.chdir(r'D:\test')
print("Скрипт ", script)
print("Полный путь ", fullpath)
print("Имя файла ", filename)
print("Директория ", directory)



def splitImages(path):
    inputpdf = PdfFileReader(open(path, "rb"))
    for i in range(inputpdf.numPages):
        now = datetime.now()
        dt_string = now.timestamp()
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open("./prikazi/document-page%s-%s.pdf" % (i, dt_string), "wb") as outputStream:
            output.write(outputStream)
        pages = convert_from_path("./prikazi/document-page%s-%s.pdf" % (i, dt_string), 100)
        for page in pages:
            page.save('./prikazi/document-page%s-%s.jpeg' % (i,dt_string), 'JPEG')
    
#Нейросеть-------------------------------------------------------------------
net = cv2.dnn.readNet("yolov3_training_last.weights", "yolov3_testing.cfg")
classes = ["docNumber"]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
#----------------------------------------------------------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
inputpdf = PdfFileReader(open(fullpath, "rb"))

for i in range(inputpdf.numPages):
    print("Процент выполнения: ", int(100 * (i+1) / inputpdf.numPages), "%")
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("%s/%s-page%s.pdf" % (directory, filename, i), "wb") as outputStream:
        output.write(outputStream)
    pages = convert_from_path("%s/%s-page%s.pdf" % (directory, filename, i), 100)
    for page in pages:
        page.save("%s/%s-page%s.jpeg" % (directory, filename, i), 'JPEG')
        

    
    #Нейросеть распознает участок на скане документа в котором предположительно находится номер
    #судебного приказа.
    path = os.path.abspath("%s/%s-page%s.jpeg" % (directory, filename, i))
    
    img = cv2.imread(path)
    img = cv2.resize(img, None, fx=1, fy=1)
    height, width, channels = img.shape

    
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers) 
    #-------------------------------------------------------------------------
    
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # Объект распознан
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Координаты распозноннаго объекта
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    if not boxes:
        if not os.path.exists('%s/Подгрузить руками %s' % (directory, filename)):
            os.makedirs('%s\Подгрузить руками %s' % (directory, filename))
        os.rename("%s\%s-page%s.pdf" % (directory, filename, i), '%s\Подгрузить руками %s\Не надйена область распознавания %s-page%s.pdf' % (directory, filename, filename, i) ) 
        continue    
    else:

        # original_img = Image.open(path).convert('L')
        # w, h = original_img.size
        
        # im_crop = original_img.crop((0, 190, w, 350))
        im_crop = Image.fromarray(img.astype(np.uint8))
        x, y, w, h = boxes[0]
        im_crop = im_crop.crop((x-15, y, x+w+15, y+h))
        label = im_crop
        basewidth = 220
        wpercent = (basewidth/float(im_crop.size[0]))
        hsize = int((float(im_crop.size[1])*float(wpercent)))
        im_crop = im_crop.resize((basewidth,hsize), Image.ANTIALIAS)
        
        ret, cropped_img = cv2.threshold(np.array(im_crop), 155, 255, cv2.THRESH_BINARY)
        # img = Image.fromarray(original_img.astype(np.uint8))
        img_cropped1 = Image.fromarray(cropped_img.astype(np.uint8))
        # img = Image.fromarray(cropped_img.astype(np.uint8))
        text = pytesseract.image_to_string(cropped_img, lang='rus', config='--psm 6 --oem 1')
        text = text.replace(" ", "")
        match = r'№\d-(\d+.\d+\-\d+\/\d+|\d+\/\d+|\d-\d+\/\d+)'
        result = re.search(match, text)
        
        if not os.path.exists('%s\Подгрузить руками %s' % (directory, filename)):
            os.makedirs('%s\Подгрузить руками %s' % (directory, filename))
        
        if not os.path.exists('%s\Грузить в базу %s' % (directory, filename)):
            os.makedirs('%s\Грузить в базу %s' % (directory, filename))
            
        if result is None:
            os.rename("%s/%s-page%s.pdf" % (directory, filename, i), '%s\Подгрузить руками %s\Не получилось распознать текст %s-page%s.pdf' % (directory, filename, filename, i))
        else:
            print("%s\%s-page%s.pdf" % (directory, filename, i))
            os.rename("%s\%s-page%s.pdf" % (directory, filename, i), '%s\Грузить в базу %s\%s.pdf' % (directory, filename,result[0].replace("/", "--")))
            label.save('%s\Грузить в базу %s\label - %s.jpeg' % (directory, filename,result[0].replace("/", "--")), 'JPEG')
        
 
print("Распознавание завершено!")   
    
#Удалим временные файлы
os.chdir(directory)
for file in glob.glob("*.jpeg"):
    print(file)
    if '-page' in file:
        os.remove(file)
    


#  -c tessedit_char_whitelist=0123456789№-/

# ^№+ +\d+-+\d+-+\d*+\/+\d* regular expression