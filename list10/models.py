from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, Text
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import csv
from sqlalchemy.orm import sessionmaker


class Base(DeclarativeBase):
    pass

class Station(Base):
    __tablename__ = "bike_stations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

class Rental(Base):
    __tablename__ = "rentals"

    uid: Mapped[int] = mapped_column(primary_key=True)
    bike_number: Mapped[int] = mapped_column(nullable=False)
    start_time: Mapped[str] = mapped_column(Text, nullable=False)
    end_time: Mapped[str] = mapped_column(Text, nullable=False)
    start_station_name: Mapped[int] = mapped_column(nullable=True)
    end_station_name: Mapped[int] = mapped_column(nullable=True)
    duration: Mapped[int] = mapped_column(nullable=False)

engine = create_engine("sqlite:///bike_rentals.db", echo=False)
Session = sessionmaker(bind=engine, autoflush=False)

"""
Session = None
engine = None

def init_session(db_name: str):
    global Session, engine
    engine = create_engine(f"sqlite:///{db_name}", echo=False)
    Session = sessionmaker(bind=engine, autoflush=False)
    return Session
"""
if __name__ == "__main__":
    # Create tables
    Base.metadata.create_all(engine)

    # Create session
    session = Session()

    # Load rentals from CSV
    with open("C:\\Users\\alicj\\Documents\\Studia\\Python\\scripting-languages\\list10\\data\\historia_przejazdow_2021-12.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rowId = 0
        for row in reader:
            rowId+=1
            if rowId%1000 == 0:
                print(f"Read {rowId} records")
            uid = int(row['UID wynajmu'])
            bike_number = int(row['Numer roweru'])
            start_time = row['Data wynajmu']
            end_time = row['Data zwrotu']
            start_station_name = row['Stacja wynajmu']
            end_station_name = row['Stacja zwrotu']
            duration = int(row['Czas trwania'])

                # Dodaj brakującą stację początkową, jeśli nie istnieje
            if start_station_name is not None:
                start_station = session.query(Station).filter_by(name=start_station_name).first()
                if not start_station:
                    start_station = Station(name=start_station_name)
                    session.add(start_station)
                    session.flush()

            # Dodaj brakującą stację końcową, jeśli nie istnieje
            if end_station_name is not None:
                end_station = session.query(Station).filter_by(name=end_station_name).first()
                if not end_station:
                    end_station = Station(name=end_station_name)
                    session.add(end_station)
                    session.flush()

            rental = Rental(
                uid = int(row['UID wynajmu']),
                bike_number = int(row['Numer roweru']),
                start_time = row['Data wynajmu'],
                end_time = row['Data zwrotu'],
                start_station_name = row['Stacja wynajmu'],
                end_station_name = row['Stacja zwrotu'],
                duration = int(row['Czas trwania'])
                
            )
            session.add(rental)

    # Commit all changes
    session.commit()
