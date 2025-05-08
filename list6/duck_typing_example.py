import os
import pandas as pd
from TimeSeries import TimeSeries
from typing import List, Dict
from SeriesValidator import *
from SimpleReporter import SimpleReporter


def parse_one_timeseries_from_one_file(file_name: str, folder_path: str):
    filepath = os.path.join(folder_path, file_name)
    print(filepath)
    try:    
        df = pd.read_csv(filepath, quotechar='"', delimiter=',', encoding='utf-8', header=[1, 2, 3, 4, 5, 6])
        date_list = df.iloc[:, 0].values.tolist()
        df = df.iloc[:, 1:]
        headers = df.columns.tolist()   
        header = headers[0]
        
        indicator = header[1]
        station_code = header[0]
        time_averaging = header[2]
        unit = header[3]
        df[header] = df[header].astype(float)
        values = df[header].tolist()

        ts = TimeSeries(indicator, station_code, time_averaging, date_list, values, unit)   
        return ts
    except Exception as e:
        print(f"Error processing file {file_name}: {e}")


def run_validators(series: TimeSeries, validators: List[SeriesValidator]) -> Dict[str, List[str]]:
    results = {}

    key = f'Station: {series.station_code}, Indicator: {series.indicator}, Unit: {series.unit}, Time Averaging: {series.time_averaging}'
    results[key] = []
    for validator in validators:
        messages = validator.analyze(series)
        if messages:
            results[key].extend(messages)

    return results


def main():
    folder_path = "C:/Users/alicj/Documents/Studia/Python/scripting-languages/list5/measurements"
    ts = parse_one_timeseries_from_one_file("2023_NOx_1g.csv", folder_path)
    
    analyzing_objects = [
        OutlierDetector(threshold=15),
        ZeroSpikeDetector(threshold=24),
        ThresholdDetector(threshold=1000),
        SimpleReporter()
    ]

    results = run_validators(ts, analyzing_objects)

    for key, messages in results.items():
        print(f"Results for {key}:")
        if messages:
            for message in messages:
                print(f"  - {message}")
        else:
            print("  - No anomalies detected.")
        print()
    print("Validation complete.")


if __name__ == "__main__":
    main()
