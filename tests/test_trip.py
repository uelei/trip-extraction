from datetime import datetime, timedelta

from trip_extraction.model import Trip, Waypoint


def test_trip_model_valid():
    now = datetime.now()
    now_str = now.isoformat()
    after = now + timedelta(minutes=4)
    start_wp = Waypoint(timestamp=now_str, lat=10.231, lng=34.987712)

    end_wp = Waypoint(timestamp=after, lat=10.231, lng=34.967712)

    trip = Trip(start=start_wp, end=end_wp)

    assert int(trip.distance) == 2191
