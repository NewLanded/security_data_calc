def get_result_ts_code_list():
    code_str = """
002365.SZ
002365.SZ
002365.SZ
002365.SZ
002365.SZ
002626.SZ
002626.SZ
002626.SZ
002626.SZ
002626.SZ
002626.SZ
002742.SZ
002742.SZ
002742.SZ
600179.SH
600179.SH
600179.SH
600179.SH
600179.SH
600179.SH
600179.SH
600179.SH
600698.SH
600698.SH
600698.SH
600698.SH
600698.SH
600698.SH
600698.SH
601333.SH
601333.SH
601333.SH
601333.SH
601333.SH
601333.SH
601333.SH
603806.SH
    """
    result_ts_code = code_str.split("\n")
    result_ts_code = list(set(result_ts_code))
    result_ts_code = [i.strip() for i in result_ts_code]
    result_ts_code = [i for i in result_ts_code if i != ""]
    return result_ts_code


if __name__ == "__main__":
    get_result_ts_code_list()
