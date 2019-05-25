import datetime
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from util.util_data.result import Result
from util.util_data.security_data import SecurityData

warnings.filterwarnings("ignore")

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
        "open": data["open"]["next_0_day"] / percent_series,
        "close": data["close"]["next_0_day"] / percent_series,
        "high": data["high"]["next_0_day"] / percent_series,
        "low": data["low"]["next_0_day"] / percent_series,

        "turnover_rate_f": data["turnover_rate_f"]["next_0_day"],
        "pct_chg": data["turnover_rate_f"]["next_0_day"],
    }).values

    for day, target_data in target_data_list:
        print("day is {0}".format(day))
        depth_list = []
        training_score_list = []
        test_score_list = []
        X_train, X_test, y_train, y_test = train_test_split(data, target_data, random_state=0)
        print("True result ratio:", len(y_test[np.where(y_test == True)]) / len(y_test), len(y_test[np.where(y_test == True)]))
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
            "low": data["low"]["next_0_day"] / percent_series,

            "turnover_rate_f": data["turnover_rate_f"]["next_0_day"],
            "pct_chg": data["turnover_rate_f"]["next_0_day"],
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
                date = datetime.datetime(date_now.year, date_now.month, 24)
                all_ts_code = Result().get_strategy_result_data("bbond", 'B', date)
                for ts_code in all_ts_code:
                    security_point_data = SecurityData().get_security_point_data(ts_code, date, date)
                    security_daily_basic_data = SecurityData().get_security_daily_basic_data(ts_code, date, date)

                    security_data = pd.merge(security_point_data, security_daily_basic_data, on=["ts_code", "trade_date"])
                    security_data.drop(['close_y'], axis=1, inplace=True)
                    security_data.rename(index=str, columns={"close_x": "close"}, inplace=True)

                    security_data.set_index(security_daily_basic_data["trade_date"], inplace=True)
                    security_data = security_data.sort_index()

                    if security_data.empty is False:
                        security_data = security_data.loc[date]
                    else:
                        continue

                    predict_data = [security_data["open"], security_data["close"], security_data["high"],
                                    security_data["low"]]
                    predict_data = np.array([predict_data]) / (predict_data[0] / 100)
                    predict_data = np.array([[predict_data[0][0], predict_data[0][1], predict_data[0][2], predict_data[0][3],
                                              security_data["turnover_rate_f"], security_data["pct_chg"]]])
                    predict_result_now = forest.predict(predict_data)
                    if predict_result_now == [True]:
                        print(ts_code, predict_result_now)
                    # print(ts_code, predict_result_now)

                print("\n\n")
        print("\n\n\n")


def start(data):
    idea_07(data)
    # idea_08(data)


if __name__ == "__main__":
    result = pd.read_csv('./penetrate_lower_bband.csv', index_col=0, header=[0, 1])
    # result = result.iloc[0:5]
    start(result)
    # print(result[['close', 'open', 'pct_chg']].iloc[1:5])
