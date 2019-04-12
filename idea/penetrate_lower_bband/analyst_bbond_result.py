import pandas as pd


def start(data):
    # 上穿布林线下线后, 第一天跌, 那么后5天会赚的几率
    data


if __name__ == "__main__":
    result = pd.read_csv('./penetrate_lower_bband.csv', index_col=0, header=[0, 1])
    start(result)
    print(result[['close', 'open', 'pct_chg']].iloc[1:5])


