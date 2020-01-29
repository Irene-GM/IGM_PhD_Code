import os
import datetime
import csv
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from matplotlib.dates import DateFormatter, MonthLocator
from collections import defaultdict

def generate_dates(year):
    basedate = datetime.datetime(year, 1, 1)
    for x in range(0, 365):
        increment = basedate + datetime.timedelta(days=x)
        yield(increment)

def format_ints(m, d):
    if m<10:
        mo = str(m).zfill(2)
    else:
        mo = str(m)
    if d<10:
        da = str(d).zfill(2)
    else:
        da = str(d)
    return mo, da

def find_whiskers(path_in):
    l = []
    k = 1
    idx = np.genfromtxt(path_in, delimiter=";", usecols=range(0,4), dtype=str, skip_header=1)
    dic = defaultdict(list)
    dicsites = defaultdict(list)
    for row in idx:
        date = datetime.datetime.strptime(row[2], "%Y-%m-%d")
        value = float(row[3])
        dic[date.month].append(value)
        # if date.year == 2014:
        place = row[1].split("_")[0]
        akey = (place, date.month)
        dicsites[akey].append(value)
    data = [dic[i] for i in range(1, 13)]
    ax = plt.boxplot(data)
    dicwhiskers = defaultdict(tuple)
    for i in range(2, 25, 2):
        lower_whisker = ax['whiskers'][i-2].get_ydata()
        upper_whisker = ax['whiskers'][i-1].get_ydata()
        dicwhiskers[k] = [lower_whisker, upper_whisker]
        k += 1
    return dicwhiskers, dicsites

def make_signal(dicwhiskers):
    xaxis = []
    yaxis = []
    basedate = datetime.datetime(2013, 12, 2)
    delta = datetime.timedelta(days=30)
    for i in range(12):
        newd = basedate + delta
        xaxis.append(newd)
        basedate = newd

    for key in sorted(dicwhiskers.keys()):
        chunk = dicwhiskers[key]
        avg = np.mean(chunk)
        if avg < 0:
            avg = 0
        yaxis.append(avg)

    print(type(xaxis), type(yaxis))
    return xaxis, yaxis

def average_sites(dicsites):
    twelve = [0] * 12
    dic = defaultdict(list)
    for key in sorted(dicsites.keys()):
        place = key[0]
        pos = int(key[1])
        val = np.round(np.mean(dicsites[key]), decimals=0)
        if val < 0:
            val = 0
        if len(dic[place]) == 0:
            dic[place] = twelve
        else:
            dic[place][pos-1] = val
    for key in sorted(dic.keys()):
        print("Hey", key, dic[key])
    return dic

def average_sites_per_month(dicsites):
    twelve = [0] * 12
    dic = defaultdict(list)
    for key in sorted(dicsites.keys()):
        place = key[0]
        pos = int(key[1])
        val = np.round(np.mean(dicsites[key]), decimals=0)
        if val < 0:
            val = 0
        if len(dic[place]) == 0:
            dic[place] = twelve
        else:
            curr = dic[place][:]
            curr[pos-1] = val
            dic[place] = curr[:]
            print(place, dic[place], val)
    return dic

def average_sites_per_month_and_year(path_in, yyyy, dicpixels):
    twelve = [0] * 12
    idx = np.genfromtxt(path_in, delimiter=";", usecols=range(0, 4), dtype=str, skip_header=1)
    dicsites = defaultdict(list)
    for row in idx:
        date = datetime.datetime.strptime(row[2], "%Y-%m-%d")
        if date.year == yyyy:
            value = float(row[3])
            place = row[1].split("_")[0]
            akey = (place, date.month)
            dicsites[akey].append(value)

    for key in sorted(dicpixels.keys()):
        for i in range(1, 13):
            newkey = (key, i)
            if len(dicsites[newkey]) == 0:
                dicsites[newkey] = [0.0, 0.0]

    newdic = defaultdict(list)
    for key in sorted(dicsites.keys()):
        place = key[0]
        newdic[place].append(np.max(dicsites[key]))

    return newdic


