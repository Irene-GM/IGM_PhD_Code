import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error, r2_score
from collections import defaultdict
from scipy.signal import argrelextrema, savgol_filter, gauss_spline, spline_filter
from operator import itemgetter
import seaborn as sb
import matplotlib as mpl
from matplotlib.dates import DateFormatter

def evaluate(observations, predictions):
    obs = np.array(observations)
    pred = np.array(predictions)
    n = len(obs)
    sum_obs = sum(obs ** 2)
    sq_sum = sum((obs - pred) ** 2)

    # Mean of the observations and predictions
    mean_obs = np.mean(obs)
    mean_pred = np.mean(pred)

    # Standard deviation of the observations and predictions
    stdev_obs = np.std(obs)
    stdev_pred = np.std(pred)

    # Correlation coefficient
    # Returns a matrix like this:
    # [[1.0, 0.9923316965546289], [0.9923316965546289, 1.0]]
    correlation = np.corrcoef(obs, pred)

    # Intercept and slope of OLS regression
    #   Intercept is a matrix like this:
    #   array([[-0.02669013, -0.02264611], [-0.02264611, -0.02669013]])
    #   Slope is a matrix like this
    #   array([[ 1.04609058,  1.03806884], [ 1.03806884,  1.04609058]])
    slope = correlation * stdev_pred / stdev_obs
    intercept = mean_pred - slope * mean_obs

    # Mean Absolute Error (MAE)
    sum_abs = sum(abs(obs - pred))
    mae = sum_abs / n
    mse = sq_sum / n
    msea = intercept ** 2
    msei = 2 * intercept * (slope - 1) * mean_obs
    msep = (slope - 1) ** 2 * sum_obs / n
    mses = msea + msei + msep
    mseu = mse - mses

    # Root Mean Square Error (RMSE)
    # RMSES is a matrix like this:
    # array([[ 0.0154833 ,  0.01293596], [ 0.01293596,  0.0154833 ]])
    # RMSEU is a matrix like this:
    # array([[ 0.04147761,  0.0423413 ], [ 0.0423413 ,  0.04147761]])
    rmse = np.sqrt(mse)
    rmses = np.sqrt(mses)
    rmseu = np.sqrt(mseu)

    # Indices of agreement
    #   d1: Based on MAE
    #   d2: Based on RMSE
    pe1 = sum(abs(pred - mean_obs) + abs(obs - mean_obs))
    pe2 = sum((abs(pred - mean_obs) + abs(obs - mean_obs)) ** 2)
    d1 = 1 - n * mae / pe1
    d2 = 1 - n * mse / pe2

    # The output should be the following for this example:
    # [0.50413223140495866, 0.50067784684676719, 0.32746467365551984, 0.34255771110890154, 0.99233169655462861, -0.022646114907439507, 1.0380688421681805, 0.034876667833470279, 0.94108912881591422, 0.044273297270294019, 0.012935955298159947, 0.042341302668999582, 0.99561710541432158]
    y = [mean_obs, mean_pred, stdev_obs, stdev_pred, correlation.tolist()[0][1], intercept.tolist()[0][1], slope.tolist()[0][1], mae, d1, rmse, rmses.tolist()[0][1], rmseu.tolist()[0][1], d2]
    return y


def calculate_metrics(target, fit):
    print("Target: ", target[0:10])
    print("Fit: ", fit[0:10])
    evaluation = evaluate(target, fit)
    rmse = np.sqrt(mean_squared_error(target, fit))
    rmses = evaluation[-3]
    rmseu = evaluation[-2]
    nrmse = np.divide(rmse, np.mean(target))
    r2 = r2_score(target, fit)

    print("RMSE (ytest and y_pred): ", rmse)
    print("\tRMSE systematic: ", rmses)
    print("\tRMSE UNsystematic: ", rmseu)
    print("NRMSE: ", nrmse)
    print("R2 score: ", r2)
    print("")

    return nrmse, r2


def func(x, *params):
    y = np.zeros_like(x)
    for i in range(0, len(params), 3):
        ctr = params[i]
        amp = params[i+1]
        wid = params[i+2]
        y = y + amp * np.exp(-((x - ctr)/wid)**2)
    return y


