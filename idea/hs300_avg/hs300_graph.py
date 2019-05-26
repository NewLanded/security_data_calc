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


def hs300(data):
    plt.figure(figsize=(20, 20))

    data['close'].plot(kind='line')

    # data_ori = data.loc[datetime.datetime(2018, 1, 10):datetime.datetime(2019, 1, 3)]
    # data_now = data.loc[datetime.datetime(2019, 4, 1):]
    #
    # data_ori.reset_index(drop=True, inplace=True)
    # data_now.reset_index(drop=True, inplace=True)
    #
    # data_ori['close'].plot(kind='line')
    # data_now['close'].plot(kind='line')

    plt.show()


def zx_security(data):
    plt.figure(figsize=(20, 20))

    data['close'].plot(kind='line')

    # data_ori = data.loc[datetime.datetime(2018, 1, 10):datetime.datetime(2019, 1, 3)]
    # data_now = data.loc[datetime.datetime(2019, 4, 1):]
    #
    # data_ori.reset_index(drop=True, inplace=True)
    # data_now.reset_index(drop=True, inplace=True)
    #
    # data_ori['close'].plot(kind='line')
    # data_now['close'].plot(kind='line')

    plt.show()


def start():
    security_data = SecurityData().get_index_point_data('399300.SZ', datetime.datetime(2016, 5, 3), datetime.datetime.now())
    hs300(security_data)

    security_data = SecurityData().get_security_point_data('600030.SH', datetime.datetime(2016, 5, 3), datetime.datetime.now())
    zx_security(security_data)


if __name__ == "__main__":
    start()
