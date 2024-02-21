import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

import settings
from main import app, get_session
from models import Place

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
            app.dependency_overrides[get_session] = lambda: session
            yield session
            session.close()
            app.dependency_overrides.clear()

        transaction.rollback()


@pytest.fixture
def client():
    return TestClient(app, headers={"API-KEY": settings.API_KEY})


@pytest.fixture
def new_york():
    return Place(
        name="New York",
        description="The Big Apple.",
        location="POINT (-74.0060 40.7128)",
    )


@pytest.fixture
def chicago():
    return Place(
        name="Chicago",
        description="The Windy City.",
        location="POINT (-87.6298 41.8781)",
    )


@pytest.fixture
def newark():
    return Place(
        name="Newark",
        description="Noted for its arts and history.",
        location="POINT (-74.1724 40.7357)",
    )


def test_create_place(client: TestClient, session: Session):
    response = client.post(
        "/places",
        json={
            "name": "New York",
            "description": "The Big Apple.",
            "location": {"latitude": 40.7128, "longitude": -74.0060},
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "name": "New York",
        "description": "The Big Apple.",
        "location": {"latitude": 40.7128, "longitude": -74.0060},
    }


def test_list_places(
    new_york: Place, chicago: Place, client: TestClient, session: Session
):
    session.add(new_york)
    session.add(chicago)
    session.commit()

    response = client.get("/places")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "name": "New York",
            "description": "The Big Apple.",
            "location": {"latitude": 40.7128, "longitude": -74.006},
        },
        {
            "name": "Chicago",
            "description": "The Windy City.",
            "location": {"latitude": 41.8781, "longitude": -87.6298},
        },
    ]


def test_pagination(
    new_york: Place,
    chicago: Place,
    client: TestClient,
    session: Session,
):
    session.add(new_york)
    session.add(chicago)
    session.commit()

    response = client.get("/places?limit=1")
    assert response.json() == [
        {
            "name": "New York",
            "description": "The Big Apple.",
            "location": {"latitude": 40.7128, "longitude": -74.006},
        },
    ]

    response = client.get("/places?offset=1")
    assert response.json() == [
        {
            "name": "Chicago",
            "description": "The Windy City.",
            "location": {"latitude": 41.8781, "longitude": -87.6298},
        },
    ]


def test_search_by_name(
    new_york: Place,
    chicago: Place,
    newark: Place,
    client: TestClient,
    session: Session,
):
    session.add(new_york)
    session.add(chicago)
    session.add(newark)
    session.commit()

    response = client.get("/places?name=new")

    assert {city["name"] for city in response.json()} == {"New York", "Newark"}


def test_search_by_location(
    new_york: Place,
    chicago: Place,
    newark: Place,
    client: TestClient,
    session: Session,
):
    session.add(new_york)
    session.add(chicago)
    session.add(newark)
    session.commit()

    response = client.get("/places?longitude=-74.0475&latitude=40.7099&radius=50000")

    assert {city["name"] for city in response.json()} == {"New York", "Newark"}
