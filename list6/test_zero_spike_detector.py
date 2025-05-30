import pytest
from datetime import datetime
from TimeSeries import TimeSeries
from SeriesValidator import ZeroSpikeDetector

def test_zero_spike_detection():
    dates = [
        datetime(2023, 1, 1, 0, 0),
        datetime(2023, 1, 1, 1, 0),
        datetime(2023, 1, 1, 2, 0),
        datetime(2023, 1, 1, 3, 0),
        datetime(2023, 1, 1, 4, 0),
    ]
    values = [5.0, 0.0, None, 0.0, 8.0]

    ts = TimeSeries(
        indicator="SO2",
        station_code="ST003",
        time_averaging=1.0,
        date_list=dates,
        values=values,
        unit="ppm"
    )

    validator = ZeroSpikeDetector(threshold=3)
    messages = validator.analyze(ts)

    assert len(messages) == 1
    assert "Threshold of 3 zero spikes exceeded" in messages[0]
    assert "2023-01-01 03:00:00" in messages[0]
