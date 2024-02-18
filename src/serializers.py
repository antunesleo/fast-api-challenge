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
        return f"{location.latitude},{location.longitude}"


class PlaceRead(PlaceBase):
    @field_validator("location", mode="before")
    @classmethod
    def validate_location(cls, location: str) -> Location:
        lat, lng = location.split(",")
        return Location(latitude=float(lat), longitude=float(lng))
