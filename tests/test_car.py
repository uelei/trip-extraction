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
