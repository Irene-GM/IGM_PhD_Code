# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 21:15:27 2015

@author: GarciaMartiI
"""

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
               "landuse", "soil", "dforests", "drec", "dbuiltup"]

path = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\rules\test32.csv'
path_index = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\mdt_cluster_index.csv'

index = []
i = 0
j = 0
k = 0
dic = defaultdict(list)

try:
    f = open(path, "r")
    findex = open(path_index, "r")
    
    reader = csv.reader(f, delimiter=";")
    readerindex = csv.reader(findex, delimiter=";")
    
    for row in readerindex:
        newrow = [int(float(item)) for item in row]
        index.append(newrow)
    
    for row in index:
        dic[header[k]] = row
        k += 1
    
    for row in reader:
        anotherrow = []
        for item in row[0:3]:
            feature = int(item[2:4])
            cluster = int(item[4:6])
            l = dic[header[feature]]
            anotherrow.append((header[feature], index[feature][cluster-1], index[feature][cluster]))
            j += 1
        anotherrow.append(row[3])
        print anotherrow
        i+=1



finally:
    f.close()
    findex.close()