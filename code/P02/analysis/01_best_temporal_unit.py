import sys
sys.path.append(r'D:\PycharmProjects\IGM_PhD_Materials\code\P02')
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from utils import *
import seaborn as sb
import matplotlib.pyplot as plt
from collections import defaultdict
from operator import itemgetter
import datetime


def show_error_plots(rmse_list, rmses_list, rmseu_list, nrmse_list, labels):
    path_fig = r"C:\Users\irene\Pictures\paper2_redo\{0}"
    name_fig = "Figure_05_Performance_Time_Scales.png"
    s = 30
    plt.clf()
    plt.close()
    xlinspace = np.linspace(0, 10, 11)

    # plt.suptitle("Performance of RF at multiple time scales", size=36)

    plt.subplots_adjust(hspace=.5, wspace=.3)
    ax1 = plt.subplot(2, 3, 1)
    plt.plot(xlinspace, nrmse_list, "-", label="NRMSE", linewidth=2, color="darkblue")
    # plt.title("Evolution of NRMSE", size=s)
    plt.xticks(xlinspace, labels, size='medium', rotation=70, fontsize = 22)
    plt.xlabel('Temporal aggregation', size=s)
    plt.ylabel('Normalized RMSE', size=s)
    ax1.grid(b=True, which='major', color='#A6A6A6', linewidth=0.5)
    ax1.grid(b=True, which='major', color='#A6A6A6', linewidth=0.5)

    ax2 = plt.subplot(2, 3, 2)
    plt.plot(xlinspace, rmse_list, "-", color="darkblue", label="RMSE", linewidth=3)
    plt.plot(xlinspace, rmses_list, "-", color="darkgreen", label="RMSEs", linewidth=2)
    plt.plot(xlinspace, rmseu_list, "-", color="darkgray", label="RMSEu", linewidth=2)
    # plt.title("Evolution of RMSE", size=s)
    plt.xlabel('Temporal aggregation', size=s)
    plt.ylabel('RMSE', size=s)
    plt.xticks(xlinspace, labels, size='medium', rotation=70, fontsize = 22)
    ax2.grid(b=True, which='major', color='#A6A6A6', linewidth=0.5)
    ax2.grid(b=True, which='major', color='#A6A6A6', linewidth=0.5)
    ax2.legend(bbox_to_anchor=(1.5, 0.0), loc='lower right', borderaxespad=0., prop={'size':20})

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    fig = plt.gcf()
    plt.show()
    fig.savefig(path_fig.format(name_fig), format="png", dpi=300)


def show_feature_importances(rf, combination, headers, lim):
    cols = [headers[item] for item in combination[1:]] # Skip label tick count
    i = 1
    print("\nFeature Importances")
    print("-"*40)
    for item in list(reversed(sorted(zip(cols, rf.feature_importances_), key=lambda x: x[1])))[:lim]:
        score = np.round(item[1] * 100, decimals=2)
        dicfirf[item[0]].append(score)
        print(i, ")\t", item[0], "\t\t", score, "%")
        i += 1
    print(dicfirf)

def show_avg_fi(dic):
    l = []
    for key in dic.keys():
        mean = np.mean(dic[key])
        l.append((key, mean))

    lsort = list(reversed(sorted(l, key=itemgetter(1))))
    return lsort[0:10]


def bound_target(path):
    l = []
    k = 1
    idx = np.genfromtxt(path_in, delimiter=";", usecols=range(0,4), dtype=str, skip_header=1)
    dic = defaultdict(list)
    for row in idx:
        date = datetime.datetime.strptime(row[2], "%Y-%m-%d")
        value = float(row[3])
        dic[date.month].append(value)
    data = [dic[i] for i in range(1, 13)]
    ax = plt.boxplot(data)
    dicwhiskers = defaultdict(tuple)
    for i in range(2, 25, 2):
        lower_whisker = ax['whiskers'][i-2].get_ydata()
        upper_whisker = ax['whiskers'][i-1].get_ydata()
        dicwhiskers[k] = [lower_whisker, upper_whisker]
        k += 1

    for row in idx:
        date = datetime.datetime.strptime(row[2], "%Y-%m-%d")
        value = float(row[3])
        low_whisker = dicwhiskers[date.month][0]
        upp_whisker = dicwhiskers[date.month][1]
        low_bound = low_whisker[0]
        upp_bound = upp_whisker[1]
        Y_value_bounded = np.divide((value - low_bound), (upp_bound - low_bound))
        l.append(Y_value_bounded)

    return [np.array(l), dicwhiskers, idx]

