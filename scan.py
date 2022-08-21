import logging
from tabnanny import verbose
import numpy as np
from math import sqrt
from math import ceil
import cv2
import sys
import os
import platform
import logging
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
from virus_total_apis import PublicApi as VirusTotalPublicApi
import json
import time
import hashlib
import urllib
from urllib import request
from PIL import Image

#import update

log_format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="Scan_logs.log", level=logging.DEBUG,
                    format=log_format, filemode='w')
logger = logging.getLogger()
tf.get_logger().setLevel(logging.ERROR)

Image.MAX_IMAGE_PIXELS = 1000000000  # To avoid Decompression Bomb Warning
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # disable tenserflow debug info

cwd = os.getcwd()
ResFile_object = open('ResultLog', 'a')

OS_NAME = platform.system()
formatted_OS_NAME = OS_NAME.casefold()
if(formatted_OS_NAME == "windows"):
    tmp_root = cwd+"\\temp\samples\\"

elif(formatted_OS_NAME == "linux" or formatted_OS_NAME == "darwin"):
    tmp_root = os.path.dirname(__file__)+"temp/samples/"

cwd = os.getcwd()  # current working directory

MalLabel = ['Adialer.C', 'Agent.FYI', 'Allaple.A', 'Allaple.L', 'Alueron.gen!J', 'Autorun.K', 'C2LOP.P', 'C2LOP.gen!g', 'Dialplatform.B', 'Dontovo.A', 'Fakerean', 'Instantaccess', 'Lolyda.AA1', 'Lolyda.AA2', 'Lolyda.AA3', 'Lolyda.AT', 'Malex.gen!J', 'Obfuscator.AD', 'Rbot!gen', 'Skintrim.N', 'Swizzor.gen!E', 'Swizzor.gen!I', 'VB.AT', 'Wintrim.BX', 'Yuner.A']

def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles   

class MalScan:
    def __init__(self):
        try:
            allFiles = getListOfFiles(cwd)
            for file in allFiles:
                fn = file
                if os.stat(fn).st_size == 0:
                    logger.debug("skipping : "+fn)
                else:
                    self.label = ''
                    self.convert(fn)
                    conn = self.testConnection()
                    if conn == 1:
                        #print("Your are Online.................OK")
                        md5, sha1 = self.hash_file(fn)
                        #print("Using OSINT.......................")
                        vt = self.apiFunction(md5, sha1)
                        #print("OSINT status : ",vt)
                        if (vt == 1):
                            ResFile_object.write(fn+"\t"+self.label)
                            #print("Malware : ",self.label)
                        else:
                            #print("\n........Using CNN.........\n")
                            #print("Predicting......................... | File : "+fn)
                            self.predictor(self.timg,fn)

                    else:
                        #print("you are Offline")
                        #print("\n........Using CNN.........\n")
                        #print("Predicting......................... | File : "+fn)
                        self.predictor(self.timg,fn)

        except Exception as e:
            logger.debug("Error : \n", e, "or file not found")

    def convert(self, filename):
        logger.debug("# Converting input file to grayscale image #")
        #print("Coverting to grayscale....................")
        input_file_name = filename
        
        with open(input_file_name, 'rb') as binary_file:
            data = binary_file.read()

        data_len = len(data)
        d = np.frombuffer(data, dtype=np.uint8)
        sqrt_len = int(ceil(sqrt(data_len)))
        new_len = sqrt_len*sqrt_len
        pad_len = new_len - data_len
        padded_d = np.hstack((d, np.zeros(pad_len, np.uint8)))
        im = np.reshape(padded_d, (sqrt_len, sqrt_len))
        os.chdir(tmp_root)
        cv2.imwrite('test.png', im)
        os.chdir(cwd)
        test = ImageDataGenerator().flow_from_directory(
            directory="temp", target_size=(64, 64), batch_size=2)
        self.timg, label = next(test)
        # print(timg)

    def hash_file(self, filename):
        logger.debug("# Hashing file #")
        sha1_hash = hashlib.sha1()
        md5_hash = hashlib.md5()
        with open(filename, 'rb') as file:
            chunk = 0
            while chunk != b'':
                chunk = file.read(1024)
                sha1_hash.update(chunk)
            hashValueSHA1 = sha1_hash.hexdigest()
        with open(filename, 'rb') as f:
            block = 0
            while block != b'':
                block = f.read(1024)
                md5_hash.update(block)
            hashValueMD5 = md5_hash.hexdigest()

        return hashValueMD5, hashValueSHA1

    def testConnection(self):
        logger.debug("# Testing Connection #")
        #print("Testing Connection.....................................................")
        try:
            urllib.request.urlopen('https://www.google.com/', timeout=5)
            return 1
        except Exception as e:
            return 0

    def apiFunction(self, hashValueMD5, hashValueSHA1):
        logger.debug("# API Functions #")
        apiKey = '1bd77df1a5fc990ab37a419841880aaf32a2c324b43b61e0b23e3a37936553fe'
        # print(hashValueMD5,hashValueSHA1)

        vt = VirusTotalPublicApi(apiKey)
        response = vt.get_file_report(hashValueMD5)

        if response['response_code'] == 200:
            results = response['results']

            # print(response['response_code'])
            # print(results)

            if results['response_code'] == 1:

                if results['sha1'].lower() != hashValueSHA1.lower():
                    #print("sha1 is conflicting")
                    return -1

                #print('Response Code  : ', results['response_code'])
                # print(results['verbose_msg'])
                #print('\nTotal Engines Scaned : ', results['total'])
                #print('Engines Detetcted    : ', results['positives'])

                if results['positives'] > 0:
                    engine = list(results['scans'].keys())[0]
                    self.label = results['scans'][engine]['result']
                    return 1
                elif results['positives'] == 0:
                    return 0
            else:
                #print('Response Code : ', results['response_code'])
                #print('Error : ', results['verbose_msg'])
                return -1

        else:
            # print(response['response_code'])
            # print(response['error'])
            return -1

    def predictor(self, img,fn):
        logger.debug("# Predicting the result #")
        model = keras.models.load_model('CNN_Model')
        result = model.predict(img)
        print('',flush=True)
        if(result[0][0] > result[0][1]):
            # file is benign
            #print("Benign")
            #print("\n")
            ResFile_object.write(fn+"\t"+"0\t\n")
            return 1
        elif(result[0][0] == result[0][1]):
            # either benign or malware
            ResFile_object.write(fn+"\t"+"2\t\n")
            #print("Unknown")
            #print("\n")
            return 0
        else:
            # file is malware
            family = keras.models.load_model('Malware_Family')
            fam = family.predict(img)
            max = fam[0][0]
            print('',flush=True)
            for i in range(0, len(fam[0])):    
            #Compare elements of array with max    
                if(fam[0][i] > max):    
                    max = fam[0][i]
                    index = i
            self.label = MalLabel[index]
            ResFile_object.write(fn+"\t"+"1\t"+self.label+"\n")
            #print("Malware : ",self.label)
            #rint("\n")
            return -1
        

if __name__ == "__main__":
    scan = MalScan()
    ResFile_object.close()
