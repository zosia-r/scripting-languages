import pytest
from datetime import datetime
from TimeSeries import TimeSeries
from SeriesValidator import OutlierDetector, ZeroSpikeDetector, ThresholdDetector
from Measurements import Measurements


@pytest.fixture
def sample_ts():
    date_list = [datetime(2023, 1, 1, 0), datetime(2023, 1, 1, 1), datetime(2023, 1, 1, 2), 
                  datetime(2023, 1, 1, 3), datetime(2023, 1, 1, 4)]
    values = [10.0, 0.0, 0.0, 30.0, 25.0]
    ts = TimeSeries(indicator='TEMP', station_code='ST01', time_averaging=1.0,
                    date_list=date_list, values=values, unit='C')
    return ts

@pytest.fixture
def sample_measurements(sample_ts):
    measurements = Measurements(folder_path='../list5/measurements')
    measurements._loaded_series = [sample_ts]
    return measurements


@pytest.mark.parametrize("validators", [
    ([OutlierDetector(threshold=5)]),
    ([ZeroSpikeDetector(threshold=2)]),
    ([ThresholdDetector(threshold=29)]),
])
def test_detect_all_anomalies_returns_messages(sample_measurements, validators):
    import io
    import sys

    captured_output = io.StringIO()
    sys.stdout = captured_output

    sample_measurements.detect_all_anomalies(validators=validators, preload=False)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert "Results for" in output

    assert any([
        "zero spikes" in output,
        "No anomalies detected." in output,
        "Threshold" in output,
    ])
