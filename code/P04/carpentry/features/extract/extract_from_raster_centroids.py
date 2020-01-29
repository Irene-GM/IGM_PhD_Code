import gdal
import csv
from osgeo import ogr, osr
import numpy as np

def reproject(x, y):
    source = osr.SpatialReference()
    source.ImportFromEPSG(28992)
    target = osr.SpatialReference()
    target.ImportFromEPSG(4326)
    text = "POINT({0} {1})".format(x, y)
    point = ogr.CreateGeometryFromWkt(text)
    transform = osr.CoordinateTransformation(source, target)
    point.Transform(transform)
    return [point.GetX(), point.GetY()]

def extractSingleData(tif, x, y, numband):
    geotransform = tif.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixel_width = geotransform[1]
    pixel_height = geotransform[5]

    xoffset = int(np.divide(x - originX, pixel_width))
    yoffset = int(np.divide(y - originY, pixel_height))

    band = tif.GetRasterBand(numband)
    data = band.ReadAsArray(xoffset, yoffset, 1, 1)

    if data == None:
        return -99
    else:
        return data[0][0]



################
# Main program #
################


path_raster = r"D:/UTwente/IGM_PhD_Materials/data/geo/raster/Beleving_Reclass_RD_New.tif"
path_points = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/1km_clipped/1km_clipped_centroids_text.csv"
path_out = r"D:/PycharmProjects/IGM_PhD_Materials/data/P04/out/features/country_features/Centroids_NR_BL.csv"

tif = gdal.Open(path_raster)

with open(path_points, "r", newline="") as r:
    with open(path_out, "w", newline="") as w:
        reader = csv.reader(r, delimiter=";")
        writer = csv.writer(w, delimiter=";")
        next(reader)
        i = 0
        for row in reader:
            rowid = int(row[2])
            latitude = float(row[1])
            longitude = float(row[0])
            value = extractSingleData(tif, longitude, latitude, 1)
            writer.writerow([i, value])
            i += 1