################
# Main program #
################

dicpixels = {'Schiermonnikoog': [206, 28], 'Twiske': [121, 144],
             'Montferland': [198, 206], 'Eijsden': [180, 312],
             'Wassenaar': [85, 177], 'Bilthoven': [144, 176],
             'Gieten': [247, 80], 'Dronten': [175, 135],
             'KwadeHoek': [60, 212], 'Appelscha': [218, 90],
             'Ede': [176, 191], 'Veldhoven': [151, 258],
             'Vaals': [185, 318], 'Nijverdal': [225, 156],
             'HoogBaarlo': [186, 181]}

path_in = r"F:/season_server/PycharmProjects/NL_predictors/data/versions/v8/predictions_v8/{0}/{1}"
path_samples = r"D:\PycharmProjects\IGM_PhD_Materials\data\P02\in\random_FS_nymphs_with_zeros_savitzky_golay.csv"
basename = "NL_Prediction_{0}_{1}_{2}.csv"
year = 2014
l = []
dicwhiskers, dicsites = find_whiskers(path_samples)
x12, y12 = make_signal(dicwhiskers)
avg_sites = average_sites_per_month(dicsites)
avg_sites_2014 = average_sites_per_month_and_year(path_samples, 2014, dicpixels)

for date in generate_dates(year):
    lyr = np.empty((350, 300))
    m, d = format_ints(date.month, date.day)
    name = basename.format(date.year, m, d)
    # print("Reading ", name)
    with open(path_in.format(year, name), "r", newline="") as r:
        reader = csv.reader(r, delimiter=";")
        for row in reader:
            i = int(float(row[1]))
            j = int(float(row[2]))
            v = int(float(row[3]))
            lyr[i,j] = v
        l.append(lyr)

stack = np.dstack(l)
i = 1
plt.subplots_adjust(hspace=0.5, wspace=0.5)
basedate = datetime.datetime(2014, 1, 1)
month_loc = MonthLocator()
month_fmt = DateFormatter("%m")

xlin1 = np.linspace(0, 1, 365)
xlin2 = np.linspace(0, 1, 12)

for key in sorted(dicpixels.keys()):
    xpix = dicpixels[key][1]
    ypix = dicpixels[key][0]
    lv = stack[xpix, ypix, :]
    ld = [basedate + datetime.timedelta(item) for item in range(len(l))]
    ax = plt.subplot(3, 5, i)
    plt.plot_date(xlin2, y12, "-", linewidth=5, color="#67666A", label="Long-term monthly avg. all sites")
    plt.plot_date(xlin2, avg_sites[key], "-", linewidth=3, color="darkred", label="Long-term monthly avg. per site", )
    plt.plot_date(xlin2, avg_sites_2014[key], "-", linewidth=3, color="black", label="2014 monthly avg. per site", )
    plt.plot_date(xlin1, lv, "-", color="#0E1F9C", label="Daily predicted AQT")


    plt.ylim(0, 100)
    plt.title(key, size=18)
    ax.grid(color="#ABABAB")
    # ax.xaxis.set_major_locator(month_loc)
    # ax.xaxis.set_major_formatter(month_fmt)
    plt.xticks(xlin2, range(1, 13))
    plt.xlabel("Month")
    plt.ylabel("AQT")

    i+= 1

ax.legend(bbox_to_anchor=(-2.5, -0.44), ncol=2, loc="lower center", borderaxespad=0.0, prop={'size':16})
manager = plt.get_current_fig_manager()
# manager.resize(*manager.window.maxsize())
manager.full_screen_toggle()
fig = plt.gcf()
plt.show()

path_figs = r"C:/Users/irene/Pictures/paper2_redo/{0}.png"
fig.savefig(path_figs.format("Temporality_Corrected_2014_max"), format="png", dpi=300)

