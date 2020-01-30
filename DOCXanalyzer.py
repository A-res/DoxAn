#!/usr/bin/env python
# coding: utf-8



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

def clicked():
    global file 
    file= filedialog.asksaveasfilename()
    txt.insert(0,file)

def clicked2():
    global file 
    file= filedialog.asksaveasfilename()
    txt2.insert(0,file)
def xer():
    section = int(txt_choice.get())
    print(section)

def analyZER():
    Tdocx = (gettext(file))
    Tdocx = re.split("[,\-!#№?: ]+",Tdocx)
    Tspl = pd.Series(Tdocx)

    #Обучающая выборка

    Tdf= pd.read_csv('training_j.csv')
    Tdf= Tdf['Значение']

    #Здесь мы назначаем группы в которые нам нужно будет распределить информацию

    Gdf = pd.read_csv('training_j.csv')
    Gdf = Gdf['Раздел']

    #Набор для индентификации

    text_clf = Pipeline([('tfidf', TfidfVectorizer()),('clf',RandomForestClassifier())])

    text_clf.fit(Tdf,Gdf) # Обучение системы. Что каждому Tdf соответствует Gdf
    res = text_clf.predict(Tspl) #Задаем df который будет обрабатываться



    #Преобразуем типы информации для объеденения в один df

    Rdf = pd.Series(res)
    Rdf=Rdf.to_frame().reset_index()
    Rdf.columns = ['id','Группа']

    Tspl=Tspl.to_frame().reset_index()
    Tspl.columns=['id','Значение']

    #Объеденяем df 
    DF = pd.merge(Rdf,Tspl)
    DF.drop ('id',axis=1,inplace =True)
    DF.to_csv('rezultat.csv')

    #На данном этапе у нас имеется распределенная информация. Каждому значению из файла задан его раздел.
    #Далее необходимо собрать информацию по переменным

    DF_name =DF['Группа'].isin(['Имя'])
    #Чистим результаты от ненужных символов и цифр
    name = DF[DF_name].copy()
    name.drop ('Группа',axis=1,inplace =True)
    name = re.sub(r"[0123456789\n]",'',str(name))
    txt_name.delete(0,END)
    txt_name.insert(0,name)


    DF_date =DF['Группа'].isin(['Дата'])
    #Чистим результаты от ненужных символов и цифр
    date = DF[DF_date].copy()
    date.drop ('Группа',axis=1,inplace =True)
    date = re.sub(r"[абвгдеёжзийклмнопрстуфхцчшщъыьеюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЕЮЯ]",'',str(date))
    date = date[9:]
    txt_date.delete(0,END)
    txt_date.insert(0,date)

    DF_namber =DF['Группа'].isin(['Номер'])
    #Чистим результаты от ненужных символов и цифр
    namber = DF[DF_namber].copy()
    namber.drop ('Группа',axis=1,inplace =True)
    namber = re.sub(r'Значение','',str(namber))
    namber = namber[5:]
    txt_namber.delete(0,END)
    txt_namber.insert(0,namber)

    DF_text =DF['Группа'].isin(['Текст']) #Нужно как то убрать слово значение
    #Чистим результаты от ненужных символов и цифр
    text = DF[DF_text].copy()
    text.drop ('Группа',axis=1,inplace =True)
    text = re.sub(r'Значение','',str(text))
    text = text[0:270]
    txt_text.delete(0,END)
    txt_text.insert(0,text)  

def training():
    
    dom1 = (gettext(file))
    dom1 = re.split("[,\-!#№?: ]+",dom1)
    dom2 = pd.Series(dom1)
    
    for i in dom2[0:20]:
        txt_word.insert(0,i) 
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
    
#Общая настройка окна
window = Tk()
window.title('АНАЛИЗАТОР ДОКУМЕНТА')
window.geometry('1200x700')


tab_control = ttk.Notebook(window)


tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)


tab_control.add(tab1,text='Анализ документа')
#tab_control.add(tab2,text='Обучение анализатора')


    
#######################################
###Первая вкладка "Анализ документа"###
######################################

#Надпись
lbl = Label(tab1, text = 'Выберите документ', font = ("Arial",14)) 
lbl.grid(column=0, row=0)

#Кнопка выбора файла
btn1 = Button(tab1, text='Выбрать файл', command=clicked)
btn1.grid(column=2,row=0)

#Имя файла. Оно тут отображается 
txt = Entry(tab1, width=20)
txt.grid(column=1, row=0)
txt.insert(0,'file')


#Имя документа
lbl_name = Label(tab1, text = 'Имя документа', font = ("Arial",14)) 
lbl_name.grid(column=0, row=5)

txt_name = Entry(tab1, width=50)
txt_name.grid(column=1, row=5)
txt_name.insert(0,"name")


#Дата документа
lbl_date = Label(tab1, text = 'Дата документа', font = ("Arial",14)) 
lbl_date.grid(column=0, row=6)

txt_date = Entry(tab1, width=50)
txt_date.grid(column=1, row=6)
txt_date.insert(0,"date")

#Номер документа
lbl_namber = Label(tab1, text = 'Номер документа', font = ("Arial",14)) 
lbl_namber.grid(column=0, row=7)

txt_namber = Entry(tab1, width=50)
txt_namber.grid(column=1, row=7)
txt_namber.insert(0,"namber")
#Текст документа
lbl_text = Label(tab1, text = 'Текст документа', font = ("Arial",14)) 
lbl_text.grid(column=0, row=8)

txt_text = Entry(tab1, width=50)
txt_text.grid(column=1, row=8)
txt_text.insert(0,"text")

tab_control.pack(expand=1, fill='both')

#Кнопка Анализ
btn2 = Button(tab1, text='Анализ', command=analyZER)
btn2.grid(column=2,row=15)



########################################
###Вторая вкладка "Обучение"##########
######################################

##Надпись
#lbl = Label(tab2, text = 'Выберите документ', font = ("Arial",14)) 
#lbl.grid(column=0, row=0)

##Кнопка выбора файла
#btn1 = Button(tab2, text='Выбрать файл', command=clicked2)
#btn1.grid(column=2,row=0)

##Имя файла. Оно тут отображается 
#txt2 = Entry(tab2, width=20)
#txt2.grid(column=1, row=0)
#txt2.insert(0,'file')



##Отображение информации
#lbl_info = Label(tab2, text = 'Информация', font = ("Arial",14)) 
#lbl_info.grid(column=0, row=5)

#txt_info = Entry(tab2, width=90)
#txt_info.grid(column=1, row=5)
#txt_info.insert(0,"1-Имя, 2-Номер, 3-Дата, 4-Текст, 5-Исправить, 6- Пропустить")
##Отображение слова
#txt_word = Entry(tab2, width=35)
#txt_word.grid(column=0, row=20)
#txt_word.insert(0,"Слово")

#Отображение групп




#Выбор

#txt_choice = Entry(tab2, width=35)
#txt_choice.grid(column=1, row=40)
#txt_choice.insert(0,"Выбор")

#btn3 = Button(tab2, text='Обучить', command=training)
#btn3.grid(column=2,row=15)

#btn4 = Button(tab2,text='test', command=xer)
#btn4.grid(column=5, row=3)

window.mainloop()





