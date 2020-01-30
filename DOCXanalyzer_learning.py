# Загрузка библиотек
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext
import warnings
import docx
import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier , AdaBoostClassifier
from sklearn.pipeline import Pipeline
import re

warnings.simplefilter(action='ignore',category = FutureWarning)

#Работа с DOCX. Здесь мы берем данные из файла
def gettext (filename):
    doc = docx.Document (filename)
    Text = []
    for para in doc.paragraphs:
        Text.append(para.text)
    return ''.join(Text)


dom1 = (gettext(input('Выберите документ')))
dom1 = re.split("[,\-!#№?: ]+",dom1)
dom2 = pd.Series(dom1)
    
for i in dom2[0:20]:
    print(0,i) 
    section = int(input(("1-Имя, 2-Номер, 3-Дата, 4-Текст, 5-Исправить, 6- Пропустить :    ")))
    print(section)
    if section == 1: 
        fields =['Имя', i]
        with open (r'training_j.csv','a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
    elif section ==2:
        fields =['Номер', i]
        with open (r'training_j.csv','a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
    elif section ==3:
        fields =['Дата', i]
        with open (r'training_j.csv','a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
    elif section ==4: 
        fields =['Текст', i]
        with open (r'training_j.csv','a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
    elif section ==5:
        a = input("Введите исправленные данные")
        section = int(input("Выберите раздел: 1-Имя, 2-Номер, 3-Дата, 4-Текст :"))
        if section == 1: 
            fields =['Имя', a]
            with open (r'training_j.csv','a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
        elif section ==2:
            fields =['Номер', a]
            with open (r'training_j.csv','a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
        elif section ==3:
            fields =['Дата', a]
            with open (r'training_j.csv','a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
        elif section ==4: 
            fields =['Текст', a]
            with open (r'training_j.csv','a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            print("Данные внесены")
        elif section == 6:
            print("Данные не внесенны")
    