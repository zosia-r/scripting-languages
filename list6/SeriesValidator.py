from TimeSeries import TimeSeries

import abc
from typing import List



class SeriesValidator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def analyze(self, series: TimeSeries) -> List[str]:
        '''' Returns a list of strings with detected anomalies. '''
        pass



class OutlierDetector(SeriesValidator):
    def __init__(self, threshold: float = 2.0):
        self.threshold = threshold


    def analyze(self, series: TimeSeries) -> List[str]:
        stddev = series.stddev
        mean = series.mean

        if stddev is None or mean is None:
            return ['No data available for analysis.']
        
        messages = []
        for pair in series[:]:
            if abs(pair[1] - mean) > self.threshold * stddev:
                messages.append(f'Outlier detected at {pair[0]}: {pair[1]}')
        return messages
    


class ZeroSpikeDetector(SeriesValidator):
    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold


    def analyze(self, series: TimeSeries) -> List[str]:
        messages = []
        count = 0

        for pair in series[:]:
            if pair[1] == 0 or pair[1] == None:
                count += 1
                if count >= self.threshold:
                    messages.append(f'Threshold of {int(self.threshold)} zero spikes exceeded at {pair[0]}')
            else:
                count = 0
        
        return messages
    


class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float = 10.0):
        self.threshold = threshold

    def analyze(self, series: TimeSeries) -> List[str]:
        messages = []

        for pair in series[:]:
            if pair[1] > self.threshold:
                messages.append(f'Threshold of {self.threshold} exceeded at {pair[0]}: {pair[1]}')
        
        return messages