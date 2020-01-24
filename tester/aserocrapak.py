#!/usr/bin/python
import os
import cv2
import MySQLdb as mdb 
import numpy as np
import pytesseract
from PIL import Image
from sshtunnel import SSHTunnelForwarder


# Path of working folder on Disk

class OCRAsek:
    gambar= None
    devId = None 
    gambar = None 
    flagsek = None 
    profilSN = None
    maxi = None 
    minim = None
    refsntemp =None
    src_path = "/home/faoziaziz/work/asekocr-apk/tmp/" 
    img_path = "/home/faoziaziz/work/asekocr-apk/tmp/tmp.png"
    gstring = None

    

    def get_iterasi(self):
        with SSHTunnelForwarder(('36.89.87.139', 22), ssh_password='pras !@#', ssh_username='prasimax', remote_bind_address=('127.0.0.3', 3306)) as server:
            conn = mdb.connect(host='127.0.0.1', port=server.local_bind_port, user='tappingapk', passwd='trumon123!', db='Trumon')
            cur = conn.cursor()

            cur.execute("SELECT MIN(RefSN) AS minimum FROM Trumon.Image")
            self.minim = cur.fetchone()[0]
            cur.execute("SELECT MAX(RefSN) AS maximum FROM Trumon.Image")
            self.maxi = cur.fetchone()[0]
        

    def get_data(self, refsn):
        with SSHTunnelForwarder(('36.89.87.139', 22), ssh_password='pras !@#', ssh_username='prasimax', remote_bind_address=('127.0.0.3', 3306)) as server:
            conn = mdb.connect(host='127.0.0.1', port=server.local_bind_port, user='tappingapk', passwd='trumon123!', db='Trumon')
            cur = conn.cursor()

            query=("SELECT * FROM Trumon.Image WHERE  RefSN = %s")
            cur.execute(query, (refsn, ))
            record = cur.fetchall()
            self.seqNum = record[0][0]
            self.devId = record[0][1]
            self.gambar = record[0][3]
            self.flagsek = record[0][4]
            self.profilSN = record[0][5]
            self.refsntemp = refsn

    def getImage(self):
        
        fout = open('/home/faoziaziz/work/asekocr-apk/tmp/tmp.png', 'wb')
        fout.write(self.gambar)  
        fout.close()
    

    def get_string(self):
        # Read image with opencv
        #img = cv2.imread(self.img_path)

        # Convert to gray
       # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply dilation and erosion to remove some noise
        #kernel = np.ones((1, 1), np.uint8)
        #img = cv2.dilate(img, kernel, iterations=1)
        #img = cv2.erode(img, kernel, iterations=1)

        # Write image after removed noise
        #cv2.imwrite(self.src_path + "removed_noise.png", img)

        #  Recognize text with tesseract for python
        # result = pytesseract.image_to_string(Image.open(self.src_path + "removed_noise.png")) # thres.png
        result = pytesseract.image_to_string(Image.open(self.img_path))
        #  Remove template file
        #  assos.remove(temp)
        self.gstring =result
        return result

    def write_database(self):
        # this target is text tabel
        with SSHTunnelForwarder(('36.89.87.139', 22), ssh_password='pras !@#', ssh_username='prasimax', remote_bind_address=('127.0.0.3', 3306)) as server:
            conn = mdb.connect(host='127.0.0.1', port=server.local_bind_port, user='tappingapk', passwd='trumon123!', db='Trumon')
            cur = conn.cursor()

            query=(""" INSERT INTO `Teks` (`DeviceId`, `RefSN`, `Data`) VALUES (%s,%s,%s)""")
            cur.execute(query, (self.devId, self.refsntemp, `self.gstring`))
            record = cur.fetchall()
            conn.commit()

    def delete_temp(self):
        # Delete temp.png file 
        os.remove("/home/faoziaziz/work/asekocr-apk/tmp/tmp.png")
       # os.remove("/home/faoziaziz/work/asekocr-apk/tmp/removed_noise.png")
print "masuk"

#def get_indeksAkhirImage():
    #with SSHTunnelForwarder(('36.89.87.139', 22), ssh_password='pras !@#', ssh_username='prasimax', remote_bind_address=('127.0.0.3', 3306)) as server:
        #conn = mdb.connect(host='127.0.0.1', port=server.local_bind_port, user='tappingapk', passwd='trumon123!', db='Trumon')
       # cur = conn.cursor()

        #cur.execute("SELECT MAX(RefSN) AS maximum FROM Trumon.Image")
       # maximal = cur.fetchone()[0]
       # return maximal
def maximalisasi():
    with SSHTunnelForwarder(('36.89.87.139', 22), ssh_password='pras !@#', ssh_username='prasimax', remote_bind_address=('127.0.0.3', 3306)) as server:
        conn = mdb.connect(host='127.0.0.1', port=server.local_bind_port, user='tappingapk', passwd='trumon123!', db='Trumon')
        cur = conn.cursor()

        cur.execute("SELECT MAX(RefSN) AS minimum FROM Trumon.Teks")
        maksi = cur.fetchone()[0]
        return maksi

with SSHTunnelForwarder(('36.89.87.139', 22), ssh_password='pras !@#', ssh_username='prasimax', remote_bind_address=('127.0.0.3', 3306)) as server:
    conn = mdb.connect(host='127.0.0.1', port=server.local_bind_port, user='tappingapk', passwd='trumon123!', db='Trumon')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Trumon.Image WHERE RefSN IS NOT NULL")
    record = cur.fetchall()
    kamu = OCRAsek()
    while(True):
        indeksTerakhir = maximalisasi()
        print "Index Terkahir"
        print indeksTerakhir
        for row in record:
            refsn = row[2]   
        
            if refsn>indeksTerakhir:
                kamu.get_data(refsn)
                kamu.getImage()
                kalista = kamu.get_string()
                kamu.write_database()
                kamu.delete_temp()
        #print "berarti jalan"

print "nikah yu kal"