def find_guess(target):
    # Set up initial guess for the curve fit
    first_peak_xaxis = 0
    amplitude_yaxis = np.max(target)
    last_peak_xaxis = len(target) - 6 # Minus 6 because flagging ends in december, so the peak is in june
    folding_width_xaxis = 12 # This is a fixed parameter, because our seasonality is monthly

    # Candidate guess
    candidate_peaks_xaxis = []
    candidate_amplitude_yaxis = 60
    candidate_width_xaxis = 10

    guess = [first_peak_xaxis, amplitude_yaxis, folding_width_xaxis,
             last_peak_xaxis, amplitude_yaxis, folding_width_xaxis]
    for i in range(0, 8):
        milestone = first_peak_xaxis + folding_width_xaxis * (i+1)
        if milestone < len(target):
            candidate_peaks_xaxis += [milestone, candidate_amplitude_yaxis, candidate_width_xaxis]

    guess += candidate_peaks_xaxis
    return guess



def find_guess_2(target, the_site):
    the_name = the_site[0]
    the_order = the_site[1]
    what_fit = the_site[2]

    candidates_list = []
    maxm = argrelextrema(target, np.greater, order=the_order)

    first_peak_xaxis = 0
    amplitude = target[0]
    width = maxm[0][0]

    first_peak_list = [first_peak_xaxis, amplitude, width]

    j = 1
    for i in range(len(maxm[0][:-1])):
        xcoordinate = maxm[0][i]
        next_xcoordinate = maxm[0][j]
        width = next_xcoordinate - xcoordinate
        amplitude = target[xcoordinate]
        if the_name == "Eijsden_2":
            amplitude = 20
        elif the_name in ["Gieten_1", "Gieten_2"]:
            if amplitude > 200:
                amplitude = 200
        elif the_name in ["KwadeHoek_2", "Twiske_1", "Twiske_2"]:
            if amplitude > 10:
                amplitude = 10
        elif the_name in ["Montferland_1", "Montferland_2", "Nijverdal_1", "Nijverdal_2"]:
            if amplitude > 100:
                amplitude = 100
        elif amplitude > 5:
            amplitude = 5
        candidates_list+= [xcoordinate, amplitude, width]
        j += 1

    # We add the last peak
    xcoordinate = maxm[0][-1]
    next_xcoordinate = len(target)
    width = next_xcoordinate - xcoordinate
    amplitude = target[xcoordinate]
    last_peak_list = [xcoordinate, amplitude, width]

    if what_fit == "co":
        guess = first_peak_list + candidates_list + last_peak_list
    elif what_fit == "nh":
        guess = candidates_list + last_peak_list
    elif what_fit == "nt":
        guess = first_peak_list + candidates_list
    else:
        guess = candidates_list

    return guess


def find_guess_3(target, the_site):
    the_name = the_site[0]
    the_order = the_site[1]
    what_fit = the_site[2]

    candidates_list = []
    maxm = argrelextrema(target, np.greater, order=the_order)

    first_peak_xaxis = 0
    amplitude = target[0]
    width = maxm[0][0]

    first_peak_list = [first_peak_xaxis, amplitude, width]

    j = 1
    for i in range(len(maxm[0][:-1])):
        xcoordinate = maxm[0][i]
        next_xcoordinate = maxm[0][j]
        width = next_xcoordinate - xcoordinate
        amplitude = target[xcoordinate]
        if the_name == "Eijsden":
            amplitude = 20
        elif the_name in ["Gieten"]:
            if amplitude > 200:
                amplitude = 200
        elif the_name in ["KwadeHoek", "Twiske"]:
            if amplitude > 10:
                amplitude = 10
        elif the_name in ["Montferland", "Nijverdal"]:
            if amplitude > 100:
                amplitude = 100
        elif the_name in ["Bilthoven"]:
            amplitude = 2
        elif the_name in ["Appelscha"]:
            amplitude = 10
        #elif amplitude > 5:
        #     amplitude = 5
        candidates_list+= [xcoordinate, amplitude, width]
        j += 1

    # We add the last peak
    xcoordinate = maxm[0][-1]
    next_xcoordinate = len(target)
    width = next_xcoordinate - xcoordinate
    amplitude = target[xcoordinate]
    last_peak_list = [xcoordinate, amplitude, width]

    if what_fit == "co":
        guess = first_peak_list + candidates_list + last_peak_list
    elif what_fit == "nh":
        guess = candidates_list + last_peak_list
    elif what_fit == "nt":
        guess = first_peak_list + candidates_list
    else:
        guess = candidates_list

    return guess


