import matplotlib.pyplot as plt
import gdal
import numpy as np
from collections import defaultdict
import seaborn as sb
from osgeo import ogr
import matplotlib
from matplotlib.ticker import FuncFormatter
from scipy.stats import spearmanr, pearsonr, kendalltau


def save_fig_maximized(fig, path_fig, name_fig):
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    manager.window.showMaximized()
    fig = plt.gcf()
    print(manager)
    plt.show()
    fig.savefig(path_fig.format(name_fig), format="pdf", dpi=300)


################
# Main program #
################


matplotlib.rcParams['font.size'] = 32
sb.set(font_scale=4)

path_bel = r"D:\PycharmProjects\IGM_PhD_Materials\data\P03\in\Beleving_Value_In_Point.tif"
path_exp = r"D:\PycharmProjects\IGM_PhD_Materials\data\P03\in\Exposure_RD_New_classified.tif"
path_cas = r"D:\PycharmProjects\IGM_PhD_Materials\data\P03\in\Exposure_WGS84_classified.tif"

tif_bel = gdal.Open(path_bel)
bel_ban = tif_bel.GetRasterBand(1).ReadAsArray()

tif_exp = gdal.Open(path_exp)
exp_ban = tif_exp.GetRasterBand(1).ReadAsArray()

canvas_bel = np.empty((352, 311))
for i in range(bel_ban.shape[0]):
    for j in range(bel_ban.shape[1]):
        canvas_bel[i,j] = bel_ban[i,j]
roll_bel = np.roll(np.roll(canvas_bel, 6, axis=1), 1, axis=0)

canvas_exp = np.empty((352, 311))
for i in range(exp_ban.shape[0]):
    for j in range(exp_ban.shape[1]):
        canvas_exp[i,j] = exp_ban[i,j]
roll_exp = np.roll(np.roll(canvas_exp, 6, axis=1), 1, axis=0)

plt.subplot(1, 3, 1)
plt.imshow(roll_bel, interpolation="None")

plt.subplot(1, 3, 2)
plt.imshow(roll_exp, interpolation="None")

plt.subplot(1, 3, 3)
tif_cas = gdal.Open(path_cas)
cas_ban = tif_cas.GetRasterBand(1).ReadAsArray()
cas_ban[cas_ban!=5] = np.nan
plt.imshow(cas_ban, interpolation="None")

print(roll_bel.shape, roll_exp.shape, cas_ban.shape)
print(np.unique(roll_bel, return_counts=True))

lbeleving = []
lexposure = []
counter = 0
dicoc = defaultdict(int)
for i in range(0, roll_bel.shape[0]):
    for j in range(0, roll_bel.shape[1]):
        belv = roll_bel[i][j]
        expv = roll_exp[i][j]
        casv = cas_ban[i][j]
        if not np.isnan(belv) and not np.isnan(expv):
            if int(expv) > 0:
                key = (int(belv), int(expv))
                lbeleving.append(belv)
                lexposure.append(expv)
                dicoc[key] += 1

            elif casv == 5:
                key = (int(belv), 0)
                lbeleving.append(belv)
                lexposure.append(0)
                dicoc[key] += 1
                counter += 1

t = np.zeros((4, 6))
for key in dicoc.keys():
    col = key[0]
    row = key[1]-1
    if -1 not in key:
        t[row, col] = dicoc[key]

m = np.flipud(np.roll(t, 1, axis=0))

plt.clf()
xlbls = ["< 6", "6 - 6.5", "6.5 - 7", "7 - 7.5", "7.5 - 8", "> 8"]
ylbls = ["Zero", "Low", "Medium", "High"]


sc = np.sum(m, axis=0)
vt = np.divide(m, sc) * 100

mynorm = matplotlib.colors.LogNorm(vmin=0, vmax=1878)
fmt = lambda x,pos: '{:d}'.format(int(x))

flat_m = m.flatten().tolist()
flat_vt = vt.flatten().tolist()

with sb.plotting_context(font_scale=5.5):
    # sb.set(font_scale=2.5)
    # ax = sb.heatmap(m, annot=True, fmt='.0f', cmap=plt.cm.Greys, linewidths=.5, annot_kws={"size": 30}, cbar_kws={'label': '# of grid cells', 'format': FuncFormatter(fmt)}, norm=mynorm)
    ax = sb.heatmap(vt, annot=True, fmt='.0f', cmap=plt.cm.Greys, linewidths=.5, annot_kws={"size": 34})
    ax.set(xlabel="Attractiveness", ylabel="Exposure")
    ax.set(xticklabels=xlbls, yticklabels=reversed(ylbls))
    ax.xaxis.labelpad = 50
    ax.yaxis.labelpad = 50

    k = 0
    for t in ax.texts:
        # print("text: ", t)
        # t.set_text(t.get_text() + " %")
        # rounded = np.round(float(t.get_text()), decimals=0)
        txt = str(int(flat_vt[k])) + "%" + "\n(" + str(int(flat_m[k])) + ")"
        t.set_text(txt)
        k += 1

plt.show()
