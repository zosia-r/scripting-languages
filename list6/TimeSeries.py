from typing import List, Optional, Union
from datetime import datetime, date
import numpy as np

class TimeSeries:

    def __init__ (self, 
                  indicator: str, 
                  station_code: str, 
                  time_averaging: float, 
                  date_list: List[datetime], 
                  values: Union[List[Optional[float]], np.ndarray], 
                  unit: Optional[str] = None):
        self.indicator = indicator
        self.station_code = station_code
        self.time_averaging = time_averaging
        self.date_list = date_list
        self.values = values
        self.unit = unit

    def __str__(self) -> str:
        return f'TimeSeries:\nIndicator: {self.indicator}, Station code: {self.station_code}, Time averaging: {self.time_averaging}, Unit: {self.unit}\nDates: {self.date_list}\nValues: {self.values}'
    
    def __repr__(self) -> str:
        return f'TimeSeries(indicator={self.indicator}, station_code={self.station_code}, time_averaging={self.time_averaging}, date_list={self.date_list}, values={self.values}, unit={self.unit})'
    
    def __eq__(self, other) -> bool:
        return self.indicator == other.indicator and self.station_code == other.station_code and self.time_averaging == other.time_averaging and self.unit == other.unit
    
    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key, slice):
            return (self.date_list[key], self.values[key])

        elif isinstance(key, datetime) or isinstance(key, date):
            results = []
            for dt, value in zip(self.date_list, self.values):
                if isinstance(key, datetime) and dt == key:
                    return value
                elif isinstance(key, date) and dt.date() == key:
                    results.append(value)
            if results:
                return results
            raise KeyError(f'No data for date {key}')
        
        else:
            raise TypeError('Key must be of type int, slice, datetime.date or datetime.datetime')
        

    @property
    def mean(self):
        return np.mean(self.values) if self.values else None
    
    @property
    def stddev(self):
        return np.std(self.values) if self.values else None
    
        
