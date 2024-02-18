from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Session, select

from db import get_session, init_db
from models import Place
from serializers import PlaceCreate, PlaceRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/places", response_model=PlaceRead)
def create_place(place: PlaceCreate, session: Session = Depends(get_session)):
    db_place = Place.model_validate(place.model_dump(by_alias=True))
    session.add(db_place)
    session.commit()
    session.refresh(db_place)
    return db_place


@app.get("/places", response_model=list[PlaceRead])
def list_places(
    offset: int = 0,
    latitude: Annotated[float | None, Query(ge=-90, le=90)] = None,
    longitude: Annotated[float | None, Query(ge=-180, le=180)] = None,
    radius: Annotated[float | None, Query(ge=0)] = None,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session),
):
    statement = select(Place).offset(offset).limit(limit)

    if any(value is not None for value in [latitude, longitude, radius]):
        if not all(value is not None for value in [latitude, longitude, radius]):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "'latitude', 'longitude' and 'radius' must be supplied together",
            )

        statement = statement.where(Place.within_clause(latitude, longitude, radius))

    db_places = session.exec(statement)
    return db_places
