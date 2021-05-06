#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 22:45:55 2021

@author: bnzr
"""


from datetime import datetime

def check(string):
    try: 
        datetime.strptime(string, '%d.%m.%Y')
        return True
    except ValueError:
        return False
    
    
    
def messages (file):  
    fhand = open(file,'r',encoding='UTF-8')
    id = 0 
    dictionary = list()
    phones = list()
    txt=" " 


    for line in fhand :
        line= line.strip()
        if 'המדיה 'in line or 'הוסיף/ה' in line or'מוצפנות' in line :
            continue 
        
        date = line.split(",")[0].strip()
        
        if check(date):                               
          halfLine = line.split(" - ")
          dateTime = halfLine[0].split(",")
          time = dateTime[1].strip()
          phoneNum = halfLine[1].split(":")[0].strip()
          txt = halfLine[1].split(":")[1].strip()
         
          if phoneNum in phones:
              id=phones.index(phoneNum)
          else:
              phones.append(phoneNum)
              id=id+1
          dictionary.append({"datetime":date+ " "+time, "id" :id, "text": txt})

              
        else: 
           dictionary[id-1]["text"] = txt+" "+line
       
           
    fhand.close()
    return dictionary

def participants(file):
    fhand = open(file,'r',encoding='UTF-8')
    phones = list()
    id = 0
    for line in fhand :
        line= line.strip()
        if 'נוצרה'in line or 'המדיה 'in line or 'הוסיף/ה'in line or'מוצפנות' in line :
            continue 
        
        date = line.split(",")[0].strip()
        
        if check(date):                               
          halfLine = line.split(" - ")
          phoneNum = halfLine[1].split(":")[0].strip()
         
          if phoneNum in phones:
              continue
          else:
              phones.append(phoneNum)
              id=id+1

    fhand.close()
    return id

def creation(file):
    fhand = open(file,'r',encoding='UTF-8')
    for line in fhand :
        line= line.strip()
       
        date = line.split(",")[0].strip()
        
        if check(date): 
          halfLine = line.split(" - ")
          return halfLine[0]
    fhand.close()

def creator(file):
     fhand = open(file,'r',encoding='UTF-8')
     for line in fhand :
        line= line.strip()
        date = line.split(",")[0].strip()
        
        if check(date):                               
          halfLine = line.split(" - ")
          phoneNum = halfLine[1].split(":")[0].strip()
          return phoneNum

def metadata(file):
    return {"name_chat": file, "date_creation": creation(file), "num_of_participants": "<"+str(participants(file))+">", "creator": creator(file)}

def upload(file):
    message = messages(file)
    metadataFiles = metadata(file)
    uploadedFile = open(file, 'w', encoding='UTF-8')
    json = '{"messages": '+str(message)+', "metadata": '+str(metadataFiles)+'}'
    uploadedFile.write(json)
    
file=input("Enter a file name : ")
upload(file)