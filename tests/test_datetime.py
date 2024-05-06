from datetime import date, datetime

import pytest

from skytek_utils.datetime import ensure_datetime


@pytest.mark.parametrize(
    "input, expected_output",
    [
        ("2023-10-01", datetime(2023, 10, 1)),
        ("2023-10-01 15:32:29", datetime(2023, 10, 1, 15, 32, 29)),
        (datetime(2023, 10, 1, 15, 32, 29), datetime(2023, 10, 1, 15, 32, 29)),
        (datetime(2023, 10, 1), datetime(2023, 10, 1)),
        (date(2023, 10, 1), datetime(2023, 10, 1)),
    ],
)
# fmt: on
def test_ensure_datetime(input, expected_output):
    output = ensure_datetime(input)
    assert output == expected_output
