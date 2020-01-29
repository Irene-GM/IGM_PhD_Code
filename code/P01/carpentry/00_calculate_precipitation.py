# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 09:24:21 2015

@author: irene
"""

from __future__ import division
import gdal, gdalconst
import csv
import datetime


def accumulatedSpring(row, tif):
    acc_spring = 0
    norain = 0
    light = 0
    heavy = 0
    # Accumulating max. temp. from 21st Mar to 20th Jun.
    for i in range(80, 172):
        band = tif.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)
        if data != None: 
            if float(data[0][0]) == -9999:
                return [-99, -99, -99, -99]
            else:
                if data[0][0]  == 0:
                    norain += 1
                elif 0 < data[0][0] <= 10:
                    light += 1
                else: 
                    heavy +=1
                acc_spring += data[0][0]
                
    return [acc_spring, norain, light, heavy]

def accumulatedSummer(row, tif):
    acc_summer = 0
    norain = 0
    light = 0
    heavy = 0
    # Accumulating max. temp. from 21st Jun to 20th Sep.
    for i in range(172, 264):
        band = tif.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)
        if data != None: 
            if float(data[0][0]) == -9999:
                return [-99, -99, -99, -99]
            else:
                if data[0][0]  == 0:
                    norain += 1
                elif 0 < data[0][0] <= 10:
                    light += 1
                else: 
                    heavy +=1
                acc_summer += data[0][0]            
    return [acc_summer, norain, light, heavy]

def accumulatedAutumn(row, tif):
    acc_autumn = 0
    norain = 0
    light = 0
    heavy = 0
    # 1st leg: Accumulating max. temp. from 21st Sep to 20th Dec.
    for i in range(264, 356):
        band = tif.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)
        if data != None: 
            if float(data[0][0]) == -9999:
                return [-99, -99, -99, -99]
            else:
                if data[0][0]  == 0:
                    norain += 1
                elif 0 < data[0][0] <= 10:
                    light += 1
                else: 
                    heavy +=1
                acc_autumn += data[0][0]
    return [acc_autumn, norain, light, heavy]

    
def accumulatedWinter(row, tif, tifprev):
    acc_endYear = 0    
    acc_beginYear = 0
    norain = 0
    light = 0
    heavy = 0
    # Accumulating max. temp. from 21st Dec to 31st Dec.
    for i in range(356, 366):
        band = tifprev.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)

        if data != None:
            if float(data[0][0]) == -9999:
                return [-99, -99, -99, -99]
            else: 
                if data[0][0]  == 0:
                    norain += 1
                elif 0 < data[0][0] <= 10:
                    light += 1
                else: 
                    heavy +=1            
                acc_endYear += data[0][0]
    
    # Accumulating max. temp from 1st Jan to 21st March
    for i in range(1, 81):
        band = tif.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)
        if data != None:
            if float(data[0][0]) == -9999:
                return [-99, -99, -99, -99]
            else:
                if data[0][0]  == 0:
                    norain += 1
                elif 0 < data[0][0] <= 10:
                    light += 1
                else: 
                    heavy +=1      
                acc_beginYear += data[0][0]

    acc_winter = acc_endYear + acc_beginYear
    return [acc_winter, norain, light, heavy]
    
def accumulatedUntilDate(doy, tif):
    acc = 0    
    # 4th leg: Accumulating max. temp. from 1st Jan to DOY
    # ONLY IF DOY < 180, because after this the season is finishing
    # and probably there is no point in counting the forcing temp. units

    if doy < 180:
        for i in range(1, doy + 1):
            band = tif.GetRasterBand(i)
            data = band.ReadAsArray(xoffset, yoffset, 1, 1)
            if data != None:
                if float(data[0][0]) == -9999:
                    return -99
                acc+=data[0][0]
    return acc
    
def countMilestones(tif):
    d20 = 0
    d25 = 0
    d30 = 0    
    for i in range(1, 366):
        band = tif.GetRasterBand(i)
        data = band.ReadAsArray(xoffset, yoffset, 1, 1)
        if data != None:
            item = float(data[0][0])
            if item == -9999:
                return [-99, -99]
            elif item >= 20 and item < 25:
                d20 += 1
            elif item >= 25 and item < 30:
                d25 += 1
            elif item >= 30:
                d30 += 1
    return [d20, d25, d30]


## Main program
path_obs = r'D:\PycharmProjects\IGM_PhD_Materials\data\general\txt\all_NL.csv'
path_out = r'D:\PycharmProjects\IGM_PhD_Materials\data\P01\out\features_calculated\precipitation_2014.csv'
template = r"D:\UTwente\IGM_PhD_Materials\data\geo\raster\KNMI\prec"

counter = 0
yyyy = 2014
limity = 2014

tif = None
tifprev = None
# tifmin = None
# tifprevmin = None

originX = 0
originY = 0
pixel_width = 0
pixel_height = 0

try:
    f = open(path_obs, 'r')
    f_out = open(path_out, 'wb')
    
    reader = csv.reader(f, delimiter=';')    
    writer= csv.writer(f_out, delimiter=";")
    
    for row in reader:
        if row[4] != "" and row[5] != "":
            #date = datetime.datetime.strptime(row[2], "%m-%d-%Y")
            d, m, y = [int(item) for item in row[2].split(" ")[0].split("-")]
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
                    [acc_spring, norainspr, lightspr, heavyspr] = accumulatedSpring(row, tif)
                    [acc_summer, norainsum, lightsum, heavysum] = accumulatedSummer(row, tif)
                    [acc_autumn, norainaut, lightaut, heavyaut] = accumulatedAutumn(row, tif)
                    [acc_winter, norainwin, lightwin, heavywin] = accumulatedWinter(row, tif, tifprev)
                    acc_until_date = accumulatedUntilDate(doy, tif)
                    # d20, d25, d30 = countMilestones(tif)
                    
                    # acc = acc_winter + acc_until_date
                    
                    # Obtain the week average temperature and the average
                    # maximum temperatures for the week of the observation
                    # week = weekGenerator(date)
                    # avg_min, avg_max, avg_week = accumulatedWeek(week, tif, tifprev, tifmin, tifprevmin)               
                    
                    # print row[0], "\t", row[1], "\t", avg_min, "\t", avg_max, "\t", avg_week, "\t", acc_winter, "\t", acc_until_date, "\t", acc
                    # new_row = [row[0], avg_min, avg_max, avg_week, acc_winter, acc_until_date, acc]
                    # new_row = [row[0], avg_min, avg_max, avg_week, acc_autumn, acc_winter, acc_until_date]
                    
                    # Only write if value is not -99:
                    if acc_spring != -99:
                        # new_row = [row[0], acc_spring, acc_summer, acc_autumn, acc_winter, acc_until_date, d20, d25, d30]
                        new_row = [row[1]] + [acc_spring, norainspr] + [acc_summer, norainsum] + [acc_autumn, norainaut] + [acc_winter, norainwin] + [acc_until_date]
                        print new_row
                        writer.writerow(new_row)
                    
                    # FER EN GEE EL ACUMULAT FINS LA DATA DELS ENV INDICES
                    # I LA MITJA DE CADASCUN PER PUNT
                    
                    counter +=1
                else:
                    print "Could not open .tif files: No layers before 2005."
            else:
                print "Date.year: ", date.year
                if date.year > (limity-1) and date.year < (limity+1):

                    print "\nProcessing ", date.year
                    
                    print "Opening tif files"
                    previous_year_tif = template + str(year-1) + '/' + str(year-1) + ".tif"
                    this_year_tif = template + str(year) + '/' + str(year) + ".tif"
                    tifprev = gdal.Open(previous_year_tif)
                    tif = gdal.Open(this_year_tif)
                    
                    # previous_year_tif_min = template_min + str(year-1) + '/' + str(year-1) + ".tif"
                    # this_year_tif_min = template_min + str(year) + '/' + str(year) + ".tif"
                    # tifprevmin = gdal.Open(previous_year_tif_min)
                    # tifmin = gdal.Open(this_year_tif_min)                    
                    
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