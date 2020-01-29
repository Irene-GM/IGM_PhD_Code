# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 08:39:10 2015

@author: irene
"""

from __future__ import division
import gdal, gdalconst
import csv
import datetime


def accumulatedSpring(tif, tifmin):
    acc_spring = 0.0
    # Accumulating max. temp. from 21st Mar to 20th Jun.
    for i in range(80, 172):
        band = tif.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)
        bandmin = tifmin.GetRasterBand(i)
        datamin = bandmin.ReadAsArray(xoffset, yoffset, 1, 1)
        if data != None and datamin != None: 
            if float(data[0][0]) == -9999 and float(datamin[0][0]) == -9999:
                return -99
            else:
                mean = (data[0][0] + datamin[0][0]) / 2
                # print            
                # print data[0][0], datamin[0][0], mean
                # print
                acc_spring += mean
                # print "Accspring: ", xoffset, yoffset, acc_spring
    # print "\n\t\t RETURNINNNNNNNNNNNNNGGGGG: ", acc_spring
    return acc_spring

def accumulatedSummer(tif, tifmin):
    acc_summer = 0
    
    # Accumulating max. temp. from 21st Jun to 20th Sep.
    for i in range(172, 264):
        band = tif.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)
        bandmin = tifmin.GetRasterBand(i)
        datamin = bandmin.ReadAsArray(xoffset, yoffset, 1, 1)
        if data != None and datamin != None: 
            if float(data[0][0]) == -9999 and float(datamin[0][0]) == -9999:
                return -99
            else:
                mean = (data[0][0] + datamin[0][0]) / 2
            acc_summer += mean
            
    return acc_summer

def accumulatedAutumn(tif, tifmin):
    acc_autumn = 0
    # 1st leg: Accumulating max. temp. from 21st Sep to 20th Dec.
    for i in range(264, 356):
        band = tif.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)
        bandmin = tifmin.GetRasterBand(i)
        datamin = bandmin.ReadAsArray(xoffset, yoffset, 1, 1)
        if data != None and datamin != None: 
            if float(data[0][0]) == -9999 and float(datamin[0][0]) == -9999:
                return -99
            else:
                mean = (data[0][0] + datamin[0][0]) / 2
            acc_autumn += mean
    return acc_autumn

    
def accumulatedWinter(tif, tifprev, tifmin, tifprevmin):
    acc_endYear = 0    
    acc_beginYear = 0
    hardfreeze = 0
    belowzero = 0
    w = []
    # Accumulating max. temp. from 21st Dec to 31st Dec.
    for i in range(356, 366):
        band = tifprev.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)
        bandmin = tifprevmin.GetRasterBand(i)
        datamin = bandmin.ReadAsArray(xoffset, yoffset, 1, 1)

        if data != None and datamin != None:
            if float(data[0][0]) == -9999 and float(datamin[0][0]) == -9999:
                return [-99, -99, -99]
            else: 
                mean = (data[0][0] + datamin[0][0]) / 2
                if mean < -5:
                    hardfreeze += 1
                elif -5 < mean <= 0:
                    belowzero += 1
            acc_endYear += mean
    
    # Accumulating max. temp from 1st Jan to 21st March
    for i in range(1, 81):
        band = tif.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)
        bandmin = tifmin.GetRasterBand(i)
        datamin = bandmin.ReadAsArray(xoffset, yoffset, 1, 1)
        if data != None and datamin != None:
            if float(data[0][0]) == -9999 and float(datamin[0][0]) == -9999:
                return [-99, -99, -99]
            else: 
                mean = (data[0][0] + datamin[0][0]) / 2
                if mean < -5:
                    hardfreeze += 1
                elif -5 < mean <= 0:
                    belowzero += 1
            acc_beginYear += mean

    acc_winter = acc_endYear + acc_beginYear
    w.append(acc_winter)
    w.append(hardfreeze)
    w.append(belowzero)

    return w
    
def accumulatedUntilDate(doy, tif, tifmin):
    acc = 0      
    for i in range(1, doy + 1):
        band = tif.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)
        bandmin = tifmin.GetRasterBand(i)
        datamin = bandmin.ReadAsArray(xoffset, yoffset, 1, 1)
        if data != None and datamin != None:
            if float(data[0][0]) == -9999 and float(datamin[0][0]) == -9999:
                return -99
            else: 
                mean = (data[0][0] + datamin[0][0]) / 2
                acc += mean
    return acc
    
def countMilestones(tif, tifmin):
    d20 = 0
    d25 = 0
    d30 = 0    
    for i in range(1, 366):
        band = tif.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)
        if data != None:
            item = float(data[0][0])
            if item == -9999:
                return [-99, -99, -99]
            elif item >= 20 and item < 25:
                d20 += 1
            elif item >= 25 and item < 30:
                d25 += 1
            elif item >= 30:
                d30 += 1
    return [d20, d25, d30]


## Main program

path_obs = r'D:\PycharmProjects\IGM_PhD_Materials\data\general\txt\all_NL.csv'
path_out = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\features_calculated\temperature_2012.csv'

template = r"D:\UTwente\IGM_PhD_Materials\data\geo\raster\KNMI\prec"
template_min = r"D:\UTwente\IGM_PhD_Materials\data\geo\raster\KNMI\prec"

counter = 0
yyyy = 2012
limity = 2012

tif = None
tifprev = None
tifmin = None
tifprevmin = None

originX = 0
originY = 0
pixel_width = 0
pixel_height = 0

try:
    first = True
    f = open(path_obs, 'r')
    f_out = open(path_out, 'wb')
    
    reader = csv.reader(f, delimiter=';')    
    writer= csv.writer(f_out, delimiter=";")
    
    for row in reader:
        # print row
        if row[4] != "" and row[5] != "":
            d, m, y = [int(item) for item in row[2].split(" ")[0].split("-")]
            # date = datetime.datetime.strptime(row[2], "%Y-%m-%d")            
            date = datetime.datetime(year=y, month=m, day=d)
            doy = date.timetuple().tm_yday
            year = date.timetuple().tm_year
            if date.year == yyyy and date.year < (limity+1):         
                if tif != None and tifprev != None:   
                    x = float(row[5]) 
                    y = float(row[4]) 
                    
                    xoffset = int((x - originX) / pixel_width)
                    yoffset = int((y - originY) / pixel_height)

                    # Obtain FOR EACH POINT the accumulation of temperatures 
                    # for each season
                    
                    acc_spring = accumulatedSpring(tif, tifmin)   
                    acc_summer = accumulatedSummer(tif, tifmin)                    
                    acc_autumn = accumulatedAutumn(tif, tifmin)                    
                    [acc_winter, hardfreeze, belowzero] = accumulatedWinter(tif, tifprev, tifmin, tifprevmin)
                    acc_until_date = accumulatedUntilDate(doy, tif, tifmin)
                    d20, d25, d30 = countMilestones(tif, tifmin)
                    
                    # Only write if value is not -99:
                    if acc_spring != -99:
                        new_row = [row[1], acc_spring, acc_summer, acc_autumn, acc_winter, acc_until_date, d20, d25, d30]
                        print new_row
                        writer.writerow(new_row)
                    counter +=1
                else:
                    print "Could not open .tif files: No layers before 2005."
            else:
                if date.year > (limity-1) and date.year < (limity+1):
                    print "\nProcessing ", date.year                    
                    print "Opening tif files"
                    previous_year_tif = template + str(year-1) + '/' + str(year-1) + ".tif"
                    this_year_tif = template + str(year) + '/' + str(year) + ".tif"
                    tifprev = gdal.Open(previous_year_tif)
                    tif = gdal.Open(this_year_tif)
                    print tif.GetProjection()
                    
                    previous_year_tif_min = template_min + str(year-1) + '/' + str(year-1) + ".tif"
                    this_year_tif_min = template_min + str(year) + '/' + str(year) + ".tif"
                    tifprevmin = gdal.Open(previous_year_tif_min)
                    tifmin = gdal.Open(this_year_tif_min)                    
                    
                    print "Geotransforming"                    
                    geotransform = tif.GetGeoTransform()
                    
                    originX = geotransform[0]
                    originY = geotransform[3]
                    pixel_width = geotransform[1]
                    pixel_height = geotransform[5]
                    yyyy = date.year
                elif date.year <= (limity+1):
                    yyyy = date.year                
                else:
                    print "End!\n"
                    print "Processed %d observations. ", counter
                    break


                
    print "Observations WITH coordinates up to 31/12/2012: ", counter
    
finally:
    f.close()
    f_out.close()