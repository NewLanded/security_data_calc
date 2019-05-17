def get_result_ts_code_list():
    code_str = """
000911.SZ
000911.SZ
000911.SZ
000911.SZ
002179.SZ
002179.SZ
002179.SZ
002179.SZ
002179.SZ
002179.SZ
002179.SZ
002179.SZ
002179.SZ
002179.SZ
002200.SZ
002200.SZ
002200.SZ
002200.SZ
002667.SZ
002667.SZ
002816.SZ
002868.SZ
600882.SH
600882.SH
600882.SH
601128.SH
601128.SH
601128.SH

    """
    result_ts_code = code_str.split("\n")
    result_ts_code = list(set(result_ts_code))
    result_ts_code = [i.strip() for i in result_ts_code]
    result_ts_code = [i for i in result_ts_code if i != ""]
    return result_ts_code


if __name__ == "__main__":
    get_result_ts_code_list()
