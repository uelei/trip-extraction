from typing import TYPE_CHECKING

from trip_extraction.const import DISTANCE_FORMULA

if TYPE_CHECKING:
    from trip_extraction.model import Waypoint


def calculate_distance_between_two_waypoints(
    point_a: "Waypoint", point_b: "Waypoint"
) -> int:

    distance = DISTANCE_FORMULA(
        (point_a.lat, point_a.lng), (point_b.lat, point_b.lng)
    ).meters

    return int(distance)


def calculate_speed(distance: int, time: int) -> float:

    result = distance / time
    return result
