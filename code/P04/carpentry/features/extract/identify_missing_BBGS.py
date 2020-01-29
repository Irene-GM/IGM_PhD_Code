import numpy as np

path_ref = r"D:/PycharmProjects/IGM_PhD_Materials/data/P04/out/features/country_features/Centroids_1km_LGN_LC1km.csv"
path_mis = r"D:/PycharmProjects/IGM_PhD_Materials/data/P04/out/features/country_features/Centroids_1km_BBG_value.csv"
path_out = r"D:/PycharmProjects/IGM_PhD_Materials/data/P04/out/features/country_features/missing_BBGs/missing_BBGs_01.csv"

mref = np.loadtxt(path_ref, delimiter=";").astype(np.int)
mmis = np.loadtxt(path_mis, delimiter=";").astype(np.int)

target = mmis[:, 0].tolist()

counter = 0
missing = []
for row in mref:
    rowid = row[0]
    if rowid in target:
        pass
    else:
        missing.append(rowid)
        counter += 1

print(missing)
print(len(missing))

np.savetxt(path_out, np.array(missing), fmt="%d")

