import datetime
import json
import re

import numpy as np
import pandas as pd

from util.util_base.date_util import convert_datetime_to_str


def print_format_result(result):
    class DatetimeNpPdEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return "datetime.datetime({0}, {1}, {2})".format(obj.year, obj.month, obj.day)
            elif isinstance(obj, np.ndarray):
                return "np.array({0})".format(obj.tolist())
            elif isinstance(obj, pd.Series):
                return "pd.Series({0})".format(obj.to_dict())
            elif isinstance(obj, pd.DataFrame):
                return "pd.DataFrame({0})".format(obj.to_dict())
            else:
                return json.JSONEncoder.default(self, obj)

    result = json.dumps(result, indent=4, ensure_ascii=False, cls=DatetimeNpPdEncoder)
    result = re.sub(r'"(datetime.datetime\(.*?\))"', r"\1", result)
    result = re.sub(r'"(np.array\(.*?\))"', r"\1", result)
    result = re.sub(r'"(pd.Series\(.*?\))"', r"\1", result)
    result = re.sub(r'"(pd.DataFrame\(.*?\))"', r"\1", result)
    result = re.sub(r"null", "None", result)
    print(result)


def format_result(result):
    class DatetimeNpPdEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return convert_datetime_to_str(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, pd.Series):
                return obj.tolist()
            elif isinstance(obj, pd.DataFrame):
                return obj.to_dict()
            else:
                return json.JSONEncoder.default(self, obj)

    result = json.dumps(result, cls=DatetimeNpPdEncoder)
    return result


if __name__ == "__main__":
    print_format_result([datetime.datetime(2015, 1, 1), "中文", np.array([[1, 2], [3, 4]]), pd.Series([1, 2]), pd.DataFrame({"a": [1, 2], "b": [3, 4]})])
