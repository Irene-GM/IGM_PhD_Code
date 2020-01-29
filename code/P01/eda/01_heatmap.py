# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 13:33:08 2015

@author: GarciaMartiI
"""

import csv
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

path = r'\\ad.utwente.nl\home\GarciaMartiI\Documents\workspace\Special\TGIS\results\rules\heatmap\output_AprioriClose_39features_25.csv'
pathnk = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\separate\AprioriClose_39features_NK25.csv'
pathtr = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\results\separate\AprioriClose_39features_TR25.csv'
pathran = r'\\ad.utwente.nl\home\garciamartii\Documents\workspace\Special\TGIS\inputRandom10km\TB_breaks\patterns\output_AprioriClose_39features_25_TB_breaks_10km.csv'
# path_out = r'\\ad.utwente.nl\home\GarciaMartiI\Documents\workspace\Special\TGIS\results\rules\heatmap\heatmap.csv'
labels = [     "accspr", "accsum", "accaut", "accwin", "accdate", "d20", "d25", "d30", 
               "precspr", "norainspr", "precsum", "norainsum", "precaut", "norainaut", "precwin", "norainwin",
               "ndvispr", "ndvisum", "ndviaut", "ndviwin", "evispr", "evisum", "eviaut", "eviwin", "ndwispr", "ndwisum", "ndwiaut", "ndwiwin",
               "weekday", "woy", "env", "actv", "agegroup", 
               "landuse", "soil", "fisio", "dforests", "drec", "dbuiltup"]
               
classes = [ "4", "3", "2", "1"]

def colorbar_index(maximum, mat, ncolors,  cmap):
    cmap = cmap_discretize(cmap, ncolors)
    
    mappable = cm.ScalarMappable(cmap=cmap)
    mappable.set_array([])
    mappable.set_clim(0, maximum)
    colorbar = plt.colorbar(mappable, orientation="horizontal", shrink=0.5, pad=0.2)
    colorbar.set_label('Frequency')
    # ticks = np.array([0, 4, 8, 12,17, 22, 26, 30])
    # colorbar.set_ticks(np.linspace(0, maximum, 7))
    # colorbar.set_ticks(ticks)
    # colorbar.set_ticklabels(range(1, int(maximum), 1))


def cmap_discretize(cmap, N):
    """Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet. 
        N: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)
    """
    
    if type(cmap) == str:
        cmap = plt.get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1., N), (0.,0.,0.,0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., N+1)
    cdict = {}
    for ki,key in enumerate(('red','green','blue')):
        cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki])
                       for i in xrange(N+1) ]

    # Return colormap object.
    return mcolors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)

def heatmap(reader):
    for row in reader:
        if len(row)>3:
            sublist = row[:-1]
            for item in sublist:
                feature = int(item[2:4])
                cluster = int(item[4:6])
                key = str(feature) + " " + str(cluster)
                dic[key] += 1
                
    print "dic 2 de 2: ", dic['2 2']
    print dic
    mymat = np.zeros((4, 39))
    mat = np.zeros((3, 39))
    value34 = 0    
    
    value36 = 0
    value37 = 0
    value38 = 0
    
    for key in dic.keys():
        value = dic[key]
        feature, classs = key.split(" ")
        if int(feature) == 28:
            mat[int(classs)+1, feature] = value
        elif int(feature) == 34:
            value34 = value
        elif int(feature) == 31:
            mat[int(classs)+1, feature] = value
        # Only for NK
        elif int(feature) == 36:
            value36 = value
        elif int(feature) == 37:
            value37 = value
        elif int(feature) == 38:
            value38 = value
            
            
        else:
            mat[int(classs)-2, feature] = value

    mymat[:-1,:] = mat
    mymat[3, 34] = value34
    
    mymat[0, 36] = value36
    mymat[0, 37] = value37
    mymat[0, 38] = value38

    return mymat


index = []
translated = []
i = 0
j = 0
k = 0
dic = defaultdict(int)

try:
    f = open(path, "r")
    fnk = open(pathnk, "r")
    ftr = open(pathtr, "r")
    fran = open(pathran, "r")
    reader = csv.reader(f, delimiter=";")
    readernk = csv.reader(fnk, delimiter=";")
    readertr = csv.reader(ftr, delimiter=";")
    readerran = csv.reader(fran, delimiter=";")
    
    # plt.imshow(mymat[::-1], interpolation='None', cmap="Paired")
        
    mat = heatmap(reader)
    print "Maximum: ", mat.max()
    maximum = mat.max()
    cmap = plt.get_cmap('gray_r')
    colorbar_index(maximum, mat, ncolors=7, cmap=cmap)    
    x = np.linspace(0, 39, 40)
    y = np.linspace(0, 4, 5)
    plt.imshow(mat[::-1], interpolation='None', cmap=cmap)
    plt.xticks(x, labels, rotation=70)
    plt.yticks(y, classes)
    plt.title("(a)\nHeat map of features and its classes produced mining NK+TR")
    plt.ylabel("Class")
    plt.xlabel("Feature")
    plt.show()
        
finally:
    f.close()
