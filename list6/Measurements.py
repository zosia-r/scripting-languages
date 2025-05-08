import os
import csv
from typing import List, Dict
from datetime import datetime
from collections import defaultdict
from TimeSeries import TimeSeries
from run_validators import parse_timeseries
import pandas as pd
from SeriesValidator import SeriesValidator 
from run_validators import *

class Measurements:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self._file_info = [] 
        self._loaded_series = []
        
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                try:
                    year, param, freq  = filename[:-4].split('_')
                    folder_path = './../list5/measurements'
                    full_path = os.path.join(folder_path, filename)
                    self._file_info.append({
                        "filename": filename,
                        "path": full_path,
                        "param": param,
                        "freq": freq,
                        "year": int(year)   
                    })
                except ValueError:
                    continue  # pomiń błędne nazwy
    
    def parse_timeseries_from_one_file(self, file_name: str):
        folder_path = self.folder_path
        filepath = os.path.join(folder_path, file_name)
        print(filepath)
        try:    
            df = pd.read_csv(filepath, quotechar='"', delimiter=',', encoding='utf-8', header=[1, 2, 3, 4, 5, 6])
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

                self._loaded_series.append(ts)
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")
    
    def __len__(self):
        return len(self._loaded_series)

    def __contains__(self, parameter_name: str) -> bool:
        for ts in self._loaded_series:
            if ts is not None and ts.indicator == parameter_name:
                return True
        return False
    
    def get_by_parameter(self, param_name: str) -> List[TimeSeries]:
        result = []
        for ts in self._loaded_series:
            if ts is not None and ts.indicator == param_name:
                result.append(ts)
        return result
    
    def get_by_station(self, station_code: str) -> List[TimeSeries]:
        result = []
        for ts in self._loaded_series:
            if ts is not None and ts.station_code == station_code:
                result.append(ts)
        return result

    def load_series_for_file(self, filename: str):
        self._loaded_series.append(self.parse_timeseries_from_one_file(filename))

    def detect_all_anomalies(self, validators: list[SeriesValidator], preload: bool = False):
        if preload:
            self._loaded_series = parse_timeseries(self.folder_path)

        validators = [
            OutlierDetector(threshold=15),
            ZeroSpikeDetector(threshold=24),
            ThresholdDetector(threshold=1000)
        ]

        results = run_validators(self._loaded_series, validators)
    
        for key, messages in results.items():
            print(f"Results for {key}:")
            if messages:
                for message in messages:
                    print(f"  - {message}")
            else:
                print("  - No anomalies detected.")
            print()
        print("Validation complete.")
