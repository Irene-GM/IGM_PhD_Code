# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 10:24:53 2015

@author: GarciaMartiI
"""

import csv
from collections import defaultdict
import datetime

def formatFields(ms, spr, summ, aut, win):
    date = datetime.datetime.fromtimestamp(ms/1000.0)
    if spr == "":
        spr = 0
    if summ == "":
        summ = 0
    if aut == "":
        aut = 0
    if win == "":
        win = 0
        
    spring = round(float(spr), 2)
    summer = round(float(summ), 2)
    autumn = round(float(aut), 2)
    winter = round(float(win), 2)
    return [date.strftime("%d-%m-%Y"), spring, summer, autumn, winter]


path_ndvi = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\features_calculated\vegetation\Accumulated_NDVI_seasons_random.csv'
path_evi = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\features_calculated\vegetation\Accumulated_EVI_seasons_random.csv'
path_ndwi = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\features_calculated\vegetation\Accumulated_NDWI_seasons_random.csv'
path_out = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\features_calculated\remotesensing.csv'

try:

    envidic = defaultdict(list)    
    
    fndvi = open(path_ndvi, "r")
    fevi = open(path_evi, "r")
    fndwi = open(path_ndwi, "r")
    fout = open(path_out, "wb")
    
    reader_ndvi = csv.reader(fndvi, delimiter=",")
    reader_evi = csv.reader(fevi, delimiter=",")
    reader_ndwi = csv.reader(fndwi, delimiter=",")
    writer = csv.writer(fout, delimiter=";")

    first = True    
    for row in reader_ndvi:        
        if first:
            first = False
        else:
            # system:index,autumn,date,id,latitude,longitude,spring,summer,timestamp,winter,geometry
            # 3,-0.07434239104365972,1009843200000,2.0,427805.600764,60001.1081186,0.3691572292388597,0.25515259185513844,1.0098396E12,-0.6706818875878012,"{""geodesic"":true,""type"":""Point"",""coordinates"":[4.0089736,51.8307492]}"
            key = int(float(row[3]))
            datems = int(row[2])
            spr = row[6]
            summ = row[7]
            aut = row[1]
            win = row[9]
            items_ndvi = formatFields(datems, spr, summ, aut, win)
            envidic[key] = items_ndvi

    first = True    
    for row in reader_evi:
        if first:
            first = False
        else:
            # [system:index,autumn,date,fall,id,spring,summer,timestamp,geometry]
            key = int(float(row[3]))
            spr = row[6]
            summ = row[7]
            aut = row[1]
            win = row[9]
            items_evi = formatFields(datems, spr, summ, aut, win)
            envidic[key].append(items_evi[1])
            envidic[key].append(items_evi[2])
            envidic[key].append(items_evi[3])
            envidic[key].append(items_evi[4])
            
    first = True    
    for row in reader_ndwi:
        if first:
            first = False
        else:
            # [system:index,autumn,date,fall,id,spring,summer,timestamp,geometry]
            key = int(float(row[3]))
            spr = row[6]
            summ = row[7]
            aut = row[1]
            win = row[9]
            items_ndwi = formatFields(datems, spr, summ, aut, win)
            envidic[key].append(items_ndwi[1])
            envidic[key].append(items_ndwi[2])
            envidic[key].append(items_ndwi[3])
            envidic[key].append(items_ndwi[4])
                    
    for key in sorted(envidic.keys()):
        item = [key] + envidic[key]
        if len(item) == 14:
            writer.writerow(item)
        

finally:
    fndvi.close()
    fevi.close()
    fndwi.close()
    fout.close()