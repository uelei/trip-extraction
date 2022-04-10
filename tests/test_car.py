import json
from datetime import datetime, timedelta

from trip_extraction.model import Car, Waypoint


def test_empty_car_trip():
    car = Car()

    assert car.trips == []

    assert car.last_recorded_point is None


def test_car_record_waypoint():
    car = Car()
    now = datetime.now()
    now_str = now.isoformat()
    wp = Waypoint(timestamp=now_str, lat=10.2, lng=34.9)

    car.record_point(wp)

    assert car.last_recorded_point == wp

    assert car.trips == []


def test_car_trip_started():
    car = Car()
    now = datetime.now()
    now_str = now.isoformat()
    wp = Waypoint(timestamp=now_str, lat=10.2, lng=34.9)

    car.record_point(wp)

    assert car.last_recorded_point == wp

    assert car.trips == []

    past2m = now + timedelta(minutes=2)
    wp2 = Waypoint(timestamp=past2m.isoformat(), lat=10.2, lng=34.95)

    car.record_point(wp2)

    assert car.last_recorded_point == wp2

    assert car.trips != []


def test_car_trip_stoped():
    car = Car()
    now = datetime.now()
    now_str = now.isoformat()
    wp = Waypoint(timestamp=now_str, lat=10.2, lng=34.9)

    car.record_point(wp)

    assert car.last_recorded_point == wp

    assert car.trips == []

    past2m = now + timedelta(minutes=2)
    wp2 = Waypoint(timestamp=past2m.isoformat(), lat=10.2, lng=34.95)

    car.record_point(wp2)

    assert car.last_recorded_point == wp2

    assert car.trips != []

    trip = car.trips[0]

    assert trip.end.timestamp == wp2.timestamp

    past5m = past2m + timedelta(minutes=5)
    wp3 = Waypoint(timestamp=past5m.isoformat(), lat=10.2, lng=34.95)

    car.record_point(wp3)

    assert car.last_recorded_point == wp3

    trip = car.trips[0]

    assert trip.end.timestamp == wp2.timestamp


def test_car_jumps_waypoints():
    car = Car()
    now = datetime.now()
    now_str = now.isoformat()
    wp = Waypoint(timestamp=now_str, lat=10.2, lng=34.9)

    car.record_point(wp)

    assert car.last_recorded_point == wp

    assert car.trips == []

    past2m = now + timedelta(minutes=2)
    wp2 = Waypoint(timestamp=past2m.isoformat(), lat=10.2, lng=34.95)

    car.record_point(wp2)

    assert car.last_recorded_point == wp2

    assert car.trips != []

    trip = car.trips[0]

    assert trip.end.timestamp == wp2.timestamp

    # jump waypoint
    past3m = past2m + timedelta(minutes=1)
    wp3 = Waypoint(timestamp=past3m.isoformat(), lat=10.2, lng=-90.10)

    car.record_point(wp3)

    assert car.last_recorded_point == wp2

    trip = car.trips[0]

    assert trip.end.timestamp == wp2.timestamp


def test_car_with_sample_data():
    car = Car()

    with open("data/waypoints.json") as file:
        records = json.load(file)

    for record in records:
        wp = Waypoint(**record)
        car.record_point(waypoint=wp)

    assert len(car.trips) == 2

    trip1, trip2 = car.trips

    assert trip1.to_dict()["start"]["timestamp"] == "2018-08-12T10:02:24Z"
    assert trip1.to_dict()["end"]["timestamp"] == "2018-08-12T10:31:13Z"
    assert trip1.to_dict()["start"]["lat"] == 51.55017
    assert trip1.to_dict()["start"]["lng"] == 12.41016
    assert trip1.to_dict()["end"]["lat"] == 51.60519
    assert trip1.to_dict()["end"]["lng"] == 12.3008

    assert trip2.to_dict()["start"]["timestamp"] == "2018-08-12T13:11:46Z"
    assert trip2.to_dict()["end"]["timestamp"] == "2018-08-12T13:40:08Z"
    assert trip2.to_dict()["start"]["lat"] == 51.60136
    assert trip2.to_dict()["start"]["lng"] == 12.30293
    assert trip2.to_dict()["end"]["lat"] == 51.55
    assert trip2.to_dict()["end"]["lng"] == 12.41017

    # assert trip1.to_dict()["distance"] == 13095
    # assert trip2.to_dict()["distance"] == 14357
