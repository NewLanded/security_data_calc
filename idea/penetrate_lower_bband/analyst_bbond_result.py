import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from util.util_data.result import Result
from util.util_data.security_data import SecurityData


def idea_08_2(data):
    """
    测试不同max_depth的表现
    """
    data_low_le_low = data[
        (result["open"]["next_1_day"] <= result["close"]["next_0_day"]) & (
                result["close"]["next_1_day"] <= result["close"]["next_0_day"]) & (
                result["open"]["next_1_day"] <= result["close"]["next_1_day"])]
    data_low_ge_low = data[
        (result["open"]["next_1_day"] <= result["close"]["next_0_day"]) & (
                result["close"]["next_1_day"] <= result["close"]["next_0_day"]) & (
                result["open"]["next_1_day"] >= result["close"]["next_1_day"])]

    data_high_low = data[
        (result["open"]["next_1_day"] >= result["close"]["next_0_day"]) & (result["close"]["next_1_day"] <= result["close"]["next_0_day"])]

    data_high_le_high = data[
        (result["open"]["next_1_day"] >= result["close"]["next_0_day"]) & (
                result["close"]["next_1_day"] >= result["close"]["next_0_day"]) & (
                result["open"]["next_1_day"] <= result["close"]["next_1_day"])]
    data_high_ge_high = data[
        (result["open"]["next_1_day"] >= result["close"]["next_0_day"]) & (
                result["close"]["next_1_day"] >= result["close"]["next_0_day"]) & (
                result["open"]["next_1_day"] >= result["close"]["next_1_day"])]

    print(len(data_low_le_low), len(data_low_ge_low), len(data_high_low), len(data_high_le_high), len(data_high_ge_high))

    data = data_low_ge_low

    percent_series = data["open"]["next_0_day"] / 100

    target_day_list = ["next_2_day", "next_3_day", "next_4_day", "next_5_day"]
    target_data_list = []
    for day in target_day_list:
        target_data_list.append([day, (data["close"][day] > data["high"]["next_1_day"]).values])
    data = pd.DataFrame({
        "open": data["open"]["next_0_day"] / percent_series,
        "close": data["close"]["next_0_day"] / percent_series,
        "high": data["high"]["next_0_day"] / percent_series,
        "low": data["low"]["next_0_day"] / percent_series
    }).values

    for day, target_data in target_data_list:
        print("day is {0}".format(day))
        depth_list = []
        training_score_list = []
        test_score_list = []
        for max_depth in range(1, 31):
            X_train, X_test, y_train, y_test = train_test_split(data, target_data, random_state=0)
            forest = RandomForestClassifier(n_estimators=100, random_state=0, max_depth=max_depth)
            forest.fit(X_train, y_train)
            print("Accuracy on training set: {:.3f}".format(forest.score(X_train, y_train)))
            print("Accuracy on test set: {:.3f}".format(forest.score(X_test, y_test)))
            training_score_list.append(forest.score(X_train, y_train))
            test_score_list.append(forest.score(X_test, y_test))
            depth_list.append(max_depth)

        # plt.figure(figsize=(22, 15))
        plt.figure(figsize=(6, 6))
        plt.locator_params(nbins=30, axis='x')
        plt.plot(depth_list, training_score_list, ls="-", lw=2, label="training figure")
        plt.plot(depth_list, test_score_list, ls="-", lw=2, label="test figure")  # ls: 折线图线条风格, lw: 线条宽度, label: 标签文本
        plt.title(day)
        plt.legend()  # 用以显示label的内容
        # plt.show()
        plt.savefig('./day_' + str(day) + '.png')
        print("\n\n\n\n\n")


