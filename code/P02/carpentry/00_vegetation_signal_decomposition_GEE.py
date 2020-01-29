import statsmodels.api as sm
import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
import datetime
import itertools

init_date = datetime.datetime(2006, 1, 1)

print("Reading one")
mndvi = np.loadtxt(r'D:\Data\GEE\Paper2\NL_signal_NDVI.csv', delimiter=";").astype(int)
print("Reading two")
mevi = np.loadtxt(r'D:\Data\GEE\Paper2\NL_signal_EVI.csv', delimiter=";").astype(int)
print("Reading three")
mndwi = np.loadtxt(r'D:\Data\GEE\Paper2\NL_signal_NDWI.csv', delimiter=";").astype(int)

print("Processing NDVI data frame")
df_ndvi = pd.DataFrame(mndvi.T)
df_ndvi.columns = ["ndvi_" + str(item) for item in list(range(0, 105000))]
df_ndvi.index = pd.DatetimeIndex(freq="m", start=init_date, periods=108)
res_ndvi = sm.tsa.seasonal_decompose(df_ndvi)
res_ndvi.seasonal.index.name = "NDVI seasonal decomposition for the flagging sites"
# res_ndvi.plot()

print("Done!")

print("Processing EVI data frame")
df_evi = pd.DataFrame(mevi.T)
df_evi.columns = ["evi_" + str(item) for item in list(range(0, 105000))]
df_evi.index = pd.DatetimeIndex(freq="m", start=init_date, periods=108)
res_evi = sm.tsa.seasonal_decompose(df_evi)
res_evi.seasonal.index.name = "EVI seasonal decomposition for the flagging sites"

print("Processing NDWI data frame")
df_ndwi = pd.DataFrame(mndwi.T)
df_ndwi.columns = ["ndwi_" + str(item) for item in list(range(0, 105000))]
df_ndwi.index = pd.DatetimeIndex(freq="m", start=init_date, periods=108)
res_ndwi = sm.tsa.seasonal_decompose(df_ndwi)
res_ndwi.seasonal.index.name = "NDWI seasonal decomposition for the flagging sites"

veg_decomposition_ndvi = np.divide(res_ndvi.seasonal.T.as_matrix(), 10000)
veg_decomposition_evi = np.divide(res_evi.seasonal.T.as_matrix(), 10000)
veg_decomposition_ndwi = np.divide(res_ndwi.seasonal.T.as_matrix(), 10000)

max_ndvi = np.amax(veg_decomposition_ndvi, axis=1)
min_ndvi = np.amin(veg_decomposition_ndvi, axis=1)
max_evi = np.amax(veg_decomposition_evi, axis=1)
min_evi = np.amin(veg_decomposition_evi, axis=1)
max_ndwi = np.amax(veg_decomposition_ndwi, axis=1)
min_ndwi = np.amin(veg_decomposition_ndwi, axis=1)

minmax = np.vstack((min_ndvi, max_ndvi, min_evi, max_evi, min_ndwi, max_ndwi)).T
print("Minmax: ")
print(minmax.shape)

# veg_decomposition = np.concatenate((veg_decomposition_ndvi, veg_decomposition_evi, veg_decomposition_ndwi), axis=1)
# veg_decomposition = np.concatenate((veg_decomposition_ndvi))
# print(veg_decomposition.shape)
# path_out = r"D:\Data\GEE\IJGIS\NL_signal_decomposition.csv"
path_out = r"M:\Documents\workspace\Special\Paper2\data\NL\NL_signal_decomposition.csv"
# np.savetxt(path_out, minmax, delimiter=';', fmt='%.4f')

# We need to write it backwards, as points start from bottom left corner instead of top left

rows = range(0, 350)
cols = range(0, 300)
pairs = list(itertools.product(rows, cols))

teaser = np.ones((350, 300)) * -99

counter = 0
with open(path_out, "w", newline="") as w:
    writer = csv.writer(w, delimiter=";")
    for row in minmax:
        to_list = [round(elem, 4) for elem in row.tolist()]
        xi = pairs[counter][0]
        yi = pairs[counter][1]
        newrow = [counter+1, xi, yi] + to_list
        teaser[xi, yi] = to_list[0]
        writer.writerow(newrow)
        counter+=1

plt.imshow(teaser[::-1], interpolation="None")
plt.show()