from datetime import datetime

from pydantic import BaseModel, validator

from trip_extraction.calcs import calculate_distance_between_two_waypoints
from trip_extraction.exceptions import InvalidLatitude, InvalidLongitude


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

    class Config:
        allow_mutation = False


class Trip(BaseModel):

    start: Waypoint
    end: Waypoint

    @property
    def distance(self) -> int:
        return calculate_distance_between_two_waypoints(self.start, self.end)
