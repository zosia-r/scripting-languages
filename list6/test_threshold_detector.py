import pytest
from datetime import datetime
from TimeSeries import TimeSeries
from SeriesValidator import ThresholdDetector

def test_threshold_detector_detects_exceeding_values():
    dates = [
        datetime(2023, 1, 1, 0, 0),
        datetime(2023, 1, 1, 1, 0),
        datetime(2023, 1, 1, 2, 0)
    ]
    values = [5.0, 15.0, 8.0]

    ts = TimeSeries(
        indicator="NO2",
        station_code="ST004",
        time_averaging=1.0,
        date_list=dates,
        values=values,
        unit="g/m"
    )

    validator = ThresholdDetector(threshold=10.0)
    messages = validator.analyze(ts)

    assert len(messages) == 1
    assert "Threshold of 10.0 exceeded at 2023-01-01 01:00:00" in messages[0]
