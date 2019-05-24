import pandas as pd


def start(data):
    pass


if __name__ == "__main__":
    # aa.loc[:, ('B', 'E')] = [9, 10]  # 多重索引赋值

    result = pd.read_csv('./penetrate_lower_bband.csv', index_col=0, header=[0, 1])
    # result = start(result)
    result_2 = result.set_index([["ts_code", "next_0_day"], ["trade_date", "next_0_day"]])
    aa = 1
    # result.to_csv('./penetrate_lower_bband_added_columns.csv')
