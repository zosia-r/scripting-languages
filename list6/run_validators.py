from TimeSeries import TimeSeries
from SeriesValidator import SeriesValidator, OutlierDetector, ZeroSpikeDetector, ThresholdDetector
from typing import List, Dict, Union, Any
from datetime import datetime
import os
import warnings
import pandas as pd

def parse_timeseries(file_path: str):
    series = []

    for filename in os.listdir(file_path):
        if filename.endswith('.csv'):
            try:    
                filepath = os.path.join(file_path, filename)

                df = pd.read_csv(filepath, quotechar='"', delimiter=',', encoding='utf-8', header=[1, 2, 3, 4, 5])
                date_list_str: Union[List[Any], str] = df.iloc[:, 0].values.tolist()
                df = df.iloc[:, 1:]
                headers = df.columns.tolist()

                i: int
                date: str
                date_list: List[datetime] = []
                for i, date in enumerate(date_list_str):
                    if isinstance(date, str):
                        date_list[i] = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

                for header in headers:
                    indicator = header[1]
                    station_code = header[0]
                    time_averaging_str: str = header[2]
                    time_averaging: float = float(time_averaging_str)
                    unit = header[3]
                    df[header] = df[header].astype(float)
                    values = df[header].tolist()
                    ts = TimeSeries(indicator, station_code, time_averaging, date_list, values, unit)

                    series.append(ts)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")


    return series

            
                




def run_validators(series: List[TimeSeries], validators: List[SeriesValidator]) -> Dict[str, List[str]]:
    results: Dict[str, List[str]] = {}

    for ts in series:
        if ts is not None:
            key = f'Station: {ts.station_code}, Indicator: {ts.indicator}, Unit: {ts.unit}, Time Averaging: {ts.time_averaging}'
            results[key] = []
            for validator in validators:
                messages = validator.analyze(ts)
                if messages:
                    results[key].extend(messages)

    return results


if __name__ == "__main__":

    warnings.filterwarnings("ignore")

    path = '../list5/measurements'

    series = parse_timeseries(path)

    validators = [
        OutlierDetector(threshold=15),
        ZeroSpikeDetector(threshold=24),
        ThresholdDetector(threshold=1000)
    ]

    results = run_validators(series, validators)
    
    for key, messages in results.items():
        print(f"Results for {key}:")
        if messages:
            for message in messages:
                print(f"  - {message}")
        else:
            print("  - No anomalies detected.")
        print()
    print("Validation complete.")