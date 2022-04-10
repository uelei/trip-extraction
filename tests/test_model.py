from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from trip_extraction.model import Trip, Waypoint


def test_waypoint_model_valid():
    now = datetime.now()
    now_str = now.isoformat()
    wp = Waypoint(timestamp=now_str, lat=10.231, lng=34.987712)

    assert wp.lat == 10.231
    assert wp.lng == 34.987712
    assert wp.timestamp == now


def test_waypoint_model_invalid_lat():
    with pytest.raises(ValidationError) as exc_info:
        Waypoint(
            timestamp=datetime.now().isoformat(), lat=100.231, lng=24.987712
        )
    assert exc_info.value.errors() == [
        {"loc": ("lat",), "msg": "latitude invalid", "type": "value_error"}
    ]


def test_waypoint_model_invalid_lng():
    with pytest.raises(ValidationError) as exc_info:
        Waypoint(
            timestamp=datetime.now().isoformat(), lat=10.231, lng=224.987712
        )
    assert exc_info.value.errors() == [
        {"loc": ("lng",), "msg": "longitude invalid", "type": "value_error"}
    ]


def test_waypoint_model_invalid_lat_lng():
    with pytest.raises(ValidationError) as exc_info:
        Waypoint(
            timestamp=datetime.now().isoformat(), lat=100.231, lng=224.987712
        )
    assert exc_info.value.errors() == [
        {"loc": ("lat",), "msg": "latitude invalid", "type": "value_error"},
        {"loc": ("lng",), "msg": "longitude invalid", "type": "value_error"},
    ]


def test_waypoint_model_invalid_timestamp():
    with pytest.raises(ValidationError) as exc_info:
        Waypoint(timestamp="banana", lat=10.231, lng=24.987712)
    assert exc_info.value.errors() == [
        {
            "loc": ("timestamp",),
            "msg": "invalid datetime format",
            "type": "value_error.datetime",
        }
    ]


def test_trip_model_valid():
    now = datetime.now()
    now_str = now.isoformat()
    after = now + timedelta(minutes=4)
    start_wp = Waypoint(timestamp=now_str, lat=10.231, lng=34.987712)

    end_wp = Waypoint(timestamp=after, lat=10.231, lng=34.967712)

    trip = Trip(start=start_wp, end=end_wp)

    assert trip.distance == 2191
