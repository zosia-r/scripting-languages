import pytest
from datetime import datetime
from TimeSeries import TimeSeries

@pytest.fixture
def timeseries_complete():
    return TimeSeries(
        indicator="PM10",
        station_code="ST001",
        time_averaging=1.0,
        date_list=[
            datetime(2022, 1, 1, 0, 0),
            datetime(2022, 1, 1, 1, 0),
            datetime(2022, 1, 1, 2, 0)
        ],
        values=[10.0, 10.0, 10.0],
        unit="g/m3"
    )

@pytest.fixture
def timeseries_with_none():
    return TimeSeries(
        indicator="PM10",
        station_code="ST001",
        time_averaging=1.0,
        date_list=[
            datetime(2022, 1, 1, 0, 0),
            datetime(2022, 1, 1, 1, 0),
            datetime(2022, 1, 1, 2, 0),
            datetime(2022, 1, 1, 3, 0)
        ],
        values=[10.0, None, 10.0, None],
        unit="g/m3"
    )

def test_mean_stddev_complete(timeseries_complete):
    assert timeseries_complete.mean == pytest.approx(10.0)
    assert timeseries_complete.stddev == pytest.approx(0.0)

def test_mean_stddev_with_none(timeseries_with_none):
    assert timeseries_with_none.mean == pytest.approx(10.0)
    assert timeseries_with_none.stddev == pytest.approx(0.0)
