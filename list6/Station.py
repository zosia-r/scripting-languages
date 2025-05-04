from typing import Optional
from datetime import datetime

class Station:
    
    def __init__ (self, 
                  code: str, 
                  international_code: Optional[str], 
                  name: Optional[str] = None, 
                  old_code: Optional[str] = None, 
                  open_date: Optional[datetime] = None, 
                  close_date: Optional[datetime] = None, 
                  station_type: Optional[str] = None,
                  area_type: Optional[str] = None, 
                  kind: Optional[str] = None, 
                  voivodeship: Optional[str] = None, 
                  town: Optional[str] = None, 
                  address: Optional[str] = None, 
                  coordinate_N: Optional[float] = None, 
                  coordinate_E: Optional[float] = None):
        self.code = code
        self.international_code = international_code
        self.name = name
        self.old_code = old_code
        self.open_date = open_date
        self.close_date = close_date
        self.station_type = station_type
        self.area_type = area_type
        self.kind = kind
        self.voivodeship = voivodeship
        self.town = town
        self.address = address
        self.coordinate_N = coordinate_N
        self.coordinate_E = coordinate_E

    def __str__(self) -> str:
        return f'Station:\ncode: {self.code}, name: {self.name}\nAddress: {self.voivodeship}, {self.town}, {self.address}\n'

    def __repr__(self) -> str:
        return f'Station(code={self.code}, international_code={self.international_code}, name={self.name}, old_code={self.old_code}, open_date={self.open_date}, close_date={self.close_date}, station_type={self.station_type}, area_type={self.area_type}, kind={self.kind}, voivodeship={self.voivodeship}, town={self.town}, address={self.address}, coordinate_N={self.coordinate_N}, coordinate_E={self.coordinate_E})'

    def __eq__(self, other) -> bool:
        return self.code == other.code


