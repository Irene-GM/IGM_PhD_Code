# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 12:44:21 2015

@author: irene
"""

import csv
import numpy as np
import re


header = [    "accspr", "accsum", "accaut", "accwin", "accdate", "d20", "d25", "d30",
              "precspr", "norainspr", "precsum", "norainsum", "precaut", "norainaut", "precwin", "norainwin",
              "ndvispr", "ndvisum", "ndviaut", "ndviwin", "evispr", "evisum", "eviaut", "eviwin", "ndwispr", "ndwisum", "ndwiaut", "ndwiwin",
              "weekday", "woy", "env", "actv", "agegroup",
              "landuse", "soil", "fisio", "dforests", "drec", "dbuiltup"]



path = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\mdt_cluster_raw.csv'
path_out = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\mdt_integers.csv'


def convertToInt(mat):
    j = 0
    newcol = []
    cols = []
    for feature in mat.T:
        for v in feature:
            number = re.findall(r"\d+", v[0])
            if j < 10:
                newstr = str(99) + str(0) + str(j) + str(0) + str(number[0])
                newvalue = int(newstr)
                newcol.append(newvalue)
            elif j >= 10:
                newstr = str(99) + str(j) + str(0) + str(number[0])
                newvalue = int(newstr)
                newcol.append(newvalue)
        cols.append(newcol)
        newcol = []
        j += 1
    m = np.array(cols)
    m.astype(int)
    return m.T


transactions = []
m = []
try:
    f = open(path, "r")
    fout = open(path_out, "wb")
    reader = csv.reader(f, delimiter=";")
    # writer = csv.writer(fout, delimiter=" ")
    
    for row in reader:
        transactions.append(row)    
    m = np.array(transactions)
    mint = convertToInt(m)

    np.savetxt(path_out, mint.astype(int), fmt="%d", delimiter=" ")
    print mint.shape
    
finally:
    f.close()
    fout.close()

    