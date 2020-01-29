import gdal, gdalconst
import ogr
import csv

def find_minimum_distance():
    pass

def calculate_distance_centroids(l, path_features, path_out):
    driver = ogr.GetDriverByName("ESRI Shapefile")
    targetFeatures = driver.Open(path_features, 0)
    target = targetFeatures.GetLayer()
    nlines = target.GetFeatureCount()

    counter = 0

    rowid = 0
    with open(path_out, "w", newline="") as w:
        writer = csv.writer(w, delimiter=";")
        i = 0
        for row in l:
            # rowid = int(row[2])
            minDist = 100000000
            latitude = float(row[1])
            longitude = float(row[0])
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(longitude, latitude)
            for line in range(0, nlines):
                lineFeature = target.GetFeature(line)
                distance = point.Distance(lineFeature.GetGeometryRef())
                if distance < minDist:
                    minDist = distance
                if minDist == 0:
                    break
            newrow = [i, int(minDist)]
            print(newrow)
            writer.writerow(newrow)
            w.flush()
            counter += 1
            rowid += 1
            i += 1
            if counter % 1000 == 0:
                print("Processed ", counter)

################
# Main program #
################

# Ran each line in separate Python consoles to get some "concurrence"

path_centroids = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/1km_clipped/1km_clipped_centroids_text.csv"

# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/OSM/NL_OSM_Bike_Routes_RD_New.shp"
# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/OSM/NL_OSM_Walking_Paths_National_RD_New.shp"
# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/OSM/NL_OSM_Walking_Paths_Regional_RD_New.shp"
# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/OSM/NL_OSM_Walking_Paths_Local_RD_New.shp"

# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/BBG_reclassified/Recreation.shp"
# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/BBG_reclassified/Built-up.shp"
# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/BBG_reclassified/Forest.shp"

# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/TOP10NL_functional/TOP10NL_campings.shp"
# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/TOP10NL_functional/TOP10NL_safaripark.shp"
# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/TOP10NL_functional/TOP10NL_crossbaan.shp"
# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/TOP10NL_functional/TOP10NL_heemtuin.shp"
# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/TOP10NL_functional/TOP10NL_caravanpark.shp"
# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/TOP10NL_functional/TOP10NL_jachthaven.shp"
# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/TOP10NL_functional/TOP10NL_golfterrein.shp"
# path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/TOP10NL_waterbodies/TOP10NL_Waterbodies.shp"
path_features = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/Zwemwaterlocaties/ZwemWaterLocaties_NatReg.shp"

path_out = r"D:/PycharmProjects/IGM_PhD_Materials/data/P04/out/features/country_features/Centroids_1km_{0}_distance.csv"


l = []
with open(path_centroids, "r", newline="") as r:
    reader = csv.reader(r, delimiter=";")
    next(reader)
    for row in reader:
        l.append(row)

print("Processing: ", path_features)
calculate_distance_centroids(l, path_features, path_out.format("NR_ZWL"))
