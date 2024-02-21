from typing import Any, Optional

from geoalchemy2 import Geography, WKTElement
from sqlmodel import Column, Field, SQLModel, func


class Place(SQLModel, table=True):
    # 'place' conflicts with a default existing table on the postgis/postgis Docker image.
    __tablename__ = "app_place"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    location: Any = Field(sa_column=Column(Geography("POINT")))

    @classmethod
    def within_clause(cls, latitude, longitude, radius):
        point = WKTElement(f"POINT({longitude} {latitude})")
        return func.ST_DWithin(cls.location, point, radius)
