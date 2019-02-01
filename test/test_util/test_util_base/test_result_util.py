import datetime

import numpy as np
import pandas as pd
import pytest
from nose.tools import assert_equal, assert_almost_equal, assert_dict_equal, assert_list_equal

from source.util.util_base.result_util import format_result, print_format_result


def test_format_result():
    data = [datetime.datetime(2015, 1, 1), "中文", np.array([[1, 2], [3, 4]]), pd.Series([1, 2]), pd.DataFrame({"a": [1, 2], "b": [3, 4]})]
    result = format_result(data)
    expect_result = "[\"20150101\", \"\\u4e2d\\u6587\", [[1, 2], [3, 4]], [1, 2], {\"a\": {\"0\": 1, \"1\": 2}, \"b\": {\"0\": 3, \"1\": 4}}]"

    print_format_result(result)
    assert_equal(result, expect_result)


if __name__ == "__main__":
    import os

    pytest.main([os.path.join(os.path.curdir, __file__), "-s", "--tb=short"])
