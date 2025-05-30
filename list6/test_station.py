import pytest


from Station import Station

def test_station_eq_same_code():
    station1 = Station(code="XYZ123", name="Station A")
    station2 = Station(code="XYZ123", name="Station B")
    assert station1 == station2

def test_station_eq_different_code():
    station1 = Station(code="XYZ123", name="Station A")
    station2 = Station(code="ABC987", name="Station A")
    assert station1 != station2

def test_station_eq_non_station_object():
    station = Station(code="XYZ123", name="Station A")
    not_a_station = "XYZ123"
    assert station != not_a_station
