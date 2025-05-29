from TimeSeries import TimeSeries

import abc
from typing import List, Optional, Union, Set
from datetime import datetime, timedelta



class SeriesValidator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def analyze(self, series: TimeSeries) -> List[str]:
        '''' Returns a list of strings with detected anomalies. '''
        pass



class OutlierDetector(SeriesValidator):
    def __init__(self, threshold: float = 2.0) -> None:
        self.threshold: float  = threshold


    def analyze(self, series: TimeSeries) -> List[str]:
        stddev: Optional[float] = series.stddev
        mean: Optional[float] = series.mean

        if stddev is None or mean is None:
            return ['No data available for analysis.']
        
        messages: List[str] = []
        for pair in series[:]:
            if abs(pair[1] - mean) > self.threshold * stddev:
                messages.append(f'Outlier detected at {pair[0]}: {pair[1]}')
        return messages
    


class ZeroSpikeDetector(SeriesValidator):
    def __init__(self, threshold: float = 3.0) -> None:
        self.threshold: float = threshold


    def analyze(self, series: TimeSeries) -> List[str]:
        messages: List[str] = []
        count: int = 0

        for pair in series[:]:
            if pair[1] == 0 or pair[1] == None:
                count += 1
                if count >= self.threshold:
                    messages.append(f'Threshold of {int(self.threshold)} zero spikes exceeded at {pair[0]}')
            else:
                count = 0
        
        return messages
    


class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float = 10.0) -> None:
        self.threshold: float = threshold

    def analyze(self, series: TimeSeries) -> List[str]:
        messages: List[str] = []

        for pair in series[:]:
            if pair[1] > self.threshold:
                messages.append(f'Threshold of {self.threshold} exceeded at {pair[0]}: {pair[1]}')
        
        return messages
    

class CompositeValidator(SeriesValidator):
    def __init__(self, validators: List[SeriesValidator], mode: str = 'OR') -> None:
        if mode.upper() not in ('OR', 'AND'):
            raise ValueError("mode must be 'OR' or 'AND'")
        self.validators: List[SeriesValidator] = validators
        self.mode: str = mode.upper()

    def analyze(self, series: TimeSeries) -> List[str]:
        all_messages: List[str] = []
        for validator in self.validators:
            messages: List[str] = validator.analyze(series)
            if messages:
                all_messages.extend(messages)

        match self.mode:
            case 'OR':
                return self._get_all_messages(all_messages)

            case 'AND':
                return self._get_common_messages(all_messages)
        
    def _get_common_messages(self, all_messages: List[List[str]]) -> List[str]:
        if not all_messages:
            return []

        common: Set = set()

        sublist1: List[str] = all_messages[0]
        if not sublist1:
            return []
        
        for item in sublist1:
            present: bool = True
            for sublist in all_messages[1:]:
                if item not in sublist:
                    present = False
                    break
            if present:
                common.add(item)

        return list(common)

    
    def _get_all_messages(self, all_messages: List[str]) -> List[str]:
        if not all_messages:
            return []
        
        flat_messages: List[str] = [item for sublist in all_messages for item in sublist]
        all: Set = set(flat_messages)
        return list(all)