from Measurements import Measurements
import os
import pandas as pd
from TimeSeries import TimeSeries
from typing import List, Dict
from SeriesValidator import *
from SimpleReporter import SimpleReporter

def main():
    folder_path = "C:/Users/alicj/Documents/Studia/Python/scripting-languages/list5/measurements"
    
    measurements = Measurements(folder_path)
    
    print(f"Liczba TimeSeries: {len(measurements)}") 
    
    parameter_name = "NO2"
    if parameter_name in measurements:
        print(f"Znaleziono parametr: {parameter_name}")
    else:
        print(f"Nie znaleziono parametru: {parameter_name}")
    
    print(f"TimeSeries dla parametru '{parameter_name}':")
    param_series = measurements.get_by_parameter(parameter_name)
    for ts in param_series:
        print(ts) 
    
    station_code = "DsJelGorOgin"
    print(f"TimeSeries dla stacji '{station_code}':")
    station_series = measurements.get_by_station(station_code)
    for ts in station_series:
        print(ts) 
    
    file_name = "2023_NO2_1g.csv"
    print(f"Ładowanie danych z pliku: {file_name}")
    measurements.load_series_for_file(file_name)
    print(f"Liczba TimeSeries po załadowaniu pliku: {len(measurements)}")
    
    file_name = "2023_NOx_1g.csv"
    print(f"Ładowanie danych z pliku: {file_name}")
    measurements.load_series_for_file(file_name)
    print(f"Liczba TimeSeries po załadowaniu pliku: {len(measurements)}")

    station_code = "DsJelGorOgin"
    print(f"TimeSeries dla stacji '{station_code}':")
    station_series = measurements.get_by_station(station_code)
    for ts in station_series:
        print(ts)  

    load_everything = False
    measurements.detect_all_anomalies([], False)  
    
    if load_everything:
        print(f"Liczba TimeSeries: {len (measurements)}")  
        
        parameter_name = "O3"
        if parameter_name in measurements:
            print(f"Znaleziono parametr: {parameter_name}")
        else:
            print(f"Nie znaleziono parametru: {parameter_name}")
        
        print(f"TimeSeries dla parametru '{parameter_name}':")
        param_series = measurements.get_by_parameter(parameter_name)
        for ts in param_series:
            print(ts) 
        
        station_code = "DsJelGorOgin"
        print(f"TimeSeries dla stacji '{station_code}':")
        station_series = measurements.get_by_station(station_code)
        for ts in station_series:
            print(ts) 

        print(f"Liczba TimeSeries: {len(measurements)}") 
    

if __name__ == "__main__":
    main()
