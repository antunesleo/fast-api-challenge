from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Query
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
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session),
):
    statement = select(Place).offset(offset).limit(limit)
    db_places = session.exec(statement).all()
    return db_places
