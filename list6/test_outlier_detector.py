import pytest
from datetime import datetime
from TimeSeries import TimeSeries
from SeriesValidator import OutlierDetector

def test_outlier_detection():
    dates = [
        datetime(2023, 1, 1, 0, 0),
        datetime(2023, 1, 1, 1, 0),
        datetime(2023, 1, 1, 2, 0),
        datetime(2023, 1, 1, 3, 0),
        datetime(2023, 1, 1, 4, 0),
    ]
    values = [10.0, 1100000.0, 10.5, 10.8, 10.0]

    ts = TimeSeries(
        indicator="PM2.5",
        station_code="ST002",
        time_averaging=1.0,
        date_list=dates,
        values=values,
        unit="g/m3"
    )

    validator = OutlierDetector(threshold=2.0)
    messages = validator.analyze(ts)

    assert len(messages) == 1
    assert "Outlier detected" in messages[0]
    assert "2023-01-01 04:00:00" in messages[0]