def visualization_1(data):
    """从结果来看, 没吊用"""
    data_low_low = data[
        (result["open"]["next_1_day"] < result["close"]["next_0_day"]) & (result["close"]["next_1_day"] < result["close"]["next_0_day"])]
    data_low_high = data[
        (result["open"]["next_1_day"] < result["close"]["next_0_day"]) & (result["close"]["next_1_day"] > result["close"]["next_0_day"])]
    data_high_low = data[
        (result["open"]["next_1_day"] > result["close"]["next_0_day"]) & (result["close"]["next_1_day"] < result["close"]["next_0_day"])]
    data_high_high = data[
        (result["open"]["next_1_day"] > result["close"]["next_0_day"]) & (result["close"]["next_1_day"] > result["close"]["next_0_day"])]

    data = data_low_low

    percent_series = data["open"]["next_0_day"] / 100

    target_day_list = ["next_2_day"]
    target_data_list = []
    for day in target_day_list:
        target_data_list.append([day, data["close"][day] > data["high"]["next_1_day"]])
    data = pd.DataFrame({
        "open": data["open"]["next_0_day"] / percent_series,
        "close": data["close"]["next_0_day"] / percent_series,
        "high": data["high"]["next_0_day"] / percent_series,
        "low": data["low"]["next_0_day"] / percent_series
    })

    for day, target_data in target_data_list:  # 这里要debug着看, 不然不出图???, 可以试着把图保存下来再看
        pd.scatter_matrix(data, c=target_data, figsize=(15, 15), marker='o', hist_kwds={'bins': 20}, s=60, alpha=0.8)


def idea_08(data):
    """
    测试不同max_depth的表现
    """
    data_low_low = data[
        (result["open"]["next_1_day"] < result["close"]["next_0_day"]) & (result["close"]["next_1_day"] < result["close"]["next_0_day"])]
    data_low_high = data[
        (result["open"]["next_1_day"] < result["close"]["next_0_day"]) & (result["close"]["next_1_day"] > result["close"]["next_0_day"])]
    data_high_low = data[
        (result["open"]["next_1_day"] > result["close"]["next_0_day"]) & (result["close"]["next_1_day"] < result["close"]["next_0_day"])]
    data_high_high = data[
        (result["open"]["next_1_day"] > result["close"]["next_0_day"]) & (result["close"]["next_1_day"] > result["close"]["next_0_day"])]

    data = data_low_low

    percent_series = data["open"]["next_0_day"] / 100

    target_day_list = ["next_2_day", "next_3_day", "next_4_day", "next_5_day"]
    target_data_list = []
    for day in target_day_list:
        target_data_list.append([day, (data["close"][day] > data["high"]["next_1_day"]).values])
    data = pd.DataFrame({
        # "open_previous_close_diff": (data["close"]["previous_1_day"] - data["open"]["next_0_day"]) / percent_series,
        # "high_low_diff": (data["high"]["next_0_day"] - data["low"]["next_0_day"]) / percent_series,
        # "open_close_diff": (data["open"]["next_0_day"] - data["close"]["next_0_day"]) / percent_series,
        # "close_low_diff": (data["close"]["next_0_day"] - data["low"]["next_0_day"]) / percent_series,

        "open": data["open"]["next_0_day"] / percent_series,
        "close": data["close"]["next_0_day"] / percent_series,
        "high": data["high"]["next_0_day"] / percent_series,
        "low": data["low"]["next_0_day"] / percent_series
    }).values

    for day, target_data in target_data_list:
        print("day is {0}".format(day))
        depth_list = []
        training_score_list = []
        test_score_list = []
        X_train, X_test, y_train, y_test = train_test_split(data, target_data, random_state=0)
        print("----------------", len(y_test[np.where(y_test==True)]) / len(y_test), len(y_test[np.where(y_test==True)]))
        for max_depth in range(1, 21):
            forest = RandomForestClassifier(n_estimators=100, random_state=0, max_depth=max_depth)
            forest.fit(X_train, y_train)
            print("Accuracy on training set: {:.3f}".format(forest.score(X_train, y_train)))
            print("Accuracy on test set: {:.3f}".format(forest.score(X_test, y_test)))
            training_score_list.append(forest.score(X_train, y_train))
            test_score_list.append(forest.score(X_test, y_test))
            depth_list.append(max_depth)

        # plt.figure(figsize=(22, 15))
        plt.figure(figsize=(6, 6))
        plt.locator_params(nbins=30, axis='x')
        plt.plot(depth_list, training_score_list, ls="-", lw=2, label="training figure")
        plt.plot(depth_list, test_score_list, ls="-", lw=2, label="test figure")  # ls: 折线图线条风格, lw: 线条宽度, label: 标签文本
        plt.title(day)
        plt.legend()  # 用以显示label的内容
        # plt.show()
        plt.savefig('./day_' + str(day) + '.png')
        print("\n\n\n\n\n")


