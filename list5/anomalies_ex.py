import numpy as np
from datetime import datetime
from ex1 import parse_measurements


def anomaly(time, value, station, unit, missing_percentage=0.02, zero_percentage=0.02, max_change=200, time_format='%m/%d/%y %H:%M'):
    '''Function to detect anomalies in data.
    :param time: list of dates
    :param value: list of values
    :param station: list of station codes
    :param unit: size of anomaly
    '''
    
    count_values = len(value)
    count_nan = value.count(None)
    count_0 = value.count(0)

    array = np.array([v for v in value if v is not None and v > 0], dtype=float)
    array = array[~np.isnan(array)]
    
    if len(array) >= 2:
        max_percentage_change = np.max(np.abs(np.diff(array) / array[:-1])) * 100
    else:
        max_percentage_change = 0


    time_anomaly = False
    try:
        time_parsed = [t if isinstance(t, datetime) else datetime.strptime(str(t), time_format) for t in time]
        time_diffs = np.diff([t.timestamp() for t in time_parsed])
        if len(set(time_diffs)) > 1:
            time_anomaly = True
    except Exception as e:
        print(f"\t[!] Failed to check time intervals: {e}")
        time_anomaly = True

    if (count_nan > missing_percentage*count_values or
        count_0 > zero_percentage*count_values or
        max_percentage_change > max_change or
        time_anomaly):
        print(f'Anomalies in {station} for {unit}:')
        if count_nan > 0.02*count_values:
            print(f'\t NaN values: {count_nan} ({count_nan/count_values*100:.3f}%)')
        if count_0 > 0.02*count_values:
            print(f'\t 0 values: {count_0} ({count_0/count_values*100:.3f}%)')
        if max_percentage_change > 100:
            print(f'\t Max percentage change: {max_percentage_change:.2f}%')
        if time_anomaly:
            print(f'\t Irregular time intervals detected: {len(set(time_diffs))} unique intervals: {set(time_diffs)}')
        print('*'*5)
    else:
        print(f'No anomalies for station {station} for {unit}')



if __name__ == '__main__':
    data = parse_measurements('measurements')
    i=0
    for station, measurements in data.items():
        j=0
        for info, data in measurements.items():
            unit = info[0]
            time = [x[0] for x in data]
            value = [x[1] for x in data]
            anomaly(time, value, station, unit)
            j+=1
            if j>5:
                break
        i+=1
        if i>5:
                break
