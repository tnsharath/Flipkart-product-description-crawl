# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 20:35:28 2020

@author: Sharath
"""
import requests
import lxml.html as lh
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from pathlib import Path
from tkinter import *

def crawlWeb(url):
    response = requests.get(url)
    doc = lh.fromstring(response.content)
    tr_elements = doc.xpath('//tr')
    product_name = doc.xpath('.//span[@class="_35KyD6"]/text()')
    #Create empty list
    col=[]
   
    col.append(("Attribute",[]))
    col.append(("Value",[]))
    for j in range(len(tr_elements)):
   
        T=tr_elements[j]
        i=0
    
        for t in T.iterchildren():
            data=t.text_content() 
            if i>0:
                try:
                    data=int(data)
                except:
                    pass
            col[i][1].append(data)
            i+=1
    return col, product_name[0]

def writeToExcel(path, col):
    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    writer = ExcelWriter(path)
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()
    message.configure(text="Success!!!")
    
def mainMethod(url):
    col, product_name = crawlWeb(url)
    product_name = product_name.replace("/", "")
    Path(r'C:\Users\Sharath\Desktop\Specs\\').mkdir(parents=True, exist_ok=True)
    path = r'C:\Users\Sharath\Desktop\Specs\%s.xlsx' %product_name
    writeToExcel(path, col)

def clicked():

    try:
        mainMethod(txt.get())
    except:
        message.configure(text ="Something went wrong!!")


window = Tk()

window.title("Snipper")

window.geometry('350x200')

lbl = Label(window, text="Paste URL")

lbl.grid(column=1, row=0)

txt = Entry(window, width=60)

txt.grid(column=1, row=2)

message = Label(window, text="")
message.grid(column = 1, row = 4)
btn = Button(window, text="Snip", command=clicked)

btn.grid(column=1, row=3)

window.mainloop()