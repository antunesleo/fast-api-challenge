from sqlmodel import Session, SQLModel, create_engine

import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
