import argparse
import pandas as pd
import os
import random
from datetime import datetime
import logging
import sys

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()  
    ]
)
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logging.getLogger().addHandler(error_handler)


def parse_args():
    parser = argparse.ArgumentParser(description="Air Quality Analysis CLI")

    # Common arguments
    parser.add_argument('-p', '--parameter', required=True, help='Measured parameter (e.g., As(PM10), NO2, O3)')
    parser.add_argument('-f', '--frequency', required=True, choices=['1g', '24g'], help='Measurement frequency')
    parser.add_argument('-s', '--start', required=True, help='Start date (yyyy-mm-dd)')
    parser.add_argument('-e', '--end', required=True, help='End date (yyyy-mm-dd)')

    # Subparsers – commands
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Command: station
    station_parser = subparsers.add_parser('station', help='Random station with measurements')

    # Command: statistics
    stat_parser = subparsers.add_parser('statistics', help='Statistics for a specific station')
    stat_parser.add_argument('--station', required=True, help='Station name')

    return parser.parse_args()


def find_file(parameter, frequency):
    files = os.listdir("measurements")
    for file in files:
        if parameter in file and frequency in file:
            logging.info(f"File {file} found.")
            return os.path.join("measurements", file)
    logging.error(f"File for {parameter} {frequency} not found.")
    raise FileNotFoundError(f"File not found for {parameter} {frequency}")


def is_between_dates(date_str, start_str, end_str):
    try:
        date = datetime.strptime(date_str, "%m/%d/%y %H:%M")
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d")

        return start <= date <= end
    except ValueError as e:
        logging.warning(f"Wrong format of date: {e}")
        return False


def get_station_codes(file):
    try:
        df = pd.read_csv(file, dtype=str)
        logging.info(f"File {file} opened and closed successfully.")
    except FileNotFoundError:
        logging.critical(f"File {file} could not be opened.")
        raise
    station_codes = df.iloc[0].to_numpy()
    return list(station_codes)


def get_station_number(file, station_code):
    stations = get_station_codes(file)
    try:
        number = stations.index(station_code)
        return number
    except ValueError:
        logging.error(f"Station code '{station_code}' not found.")
        raise


def load_data(file, start_date, end_date):
    try:
        df = pd.read_csv(file, header=0, dtype=str)
        logging.info(f"File {file} opened and closed successfully.")
    except FileNotFoundError:
        logging.critical(f"File {file} could not be opened.")
        raise

    bytes_read = 0
    filtered_rows = []
    for _, row in df.iterrows():
        bytes_read += row.memory_usage(deep=True)
        logging.debug(f"Bytes read so far: {bytes_read}")  # Logowanie liczby przeczytanych bajtów
        if is_between_dates(row["Nr"], start_date, end_date):
            filtered_rows.append(row)

    filtered_df = pd.DataFrame(filtered_rows)
    return filtered_df


def get_station_info(station_code, file='stacje.csv'):
    try:
        df = pd.read_csv(file, header=0, dtype=str)
        logging.info(f"File {file} opened and closed successfully.")
    except FileNotFoundError:
        logging.critical(f"File {file} could not be opened.")
        raise
    match = df[df['Kod stacji'].str.startswith(station_code)]
   
    if not match.empty:
        name = match.iloc[0]['Nazwa stacji']
        address = "Województwo " + match.iloc[0]['Województwo'] + ", " + match.iloc[0]['Miejscowość'] + ", " + match.iloc[0]['Adres']
        return name, address
    else:
        logging.warning(f"No information found for station '{station_code}' in stacje.csv")
        return None, None


def random_station(file, df):
    if df.empty:
        logging.warning("No stations satisfying the criteria.")
        return
    
    stations = get_station_codes(file)
    for i in range(len(stations)-1, 0, -1):
        is_empty = df[str(i)].isna().all()
        if is_empty:
            del stations[i]
    del stations[0]

    if not stations:
        logging.warning("No stations satisfying the criteria.")
        return
    
    station = random.choice(stations)
    name, address = get_station_info(station)
    logging.info(f"Random station: {name}, Address: {address}")


def statistics(df, station, file):
    try:
        station_nr = get_station_number(file, station)
    except Exception:
        raise ValueError(f"Station with code '{station}' was not found.")

    if str(station_nr) not in df.columns:
        logging.error(f"Column for station number {station_nr} is missing in the dataset.")
        raise ValueError(f"Column for station number {station_nr} is missing in the dataset.")

    data = pd.to_numeric(df[str(station_nr)], errors='coerce').dropna().astype(float)

    if data.empty:
        logging.warning(f"No available data for station '{station}'.")
        raise ValueError(f"No available data for station '{station}'.")

    print(f"Statistics for station {station}:")
    print(f"Average: {data.mean():.2f}")
    print(f"Standard deviation: {data.std():.2f}")


def main():
    args = parse_args()

    file = find_file(args.parameter, args.frequency)
    
    df = load_data(file, args.start, args.end)
    
    if args.command == "station":
        random_station(file, df)
    elif args.command == "statistics":
        statistics(df, args.station, file)


if __name__ == "__main__":
    main()
