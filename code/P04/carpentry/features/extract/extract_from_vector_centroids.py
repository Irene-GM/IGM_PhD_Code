# from shapely.geometry import shape, Point
import fiona
import csv
import threading
from osgeo import ogr
import random
import numpy as np
from queue import Queue

def create_tasks(npts, nfeat):
    q = Queue()
    prev_batch_pt = 0
    prev_batch_poly = 0
    for batch_pt in range(0, npts, 1000):
        for batch_poly in range(0, nfeat, 1000):
            q.put((prev_batch_pt, batch_pt, prev_batch_poly, batch_poly))
            prev_batch_poly = batch_poly
        prev_batch_pt = batch_pt
        q.put((prev_batch_pt, batch_pt, batch_poly, nfeat))
    q.put((batch_pt, npts, batch_poly, nfeat))
    return q

def make_chunk(layer, start, end):
    l = []
    for i in range(start, end):
        feature = layer.GetFeature(i)
        l.append(feature)
    return l


def check_chunk_gdal(lpoly, lpts):
    i = 0
    for pt in lpts:
        rowid = pt[0]
        point = pt[1]
        for poly in lpoly:
            if board[rowid] == False:
                distance = point.Distance(poly.GetGeometryRef())
                if distance < 500:
                    if point.Within(poly.GetGeometryRef()):
                        print("TB #{0}".format(rowid), "\t{0}/1K".format(i), "\tBBG:{0}".format(poly.GetFieldAsString("BG2008A")))
                        board[rowid] = True
                        newrow = [rowid, int(poly.GetFieldAsString("BG2008A"))]
                        writer.writerow(newrow)
                        w.flush()
                        break
        i += 1

def worker():
    while True:
        item = q.get()
        left_pt = item[0]
        right_pt = item[1]
        left_poly = item[2]
        right_poly = item[3]

        list_poly = make_chunk(layer, left_poly, right_poly)
        list_points = lpts[left_pt:right_pt]

        check_chunk_gdal(list_poly, list_points)
        q.task_done()


################
# Main program #
################

path_points = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/1km_clipped/1km_clipped_centroids_text.csv"
path_polygons = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/BBG2008/BBG2008.shp"
path_out = r"D:/PycharmProjects/IGM_PhD_Materials/data/P04/out/features/country_features/Centroids_1km_BBG_value.csv"

lpts = []
rowid = 0
with open(path_points, "r", newline="") as r:
    reader = csv.reader(r, delimiter=";")
    next(reader)
    for row in reader:

        # Original rowid, lat, lon
        # rowid = int(row[2])
        # latitude = float(row[1])
        # longitude = float(row[0])

        latitude = float(row[1])
        longitude = float(row[0])

        # In shapely
        # point = Point(longitude, latitude)
        # In gdal
        text = "POINT({0} {1})".format(longitude, latitude)
        point = ogr.CreateGeometryFromWkt(text)
        lpts.append((rowid, point))

        rowid += 1

random.shuffle(lpts)
driver = ogr.GetDriverByName("ESRI Shapefile")
shapefile = driver.Open(path_polygons)
layer = shapefile.GetLayer(0)

npts = len(lpts)
nfeat = layer.GetFeatureCount()

board = [False] * 105000
values = [-1] * nfeat

q = create_tasks(npts, nfeat)

with open(path_out, "a", newline="") as w:
    writer = csv.writer(w, delimiter=";")
    for i in range(16):
        t = threading.Thread(target=worker)
        t.daemon =True
        t.start()
    q.join()