def bounded_descaling(ypred, dicwhiskers, idx, lim):
    i = 0
    l = []
    test_metadata = idx[lim:, :]
    for row in test_metadata:
        date = datetime.datetime.strptime(row[2], "%Y-%m-%d")
        low_whisker = dicwhiskers[date.month][0]
        upp_whisker = dicwhiskers[date.month][1]
        low_bound = low_whisker[0]
        upp_bound = upp_whisker[1]
        Y_value_bounded = np.round(ypred[i] * (upp_bound - low_bound) + low_bound)
        l.append(Y_value_bounded)
        i += 1
    return np.array(l)



################
# Main program #
################

dicfirf = defaultdict(list)

path_in = r"D:\PycharmProjects\IGM_PhD_Materials\data\P02\in\random_FS_nymphs_without_zeros_savitzky_golay.csv"

m, all_observations, headers_list, combinations, descale, descale_target = load_stuff(path_in, experiment=1)

target_limits = descale[0]
maxlim = m.shape[0]
lim = int(np.divide(maxlim * 70, 100))
origY = descaling(m[:,0], target_limits)

nrmse_list, rmse_list, rmses_list, rmseu_list, r2_list, mae_list = ([] for i in range(6))

labels = ["Xdays-1", "Xdays-2", "Xdays-3", "Xdays-4", "Xdays-5", "Xdays-6", "Xdays-7", "Xdays-14", "Xdays-30", "Xdays-90", "Xdays-365"]

ldic, lrf, lgbr, lrmse, lrmses, lrmseu, lnrmse, partial_rmse, partial_rmses, partial_rmseu, partial_nrmse = ([] for i in range(11))

target_bound, whiskers, idx = bound_target(path_in)

for combination in combinations:
    msel = select_columns(m, combination)
    # xtrain = msel[:lim, 1:]
    # ytrain = msel[:lim, 0]
    # xtest = msel[lim:, 1:]
    # ytest = msel[lim:, 0]
    xtrain = msel[:lim, 1:]
    ytrain = target_bound[:lim]
    xtest = msel[lim:, 1:]
    ytest = target_bound[lim:]
    old_mean = np.mean(origY[lim:])
    print("old mean: ", old_mean)

    print("Training...\n")

    # Now we go for the modelling
    for i in range(0,10):
        rf = RandomForestRegressor(n_estimators=500, n_jobs=4, max_features="auto", oob_score=False, bootstrap=True, criterion="mse", max_leaf_nodes=None, min_samples_leaf=1, warm_start=False)
        rf.fit(xtrain, ytrain)
        pred_rf = rf.predict(xtest)

        pred_rf_desc = bounded_descaling(pred_rf, whiskers, idx, lim)
        ytest_desc = bounded_descaling(ytest, whiskers, idx, lim)

        show_feature_importances(rf, combination, headers_list, 10)
        # show_feature_importances(gbr, combination, headers_list, 5)

        rfrmse, rfrmses, rfrmseu, rfnrmse, rfmae, rfr2, rfmean, rfmean_pred = show_model_evaluation(ytest_desc, pred_rf_desc)

        good_nrmse = np.divide(rfrmse, old_mean)

        partial_rmse.append(rfrmse)
        partial_rmses.append(rfrmses)
        partial_rmseu.append(rfrmseu)
        partial_nrmse.append(good_nrmse)

    lrmse.append(np.mean(np.array(partial_rmse)))
    lrmses.append(np.mean(np.array(partial_rmses)))
    lrmseu.append(np.mean(np.array(partial_rmseu)))
    lnrmse.append(np.mean(np.array(partial_nrmse)))

    partial_rmse, partial_rmses, partial_rmseu, partial_nrmse = ([] for i in range(4))

    ldic.append(dicfirf)
    dicfirf = defaultdict(list)

show_error_plots(lrmse, lrmses, lrmseu, lnrmse, labels)
plt.show()

