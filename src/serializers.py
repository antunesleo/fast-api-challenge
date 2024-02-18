from pydantic import BaseModel, Field, field_serializer, field_validator


class Location(BaseModel):
    latitude: float
    longitude: float


class PlaceCreate(BaseModel):
    name: str
    description: str
    location: Location = Field(..., serialization_alias="coords")

    @field_serializer("location")
    def serialize_location(location: Location):
        return f"{location.latitude},{location.longitude}"


class PlaceRead(BaseModel):
    name: str
    description: str
    location: Location = Field(..., validation_alias="coords")

    @field_validator("location", mode="before")
    @classmethod
    def validate_location(cls, coords: str) -> Location:
        lat, lng = coords.split(",")
        return Location(latitude=float(lat), longitude=float(lng))