def idea_07(data):
    """
    随机森林尝试
    # https://www.cnblogs.com/zichun-zeng/p/4761602.html  模型保存
    """
    max_depth_map_list = [
        {
            "next_2_day": 1,
            "next_3_day": 1,
            "next_4_day": 1,
            "next_5_day": 1,
        },
        {
            "next_2_day": 4,
            "next_3_day": 1,
            "next_4_day": 4,
            "next_5_day": 1,
        },
        {
            "next_2_day": 1,
            "next_3_day": 1,
            "next_4_day": 1,
            "next_5_day": 1,
        },
        {
            "next_2_day": 1,
            "next_3_day": 1,
            "next_4_day": 1,
            "next_5_day": 3,
        }
    ]

    data_low_low = data[
        (result["open"]["next_1_day"] < result["close"]["next_0_day"]) & (result["close"]["next_1_day"] < result["close"]["next_0_day"]) & (
                result["open"]["next_1_day"] >= result["close"]["next_1_day"])]
    data_low_high = data[
        (result["open"]["next_1_day"] < result["close"]["next_0_day"]) & (result["close"]["next_1_day"] > result["close"]["next_0_day"])]
    data_high_low = data[
        (result["open"]["next_1_day"] > result["close"]["next_0_day"]) & (result["close"]["next_1_day"] < result["close"]["next_0_day"])]
    data_high_high = data[
        (result["open"]["next_1_day"] > result["close"]["next_0_day"]) & (result["close"]["next_1_day"] > result["close"]["next_0_day"])]

    for point_tendency_type_str, data, max_depth_map in zip(["data_low_low", "data_low_high", "data_high_low", "data_high_high"],
                                                            [data_low_low, data_low_high, data_high_low, data_high_high],
                                                            max_depth_map_list):
        print(point_tendency_type_str)
        percent_series = data["open"]["next_0_day"] / 100

        target_day_list = ["next_2_day", "next_3_day", "next_4_day", "next_5_day"]
        target_data_list = []
        for day in target_day_list:
            target_data_list.append([day, (data["close"][day] > data["high"]["next_1_day"]).values])
        data = pd.DataFrame({
            "open": data["open"]["next_0_day"] / percent_series,
            "close": data["close"]["next_0_day"] / percent_series,
            "high": data["high"]["next_0_day"] / percent_series,
            "low": data["low"]["next_0_day"] / percent_series
        }).values

        forest_list = []
        for day, target_data in target_data_list:
            max_depth = max_depth_map[day]
            X_train, X_test, y_train, y_test = train_test_split(data, target_data, random_state=0)
            forest = RandomForestClassifier(n_estimators=100, random_state=0, max_depth=max_depth)
            forest.fit(X_train, y_train)
            forest_list.append([day, forest, X_train, X_test, y_train, y_test])

        for day, forest, X_train, X_test, y_train, y_test in forest_list:
            if forest.score(X_train, y_train) > 0.71 and forest.score(X_test, y_test) > 0.71:
                print("day is {0}".format(day))
                print("Accuracy on training set: {:.3f}".format(forest.score(X_train, y_train)))
                print("Accuracy on test set: {:.3f}".format(forest.score(X_test, y_test)))

                # all_ts_code = get_result_ts_code_list()
                date_now = datetime.datetime.now()
                date = datetime.datetime(date_now.year, date_now.month, date_now.day)
                all_ts_code = Result().get_strategy_result_data("bbond", 'B', date)
                for ts_code in all_ts_code:
                    security_point_data = SecurityData().get_security_point_data(ts_code, date, date)
                    if security_point_data.empty is False:
                        security_point_data = security_point_data.loc[date]
                    else:
                        continue

                    predict_data = [security_point_data["open"], security_point_data["close"], security_point_data["high"],
                                    security_point_data["low"]]
                    predict_data = np.array([predict_data]) / (predict_data[0] / 100)
                    predict_result_now = forest.predict(predict_data)
                    if predict_result_now == [True]:
                        print(ts_code, predict_result_now)
                    # print(ts_code, predict_result_now)

                print("\n\n")
        print("\n\n\n")


def start(data):
    # idea_07(data)
    idea_08(data)
    # idea_08_2(data)
    # visualization_1(data)


if __name__ == "__main__":
    result = pd.read_csv('./penetrate_lower_bband.csv', index_col=0, header=[0, 1])
    # result = result.iloc[0:5]
    start(result)
    # print(result[['close', 'open', 'pct_chg']].iloc[1:5])
