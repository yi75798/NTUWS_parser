#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   test.py
# Time    :   2023/02/23 19:53:28
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description : NTUWS parser 圖形化介面

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from main import *
#import csv
#import re

### 設定工作路徑
base_path = os.path.dirname(__file__)
os.chdir(base_path)


win = tk.Tk()
win.title('NTUWS 資料處理程式')
win.geometry('500x200')
# win.configure(bg='lightgray')
win.resizable(True, False)
# win.iconbitmap('icon.ico')

'''Label區域'''
# img = Image.open('NTUWS_logo.png').resize((131, 44))
# tk_img = ImageTk.PhotoImage(img)
# bn = tk.Label(image=tk_img)
# bn.pack(side='bottom', anchor=SW)

lb = tk.Label(text="輸入檔案", height=1)
lb.place(x=0 ,y=5)

lb2 = tk.Label(text="輸出路徑", height=1)
lb2.place(x=0 ,y=35)

lb3 = tk.Label(text="輸出檔名", height=1)
lb3.place(x=0 ,y=75)

'''Entry區域'''
loadFile_en = tk.Entry(width=40)
loadFile_en.place(x=70 ,y=5)

outpath_en = tk.Entry(width=40)
outpath_en.place(x=70 ,y=35)

outname_en = tk.Entry(width=40)
outname_en.place(x=70, y=75)
'''Entry區域'''

### 讀取檔案
def loadFile():
    if loadFile_en == None:
        file_path = filedialog.askopenfilename(filetypes = (("csv files","*.csv"),("all files","*.*")))
        loadFile_en.insert(0,file_path) 
    else:
        file_path = filedialog.askopenfilename(filetypes = (("csv files","*.csv"),("all files","*.*")))
        loadFile_en.delete(0,'end')
        loadFile_en.insert(0,file_path)

### 輸出路徑
def select_output_path():
    if outpath_en == None:
        output_path_ = filedialog.askdirectory()
        output_path.set(output_path_)
        outpath_en.insert(0,output_path)
    else:
        output_path = filedialog.askdirectory()
        outpath_en.delete(0,'end')
        outpath_en.insert(0,output_path)

### 輸出路徑
def output_name():
    if outname_en.get():
        return str(outname_en.get()) + '.csv'
    else:
        return 'NTUWS_output.csv'
    # if outname_en.get() == None:
    #     return 'NTUWS_output.csv'
    # else:
    #     return str(outname_en.get()) + '.csv'

### 主程式
# def Parser(Import: str):
#     #  讀檔
#     with open(Import) as file:
#         rows = csv.reader(file)
#         df = []
#         for row in rows:
#             df.append(row)
    
#     # 轉置資料
#     data = {}   # 以 Id為key, 後面的東西為values, 存成data
#     for i in range(1, len(df)):
#         # 取出每一列各元素
#         Id = df[i][0]
#         name = df[i][1]
#         email = df[i][3]
#         code = df[i][4]
#         Q = df[i][9]
#         typ = df[i][10]
#         A = df[i][11]
#         crt = df[i][12]

#         if Id not in data: # 若Id不在 data中
#             data[Id] = {'name': name, 'email': email,
#                     'code': code, 'crt': crt} # 則以該Id新增新的key
#             if (typ != 'DB') or (typ != 'DIVIDER'): # 若該列不是分割線等空元素
#                 # 排除Qualtrics答案中的系統符號 ['']
#                 A = re.sub("^\['", '', A)
#                 A = re.sub("'\]$", '', A)
#                 data[Id][Q] = A # 在該Id下新增題號的key, value為答案
#             else: # 若是分割線直接跳下一圈
#                 continue
#         else: # 若Id有在data中
#             if typ != 'DB': # 直接進新增答案步驟
#                 # 排除Qualtrics答案中的系統符號 ['']
#                 A = re.sub("^\['", '', A)
#                 A = re.sub("'\]$", '', A)
#                 data[Id][Q] = A
#             else:
#                 continue 

    # ### 製作表頭
    # header = ['ID'] + list(data[next(iter(data))].keys()) # 找出第一個key, 取出其value中所有的keys

    # ### 轉換data每一個元素為list
    # out = [header]
    # for k, v in data.items():
    #     out.append([k] + list(v.values()))
    
    # return out

### 輸出
def outFile():
    try:
        out = Parser(loadFile_en.get())
        with open(os.path.join(outpath_en.get(), output_name()), 'w', newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            for i in out:
                writer.writerow(i)
        messagebox.showinfo('message', 'Data parsed successfully!')
    except FileNotFoundError:
        messagebox.showinfo('Error', 'Incorrect input/output path')

'''Button區域'''
loadFile_btn = tk.Button(text="...",height=1, command=loadFile)
loadFile_btn.place(x=450 ,y=5)
outpath_btn = tk.Button(text="...",height=1, command=select_output_path)
outpath_btn.place(x=450 ,y=35)

output_btn = tk.Button(text="輸出",height=1, command=outFile)
output_btn.place(x=180, y=120)
'''Button區域'''
win.mainloop()