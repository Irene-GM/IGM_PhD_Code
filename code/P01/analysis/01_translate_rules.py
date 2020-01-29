# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:05:06 2015

@author: GarciaMartiI
"""

import csv
from collections import defaultdict

header = [     "accspr", "accsum", "accaut", "accwin", "accdate", "d20", "d25", "d30", 
               "precspr", "norainspr", "precsum", "norainsum", "precaut", "norainaut", "precwin", "norainwin",
               "ndvispr", "ndvisum", "ndviaut", "ndviwin", "evispr", "evisum", "eviaut", "eviwin", "ndwispr", "ndwisum", "ndwiaut", "ndwiwin",
               "weekday", "woy", "env", "actv", "agegroup", 
               "landuse", "soil", "fisio", "dforests", "drec", "dbuiltup"]

#path = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\rules\output_AprioriClose_39features_20.csv'
#path_out = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\rules\rules_AprioriClose_39features_20_REMOVEME.csv'
#path_index = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\mdt_cluster_index.csv'

#path = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\separate\AprioriClose_39features_TR25.csv'
#path_out = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\separate\rules_AprioriClose_39features_TR25.csv'
#path_index = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\mdt_cluster_index.csv'

#path = r'\\ad.utwente.nl\home\GarciaMartiI\Documents\workspace\Special\TGIS\inputRandom10km\TB_breaks\patterns\output_AprioriClose_39features_25_TB_breaks_10km.csv'
#path_out = r'\\ad.utwente.nl\home\GarciaMartiI\Documents\workspace\Special\TGIS\inputRandom10km\TB_breaks\patterns\rules_AprioriClose_39features_25_TB_breaks_10km.csv'
#path_index = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\mdt_cluster_index.csv'

path = r'\\ad.utwente.nl\home\GarciaMartiI\Documents\workspace\Special\TGIS\superrandom\data\patterns\output_AprioriClose_39features_25.csv'
path_out = r'\\ad.utwente.nl\home\GarciaMartiI\Documents\workspace\Special\TGIS\superrandom\data\patterns\rules_AprioriClose_39features_25.csv'
path_index = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\mdt_cluster_index.csv'



index = []
translated = []
i = 0
j = 0
k = 0
dic = defaultdict(list)

try:
    f = open(path, "r")
    findex = open(path_index, "r")
    fout = open(path_out, "wb")
    
    reader = csv.reader(f, delimiter=";")
    readerindex = csv.reader(findex, delimiter=";")
    writer = csv.writer(fout, delimiter=";")
    
    for row in readerindex:
        newrow = [int(float(item)) for item in row]
        index.append(newrow)
    
    for row in index:
        dic[header[k]] = row
        k += 1
    
    for row in reader:
        anotherrow = []
        if len(row)>2:
            sublist = row[:-1]
            for item in sublist:
                feature = int(item[2:4])
                cluster = int(item[4:6])
                l = dic[header[feature]]
                anotherrow.append(header[feature])
                j += 1
            anotherrow.append(row[-1])
            translated.append(anotherrow)
            i+=1

    for row in translated:
        writer.writerow(row)


finally:
    f.close()
    findex.close()
    fout.close()