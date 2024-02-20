import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

import settings
from main import app, get_session

TEST_DATABASE_URL = f"{settings.DATABASE_URL}_test"


@pytest.fixture(name="engine", scope="session")
def engine_fixture():
    engine = create_engine(TEST_DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine):
    with engine.connect() as connection:
        transaction = connection.begin()

        with Session(connection) as session:
            yield session
            session.close()

        transaction.rollback()


def test_create_place(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app, headers={"API-KEY": settings.API_KEY})
    response = client.post(
        "/places",
        json={
            "name": "New York",
            "description": "The Big Apple.",
            "location": {"latitude": 40.7128, "longitude": -74.0060},
        },
    )
    app.dependency_overrides.clear()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "name": "New York",
        "description": "The Big Apple.",
        "location": {"latitude": 40.7128, "longitude": -74.0060},
    }


def test_list_places():
    pass


def test_search_places_by_name():
    pass


def test_search_places_by_location():
    pass