def ingroup(name):

    iscomplete = False
    isnohead = False
    isnotail = False
    iscandidate = False

    dic = {"Appelscha_1": [2, "co"], "HoogBaarlo_2": [2, "co"], "KwadeHoek_2": [1, "nt"], "Nijverdal_1": [1, "co"],
           "Twiske_2": [2, "co"], "Vaals_1": [2, "co"], "Wassenaar_2": [2, "co"], "Appelscha_2": [1, "nh"],
           "Montferland_1": [2, "nh"], "Schiermonnikoog_1": [1, "nh"], "Schiermonnikoog_2": [2, "nh"],
           "Twiske_1": [1, "nh"], "Wassenaar_1": [2, "nh"], "Ede_1": [1, "ca"], "Gieten_1": [1, "nt"],
           "Nijverdal_2": [2, "nt"], "Bilthoven_1": [1, "nh"], "Bilthoven_2": [2, "ca"], "Dronten_1": [2, "ca"],
           "Dronten_2": [2, "ca"], "Ede_2": [2, "nt"], "Eijsden_1": [2, "nt"], "Eijsden_2": [2, "nt"],
           "HoogBaarlo_1": [1, "ca"], "Gieten_2": [2, "ca"], "Montferland_1": [2, "ca"], "Vaals_2": [2, "ca"],
           "Veldhoven_1":[2,"ca"], "Veldhoven_2": [2, "ca"], "Montferland_2":[2, "nh"]}

    # dic = {"Appelscha": [2, "co"], "Nijverdal": [1, "co"], "Vaals": [2, "co"],
    #        "Montferland": [2, "nh"], "Schiermonnikoog": [1, "nh"], "Twiske": [1, "nh"],
    #        "Wassenaar": [2, "nh"], "Ede": [1, "ca"], "Gieten": [1, "nt"],
    #        "Bilthoven": [1, "nh"], "Dronten": [2, "ca"], "Eijsden": [2, "nt"],
    #        "HoogBaarlo": [1, "ca"], "Montferland": [2, "ca"], "Veldhoven":[2,"ca"]}


    if name != "KwadeHoek_1":
        return [name] + dic[name]
    else:
        # I could not find a fitting for KwadeHoek_1, thus
        # I decided to copy the signal for KwadeHoek_2 because
        # they have exactly the same biological habitat,
        # which is "Rhamno crataegetum", a type of bush/grass
        return ["KwadeHoek_2", 1, "nt"]

def draw_plot(target, fit, avg, place):
    nrmse, r2 = calculate_metrics(target, fit)
    #t = "{0} (R2={1})".format(place, np.round(r2, decimals=2))
    t = "{0}".format(place)
    xlinspace = np.linspace(0, target.shape[0]-1, target.shape[0])
    plt.plot(xlinspace, target, "-", color="blue", linewidth=2)
    plt.plot(xlinspace, fit, "-", color="orange", linewidth=2, label="Gaussian fit")
    plt.plot(xlinspace, avg, "-", color="green", linewidth=2, label="Averaged signal")
    plt.subplots_adjust(hspace=.5)
    plt.legend(loc=2,prop={'size':8})
    plt.title(t)
    plt.grid()

def draw_plot_seaborn(target, fit, avg, place, dates):

    nrmse, r2 = calculate_metrics(target, fit)
    t = "{0} (R2={1})".format(place, r2)
    # t = "{0}".format(place)

    zipped = zip(dates, target)
    sorted_dates = sorted(zipped,key=itemgetter(0))

    ds = [item[0] for item in sorted_dates]
    vs = [item[1] for item in sorted_dates]

    # t = "{0}".format(place)
    plt.plot_date(ds, vs, "-", color="black", linewidth=2)
    plt.plot_date(ds, fit, "-", color="grey", linewidth=2)
    plt.subplots_adjust(hspace=.2, wspace=.2)
    plt.title(t)
    plt.grid(b=True, which='major', color='lightgray', linestyle='-')
    plt.grid(b=True, which='minor', color='lightgray', linestyle='-')


################
# Main Program #
################

# path_in = r'M:\Documents\workspace\Special\IJGIS\data\tables\Flagging_Sites_All_Predictors_withHabitat_nymphs.csv'
# path_out = r'M:\Documents\workspace\Special\IJGIS\data\tables\Flagging_Sites_All_Predictors_withHabitat_nymphs_SG52.csv'

