# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 12:07:04 2015

@author: GarciaMartiI
"""

from collections import defaultdict
import csv
import time
import datetime


try:

    dic = defaultdict(list)        
    path_prec = r"D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\precipitation.csv"
    fprec = open(path_prec, "r")
    
    path_forests = r"D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\randomForest.csv"
    fforests = open(path_forests, "r")
    
    path_soil = r"D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\randomSoil.csv"
    fsoil = open(path_soil, "r")
    
    path_rs = r"D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\remotesensing.csv"
    frs = open(path_rs, "r")
    
    path_humans = r"D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\humans.csv"
    fh = open(path_humans, "r")
    
    path_bbg = r"D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\randomBBG.csv"
    fbbg = open(path_bbg, "r")

    path_fisio = r"D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\randomFisio.csv"
    ffisio = open(path_fisio, "r")

    path_recreation = r"D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\randomRecreation.csv"
    frec = open(path_recreation, "r")

    path_builtup = r"D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\randomBuiltup.csv"
    fbuilt = open(path_builtup, "r")

    path_temp = r"D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\temperature.csv"
    ftemp = open(path_temp, "r")

    path_out = r"D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\mdtsuperrandom.csv"
    fout = open(path_out, "wb")
    
    readerrs = csv.reader(frs, delimiter=";")
    readerh = csv.reader(fh, delimiter=";")
    readerbbg = csv.reader(fbbg, delimiter=";")
    readersoil = csv.reader(fsoil, delimiter=";")
    readerforests = csv.reader(fforests, delimiter=";")
    readerrec = csv.reader(frec, delimiter=";")
    readerbuilt = csv.reader(fbuilt, delimiter=";")
    readerprec = csv.reader(fprec, delimiter=";")
    readerfisio = csv.reader(ffisio, delimiter=";")
    readertemp = csv.reader(ftemp, delimiter=";")
    
    
    writer = csv.writer(fout, delimiter=";")
    lost = 0
    for row in readertemp:
        key = int(row[0])
        accspr = round(float(row[2]), 2)
        accsum = round(float(row[3]), 2)
        accaut = round(float(row[4]), 2)
        accwin = round(float(row[5]), 2)
        accdate = round(float(row[6]), 2)
        d20 = int(row[7])
        d25 = int(row[8])
        d30 = int(row[9])
        if accspr != 0:
            current = dic[key]
            temps = [accspr, accsum, accaut, accwin, accdate, d20, d25, d30]
            dic[key] = temps
        else:
            lost += 1
    print "Lost Temp: ", lost
    
    lost = 0
    for row in readerprec:        
        # This: 
        # [acc_spring, norainspr] + [acc_summer, norainsum] + [acc_autumn, norainaut] + [acc_winter, norainwin] + [acc_until_date]
        key = int(row[0])
        accspr = round(float(row[2]), 2)
        norainspr = float(row[3])
        accsum = round(float(row[4]), 2)
        norainsum = float(row[5])
        accaut = round(float(row[6]), 2)
        norainaut = float(row[7])
        accwin = round(float(row[8]), 2)
        norainwin = float(row[9])
        if accspr != 0:
            current = dic[key]       
            precs = current + [accspr, norainspr, accsum, norainsum, accaut, norainaut, accwin, norainwin]
            dic[key] = precs
        else:
            lost += 1
    print "Lost Precs: ", lost
    
    for row in readerrs:
        d, m, y = [int(item) for item in row[1].split(" ")[0].split("-")]
        date = datetime.datetime(year=y, month=m, day=d)
        datestr = date.strftime("%d-%m-%Y")
        key = int(row[0])    
        current = dic[key]
        if len(current) > 0:
            newrow = current + row[2:]
            newnewrow = [datestr] + newrow
            dic[key] = newnewrow
    
    for row in readerh:
        key = int(row[0])
        current = dic[key]
        dic[key] = current + row[2:]

    for row in readerbbg:
        key = int(row[0])
        lu = row[1]
        current = dic[key]
        dic[key] = current + [lu]
        
    for row in readersoil:
        key = int(row[0])
        soil = row[1]
        current = dic[key]
        dic[key] = current + [soil]
        
    for row in readerfisio:
        key = int(row[0])
        fisio = row[1]
        current = dic[key]
        dic[key] = current + [fisio]

    for row in readerforests:
        key = int(row[0])        
        dforest = round(float(row[1]), 2)
        current = dic[key]
        dic[key] = current + [dforest]
        
    for row in readerrec:
        key = int(row[0])
        drec = round(float(row[1]), 2)
        current = dic[key]
        dic[key] = current + [drec]
        
    for row in readerbuilt:
        key = int(row[0])
        dbuilt = round(float(row[1]), 2)
        current = dic[key]
        dic[key] = current + [dbuilt]
                
    count39 = 0
    others = 0
    for key in sorted(dic.keys()):
        if len(dic[key]) == 40:
            row = [key] + dic[key]
            writer.writerow(row)
            count39 += 1
        else:
            others += 1
    
    print "Complete observations: ", count39
    print "Incomplete observations: ", others
    print "Keys in dic: ", len(dic.keys())
        
finally:
    frs.close()
    #ftemp.close()
    fprec.close()
    fforests.close()
    fsoil.close()
    fbbg.close()
    fbuilt.close()
    frec.close()
    fout.flush()
    fout.close()
    fh.close()



