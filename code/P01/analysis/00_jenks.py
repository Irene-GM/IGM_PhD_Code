# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 15:02:22 2015

@author: GarciaMartiI
"""

import csv
import numpy as np
from jenks import jenks
import re


header = [     "id", "date",
               "accspr", "accsum", "accaut", "accwin", "accdate", "d20", "d25", "d30", 
               "precspr", "norainspr", "precsum", "norainsum", "precaut", "norainaut", "precwin", "norainwin",
               "ndvispr", "ndvisum", "ndviaut", "ndviwin", "evispr", "evisum", "eviaut", "eviwin", "ndwispr", "ndwisum", "ndwiaut", "ndwiwin",
               "weekday", "woy", "env", "actv", "agegroup", 
               "landuse", "soil", "fisio", "dforests", "drec", "dbuiltup"]


def choose_breaks(name):
    weekday = range(0, 2)
    env = range(0, 8)
    actv = range(0, 8)
    age = range(0, 3)
    landuse = range(0, 8)
    soil = range(0, 8)    
    fisio = range(0, 10)
    if name == "weekday":
        return weekday
    elif name == "env":
        return env
    elif name == "actv":
        return actv
    elif name == "agegroup":
        return age
    elif name == "landuse":
        return landuse
    elif name == "fisio":
        return fisio
    else:
        return soil
        

def remove_columns(mat, l):
    idx = range(0, len(mat.T))
    for item in l:
        idx.remove(item)
    m = mat[:, idx]  
    return m

def getBreaksForFeature(j, lbreaks):
    intify = [int(float(item)) for item in lbreaks[j]]
    return intify
    

def classify(value, breaks):
    for i in range(1, len(breaks)):
        if value < breaks[i]:
            return i
    return len(breaks) - 1


def classify_features(m, lbreaks):
    clustered = []
    chars = []
    specials = [ "weekday", "env", "actv", "agegroup", "landuse", "soil", "fisio"]
    j = 2
    for feature in m.T:      
        print "Feature: ", header[j]
        if header[j] not in specials:
            breaks = getBreaksForFeature(j-2, lbreaks)
            print breaks
            classified = np.array([classify(i, breaks) for i in feature]).tolist()
            clustered.append(classified)        
            row = [str(item) + header[j] for item in classified]
            chars.append(row)
        else:    
            noclassified = [str(item) + header[j] for item in feature]
            clustered.append(feature.tolist())    
            chars.append(noclassified)
            row = []
            breaks = choose_breaks(header[j])
        j += 1

    mdtc = np.array(clustered)
    mdtd = np.array(chars)
    # mdtb = np.array(allbreaks)
    print mdtc.T.shape
    print mdtd.T.shape
    return mdtc.T, mdtd.T


# This is the index of the TICK BITES (NATUURKALENDER + TEKENRADAR)
path_index = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\mdt_cluster_index.csv'

# PATHS TO RECLASSIFY THE EXPERIMENT WITH 10KM
path_in = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\mdtrandom_std.csv'
path_out = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\mdtrandom_cluster_tags_TB_breaks_10km.csv'
path_cluster = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\mdtrandom_cluster_raw_TB_breaks_10km.csv'

# PATH TO RECLASSIFY THE EXPERIMENT WITH 5KM
path_in_5km = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\mdtrandom_std.csv'
path_out_5km = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\mdtrandom_cluster_tags_TB_breaks_5km.csv'
path_cluster_5km = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\in\mdtrandom_cluster_raw_TB_breaks_5km.csv'

try:
    
    m = []    
    classes = []
    toremove = []    
    f = open(path_in_5km, "r")
    findex = open(path_index, "r")
        
    reader = csv.reader(f, delimiter=";")    
    readerbreaks = csv.reader(findex, delimiter=";")
    
    for row in reader:
        intify = [int(item) for item in row[2:]]
        m.append(intify)
        
    for row in readerbreaks:
        classes.append(row)
        
    mdt = np.array(m)
    mdtr = remove_columns(mdt, toremove)
    mdtc, mdtd = classify_features(mdtr, classes)
    
    # np.savetxt(path_out, mdtc.astype(int), fmt='%i', delimiter=";")
    # np.savetxt(path_out_5km, mdtd.astype(str), fmt='%s', delimiter=";")
    # np.savetxt(path_cluster_5km, mdtc.astype(str), fmt="%s", delimiter=";")
    
#    for row in allbreaks:
#        writer.writerow(row)
    

finally:
    f.close()
    findex.close()