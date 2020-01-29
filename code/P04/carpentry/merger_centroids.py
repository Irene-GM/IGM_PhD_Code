import csv
from collections import defaultdict

path_template = r"D:/PycharmProjects/IGM_PhD_Materials/data/P04/out/features/country_features/{0}"
path_centroids = r"D:/UTwente/IGM_PhD_Materials/data/geo/vector/1km_clipped/1km_clipped_centroids_text.csv"
path_out_tmp = r"D:/PycharmProjects/IGM_PhD_Materials/data/P04/out/features/country_features/{0}"
path_out = path_out_tmp.format("nl_centroids_v1.12.csv")

path_builtup = path_template.format("Centroids_1km_BBG_Builtup_distance.csv")
path_forest = path_template.format("Centroids_1km_BBG_Forest_distance.csv")
path_recreation = path_template.format("Centroids_1km_BBG_Recreation_distance.csv")

path_brr = path_template.format("Centroids_1km_OSM_BRR_distance.csv")
path_wrl = path_template.format("Centroids_1km_OSM_WRL_distance.csv")
path_wrn = path_template.format("Centroids_1km_OSM_WRN_distance.csv")
path_wrr = path_template.format("Centroids_1km_OSM_WRR_distance.csv")

path_campings = path_template.format("Centroids_1km_KDT_campings_distance.csv")
path_caravan = path_template.format("Centroids_1km_KDT_caravanpark_distance.csv")
path_cross = path_template.format("Centroids_1km_KDT_crossbaan_distance.csv")
path_golf = path_template.format("Centroids_1km_KDT_golfterrein_distance.csv")
path_heem = path_template.format("Centroids_1km_KDT_heemtuin_distance.csv")
path_haven = path_template.format("Centroids_1km_KDT_jachthaven_distance.csv")
path_safari = path_template.format("Centroids_1km_KDT_safaripark_distance.csv")
path_water = path_template.format("Centroids_1km_KDT_waterbodies_distance.csv")

path_beleving = path_template.format("Centroids_1km_NR_BL.csv")
path_bathing = path_template.format("Centroids_1km_NR_ZWL_distance.csv")
path_lu = path_template.format("Centroids_1km_BBG_value.csv")
path_lc = path_template.format("Centroids_1km_LGN_LC1km.csv")

headers = ["rowid",
           "latitude", "longitude",
           "dbuiltup", "dforest", "drecreation","dbrr", "dwrl", "dwrn", "dwrr",
           "dcamping", "dcaravan", "dcross", "dgolf", "dheem", "dhaven", "dsafari", "dwater",
           "attr", "dbath",
           "lu", "lc"]

pack = [path_builtup, path_forest, path_recreation,
        path_brr, path_wrl, path_wrn, path_wrr,
        path_campings, path_caravan, path_cross, path_golf, path_heem, path_haven, path_safari, path_water,
        path_beleving, path_bathing,
        path_lu, path_lc]

dic = defaultdict(list)

# This is the first one, because it makes the metadata
with open(path_centroids, "r", newline="") as r:
    reader = csv.reader(r, delimiter=";")
    next(reader)
    i = 0
    for row in reader:
        # key = int(row[2])
        dic[i] = [float(row[0]), float(row[1])]
        i +=1

for path in pack:
    with open(path, "r", newline="") as r:
        reader = csv.reader(r, delimiter=";")
        for row in reader:
            key = float(row[0])
            values = [float(item) for item in row[1:]]
            dic[key] += values

counter = 0
with open(path_out, "w", newline="") as w:
    writer = csv.writer(w, delimiter=";")
    writer.writerow(headers)
    for key in sorted(dic.keys()):
        newrow = [counter] + dic[key]
        print(newrow)
        writer.writerow(newrow)
        counter += 1
