def get_result_ts_code_list():
    code_str = """
    000001.SZ
    000001.SZ
    603588.SH
    603588.SH
    603588.SH
    
    """
    result_ts_code = code_str.split("\n")
    result_ts_code = list(set(result_ts_code))
    result_ts_code = [i.strip() for i in result_ts_code]
    result_ts_code = [i for i in result_ts_code if i != ""]
    return result_ts_code


if __name__ == "__main__":
    get_result_ts_code_list()
