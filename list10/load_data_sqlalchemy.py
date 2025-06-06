# C:\\Users\\alicj\\Documents\\Studia\\Python\\scripting-languages\\list10\\data\\historia_przejazdow_2021-12.csv

import sys
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Station, Rental


def get_arguments():
    if len(sys.argv) != 3:
        print("Usage: python load_data.py <database_name> <csv_path>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]


def create_session(db_name: str):
    engine = create_engine(f"sqlite:///{db_name}.db", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False)
    return Session()


def ensure_station_exists(session, station_name: str):
    if not station_name:
        return None
    station = session.query(Station).filter_by(name=station_name).first()
    if not station:
        station = Station(name=station_name)
        session.add(station)
        session.flush()
    return station


def process_csv(session, csv_path: str):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row_id, row in enumerate(reader, start=1):
            if row_id % 1000 == 0:
                print(f"Read {row_id} records")

            start_station_name = row['Stacja wynajmu']
            end_station_name = row['Stacja zwrotu']

            ensure_station_exists(session, start_station_name)
            ensure_station_exists(session, end_station_name)

            rental = Rental(
                uid=int(row['UID wynajmu']),
                bike_number=int(row['Numer roweru']),
                start_time=row['Data wynajmu'],
                end_time=row['Data zwrotu'],
                start_station_name=start_station_name,
                end_station_name=end_station_name,
                duration=int(row['Czas trwania'])
            )
            session.add(rental)


def main():
    db_name, csv_path = get_arguments()
    session = create_session(db_name)
    process_csv(session, csv_path)
    session.commit()
    print("Data import complete.")


if __name__ == "__main__":
    main()
