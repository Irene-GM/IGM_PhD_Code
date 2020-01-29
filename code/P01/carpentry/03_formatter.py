# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 21:32:54 2015

@author: GarciaMartiI
"""

import csv

path_in = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\mdt.csv'
path_out = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\mdt_std.csv'

def format_num(item):
    num = int(float(item))
    return num

def format_rs(item):
    num = float(item) * 100
    return int(num)
    
def format_environment(item):
    it = int(item)
    environment = {"tuin":0, "bos":1, "heide":2, "weiland":3, "stadspark":4, "duinen":5, "moerasgebied":6, "anders":6, "weet niet":6, "weetniet":6, "":6}
    
    print environment[1]
    return environment[it]


def format_activity(item):
    it = int(item)
    activity = {"wandelen":0, "hond uitlaten":1, "honduitladen":1, "tuinieren":2, "picknicken":3, "groenbeheer":4, "spelen":5, "anders":6, "weet niet":6, "weetniet":6, "":6}
    return activity[it]

def format_bbg(item):
    landuse = {"Landbouw":0, "Glastuinbouw":0, "Bebouwd":1, "Semi-bebouwd":1, "Bedrijfsterrein":1, "Droog natuurlijk terrein":2, "Bos":3, "Recreatie":4, "Vliegveld": 5, "Spoorweg":5, "Hoofdweg":5, "Nat natuurlijk terrein":6, "Water":7, "Buitenland":7}
    return landuse[item]

def format_fisio(item):
    fisio = {"Afgesloten Zeearmen":0, "Duinen":1, "Hogere Zandgronden":2, "Heuvelland":3, "Getijdengebied":4, "Zeekleigebied":5, "Laagveengebied":6, "Niet indeelbaar":7, "Noordzee":8, "Rivierengebied":9}
    return fisio[item]

def format_soil(item):
    soil = {"Bebouwing, enz":0, "Leem":1, "Lichte klei": 2, "Zware klei": 2, "Lichte zavel":3, "Zware zavel":3, "Moerig op zand":4, "Veen":5, "Water":6, "Zand":7}
    return soil[item]
    
def format_weekday(item):
    weekday = {0:0, 1:0, 2:0, 3:0, 4:0, 5:1, 6:1}
    return weekday[item]

def format_distance(item):
    return int(item)

try:
    f = open(path_in, "r")
    fout = open(path_out, "wb")
    
    reader = csv.reader(f, delimiter=";")
    writer = csv.writer(fout, delimiter=";")
    
    # SAMPLE ROW
    # ---------------------------------------------------------------
    #   Meta:       15;14-02-2006; (1)
    #   Temp:       1101.3;1728.0;1065.84;235.38;131.75;60;32;7; (9)
    #   Prec:       180.34;48.0;154.65;58.0;255.72;40.0;122.93;45.0; (17)
    #   Sat:        6.73;6.78;6.81;4.0;
    #               3.23;3.46;2.74;1.65;
    #               -0.39;-0.09;-0.09;-0.32;
    #   Hum:        5;7;Zeeland;duinen;XXXX;
    #   LU:         Hoofdweg;
    #   Soil:       Hogere Zandgronden;
    #   Dist:       56.69;977.35;782.76
    # ---------------------------------------------------------------
    
    for row in reader:
        print row
        key = int(row[0])
        date = row[1].split(" ")[0]
        
        accspr = format_num(row[2])
        accsum = format_num(row[3])
        accaut = format_num(row[4])
        accwin = format_num(row[5])
        accdate = format_num(row[6])
        d20 = int(row[7])
        d25 = int(row[8])
        d30 = int(row[9])
        if accspr == 0:
            print row[2], accspr
            break
    
        precspr = format_num(row[10]) 
        norainspr = int(float(row[11]))
        precsum = format_num(row[12]) 
        norainsum = int(float(row[13]))
        precaut = format_num(row[14]) 
        norainaut = int(float(row[15]))
        precwin = format_num(row[16]) 
        norainwin = int(float(row[17]))
                
        
        ndvispr = format_rs(row[18])        
        ndvisum = format_rs(row[19])
        ndviaut = format_rs(row[20])
        ndviwin = format_rs(row[21])
        
        evispr = format_rs(row[22])
        evisum = format_rs(row[23])
        eviaut = format_rs(row[24])
        eviwin = format_rs(row[25])
        
        ndwispr = format_rs(row[26])
        ndwisum = format_rs(row[27])
        ndwiaut = format_rs(row[28])
        ndwiwin = format_rs(row[29])

        # NON-random observations      
        
        # weekday = format_weekday(int(row[30]))
        # woy = int(row[31])
        # env = format_environment(row[32])
        # actv = format_activity(row[33])
#        if row[34] == '':
#            agegroup = 3
#        else:
#            agegroup = int(row[34])
        
        # Random observations
        weekday = int(row[30])
        woy = int(row[31])
        env = int(row[32])
        actv = int(row[33])
        agegroup = int(row[34])
        
        
        landuse = format_bbg(row[35])
        soil = format_soil(row[36])
        fisio = format_fisio(row[37])
        dforests = int(float(row[38]))
        drec = int(float(row[39]))
        dbuiltup = int(float(row[40]))
        
        part1 = [key, date, accspr, accsum, accaut, accwin, accdate, d20, d25, d30]
        part2 = [precspr, norainspr, precsum, norainsum, precaut, norainaut, precwin, norainwin]
        part3 = [ndvispr, ndvisum, ndviaut, ndviwin, evispr, evisum, eviaut, eviwin, ndwispr, ndwisum, ndwiaut, ndwiwin]
        part4 = [weekday, woy, env, actv, agegroup]
        part5 = [landuse, soil, fisio, dforests, drec, dbuiltup]
        
        row = part1 + part2 + part3 + part4 + part5
        writer.writerow(row)
    
finally:
    f.close()
    fout.close()