path_in = r"D:\PycharmProjects\IGM_PhD_Materials\data\P02\in\FS_nymphs_newVeg_noisy.csv"
path_out = r"D:\PycharmProjects\IGM_PhD_Materials\data\P02\in\savitzky_golay_fitting.csv"

dic = defaultdict(list)
headers = ["Site", "Date", "TickCount"]

with open(path_in, "r", newline="") as r:
    next(r)
    reader = csv.reader(r, delimiter=";")
    for row in reader:
        name = row[1]
        rowid = row[0]
        if name != "KwadeHoek_1":
            date = datetime.datetime.strptime(row[2], "%Y-%m-%d").date()
            tick_counts = int(float(row[3]))
            dic[name].append([rowid, date, tick_counts])

# guess = find_guess_3(target, the_site)
# popt, pcov = curve_fit(func, xlinspace, target, p0=np.array(guess))
# fit_gauss = func(xlinspace, *popt)

i = 1
towrite = []
# plt.suptitle("Time-series of AQT per flagging site as reported by volunteers (2006-2014)", size=36)
# path_fig = r"\\ad.utwente.nl\home\garciamartii\Documents\PhD\Papers\Journals\02_IJGIS\images\print_v3\{0}"
name_fig = "Figure_01_Data_Overview.png"
shortYearFmt = DateFormatter("%y")


for key in sorted(dic.keys()):
    path_fig = r"C:\Users\irene\Pictures\paper2_redo\{0}"
    name_fig = "Figure_01_Data_Overview.png"
    print("\n\n Processing: ", key)
    rowids = np.array([item[0] for item in dic[key]])
    dates = np.array([item[1] for item in dic[key]])
    target = np.array([item[2] for item in dic[key]])
    xlinspace = np.linspace(0, target.shape[0]-1, target.shape[0])
    the_site = ingroup(key)

    fit = savgol_filter(target, 7, 5)
    ax = plt.subplot(5, 6, i)
    plt.subplots_adjust(hspace=.5)
    plt.subplots_adjust(wspace=.2)
    # draw_plot_seaborn(target, fit, avg, key, dates)

    sort_dates, sort_target, sort_sg = zip(*sorted(zip(dates, target, fit)))
    score = np.round(r2_score(sort_target, sort_sg), decimals=2)

    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.xaxis.set_major_formatter(shortYearFmt)
    ax.grid(b=True, which='major', color='#A8A8A8', linewidth=0.5)
    ax.grid(b=True, which='major', color='#A8A8A8', linewidth=0.5)


    if i in [13]:
        ax.yaxis.labelpad = 20
        plt.ylabel("Active Questing Ticks (AQT)", size=30)
    if i in [27]:
        ax.xaxis.set_label_coords(1.1, -0.5)
        plt.xlabel("Year", size=30)

    # fig.text(0.5, 0.04, 'Year', ha='center')
    # fig.text(0.04, 0.5, 'Active Questing Ticks (AQT)', va='center', rotation='vertical')
    plt.plot_date(sort_dates, sort_target, "-", color="red", linewidth=2, label="Raw AQT")
    plt.plot_date(sort_dates, sort_sg, "-", color="blue", linewidth=2, label="Smoothed AQT")
    plt.title("{0}".format(key), fontweight="bold", size=16)

    # plt.figlegend(sort_target, sort_sg, loc = 'lower center', ncol=5, labelspacing=0. )
    # plt.legend(sort_target, sort_sg, loc = 'lower center', bbox_to_anchor = (0,-0.1,1,1), bbox_transform = plt.gcf().transFigure)
    ax.set_ylim(0, 150)
    plt.ylim(0, 150)


    for j in range(len(fit)):
        r = int(rowids[j])
        k = key
        d = dates[j]
        t = target[j]
        f = np.round(fit[j], decimals=4)
        newrow = [r, k, d, t, f]
        towrite.append(newrow)
    i+=1

# with open(path_out, "w", newline="") as w:
#     writer = csv.writer(w, delimiter=";")
#     for row in sorted(towrite):
#         writer.writerow(row)

ax.legend(bbox_to_anchor=(2.7, 0.2), loc='lower right', borderaxespad=0., prop={'size':26})

my_dpi = 300
xpix = 1600
ypix = 900


manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
fig = plt.gcf()
plt.show()
fig.savefig(path_fig.format(name_fig), format="png", dpi=300)

# plt.rcParams['figure.figsize'] = (15,10)
# fig = plt.gcf()
# fig.savefig(path_fig.format(name_fig), dpi=my_dpi)
# plt.show()

