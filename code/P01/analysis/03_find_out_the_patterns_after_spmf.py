# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 20:58:45 2015

@author: GarciaMartiI
"""

import csv
from collections import defaultdict

header = ["accspr", "accsum", "accaut", "accwin", "accdate", "d20", "d25", "d30",
          "precspr", "norainspr", "precsum", "norainsum", "precaut", "norainaut", "precwin", "norainwin",
          "ndvispr", "ndvisum", "ndviaut", "ndviwin", "evispr", "evisum", "eviaut", "eviwin", "ndwispr", "ndwisum",
          "ndwiaut", "ndwiwin",
          "weekday", "woy", "env", "actv", "agegroup",
          "landuse", "soil", "fisio", "dforests", "drec", "dbuiltup"]

path = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\rules\output_AprioriClose_39features_25.csv'
path_index = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\mdt_cluster_index.csv'
path_out = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\table_39features_25.csv'

index = []
translated = []
i = 0
j = 0
k = 0
dic = defaultdict(list)

try:
    fout = open(path_out, "wb")
    f = open(path, "r")
    findex = open(path_index, "r")

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
        if len(row) > 2:
            sublist = row[:-1]
            for item in sublist:
                feature = int(item[2:4])
                cluster = int(item[4:6])
                l = dic[header[feature]]
                anotherrow.append((header[feature], cluster))
                j += 1
            anotherrow.append(row[-1])
            translated.append(anotherrow)
            i += 1

    pieces = []
    patterns = []
    for row in translated:
        for tup in row[:-1]:
            key = tup[0]
            item = int(tup[1])
            if len(dic[key]) == item:
                what = dic[key][item - 1]
            elif item == 0:
                what = dic[key][item + 1]
            else:
                what = dic[key][item - 1], dic[key][item]
            pieces.append((key, what))
        pieces.append(row[-1])
        patterns.append(pieces)
        pieces = []

    for piece in patterns:
        print
        piece
        newrow = []
        for item in piece[:-1]:
            key = item[0]
            if isinstance(item[1], (int, long)):
                breaks = str(item[1])
            else:
                breaks = str(item[1][0]) + "-" + str(item[1][1])
            newrow.append(key)
            newrow.append(breaks)
        newrow.append(int(piece[-1]))
        if len(newrow) > 5:
            writer.writerow(newrow)


finally:
    f.close()
    fout.close()
    findex.close()