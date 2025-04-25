import csv
import os


def parse_stations(stations_path):
    ''' Parses the stations csv file 
    and returns a dictionary with station codes as keys
    and their metadata as values
    '''
    stations = {}
    with open(stations_path, encoding='utf-8', mode='r') as file:
        reader = csv.DictReader(file, quotechar='"', delimiter=',')
        for row in reader:
            code = row['Kod stacji']
            stations[code] = row
    return stations



def parse_measurements(measurements_path):
    ''' Parses the measurements directory with csv files
    and return a dictionary with keys = station codes
    and values = dictionaries of measurement data
    (indicator, time_averaging, unit, position_code) as keys
    and list of pairs of dates and values as values
    '''
    measurements = {}

    for filename in os.listdir(measurements_path):
        if filename.endswith('.csv'):
            filepath = os.path.join(measurements_path, filename)

            with open(filepath, encoding='utf-8', mode='r') as file:
                reader = csv.reader(file, quotechar='"', delimiter=',')
                
                header1 = next(reader)
                header2 = next(reader)
                header3 = next(reader)
                header4 = next(reader)
                header5 = next(reader)
                header6 = next(reader)

                if (
                header2[0] != 'Kod stacji' or 
                header3[0] != 'Wskaźnik' or 
                header4[0] != 'Czas uśredniania' or 
                header5[0] != 'Jednostka' or
                header6[0] != 'Kod stanowiska'
                ):
                    print(f"File {filename} not properly formated, skipping...")
                    break


                station_codes = header2[1:]
                indicator = header3[1]
                time_averaging = header4[1]
                unit = header5[1]

                for station_code in station_codes:
                    if station_code not in measurements:
                        measurements[station_code] = {}
                    if (indicator, time_averaging, unit) not in measurements[station_code]:
                        measurements[station_code][(indicator, time_averaging, unit)] = {}
                    measurements[station_code][(indicator, time_averaging, unit)] = []

                for row in reader:
                    timestamp = row[0]
                    values = row[1:]

                    for code, value in zip(station_codes, values):
                        if value:
                            measurements[code][(indicator, time_averaging, unit)].append((timestamp, float(value)))
                 
    return measurements





if __name__ == '__main__' :
    stations_path = 'stacje.csv'
    measurements_path = 'measurements'

    stations = parse_stations(stations_path)
    i=0
    for code, data in stations.items():
        print(f"Station Code: {code}, Data: {data}")
        i+=1
        if i>10:
            break

    measurements=parse_measurements(measurements_path)
    
    i=0
    for code, data in measurements.items():
        print(f"Station Code: {code}")
        for info, values in data.items():
            print(f'Measurement info: {info}')
            j=0
            for date, value in values:
                print(f"Date: {date}, Value: {value}")
                j+=1
                if j>5:
                    break
        i+=1
        if i>5:
            break

    

    