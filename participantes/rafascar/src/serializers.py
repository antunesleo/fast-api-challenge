from geoalchemy2.elements import WKBElement, WKTElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, field_serializer, field_validator


class Location(BaseModel):
    latitude: float
    longitude: float


class PlaceBase(BaseModel):
    name: str
    description: str
    location: Location


class PlaceCreate(PlaceBase):
    name: str
    description: str

    @field_serializer("location")
    def serialize_location(location: Location):
        return WKTElement(f"POINT({location.longitude} {location.latitude})")


class PlaceRead(PlaceBase):
    @field_validator("location", mode="before")
    @classmethod
    def validate_location(cls, location: WKBElement) -> Location:
        point = to_shape(location)
        return Location(longitude=point.x, latitude=point.y)
