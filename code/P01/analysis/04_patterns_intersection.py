# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 14:38:38 2015

@author: GarciaMartiI
"""

from __future__ import division
import csv
import numpy as np

pathp1 = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\clusters\pattern1\{0}.csv'
pathp2 = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\clusters\pattern2\thisone\{0}.csv'
pathp3 = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\clusters\accwin-d25-d30\{0}.csv'
pathp4 = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\clusters\accwin-d25-norainsum\{0}.csv'
pathp5 = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\clusters\accwin-d25-dforests\{0}.csv'
pathp6 = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\clusters\accwin-d20-d25\{0}.csv'
pathp7 = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\clusters\fisio-soil-dforests\{0}.csv'
pathp8 = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\clusters\soil-dbuiltup-drec\{0}.csv'
pathp9 = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\clusters\dforests-dbuiltup-drec\{0}.csv'

tbyear = [1843, 1565, 1015, 2186, 1085, 1175, 6250, 7615, 5816]

for year in range(2006, 2015):
    lp1 = []
    lp2 = []        
    lp3 = []     
    lp4 = []     
    lp5 = []     
    lp6 = []     
    lp7 = []     
    lp8 = []     
    lp9 = []     
    try:
        fp1 = open(pathp1.format(year))
        fp2 = open(pathp2.format(year))
        fp3 = open(pathp3.format(year))
        fp4 = open(pathp4.format(year))
        fp5 = open(pathp5.format(year))
        fp6 = open(pathp6.format(year))
        fp7 = open(pathp7.format(year))
        fp8 = open(pathp8.format(year))
        fp9 = open(pathp9.format(year))

        readerp1 = csv.reader(fp1, delimiter=";")
        readerp2 = csv.reader(fp2, delimiter=";")
        readerp3 = csv.reader(fp3, delimiter=";")
        readerp4 = csv.reader(fp4, delimiter=";")
        readerp5 = csv.reader(fp5, delimiter=";")
        readerp6 = csv.reader(fp6, delimiter=";")
        readerp7 = csv.reader(fp7, delimiter=";")
        readerp8 = csv.reader(fp8, delimiter=";")
        readerp9 = csv.reader(fp9, delimiter=";")

        for row in readerp1:
            lp1.append(int(row[0]))
            
        for row in readerp2:
            lp2.append(int(row[0]))
            
        for row in readerp3:
            lp3.append(int(row[0]))
            
        for row in readerp4:
            lp4.append(int(row[0]))

        for row in readerp5:
            lp5.append(int(row[0]))

        for row in readerp6:
            lp6.append(int(row[0]))

        for row in readerp7:
            lp7.append(int(row[0]))

        for row in readerp8:
            lp8.append(int(row[0]))

        for row in readerp9:
            lp9.append(int(row[0]))
    
        l = np.unique(np.array(lp1 + lp2 + lp3 + lp4 + lp5 + lp6 + lp7 + lp8 + lp9))        
        print "Year: ", year
        divisor = tbyear[year - 2006]
        print "\tObs in Pattern 1: ", len(lp1), "\t(", round(((len(lp1)*100) / divisor),2), ")"
        print "\tObs in Pattern 2: ", len(lp2), "\t(", round(((len(lp2)*100) / divisor),2), ")"
        print "\tObs in Pattern 3: ", len(lp3), "\t(",round(((len(lp3)*100) / divisor),2), ")"
        print "\tObs in Pattern 4: ", len(lp4), "\t(",round(((len(lp4)*100) / divisor),2), ")"
        print "\tObs in Pattern 5: ", len(lp5), "\t(",round(((len(lp5)*100) / divisor),2), ")"
        print "\tObs in Pattern 6: ", len(lp6), "\t(",round(((len(lp6)*100) / divisor),2), ")"
        print "\tObs in Pattern 7: ", len(lp7), "\t(",round(((len(lp7)*100) / divisor),2), ")"
        print "\tObs in Pattern 8: ", len(lp8), "\t(",round(((len(lp8)*100) / divisor),2), ")"
        print "\tObs in Pattern 9: ", len(lp9), "\t(",round(((len(lp9)*100) / divisor),2), ")"
        print
        print "\tUnique observations: ", len(l),"\t(", round(((len(l)*100) / divisor),2), ")"
    
    
    finally:
        fp1.close()
        fp2.close()
