import datetime
import pandas as pd
import matplotlib.pyplot as plt
from util.util_data.security_data import SecurityData
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def start(all_ts_code, date):
    """失败 准确率太低"""
    for ts_code in all_ts_code:
        print(ts_code)
        qfq_security_point_data = SecurityData().get_qfq_security_point_data(ts_code, datetime.datetime(2016, 5, 4), datetime.datetime(2019, 1, 31))
        qfq_security_point_data.sort_index(ascending=False, inplace=True)
        qfq_security_point_data.index.rename("date", inplace=True)

        security_daily_basic = SecurityData().get_security_daily_basic_data(ts_code, datetime.datetime(2016, 5, 4), datetime.datetime(2019, 1, 31))
        security_daily_basic.sort_index(ascending=False, inplace=True)
        security_daily_basic.index.rename("date", inplace=True)

        target_name_list = ["next_2_day", "next_3_day", "next_4_day", "next_5_day", "next_6_day", "next_7_day", "next_8_day", "next_9_day", "next_10_day"]
        target_data_list = []
        for window_num in range(3, 12):
            target_data_now = qfq_security_point_data["close"].rolling(window=window_num).apply(lambda x: x[0] > x[-1], raw=True)
            target_data_now = target_data_now.iloc[12:]
            target_data_list.append(target_data_now.values)

        percent_series = qfq_security_point_data["open"] / 100
        data = pd.DataFrame({
            "open": qfq_security_point_data["open"] / percent_series,
            "close": qfq_security_point_data["close"] / percent_series,
            "high": qfq_security_point_data["high"] / percent_series,
            "low": qfq_security_point_data["low"] / percent_series,
            "turnover_rate_f": security_daily_basic["turnover_rate_f"]
        }, index=qfq_security_point_data["trade_date"])
        data = data.iloc[12:]
        data = data.fillna(0)
        data = data.values

        for day, target_data in zip(target_name_list, target_data_list):
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
                if forest.score(X_test, y_test) > 0.7:
                    training_score_list.append(forest.score(X_train, y_train))
                    test_score_list.append(forest.score(X_test, y_test))
                    depth_list.append(max_depth)

            if test_score_list:
                # plt.figure(figsize=(22, 15))
                plt.figure(figsize=(6, 6))
                plt.locator_params(nbins=30, axis='x')
                plt.plot(depth_list, training_score_list, ls="-", lw=2, label="training figure")
                plt.plot(depth_list, test_score_list, ls="-", lw=2, label="test figure")  # ls: 折线图线条风格, lw: 线条宽度, label: 标签文本
                plt.title(day)
                plt.legend()  # 用以显示label的内容
                # plt.show()
                plt.savefig('./' + ts_code + 'day_' + str(day) + '.png')
                print("\n\n\n\n\n")

        aa = 1


if __name__ == "__main__":
    all_ts_code = ['000507.SZ', '300663.SZ', '601186.SH', '002013.SZ', '601118.SH', '601336.SH', '002153.SZ', '600967.SH', '603338.SH', '300349.SZ', '001979.SZ', '600283.SH',
                   '002025.SZ', '002159.SZ', '600031.SH', '600271.SH', '002579.SZ', '002179.SZ', '002439.SZ', '600036.SH', '000505.SZ']
    date = datetime.datetime.now()
    date = datetime.datetime(date.year, date.month, date.day)
    start(all_ts_code, date)
