import csv
from collections import defaultdict
import numpy as np

def read_features(path):
    lmeta = []
    ldata = []
    with open(path, "r", newline="") as r:
        reader = csv.reader(r, delimiter=";")
        for row in reader:
            lmeta.append(row[0:6])
            ldata.append(row[6:27])
    return ldata, lmeta

def summary(dic):
    dicsummary = defaultdict(int)
    empty_cell = 0
    for key in sorted(dic.keys()):
        if len(dic[key]) == 0:
            empty_cell += 1
        else:
            dicsummary[len(dic[key])]+=1
    print("Empty cells: ", empty_cell)
    print("Cell w/ TB: ", 46838 - empty_cell)
    print("Summary: ", dicsummary)

def find_ids(lids, meta):
    lpos = []
    for rowid in lids:
        i = 1
        for metaid in meta[1:]:
            if int(rowid) == int(metaid[0]):
                lpos.append(i)
            i +=1
    return lpos


################
# Main program #
################

headers = "rowid;latitude;longitude;target;dbuiltup;dforest;drecreation;dbrr;dwrl;dwrn;dwrr;dcamping;dcaravan;dcross;dgolf;dheem;dhaven;dsafari;dwater;attr;dbath;lu;lc;maxmeanhaz;maxstdhaz".split(";")

# This is the correspondence tick bite - pixel associated
path_in_link = r"D:/PycharmProjects/IGM_PhD_Materials/data/P04/out/txt/TB_reports_risk_per_pixel.csv"

# This is the characterization of each of the pixel centroids, without a target (# TB per pixel)
path_in_risk = r"D:/PycharmProjects/IGM_PhD_Materials/data/P04/in/nl_centroids_v1.12.csv"

# This file contains the X's (predictors) and the Y (target variable), now analysis can start
path_out = r"D:\PycharmProjects\IGM_PhD_Materials\data\P04\in\nl_risk_features_v1.12.csv"

meta_risk = np.loadtxt(path_in_risk, delimiter=";", skiprows=1, usecols=range(0, 3))
risk = np.loadtxt(path_in_risk, delimiter=";", skiprows=1, usecols=range(3, 24))

dic = defaultdict(list)

with open(path_in_link, "r", newline="") as r:
    reader = csv.reader(r, delimiter=";")
    next(r)
    for row in reader:
        cellid = int(float(row[0]))
        biteid = int(float(row[1]))
        dic[cellid].append(biteid)

summary(dic)

m, meta = read_features(path_in_risk)

idx_col = meta_risk[:,0]
tar_col = np.zeros((len(idx_col), 1))

print(len(dic.keys()))
print("Meta: ", len(meta))

with open(path_out, "w", newline="") as w:
    writer = csv.writer(w, delimiter=";")
    writer.writerow(headers)
    i = 0
    for key in sorted(dic.keys()):
        lpos = find_ids(dic[key], meta)
        if len(lpos) > 0:
            newrow = meta_risk[key, :].tolist() + [len(lpos)] + risk[i, :].tolist()
            # print(newrow)
            writer.writerow(newrow)
        if i % 1000 == 0:
            print("Processed: ", i)
        i += 1



