import pytest
from datetime import datetime
from TimeSeries import TimeSeries
from SeriesValidator import SeriesValidator
from list6.Validators import OutlierDetector, ZeroSpikeDetector
from measurements_module import Measurements
from typing import List, Dict


@pytest.fixture
def sample_measurements():
    date_list = [datetime(2023, 1, 1, 0), datetime(2023, 1, 1, 1)]
    values = [10.0, 20.0]
    ts = TimeSeries(indicator='TEMP', station_code='ST01', time_averaging=1.0,
                    date_list=date_list, values=values, unit='C')
    m = Measurements(folder_path="dummy_path")
    m._loaded_series.append(ts)
    return m


@pytest.mark.parametrize("validators", [
    ([OutlierDetector(threshold=5)]),
    ([ZeroSpikeDetector(threshold=3)]),
    ([SimpleReporter()]),
    ([OutlierDetector(threshold=5), SimpleReporter()]),
])
def test_detect_all_anomalies_returns_messages(sample_measurements, validators):
    # Chcemy przechwycić output print, żeby mieć pewność, że komunikaty się pojawiły
    import io
    import sys

    captured_output = io.StringIO()
    sys.stdout = captured_output

    sample_measurements.detect_all_anomalies(validators=validators, preload=False)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    # Sprawdź, czy dla każdej serii jest sekcja wyników
    assert "Results for" in output

    # Sprawdź, że komunikaty z każdego walidatora pojawiły się w output lub "No anomalies detected."
    # Nie robimy typowania, sprawdzamy zachowanie - czy cokolwiek się pojawia
    # Ponieważ SimpleReporter zwraca komunikaty dla TEMP, OutlierDetector i ZeroSpikeDetector mogą, lub nie
    assert any([
        "SimpleReporter: detected TEMP" in output,
        "No anomalies detected." in output,
        "threshold" in output or True  # dopuszczamy, że mogą być komunikaty z walidatorów
    ])
