from TimeSeries import TimeSeries
from SeriesValidator import SeriesValidator, OutlierDetector, ZeroSpikeDetector, ThresholdDetector
from typing import List, Dict
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
                date_list = df.iloc[:, 0].values.tolist()
                df = df.iloc[:, 1:]
                headers = df.columns.tolist()

                for header in headers:
                    indicator = header[1]
                    station_code = header[0]
                    time_averaging = header[2]
                    unit = header[3]
                    df[header] = df[header].astype(float)
                    values = df[header].tolist()
                    ts = TimeSeries(indicator, station_code, time_averaging, date_list, values, unit)

                    series.append(ts)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")


    return series

            
                




def run_validators(series: List[TimeSeries], validators: List[SeriesValidator]) -> Dict[str, List[str]]:
    results = {}

    for ts in series:
        key = f'Station: {ts.station_code}, Indicator: {ts.indicator}, Unit: {ts.unit}, Time Averaging: {ts.time_averaging}'
        results[key] = []
        for validator in validators:
            messages = validator.analyze(ts)
            if messages:
                results[key].extend(messages)

    return results


if __name__ == "__main__":

    warnings.filterwarnings("ignore")

    path = 'C:/Users/Zofia/Desktop/ist/IV/js/laby/scripting-languages/list5/measurements'

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