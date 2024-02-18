from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Query
from sqlmodel import Session, SQLModel, create_engine, select

from models import Place
from serializers import PlaceCreate, PlaceRead

sqlite_url = "sqlite:///db.sqlite3"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/places", response_model=PlaceRead)
def create_place(place: PlaceCreate):
    with Session(engine) as session:
        db_place = Place.model_validate(place.model_dump(by_alias=True))
        session.add(db_place)
        session.commit()
        session.refresh(db_place)
        return db_place


@app.get("/places", response_model=List[PlaceRead])
def list_places(offset: int = 0, limit: int = Query(default=100, le=100)):
    with Session(engine) as session:
        statement = select(Place).offset(offset).limit(limit)
        db_places = session.exec(statement).all()
        return db_places
