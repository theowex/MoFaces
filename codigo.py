import numpy as np
import cv2
from PIL import Image
import math

tamMoface = 800
cantRostros = 0

# https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

def mosaico(cant):
    math.sqrt(cant)
    round(math.sqrt(cant))

    print("ga")


while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    contador = 0
    for (x, y, w, h) in faces:
        contador += 1
        rostro = img[y: y + h, x: x + w]
        cv2.imwrite("face" + str(contador) + ".jpg", rostro)
        rostro2 = Image.open("face" + str(contador) + ".jpg")
        imagenred = rostro2.resize((tamMoface, tamMoface))
        imagenred.save("face" + str(contador) + ".jpg")
        #img.resize(tamMoface, tamMoface)
        #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #roi_gray = gray[y:y + h, x:x + w]
        #roi_color = img[y:y + h, x:x + w]

        #eyes = eye_cascade.detectMultiScale(roi_gray)
        #for (ex, ey, ew, eh) in eyes:
        #    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        #region = img[y:(y+h),x:(x+w)]
        #cv2.imshow('ga', region)
    for (x, y, w, h) in faces:
        print(x, y, w, h)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #contador = 0
    #--------------------------------------------------------------------------------------------
    if len(faces) > 0:
        cantRostros = len(faces)
        cantColumnas = int(math.sqrt(cantRostros))
        cantFilas = math.ceil(cantRostros / cantColumnas)
        if len(faces) == 2:
            cantColumnas, cantFilas = cantFilas, cantColumnas
        tamFila = tamMoface / cantFilas
        nroRostro = 0
        final = Image.new("RGB", (tamMoface, tamMoface), "black")
        for fila in range(cantFilas):
            if fila == cantFilas - 1: #if fila == ultimaFila
                cantColumnas = cantRostros - (cantColumnas * (cantFilas - 1))
                #tamColumna = tamMoface/(cantRostros - (cantColumnas * (cantFilas - 1)))
                #print("gagagdda")
            tamColumna = tamMoface / cantColumnas
            for columna in range(cantColumnas):
                nroRostro += 1
                imagen1 = Image.open("face" + str(nroRostro) + ".jpg")
                recorte = imagen1.crop((int(columna * tamColumna), int(fila * tamFila), int((columna + 1)* tamColumna), int((fila + 1) * tamFila)))
                #int(fila * tamFila) + int(tamFila), x: int(columna * tamColumna) + int(tamColumna)
                final.paste(recorte, (int(columna * tamColumna), int(fila * tamFila)))
                print("x:", int(columna * tamColumna), ", y:", int(fila * tamFila))

            #print("oe", fila)
        #--------------------------------------------------------------------------------------
        #final = Image.new("RGB", (800, 800), "black")
        #imagen1 = Image.open("face1.jpg")
        #final.paste(imagen1, (750, 0))
        #-----xd--este no sino se crashea :'v--final.show()
        final.save("moface.jpg")
        #----------------------------------------------------------------------------
    cv2.imshow('Screen', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
