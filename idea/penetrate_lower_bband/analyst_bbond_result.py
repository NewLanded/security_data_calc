import datetime

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import numpy as np

from strategy.manual.result_code import get_result_ts_code_list
from util.util_data.security_data import SecurityData


def idea_01(data):
    """
    上穿布林线下线后, 第一天低开低走, 那么后5天会赚的几率
    result: 0.5024657534246575
    """
    data = data[
        (result["open"]["next_1_day"] < result["close"]["next_0_day"]) & (result["close"]["next_1_day"] < result["close"]["next_0_day"])]
    raise_data = data[data["close"]["next_5_day"] > data["close"]["next_1_day"]]
    raise_percent = len(raise_data) / len(data)
    print(raise_percent)


def idea_02(data):
    """
    上穿布林线下线后, 第一天低开高走, 那么后5天会赚的几率
    result: 0.5339223729883243
    """
    data = data[
        (result["open"]["next_1_day"] < result["close"]["next_0_day"]) & (result["close"]["next_1_day"] > result["close"]["next_0_day"])]
    raise_data = data[data["close"]["next_5_day"] > data["close"]["next_1_day"]]
    raise_percent = len(raise_data) / len(data)
    print(raise_percent)


def idea_03(data):
    """
    上穿布林线下线后, 第一天高开低走, 那么后5天会赚的几率
    result: 0.5150881386316104
    """
    data = data[
        (result["open"]["next_1_day"] > result["close"]["next_0_day"]) & (result["close"]["next_1_day"] < result["close"]["next_0_day"])]
    raise_data = data[data["close"]["next_5_day"] > data["close"]["next_1_day"]]
    raise_percent = len(raise_data) / len(data)
    print(raise_percent)


def idea_04(data):
    """
    上穿布林线下线后, 第一天高开高走, 那么后5天会赚的几率
    result: 0.5430604982206406
    """
    data = data[
        (result["open"]["next_1_day"] > result["close"]["next_0_day"]) & (result["close"]["next_1_day"] > result["close"]["next_0_day"])]
    raise_data = data[data["close"]["next_5_day"] > data["close"]["next_1_day"]]
    raise_percent = len(raise_data) / len(data)
    print(raise_percent)


def idea_05(data):
    """
    上穿布林线下线后, 第一天高开高走且涨幅>2%, 那么后5天会赚的几率
    result: 0.5847529812606473
    """
    data = data[
        (result["open"]["next_1_day"] > result["close"]["next_0_day"]) & (result["close"]["next_1_day"] > result["close"]["next_0_day"]) & (
                result["pct_chg"]["next_1_day"] > 0.02)]
    raise_data = data[data["close"]["next_5_day"] > data["close"]["next_1_day"]]
    raise_percent = len(raise_data) / len(data)
    print(raise_percent)


def idea_06(data):
    """
    随机森林尝试
    Accuracy on training set: 0.766
    Accuracy on test set: 0.765
    """

    # https://www.cnblogs.com/zichun-zeng/p/4761602.html  模型保存

    data = data[
        (result["open"]["next_1_day"] < result["close"]["next_0_day"]) & (result["close"]["next_1_day"] < result["close"]["next_0_day"])]

    percent_series = data["open"]["next_0_day"] / 100

    target = (data["close"]["next_5_day"] > data["high"]["next_1_day"]).values
    data = pd.DataFrame({
        "open": data["open"]["next_0_day"] / percent_series,
        "close": data["close"]["next_0_day"] / percent_series,
        "high": data["high"]["next_0_day"] / percent_series,
        "low": data["low"]["next_0_day"] / percent_series
    }).values

    X_train, X_test, y_train, y_test = train_test_split(data, target, random_state=0)
    forest = RandomForestClassifier(n_estimators=100, random_state=0, max_depth=12)
    forest.fit(X_train, y_train)

    print("Accuracy on training set: {:.3f}".format(forest.score(X_train, y_train)))
    print("Accuracy on test set: {:.3f}".format(forest.score(X_test, y_test)))

    all_ts_code = get_result_ts_code_list()
    date = datetime.datetime(2019, 3, 29)
    for ts_code in all_ts_code:
        security_point_data = SecurityData().get_security_point_data(ts_code, date, date).loc[date]
        predict_data = [security_point_data["open"], security_point_data["close"], security_point_data["high"], security_point_data["low"]]
        predict_data = np.array([predict_data]) / (predict_data[0] / 100)
        print(ts_code, forest.predict(predict_data))


def start(data):
    # idea_01(data)
    # idea_02(data)
    # idea_03(data)
    # idea_04(data)
    # idea_05(data)
    idea_06(data)


if __name__ == "__main__":
    result = pd.read_csv('./penetrate_lower_bband.csv', index_col=0, header=[0, 1])
    # result = result.iloc[0:5]
    start(result)
    # print(result[['close', 'open', 'pct_chg']].iloc[1:5])
