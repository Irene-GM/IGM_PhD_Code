# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 19:54:49 2015

@author: GarciaMartiI
"""

from collections import defaultdict
import csv
import time
import datetime

#path_rs = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_tickbites\remotesensing.csv'
#path_humans = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_tickbites\humans.csv'
#path_bbg = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_tickbites\landuse.csv'
#path_soil = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_tickbites\newSoil.csv'
#path_fisio = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_tickbites\soil.csv'
#path_forests = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_tickbites\forest.csv'
#path_builtup = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_tickbites\builtup.csv'
#path_recreation = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_tickbites\recreation.csv'
#path_temp = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_tickbites\temperature.csv'
#path_prec = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_tickbites\precipitation.csv'
#path_out = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_tickbites\mdtrandom.csv'

path_rs = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\remotesensing.csv'
path_humans = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\humans.csv'
path_bbg = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\randomBBG.csv'
path_soil = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\randomSoil.csv'
path_fisio = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\randomFisio.csv'
path_forests = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\randomForest.csv'
path_builtup = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\randomBuiltup.csv'
path_recreation = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\randomRecreation.csv'
path_temp = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\temperature.csv'
path_prec = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\exp_random_points_10k\precipitation.csv'
path_out = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\inputRandom\mdtrandom.csv'

try:

    dic = defaultdict(list)    
    
    fprec = open(path_prec, "r")
    fforests = open(path_forests, 'r')
    fsoil = open(path_soil, 'r')
    frs = open(path_rs, 'r')
    fh = open(path_humans, 'r')
    fbbg = open(path_bbg, 'r')
    ffisio = open(path_fisio, "r")
    frec = open(path_recreation, 'r')
    fbuilt = open(path_builtup, 'r')
    ftemp = open(path_temp, 'r')
    fout = open(path_out, "wb")
    
    readerrs = csv.reader(frs, delimiter=";")
    readerh = csv.reader(fh, delimiter=";")
    readerbbg = csv.reader(fbbg, delimiter=";")
    readersoil = csv.reader(fsoil, delimiter=";")
    readerforests = csv.reader(fforests, delimiter=";")
    readerrec = csv.reader(frec, delimiter=";")
    readerbuilt = csv.reader(fbuilt, delimiter=";")
    readertemp = csv.reader(ftemp, delimiter=";")
    readerprec = csv.reader(fprec, delimiter=";")
    readerfisio = csv.reader(ffisio, delimiter=";")
    
    writer = csv.writer(fout, delimiter=";")
    lost = 0
    for row in readertemp:
        key = int(row[0])
        accspr = round(float(row[1]), 2)
        accsum = round(float(row[2]), 2)
        accaut = round(float(row[3]), 2)
        accwin = round(float(row[4]), 2)
        accdate = round(float(row[5]), 2)
        d20 = int(row[6])
        d25 = int(row[7])
        d30 = int(row[8])
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
        accspr = round(float(row[1]), 2)
        norainspr = float(row[2])
        accsum = round(float(row[3]), 2)
        norainsum = float(row[4])
        accaut = round(float(row[5]), 2)
        norainaut = float(row[6])
        accwin = round(float(row[7]), 2)
        norainwin = float(row[8])
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
        datestr = date.strftime('%d-%m-%Y')
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
    ftemp.close()
    fprec.close()
    fforests.close()
    fsoil.close()
    fbbg.close()
    fbuilt.close()
    frec.close()
    fout.flush()
    fout.close()
    fh.close()



