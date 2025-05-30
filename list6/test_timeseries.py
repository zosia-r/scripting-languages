import pytest
from TimeSeries import TimeSeries
from datetime import datetime, date, timedelta


@pytest.fixture
def sample_series():
    base_date = datetime(2024, 1, 1)
    dates = [base_date + timedelta(days=i) for i in range(5)]
    values = [1.0, 2.0, None, 4.0, 5.0]
    return TimeSeries('CO2', 'ABC123', '24h', dates, values)

def test_get_by_index(sample_series):
    result = sample_series[1]
    assert result == (datetime(2024, 1, 2), 2.0)

def test_get_by_slice(sample_series):
    result = sample_series[1:4]
    expected = [
        (datetime(2024, 1, 2), 2.0),
        (datetime(2024, 1, 3), None),
        (datetime(2024, 1, 4), 4.0)
    ]
    assert result == expected

def test_get_by_existing_date(sample_series):
    result = sample_series[datetime(2024, 1, 3)]
    assert result == None

def test_get_by_missing_date(sample_series):
    with pytest.raises(KeyError):
        sample_series[date(2024, 1, 10)]
