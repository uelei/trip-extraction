from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, validator

from trip_extraction.calcs import (
    calculate_distance_between_two_waypoints,
    calculate_speed,
)
from trip_extraction.const import IDLE_TIME_MAX, RADIUS_AREA
from trip_extraction.exceptions import InvalidLatitude, InvalidLongitude
from trip_extraction.logger import logger


class Waypoint(BaseModel):
    timestamp: datetime
    lat: float
    lng: float

    @validator("lat")
    def validate_lat(cls, input_value: float) -> float:
        if -90 < input_value > 90:
            raise InvalidLatitude
        return input_value

    @validator("lng")
    def validate_lng(cls, input_value: float) -> float:
        if -180 < input_value > 180:
            raise InvalidLongitude
        return input_value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "lat": self.lat,
            "lng": self.lng,
        }

    class Config:
        allow_mutation = False


class Trip(BaseModel):

    start: Waypoint
    end: Waypoint
    distance: int = 0

    def __init__(self, **kwargs: Dict[str, Any]):
        super().__init__(**kwargs)
        self.distance = calculate_distance_between_two_waypoints(
            self.start, self.end
        )

    def update_distance_by_waypoint(self, waypoint: Waypoint) -> None:
        self.distance += calculate_distance_between_two_waypoints(
            self.end, waypoint
        )

    def update_end_waypoint(self, waypoint: Waypoint) -> None:
        self.update_distance_by_waypoint(waypoint)
        self.end = waypoint

    def to_dict(self) -> Dict[str, Any]:
        return {
            "start": self.start.to_dict(),
            "end": self.end.to_dict(),
            "distance": int(self.distance),
        }


@dataclass
class Car:
    trips: List[Trip] = field(default_factory=list)
    last_recorded_point: Optional[Waypoint] = None

    def validate_waypoint_from_last_position(self, waypoint: Waypoint) -> bool:

        lst_recorded_point = (
            self.last_recorded_point if self.last_recorded_point else waypoint
        )

        distance = calculate_distance_between_two_waypoints(
            lst_recorded_point, waypoint
        )

        time_in_seconds = int(
            (waypoint.timestamp - lst_recorded_point.timestamp).total_seconds()
        )

        speed = calculate_speed(distance, time_in_seconds)

        if speed > 166.667:
            # greater then 10km/minute
            return False
        return True

    def record_point(self, waypoint: Waypoint) -> None:
        if not self.last_recorded_point:
            self.last_recorded_point = waypoint
            return

        last_trip = self.trips[-1] if self.trips else None
        distance = calculate_distance_between_two_waypoints(
            self.last_recorded_point, waypoint
        )

        if not self.validate_waypoint_from_last_position(waypoint):
            logger.warning("waypoint ignored jump waypoint identified")
            return

        if distance > RADIUS_AREA:
            logger.debug(f"movement of {distance} recorded.")
            if not last_trip:
                logger.debug("creating a new trip")
                self.trips.append(
                    Trip(start=self.last_recorded_point, end=waypoint)
                )
                self.last_recorded_point = waypoint
                return

            if (
                waypoint.timestamp - last_trip.end.timestamp
            ).total_seconds() > IDLE_TIME_MAX:

                self.trips.append(Trip(start=waypoint, end=waypoint))
                self.last_recorded_point = waypoint
                return

            logger.debug("update end waypoint")
            last_trip.update_end_waypoint(waypoint)

        self.last_recorded_point = waypoint
