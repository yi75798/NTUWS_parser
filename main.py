#!/usr/bin/python
# -*- encoding: utf-8 -*-
# File    :   main.py
# Time    :   2023/03/20 19:25:25
# Author  :   Hsu, Liang-Yi 
# Email:   yi75798@gmail.com
# Description : NTUWS parser 主程式
import csv
import re

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

if __name__ == '__main__':
    QTout = Parser('QT_test4.csv', 1)
    with open('QT_out_test4.csv', 'w', newline='', encoding='utf_8_sig') as csvFile:
            writer = csv.writer(csvFile)
            for i in QTout:
                writer.writerow(i)
    
    SCout = Parser('SC_test2.csv', 2)
    with open('SC_out_test.csv', 'w', newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            for i in SCout:
                writer.writerow(i)

