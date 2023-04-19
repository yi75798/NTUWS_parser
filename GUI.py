#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   GUI.py
# Time    :   2023/02/23 19:53:28
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description : NTUWS parser 圖形化介面

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
# from Main.main import Parser
import csv
import re

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

lb1 = tk.Label(text="檔案來源", height=1)
lb1.place(x=0 ,y=35)

lb2 = tk.Label(text="輸出路徑", height=1)
lb2.place(x=0 ,y=75)

lb3 = tk.Label(text="輸出檔名", height=1)
lb3.place(x=0 ,y=120)

'''Entry區域'''
loadFile_en = tk.Entry(width=40)
loadFile_en.place(x=70 ,y=5)

outpath_en = tk.Entry(width=40)
outpath_en.place(x=70 ,y=75)

outname_en = tk.Entry(width=40)
outname_en.place(x=70, y=120)
'''Entry區域'''

'''RadioButton'''
radioVar = tk.IntVar()
radio1 = tk.Radiobutton(text='Qualtrics', variable=radioVar, value=1)
radio2 = tk.Radiobutton(text='SurveyCake', variable=radioVar, value=2)

radio1.place(x= 100, y= 35)
radio2.place(x= 200, y= 35)
'''RadioButton'''

### 讀取檔案
def loadFile():
    if loadFile_en == None:
        file_path = filedialog.askopenfilename(filetypes = (("csv files","*.csv"),("all files","*.*")))
        loadFile_en.insert(0,file_path) 
    else:
        file_path = filedialog.askopenfilename(filetypes = (("csv files","*.csv"),("all files","*.*")))
        loadFile_en.delete(0,'end')
        loadFile_en.insert(0,file_path)

### 主程式
def Parser(Import: str, datatype: int):
    #  讀檔
    with open(Import) as file:
        rows = csv.reader(file)
        df = []
        for row in rows:
            df.append(row)
    
    ### Qualtrics
    if datatype == 1:
        # 建立表頭
        header = ['Id', 'name', 'phone', 'email',
                  'code', 'create_at']
        # 抓出所有QID
        unique = []
        for i in range(1, len(df)):
            Q = df[i][9]
            typ = df[i][10]
            if typ != 'DB': # 不管是不是matrix，先加母題號
                if Q in unique:
                    continue
                else:
                    unique.append(Q)
        matrix = set()
        for i in range(1, len(df)): # 處理matrix
            Q = df[i][9]
            typ = df[i][10]
            A = df[i][11]
            if typ in ('Matrix', 'Slider'):
                matrix.add(Q)
                A = eval(A)
                for QA in A: # 抓出 {問:答} 組
                    MQ = QA['label'] # 子題題目
                    MQ = Q+"_"+MQ
                    if MQ not in unique:
                        loc = unique.index(Q)
                        unique = unique[:loc+1] + [MQ] + unique[loc+1:]
                    else:
                        continue
        for i in matrix:
            unique.remove(i)
        header += unique

        ### 填入每個樣本題：答
        data = {}
        for i in range(1, len(df)):
            # 取出每一列各元素
            Id = df[i][0]
            name = df[i][1]
            phone = df[i][2]
            email = df[i][3]
            code = df[i][4]
            Q = df[i][9]
            typ = df[i][10]
            A = df[i][11]
            crt = df[i][12]

            if Id not in data:
                data[Id] = {k:'' for k in header}
                # 輸入基本資料
                data[Id]['Id'] = Id
                data[Id]['name'] = name
                data[Id]['phone'] = phone
                data[Id]['email'] = email
                data[Id]['code'] = code
                data[Id]['create_at'] = crt

                if (typ != 'DB') & (typ not in ['Matrix', 'Slider']): # 非分隔號、非網格題直接進新增答案步驟
                    # 排除Qualtrics答案中的系統符號 ['']
                    A = re.sub("^\['", '', A)
                    A = re.sub("'\]$", '', A)
                    data[Id][Q] = A
                elif (typ != 'DB') & (typ in ['Matrix', 'Slider']): # 網格題處理
                    A = eval(A)
                    for QA in A: # 抓出 {問:答} 組
                        MQ = QA['label'] # 子題題目
                        MA = QA['value'] # 子題答案
                        data[Id][Q+'_'+MQ] = MA # 在題號後加 _子題題號
                else:
                    continue
            else:
                if (typ != 'DB') & (typ not in ['Matrix', 'Slider']): # 非分隔號、非網格題直接進新增答案步驟
                    # 排除Qualtrics答案中的系統符號 ['']
                    A = re.sub("^\['", '', A)
                    A = re.sub("'\]$", '', A)
                    data[Id][Q] = A
                elif (typ != 'DB') & (typ in ['Matrix', 'Slider']): # 網格題處理
                    A = eval(A)
                    for QA in A: # 抓出 {問:答} 組
                        MQ = QA['label'] # 子題題目
                        MA = QA['value'] # 子題答案
                        data[Id][Q+'_'+MQ] = MA # 在題號後加 _子題題號
                else:
                    continue

        ### 轉換data每一個元素為list
        out = [header]
        for v in data.values():
            out.append(list(v.values()))
        
        return out

    ### Survey Cake
    if datatype == 2:
    # 轉置資料
        data = {}   # 以 Id為key, 後面的東西為values, 存成data
        for i in range(1, len(df)):
            # 取出每一列各元素
            Id = df[i][0]
            name = df[i][1]
            phone = df[i][2]
            email = df[i][3]
            code = df[i][4]
            Q = df[i][8]
            typ = df[i][9]
            A = df[i][10]
            crt = df[i][11]

            if Id not in data: # 若Id不在 data中
                data[Id] = {'name': name, 'email': email,
                        'code': code, 'creat_at': crt} # 則以該Id新增新的key
                if typ != 'DIVIDER': # 若該列是分割線等空元素
                    data[Id][Q] = A
                else:
                    continue # 跳過
            else: # 若Id有在data中
                if typ != 'DIVIDER': # 直接進新增答案步驟
                    data[Id][Q] = A
                else:
                    continue 
        ### 製作表頭
        header = ['ID'] + list(data[next(iter(data))].keys()) # 找出第一個key, 取出其value中所有的keys

        ### 轉換data每一個元素為list
        out = [header]
        for k, v in data.items():
            out.append([k] + list(v.values()))
        
        return out

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

### 輸出
def outFile():
    try:
        if radioVar.get() == 1:
            out = Parser(loadFile_en.get(), 1)
        elif radioVar.get() == 2:
            out = Parser(loadFile_en.get(), 2)
        else:
            return messagebox.showinfo('message', '請選擇檔案來源')
        with open(os.path.join(outpath_en.get(), output_name()), 'w', newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            for i in out:
                writer.writerow(i)
        messagebox.showinfo('message', f'Data parsed successfully!\n請記得更新輸出檔案header為題號')
    except FileNotFoundError:
        messagebox.showinfo('Error', 'Incorrect input/output path')

'''Button區域'''
loadFile_btn = tk.Button(text="...",height=1, command=loadFile)
loadFile_btn.place(x=450 ,y=5)
outpath_btn = tk.Button(text="...",height=1, command=select_output_path)
outpath_btn.place(x=450 ,y=75)

output_btn = tk.Button(text="輸出",height=1, command=outFile)
output_btn.place(x=180, y=160)
'''Button區域'''
win.mainloop()